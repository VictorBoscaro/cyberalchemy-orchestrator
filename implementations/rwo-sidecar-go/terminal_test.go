package rwosidecar

import (
	"bytes"
	"context"
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestRawTerminalReopensAndAdmitsOnce(t *testing.T) {
	store, runtime, reducer, path := terminalFixtureRuntime(t)
	writeTerminalLines(t, store, "attempt-1", "session-1", fakeEveLines)
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	reopened := openDurableRuntimeStore(t, path)
	defer reopened.Close()
	rebuilt, err := NewDurableRuntime(reducer, localCompilation(), reopened)
	if err != nil {
		t.Fatal(err)
	}
	candidate, err := ValidatePersistedTerminal(reopened, terminalValidationInput("attempt-1", "session-1"))
	if err != nil {
		t.Fatal(err)
	}
	coordinator, _ := NewTerminalCoordinator(reopened, rebuilt)
	first, err := coordinator.Admit(context.Background(), candidate)
	if err != nil || first.Status != "admitted" || len(first.RustResponse.CommandIntent) != 0 {
		t.Fatalf("first admission: %+v %v", first, err)
	}
	second, err := coordinator.Admit(context.Background(), candidate)
	if err != nil || second.Status != "inert" || second.SemanticCommitSequence != first.SemanticCommitSequence {
		t.Fatalf("replay admission: %+v %v", second, err)
	}
	if snapshot := rebuilt.Snapshot("stream-1"); snapshot.SemanticCommitCount != 1 || snapshot.CommittedReplayCount != 0 {
		t.Fatalf("terminal replay changed Rust counts: %+v", snapshot)
	}
	_ = runtime
}

func TestTerminalCommitBeforeAckIsInertOnReopen(t *testing.T) {
	store, runtime, reducer, path := terminalFixtureRuntime(t)
	writeTerminalLines(t, store, "attempt-1", "session-1", fakeEveLines)
	candidate, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1"))
	if err != nil {
		t.Fatal(err)
	}
	// Simulate a crash after the Rust semantic commit but before the physical
	// terminal-admission marker by calling DurableRuntime directly.
	response, err := runtime.Reduce(context.Background(), KernelRequest{Tuple: candidate.Tuple, StreamIDHint: candidate.StreamID, RawAcceptedEvent: candidate.CanonicalEvent})
	if err != nil || response.Outcome != "Applied" {
		t.Fatalf("pre-crash semantic commit: %+v %v", response, err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	reopened := openDurableRuntimeStore(t, path)
	defer reopened.Close()
	rebuilt, err := NewDurableRuntime(reducer, localCompilation(), reopened)
	if err != nil {
		t.Fatal(err)
	}
	coordinator, _ := NewTerminalCoordinator(reopened, rebuilt)
	result, err := coordinator.Admit(context.Background(), candidate)
	if err != nil || result.Status != "admitted" {
		t.Fatalf("recovered terminal commit: %+v %v", result, err)
	}
	snapshot := rebuilt.Snapshot("stream-1")
	if snapshot.SemanticCommitCount != 1 || snapshot.CommittedReplayCount != 1 || len(snapshot.Outbox) != 0 {
		t.Fatalf("semantic commit duplicated after reopen: %+v", snapshot)
	}
}

func TestRepresentationVariantConvergesOnAdmissionKey(t *testing.T) {
	store, runtime, _, _ := terminalFixtureRuntime(t)
	defer store.Close()
	writeTerminalLines(t, store, "attempt-1", "session-1", fakeEveLines)
	baseline, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1"))
	if err != nil {
		t.Fatal(err)
	}
	coordinator, err := NewTerminalCoordinator(store, runtime)
	if err != nil {
		t.Fatal(err)
	}
	admitted, err := coordinator.Admit(context.Background(), baseline)
	if err != nil || admitted.Status != "admitted" {
		t.Fatalf("baseline admission: %+v %v", admitted, err)
	}

	variantStore := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "variant.rwolog"))
	defer variantStore.Close()
	variant := [][]byte{
		[]byte("{\"type\":\"session.started\",\"sessionId\":\"session-1\",\"eventId\":\"101\"}\n"),
		[]byte("{ \"output\" : { \"answer\" : \"bounded result\" }, \"type\":\"task.output\",\"eventId\":\"102\",\"sessionId\":\"session-1\" }\n"),
		[]byte("{\"sessionId\":\"session-1\",\"eventId\":\"103\",\"type\":\"session.completed\"}\n"),
	}
	writeTerminalLines(t, variantStore, "attempt-1", "session-1", variant)
	candidate, err := ValidatePersistedTerminal(variantStore, terminalValidationInput("attempt-1", "session-1"))
	if err != nil {
		t.Fatal(err)
	}
	if candidate.OutputSHA256 != "sha256:"+digestHex([]byte(`{"answer":"bounded result"}`)) {
		t.Fatalf("representation changed canonical output digest: %+v", candidate)
	}
	// The known vector binds the design's literal unframed concatenation choice.
	wantKey := terminalAdmissionKeyForTest(terminalValidationInput("attempt-1", "session-1"))
	if candidate.AdmissionKey != wantKey {
		t.Fatalf("terminal key = %s want %s", candidate.AdmissionKey, wantKey)
	}
	if candidate.AdmissionKey != baseline.AdmissionKey || candidate.OutputSHA256 != baseline.OutputSHA256 ||
		!bytes.Equal(candidate.CanonicalOutput, baseline.CanonicalOutput) || !bytes.Equal(candidate.CanonicalEvent, baseline.CanonicalEvent) {
		t.Fatalf("provider representation changed terminal identity:\nbase=%+v\nvariant=%+v", baseline, candidate)
	}
	replay, err := coordinator.Admit(context.Background(), candidate)
	if err != nil || replay.Status != "inert" || replay.SemanticCommitSequence != admitted.SemanticCommitSequence {
		t.Fatalf("representation replay was not inert: %+v %v", replay, err)
	}
	if projection := runtime.Snapshot("stream-1"); projection.SemanticCommitCount != 1 || len(projection.Outbox) != 0 {
		t.Fatalf("representation replay re-entered Rust: %+v", projection)
	}
	stored, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	counts := countDurableRecords(stored)
	if counts[RecordTypeTerminalAdmissionV1] != 1 || counts[RecordTypeTerminalReplayInertV1] != 1 {
		t.Fatalf("terminal convergence counts = %+v", counts)
	}
}

func TestSameAdmissionKeyDifferentDigestBlocks(t *testing.T) {
	store, runtime, _, _ := terminalFixtureRuntime(t)
	defer store.Close()
	writeTerminalLines(t, store, "attempt-1", "session-1", fakeEveLines)
	first, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1"))
	if err != nil {
		t.Fatal(err)
	}
	coordinator, _ := NewTerminalCoordinator(store, runtime)
	if _, err := coordinator.Admit(context.Background(), first); err != nil {
		t.Fatal(err)
	}
	second := first
	second.OutputSHA256 = taggedDigest("different-valid-output")
	second.CanonicalOutput = []byte(`{"answer":"different"}`)
	if _, err := coordinator.Admit(context.Background(), second); !errors.Is(err, ErrTerminalDivergence) {
		t.Fatalf("divergence error = %v", err)
	}
	if snapshot := runtime.Snapshot("stream-1"); snapshot.SemanticCommitCount != 1 {
		t.Fatalf("divergence called Rust again: %+v", snapshot)
	}
}

func TestForbiddenEveEventsCannotAdmit(t *testing.T) {
	for _, eventType := range []string{
		"tool.requested", "tool.result", "delegation.requested", "subagent.started", "workflow.started",
		"workflow.step", "scheduler.requested", "seat.created", "request_input.requested",
	} {
		t.Run(eventType, func(t *testing.T) {
			store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
			defer store.Close()
			lines := [][]byte{
				[]byte("{\"eventId\":\"1\",\"sessionId\":\"session-1\",\"type\":\"session.started\"}\n"),
				[]byte("{\"eventId\":\"2\",\"sessionId\":\"session-1\",\"type\":\"" + eventType + "\"}\n"),
			}
			writeTerminalLines(t, store, "attempt-1", "session-1", lines)
			if _, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1")); !errors.Is(err, ErrTerminalPolicy) {
				t.Fatalf("policy error = %v", err)
			}
		})
	}
}

func TestGovernanceFactsAreNotSeatOutput(t *testing.T) {
	for _, fact := range []string{"auditReceipt", "toolApproval", "finalApproval", "providerSuccess", "timeout"} {
		t.Run(fact, func(t *testing.T) {
			store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
			defer store.Close()
			lines := [][]byte{
				[]byte("{\"eventId\":\"1\",\"sessionId\":\"session-1\",\"type\":\"session.started\"}\n"),
				[]byte("{\"eventId\":\"2\",\"output\":{\"" + fact + "\":true},\"sessionId\":\"session-1\",\"type\":\"task.output\"}\n"),
				[]byte("{\"eventId\":\"3\",\"sessionId\":\"session-1\",\"type\":\"session.completed\"}\n"),
			}
			writeTerminalLines(t, store, "attempt-1", "session-1", lines)
			if _, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1")); !errors.Is(err, ErrTerminalSchema) {
				t.Fatalf("schema error = %v", err)
			}
		})
	}
}

func TestRawTerminalRejectsMalformedBoundsOrderAndPostTerminal(t *testing.T) {
	tests := []struct {
		name  string
		lines [][]byte
	}{
		{"malformed", [][]byte{[]byte("not-json\n")}},
		{"wrong session", [][]byte{[]byte("{\"eventId\":\"1\",\"sessionId\":\"other\",\"type\":\"session.started\"}\n")}},
		{"duplicate id", [][]byte{fakeEveLines[0], bytes.Replace(fakeEveLines[1], []byte("eve-event-2"), []byte("eve-event-1"), 1)}},
		{"post terminal", append(append([][]byte(nil), fakeEveLines...), []byte("{\"eventId\":\"eve-event-4\",\"sessionId\":\"session-1\",\"type\":\"session.started\"}\n"))},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
			defer store.Close()
			writeTerminalLines(t, store, "attempt-1", "session-1", test.lines)
			if _, err := ValidatePersistedTerminal(store, terminalValidationInput("attempt-1", "session-1")); err == nil {
				t.Fatal("invalid terminal evidence passed")
			}
		})
	}
}

func terminalFixtureRuntime(t *testing.T) (*DurableStore, *DurableRuntime, *scriptedReducer, string) {
	t.Helper()
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	store := openDurableRuntimeStore(t, path)
	reducer := &scriptedReducer{reduce: func(_ []byte, request KernelRequest) (KernelResponse, error) {
		return KernelResponse{
			Outcome: "Applied", NextCursor: []byte("terminal-cursor"), ValidatedStreamID: request.StreamIDHint,
			AcceptedEventIdentity: taggedDigest("terminal-event"), EventPayloadDigest: taggedDigest("terminal-payload"),
		}, nil
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	return store, runtime, reducer, path
}

func writeTerminalLines(t *testing.T, store *DurableStore, attemptID, sessionID string, lines [][]byte) {
	t.Helper()
	writer, err := NewDurableEveRawWriter(store, attemptID)
	if err != nil {
		t.Fatal(err)
	}
	for _, line := range lines {
		if err := writer.Sink(context.Background(), sessionID, line); err != nil {
			t.Fatal(err)
		}
	}
}

func terminalValidationInput(attemptID, sessionID string) TerminalValidationInput {
	schema, err := os.ReadFile(filepath.Join("testdata", "eve-one-seat", "output-schema.json"))
	if err != nil {
		panic(err)
	}
	return TerminalValidationInput{
		GraphIdentity: localCompilation().GraphIdentity, StreamID: "stream-1", CommandIdentity: taggedDigest("command"),
		AttemptID: attemptID, SessionID: sessionID, TerminalClass: "completed", SourceNodeID: "worker",
		Tuple: fixtureTuple(), OutputSchemaBytes: schema, OutputSchemaSHA256: "sha256:" + digestHex(schema),
		PolicySHA256: taggedDigest("tool-free-policy"),
	}
}

func terminalAdmissionKeyForTest(input TerminalValidationInput) string {
	return "sha256:" + digestHex([]byte("RWO-TERMINAL-ADMISSION-V1\x00"+input.GraphIdentity+input.StreamID+input.CommandIdentity+input.AttemptID+input.SessionID+input.TerminalClass))
}
