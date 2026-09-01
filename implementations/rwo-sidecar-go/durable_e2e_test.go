package rwosidecar

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"reflect"
	"sync"
	"testing"
	"time"
)

func TestContentAddressRoundTripsThroughRealRust(t *testing.T) {
	fixture := startDurableE2E(t)
	defer fixture.close()
	authorization := readE2EFixture(t, "authorization-event.json")
	first, err := fixture.runtime.Reduce(context.Background(), KernelRequest{
		Tuple: fixtureTuple(), StreamIDHint: "stream-eve-one-seat", RawAcceptedEvent: authorization,
	})
	if err != nil {
		t.Fatal(err)
	}
	if first.Outcome != "Applied" || len(first.CommandIntent) == 0 {
		t.Fatalf("real Rust did not emit seat command: %+v", first)
	}
	command, err := DecodeExecuteBoundedSeatCommand(first.CommandIntent)
	if err != nil {
		t.Fatal(err)
	}
	if command.Payload.JobID != testSeatAddress || command.CommandType != "ExecuteBoundedSeat" {
		t.Fatalf("content address changed through Rust: %+v", command)
	}
	candidate := runFakeEveToTerminal(t, fixture, first, command)
	result, err := fixture.terminal.Admit(context.Background(), candidate)
	if err != nil {
		t.Fatal(err)
	}
	if result.Status != "admitted" || result.RustResponse.Outcome != "Applied" || len(result.RustResponse.CommandIntent) != 0 ||
		candidate.ResultAddress != "resultv1:sha256:"+stringsTrimSHA(candidate.OutputSHA256) {
		t.Fatalf("terminal address did not round trip: candidate=%+v result=%+v", candidate, result)
	}
	acknowledgeE2ETerminal(t, fixture, candidate, result)
}

func TestOneSeatCompletesAcrossRustAndFakeEve(t *testing.T) {
	fixture := startDurableE2E(t)
	defer fixture.close()
	authorization := readE2EFixture(t, "authorization-event.json")
	commandResponse, err := fixture.runtime.Reduce(context.Background(), KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-eve-one-seat", RawAcceptedEvent: authorization})
	if err != nil {
		t.Fatal(err)
	}
	command, err := DecodeExecuteBoundedSeatCommand(commandResponse.CommandIntent)
	if err != nil {
		t.Fatal(err)
	}
	candidate := runFakeEveToTerminal(t, fixture, commandResponse, command)
	terminalResult, err := fixture.terminal.Admit(context.Background(), candidate)
	if err != nil {
		t.Fatal(err)
	}
	serverState := fixture.server.State()
	runtimeState := fixture.runtime.Snapshot("stream-eve-one-seat")
	storeState, err := fixture.store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	counts := countDurableRecords(storeState)
	if serverState.Creates != 1 || serverState.Streams != 1 || counts[RecordTypeRawEveLineV1] != 3 ||
		counts[RecordTypeTerminalAdmissionV1] != 1 || runtimeState.SemanticCommitCount != 2 || len(runtimeState.Outbox) != 1 ||
		terminalResult.Status != "admitted" || len(terminalResult.RustResponse.CommandIntent) != 0 {
		t.Fatalf("non-vacuity counts failed: server=%+v counts=%+v runtime=%+v terminal=%+v", serverState, counts, runtimeState, terminalResult)
	}
	acknowledged := acknowledgeE2ETerminal(t, fixture, candidate, terminalResult)
	if acknowledged.State != AttemptAcknowledged {
		t.Fatalf("terminal did not close the physical attempt: %+v", acknowledged)
	}
}

func TestEveryBoundaryReopenMatchesReference(t *testing.T) {
	fixture := startDurableE2E(t)
	defer fixture.close()
	var boundaries []string
	reopen := func(name string) {
		fixture.reopenAndAssert(t)
		boundaries = append(boundaries, name)
	}

	authorization := readE2EFixture(t, "authorization-event.json")
	commandResponse, err := fixture.runtime.Reduce(context.Background(), KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-eve-one-seat", RawAcceptedEvent: authorization})
	if err != nil {
		t.Fatal(err)
	}
	reopen("semantic-commit")
	command, _ := DecodeExecuteBoundedSeatCommand(commandResponse.CommandIntent)
	prepared, err := fixture.attempts.Prepare(AttemptPreparation{CommandIntentIdentity: commandResponse.CommandIntentIdentity, AdapterProfile: "eve-leaf-v1", AttemptOrdinal: 1, MaxSendTries: 2})
	if err != nil {
		t.Fatal(err)
	}
	reopen("attempt-prepared")
	fence, err := fixture.attempts.Claim(prepared.AttemptID, "worker-1", time.Unix(10, 0), time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	reopen("lease-claimed")
	preparedRequest, err := PrepareEveTaskRequest(commandResponse.CommandIntent, commandResponse.CommandIntentIdentity, prepared.AttemptID, 1, fixture.catalog)
	if err != nil {
		t.Fatal(err)
	}
	lineage, err := fixture.attempts.ArmSend(fence, RequestBinding{RequestFingerprint: preparedRequest.RequestFingerprint, RequestPayloadSHA256: preparedRequest.RequestSHA256})
	if err != nil {
		t.Fatal(err)
	}
	created, err := fixture.adapter.Create(context.Background(), preparedRequest.RequestBytes)
	if err != nil {
		t.Fatal(err)
	}
	// This is the dangerous cut: the arm and remote create happened, but the
	// session mapping did not. Reopen must freeze the attempt, then accept only
	// the exact late response lineage without another create.
	reopen("send-armed-after-create-before-map")
	recovered, err := fixture.attempts.RecoverAfterReopen()
	if err != nil || recovered != 1 {
		t.Fatalf("armed recovery = %d, %v", recovered, err)
	}
	late, err := NewCorrelatedLateSessionProof(lineage, created.SessionID, created.ResponseSHA256, "captured-create-response")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := fixture.attempts.CorrelateLateSession(fence, late); err != nil {
		t.Fatal(err)
	}
	reopen("session-known")
	if _, err := fixture.attempts.AttachStream(fence, created.SessionID, ""); err != nil {
		t.Fatal(err)
	}
	reopen("stream-attached")
	writer, err := NewDurableEveRawWriter(fixture.store, prepared.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	lineOrdinal := 0
	if err := fixture.adapter.Stream(context.Background(), created.SessionID, "", func(ctx context.Context, sessionID string, line []byte) error {
		if err := writer.Sink(ctx, sessionID, line); err != nil {
			return err
		}
		lineOrdinal++
		reopen(fmt.Sprintf("raw-line-%d", lineOrdinal))
		writer, err = NewDurableEveRawWriter(fixture.store, prepared.AttemptID)
		return err
	}); err != nil {
		t.Fatal(err)
	}
	candidate, err := ValidatePersistedTerminal(fixture.store, e2eTerminalInput(fixture, prepared.AttemptID, created.SessionID, commandResponse.CommandIntentIdentity, command.TargetNodeID))
	if err != nil {
		t.Fatal(err)
	}
	result, err := fixture.terminal.Admit(context.Background(), candidate)
	if err != nil || result.Status != "admitted" {
		t.Fatalf("reopen continuation failed: %+v %v", result, err)
	}
	reopen("terminal-admitted")
	acknowledged := acknowledgeE2ETerminal(t, fixture, candidate, result)
	if acknowledged.State != AttemptAcknowledged {
		t.Fatalf("acknowledged state = %+v", acknowledged)
	}
	reopen("attempt-acknowledged")

	if len(boundaries) != 11 || lineOrdinal != 3 {
		t.Fatalf("reopen coverage = %v, raw lines=%d", boundaries, lineOrdinal)
	}
	storeState, err := fixture.store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	counts := countDurableRecords(storeState)
	runtimeState := fixture.runtime.Snapshot("stream-eve-one-seat")
	attemptState, err := fixture.attempts.Snapshot(prepared.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	serverState := fixture.server.State()
	if counts[RecordTypeSemanticCommitV1] != 2 || counts[RecordTypeRawEveLineV1] != 3 ||
		counts[RecordTypeTerminalAdmissionV1] != 1 || runtimeState.SemanticCommitCount != 2 || len(runtimeState.Outbox) != 1 ||
		attemptState.State != AttemptAcknowledged || serverState.Creates != 1 || serverState.Streams != 1 {
		t.Fatalf("reopen run diverged from reference counts: boundaries=%v counts=%+v runtime=%+v attempt=%+v server=%+v", boundaries, counts, runtimeState, attemptState, serverState)
	}
}

func TestIndependentStreamsShareStoreWithoutCrossTalk(t *testing.T) {
	store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
	defer store.Close()
	commandBytes := testCommandBytes(t, "seat", testSeatAddress)
	reducer := &scriptedReducer{reduce: func(_ []byte, request KernelRequest) (KernelResponse, error) {
		return KernelResponse{
			Outcome: "Applied", ValidatedStreamID: request.StreamIDHint, NextCursor: []byte("cursor-" + request.StreamIDHint),
			CommandIntent: cloneBytes(commandBytes), CommandIntentIdentity: taggedDigest("command-" + request.StreamIDHint),
			CommandPayloadDigest: "sha256:" + digestHex(commandBytes), AcceptedEventIdentity: taggedDigest("event-" + request.StreamIDHint),
			EventPayloadDigest: taggedDigest("payload-" + request.StreamIDHint),
		}, nil
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	type streamResult struct {
		stream   string
		response KernelResponse
		err      error
	}
	done := make(chan streamResult, 2)
	for _, stream := range []string{"stream-a", "stream-b"} {
		go func(stream string) {
			response, reduceErr := runtime.Reduce(context.Background(), durableRuntimeRequest(stream, "raw-"+stream))
			done <- streamResult{stream: stream, response: response, err: reduceErr}
		}(stream)
	}
	responses := make(map[string]KernelResponse)
	for range 2 {
		result := <-done
		if result.err != nil {
			t.Fatal(result.err)
		}
		responses[result.stream] = result.response
	}

	var serverMu sync.Mutex
	createCount := 0
	server := httptest.NewServer(http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		if request.Method != http.MethodPost || request.URL.Path != "/eve/v1/session" {
			http.NotFound(writer, request)
			return
		}
		body, readErr := readBounded(request.Body, defaultEveMaxBody)
		if readErr != nil || ValidateEveTaskRequest(body) != nil {
			http.Error(writer, "invalid request", http.StatusBadRequest)
			return
		}
		serverMu.Lock()
		createCount++
		sessionID := fmt.Sprintf("session-%d", createCount)
		serverMu.Unlock()
		writer.Header().Set("Content-Type", "application/json")
		writer.WriteHeader(http.StatusAccepted)
		_, _ = fmt.Fprintf(writer, `{"sessionId":%q}`, sessionID)
	}))
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	attempts, err := NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	catalog := testSeatCatalog(t, fixtureMaterialRoot(t))
	type physicalResult struct {
		stream    string
		attemptID string
		sessionID string
		err       error
	}
	physical := make(chan physicalResult, 2)
	for index, stream := range []string{"stream-a", "stream-b"} {
		go func(index int, stream string) {
			response := responses[stream]
			prepared, prepareErr := attempts.Prepare(AttemptPreparation{
				CommandIntentIdentity: response.CommandIntentIdentity, AdapterProfile: "eve-leaf-v1", AttemptOrdinal: 1, MaxSendTries: 1,
			})
			if prepareErr != nil {
				physical <- physicalResult{stream: stream, err: prepareErr}
				return
			}
			owner := fmt.Sprintf("worker-%d", index+1)
			fence, claimErr := attempts.Claim(prepared.AttemptID, owner, time.Unix(int64(20+index), 0), time.Minute)
			if claimErr != nil {
				physical <- physicalResult{stream: stream, err: claimErr}
				return
			}
			request, requestErr := PrepareEveTaskRequest(response.CommandIntent, response.CommandIntentIdentity, prepared.AttemptID, 1, catalog)
			if requestErr != nil {
				physical <- physicalResult{stream: stream, err: requestErr}
				return
			}
			lineage, armErr := attempts.ArmSend(fence, RequestBinding{RequestFingerprint: request.RequestFingerprint, RequestPayloadSHA256: request.RequestSHA256})
			if armErr != nil {
				physical <- physicalResult{stream: stream, err: armErr}
				return
			}
			created, createErr := adapter.Create(context.Background(), request.RequestBytes)
			if createErr != nil {
				physical <- physicalResult{stream: stream, err: createErr}
				return
			}
			if _, mapErr := attempts.MapSession(fence, lineage, created.SessionID, created.ResponseSHA256); mapErr != nil {
				physical <- physicalResult{stream: stream, err: mapErr}
				return
			}
			physical <- physicalResult{stream: stream, attemptID: prepared.AttemptID, sessionID: created.SessionID}
		}(index, stream)
	}
	physicalResults := make(map[string]physicalResult)
	for range 2 {
		result := <-physical
		if result.err != nil {
			t.Fatal(result.err)
		}
		physicalResults[result.stream] = result
	}

	a, b := runtime.Snapshot("stream-a"), runtime.Snapshot("stream-b")
	if len(a.Outbox) != 1 || len(b.Outbox) != 1 || bytes.Equal(a.Cursor, b.Cursor) {
		t.Fatalf("stream crosstalk: a=%+v b=%+v", a, b)
	}
	serverMu.Lock()
	observedCreates := createCount
	serverMu.Unlock()
	if observedCreates != 2 || physicalResults["stream-a"].sessionID == physicalResults["stream-b"].sessionID ||
		physicalResults["stream-a"].attemptID == physicalResults["stream-b"].attemptID {
		t.Fatalf("physical stream crosstalk: creates=%d results=%+v", observedCreates, physicalResults)
	}
	for stream, result := range physicalResults {
		state, snapshotErr := attempts.Snapshot(result.attemptID)
		if snapshotErr != nil || state.State != AttemptSessionKnown || state.SessionID != result.sessionID ||
			state.CommandIntentIdentity != responses[stream].CommandIntentIdentity {
			t.Fatalf("stream %s physical projection: %+v %v", stream, state, snapshotErr)
		}
	}
	stored, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	counts := countDurableRecords(stored)
	if counts[RecordTypeSemanticCommitV1] != 2 || counts[RecordTypeAttemptJournalV1] != 8 {
		t.Fatalf("two-stream durable counts = %+v", counts)
	}
}

type durableE2EFixture struct {
	path     string
	header   DurableStoreHeader
	store    *DurableStore
	child    *ChildKernel
	compiled CompileResponse
	runtime  *DurableRuntime
	attempts *AttemptCoordinator
	terminal *TerminalCoordinator
	catalog  *SeatMaterialCatalog
	server   *fakeEveServer
	adapter  *EveLeafAdapter
}

func startDurableE2E(t *testing.T) *durableE2EFixture {
	t.Helper()
	composition := readE2EFixture(t, "composition.json")
	var tuple VersionTuple
	if err := json.Unmarshal(readE2EFixture(t, "composition-tuple.json"), &tuple); err != nil {
		t.Fatal(err)
	}
	child := startFixtureChild(t)
	compiled, err := child.Compile(context.Background(), CompileRequest{Tuple: tuple, RawComposition: composition})
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := DurableStoreHeader{StoreFormat: DurableStoreFormatV1, GraphIdentity: compiled.GraphIdentity, RawCompositionSHA256: digestHex(composition), Tuple: tuple, StoreInstanceID: "e2e-one-seat"}
	store, err := OpenDurableStore(path, header)
	if err != nil {
		t.Fatal(err)
	}
	runtime, err := NewDurableRuntime(child, compiled, store)
	if err != nil {
		t.Fatal(err)
	}
	attempts, _ := NewAttemptCoordinator(store)
	terminal, _ := NewTerminalCoordinator(store, runtime)
	catalog := testSeatCatalog(t, fixtureMaterialRoot(t))
	server := newFakeEveServer(t)
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	return &durableE2EFixture{path: path, header: header, store: store, child: child, compiled: compiled, runtime: runtime, attempts: attempts, terminal: terminal, catalog: catalog, server: server, adapter: adapter}
}

func (fixture *durableE2EFixture) close() {
	if fixture.store != nil {
		_ = fixture.store.Close()
		fixture.store = nil
	}
	if fixture.server != nil {
		fixture.server.Close()
		fixture.server = nil
	}
}

func (fixture *durableE2EFixture) reopenAndAssert(t *testing.T) {
	t.Helper()
	before, err := fixture.store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if err := fixture.store.Close(); err != nil {
		t.Fatal(err)
	}
	fixture.store = nil
	reopened, err := OpenDurableStore(fixture.path, fixture.header)
	if err != nil {
		t.Fatal(err)
	}
	fixture.store = reopened
	fixture.runtime, err = NewDurableRuntime(fixture.child, fixture.compiled, reopened)
	if err != nil {
		t.Fatal(err)
	}
	fixture.attempts, err = NewAttemptCoordinator(reopened)
	if err != nil {
		t.Fatal(err)
	}
	fixture.terminal, err = NewTerminalCoordinator(reopened, fixture.runtime)
	if err != nil {
		t.Fatal(err)
	}
	after, err := reopened.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(before, after) {
		t.Fatalf("verified reopen changed durable projection:\nbefore=%+v\nafter=%+v", before, after)
	}
}

func runFakeEveToTerminal(t *testing.T, fixture *durableE2EFixture, commandResponse KernelResponse, command ExecuteBoundedSeatCommand) TerminalCandidate {
	t.Helper()
	preparedAttempt, err := fixture.attempts.Prepare(AttemptPreparation{CommandIntentIdentity: commandResponse.CommandIntentIdentity, AdapterProfile: "eve-leaf-v1", AttemptOrdinal: 1, MaxSendTries: 2})
	if err != nil {
		t.Fatal(err)
	}
	fence, err := fixture.attempts.Claim(preparedAttempt.AttemptID, "worker-1", time.Unix(10, 0), time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	preparedRequest, err := PrepareEveTaskRequest(commandResponse.CommandIntent, commandResponse.CommandIntentIdentity, preparedAttempt.AttemptID, 1, fixture.catalog)
	if err != nil {
		t.Fatal(err)
	}
	lineage, err := fixture.attempts.ArmSend(fence, RequestBinding{RequestFingerprint: preparedRequest.RequestFingerprint, RequestPayloadSHA256: preparedRequest.RequestSHA256})
	if err != nil {
		t.Fatal(err)
	}
	created, err := fixture.adapter.Create(context.Background(), preparedRequest.RequestBytes)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := fixture.attempts.MapSession(fence, lineage, created.SessionID, created.ResponseSHA256); err != nil {
		t.Fatal(err)
	}
	if _, err := fixture.attempts.AttachStream(fence, created.SessionID, ""); err != nil {
		t.Fatal(err)
	}
	writer, err := NewDurableEveRawWriter(fixture.store, preparedAttempt.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	if err := fixture.adapter.Stream(context.Background(), created.SessionID, "", writer.Sink); err != nil {
		t.Fatal(err)
	}
	candidate, err := ValidatePersistedTerminal(fixture.store, e2eTerminalInput(fixture, preparedAttempt.AttemptID, created.SessionID, commandResponse.CommandIntentIdentity, command.TargetNodeID))
	if err != nil {
		t.Fatal(err)
	}
	return candidate
}

func acknowledgeE2ETerminal(t *testing.T, fixture *durableE2EFixture, candidate TerminalCandidate, result TerminalAdmissionResult) AttemptSnapshot {
	t.Helper()
	current, err := fixture.attempts.Snapshot(candidate.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	fence := AttemptFence{AttemptID: current.AttemptID, Owner: current.LeaseOwner, Epoch: current.FenceEpoch}
	proof, err := NewTerminalAdmissionProof(candidate.AttemptID, candidate.SessionID, candidate.AdmissionKey, result.SemanticCommitSequence)
	if err != nil {
		t.Fatal(err)
	}
	acknowledged, err := fixture.attempts.Acknowledge(fence, proof)
	if err != nil {
		t.Fatal(err)
	}
	return acknowledged
}

func e2eTerminalInput(fixture *durableE2EFixture, attemptID, sessionID, commandIdentity, target string) TerminalValidationInput {
	schema := readE2EFixtureNoTest("output-schema.json")
	return TerminalValidationInput{
		GraphIdentity: fixture.compiled.GraphIdentity, StreamID: "stream-eve-one-seat", CommandIdentity: commandIdentity,
		AttemptID: attemptID, SessionID: sessionID, TerminalClass: "completed", SourceNodeID: target,
		Tuple: fixtureTuple(), OutputSchemaBytes: schema, OutputSchemaSHA256: "sha256:" + digestHex(schema),
		PolicySHA256: taggedDigest("tool-free-policy"),
	}
}

func readE2EFixture(t *testing.T, name string) []byte {
	t.Helper()
	value, err := os.ReadFile(filepath.Join("testdata", "eve-one-seat", name))
	if err != nil {
		t.Fatal(err)
	}
	return value
}

func readE2EFixtureNoTest(name string) []byte {
	value, _ := os.ReadFile(filepath.Join("testdata", "eve-one-seat", name))
	return value
}

func countDurableRecords(snapshot DurableStoreSnapshot) map[DurableRecordType]int {
	counts := make(map[DurableRecordType]int)
	for _, record := range snapshot.Records {
		counts[record.Type]++
	}
	return counts
}

func stringsTrimSHA(value string) string {
	const prefix = "sha256:"
	if len(value) >= len(prefix) && value[:len(prefix)] == prefix {
		return value[len(prefix):]
	}
	return value
}

var _ = http.StatusAccepted
