package rwosidecar

import (
	"context"
	"errors"
	"path/filepath"
	"reflect"
	"sync"
	"testing"
	"time"
)

var attemptTestNow = time.Date(2026, 8, 13, 18, 0, 0, 0, time.UTC)

var attemptTestCommandResponse = durableAppliedResponse("attempt-stream", "attempt-cursor", "attempt-command")

func TestAttemptPreparationRequiresDurableRustOutbox(t *testing.T) {
	store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
	defer store.Close()
	coordinator, err := NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	before, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	_, err = coordinator.Prepare(AttemptPreparation{
		CommandIntentIdentity: taggedDigest("absent-command"), AdapterProfile: "eve-leaf-v1", AttemptOrdinal: 1, MaxSendTries: 1,
	})
	if !errors.Is(err, ErrAttemptProof) {
		t.Fatalf("missing outbox error = %v", err)
	}
	after, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(before, after) {
		t.Fatal("missing outbox command created physical attempt state")
	}
}

func TestPreparedAttemptReopensAndSendsOnce(t *testing.T) {
	path, header, store, coordinator := newAttemptTestCoordinator(t)
	prepared := prepareAttemptForTest(t, coordinator, 2)
	if prepared.State != AttemptPrepared || prepared.SendTryOrdinal != 1 {
		t.Fatalf("unexpected prepared attempt: %+v", prepared)
	}
	closeAttemptStore(t, store)

	store = openDurableStoreForTest(t, path, header)
	defer store.Close()
	coordinator, err := NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	fence, err := coordinator.Claim(prepared.AttemptID, "worker-reopen", attemptTestNow, time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	createCalls := 0
	if _, err := coordinator.ArmSend(fence, attemptBinding("request-one", "payload")); err != nil {
		t.Fatal(err)
	}
	createCalls++ // the adapter may be called only after ArmSend returns synced.
	if createCalls != 1 {
		t.Fatalf("create calls = %d, want 1", createCalls)
	}
	after, err := coordinator.Snapshot(prepared.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	if after.AttemptID != prepared.AttemptID || after.State != AttemptSendArmed || after.AttemptOrdinal != 1 {
		t.Fatalf("reopen changed attempt identity or state: %+v", after)
	}
}

func TestCrashAfterSendArmedFreezesCreate(t *testing.T) {
	path, header, store, coordinator := newAttemptTestCoordinator(t)
	prepared := prepareAttemptForTest(t, coordinator, 2)
	fence := claimAttemptForTest(t, coordinator, prepared.AttemptID, "worker-a", attemptTestNow)
	lineage, err := coordinator.ArmSend(fence, attemptBinding("request-one", "payload"))
	if err != nil {
		t.Fatal(err)
	}
	closeAttemptStore(t, store)

	store = openDurableStoreForTest(t, path, header)
	defer store.Close()
	coordinator, err = NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	recovered, err := coordinator.RecoverAfterReopen()
	if err != nil {
		t.Fatal(err)
	}
	if recovered != 1 {
		t.Fatalf("recovered armed sends = %d, want 1", recovered)
	}
	after, err := coordinator.Snapshot(prepared.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	if after.State != AttemptDeliveryUnknown || after.SendTryID != lineage.SendTryID {
		t.Fatalf("recovered state = %+v, want delivery_unknown with exact lineage", after)
	}
	if _, err := coordinator.ArmSend(fence, attemptBinding("request-two", "payload")); !errors.Is(err, ErrAttemptTransition) {
		t.Fatalf("blind repost error = %v, want forbidden transition", err)
	}
	server := newFakeEveServer(t)
	defer server.Close()
	if state := server.State(); state.Creates != 0 {
		t.Fatalf("recovery performed %d unrequested creates", state.Creates)
	}
}

func TestSessionKnownReopensByReconnect(t *testing.T) {
	path, header, store, coordinator := newAttemptTestCoordinator(t)
	prepared, fence, lineage := armedAttemptForTest(t, coordinator, 2)
	responseDigest := digestHex([]byte("create-response"))
	known, err := coordinator.MapSession(fence, lineage, "session-001", responseDigest)
	if err != nil {
		t.Fatal(err)
	}
	if known.State != AttemptSessionKnown {
		t.Fatalf("session mapping state = %s", known.State)
	}
	closeAttemptStore(t, store)

	store = openDurableStoreForTest(t, path, header)
	defer store.Close()
	coordinator, err = NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	recovered, err := coordinator.RecoverAfterReopen()
	if err != nil {
		t.Fatal(err)
	}
	if recovered != 0 {
		t.Fatalf("known session was treated as armed: recovered=%d", recovered)
	}
	attached, err := coordinator.AttachStream(fence, "session-001", "")
	if err != nil {
		t.Fatal(err)
	}
	if attached.State != AttemptStreamAttached || attached.AttemptID != prepared.AttemptID {
		t.Fatalf("reconnect did not retain exact attempt/session: %+v", attached)
	}
	if _, err := coordinator.ArmSend(fence, attemptBinding("another-create", "payload")); !errors.Is(err, ErrAttemptTransition) {
		t.Fatalf("known session recreated: %v", err)
	}
}

func TestStaleFenceRejectsWithoutAppend(t *testing.T) {
	_, _, store, coordinator := newAttemptTestCoordinator(t)
	defer store.Close()
	prepared := prepareAttemptForTest(t, coordinator, 2)
	stale := claimAttemptForTest(t, coordinator, prepared.AttemptID, "worker-old", attemptTestNow)
	current, err := coordinator.Claim(prepared.AttemptID, "worker-new", attemptTestNow.Add(2*time.Minute), time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	before, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if _, err := coordinator.ArmSend(stale, attemptBinding("stale", "payload")); !errors.Is(err, ErrAttemptStaleFence) {
		t.Fatalf("stale fence error = %v", err)
	}
	after, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(before, after) {
		t.Fatal("stale fence appended a durable record")
	}
	if _, err := coordinator.ArmSend(current, attemptBinding("current", "payload")); err != nil {
		t.Fatal(err)
	}
}

func TestSingleSchedulerAblationRejectsSecondOwner(t *testing.T) {
	_, _, store, first := newAttemptTestCoordinator(t)
	defer store.Close()
	prepared := prepareAttemptForTest(t, first, 2)
	second, err := NewAttemptCoordinator(store)
	if err != nil {
		t.Fatal(err)
	}
	server := newFakeEveServer(t)
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	request := testPreparedEveRequest(t)
	type schedulerResult struct {
		err       error
		sessionID string
	}
	start := make(chan struct{})
	results := make(chan schedulerResult, 2)
	var wait sync.WaitGroup
	for index, coordinator := range []*AttemptCoordinator{first, second} {
		wait.Add(1)
		go func(index int, coordinator *AttemptCoordinator) {
			defer wait.Done()
			<-start
			owner := "scheduler-a"
			if index == 1 {
				owner = "scheduler-b"
			}
			fence, claimErr := coordinator.Claim(prepared.AttemptID, owner, attemptTestNow, time.Minute)
			if claimErr != nil {
				results <- schedulerResult{err: claimErr}
				return
			}
			lineage, armErr := coordinator.ArmSend(fence, RequestBinding{
				RequestFingerprint: request.RequestFingerprint, RequestPayloadSHA256: request.RequestSHA256,
			})
			if armErr != nil {
				results <- schedulerResult{err: armErr}
				return
			}
			created, createErr := adapter.Create(context.Background(), request.RequestBytes)
			if createErr != nil {
				results <- schedulerResult{err: createErr}
				return
			}
			if _, mapErr := coordinator.MapSession(fence, lineage, created.SessionID, created.ResponseSHA256); mapErr != nil {
				results <- schedulerResult{err: mapErr}
				return
			}
			results <- schedulerResult{sessionID: created.SessionID}
		}(index, coordinator)
	}
	close(start)
	wait.Wait()
	close(results)
	successes := 0
	for result := range results {
		if result.err == nil {
			successes++
			if result.sessionID != "session-1" {
				t.Fatalf("winning session = %q", result.sessionID)
			}
			continue
		}
		if !errors.Is(result.err, ErrAttemptLeaseHeld) && !errors.Is(result.err, ErrDurableStoreExpectation) {
			t.Fatalf("losing scheduler error = %v", result.err)
		}
	}
	if successes != 1 || server.State().Creates != 1 {
		t.Fatalf("scheduler successes=%d server=%+v", successes, server.State())
	}
	rebuilt, err := NewAttemptCoordinator(store)
	if err != nil {
		t.Fatalf("concurrent claim left corrupt projection: %v", err)
	}
	state, err := rebuilt.Snapshot(prepared.AttemptID)
	if err != nil || state.State != AttemptSessionKnown || state.SessionID != "session-1" {
		t.Fatalf("winner did not own the one mapped session: %+v %v", state, err)
	}
}

func TestKnownNotSentRetriesSameAttemptWithNextTry(t *testing.T) {
	_, _, store, coordinator := newAttemptTestCoordinator(t)
	defer store.Close()
	prepared, fence, first := armedAttemptForTest(t, coordinator, 2)
	proof, err := NewLiveKnownNotSentProof(first, "CONNECT_REFUSED_BEFORE_WRITE", "adapter-call-001")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := coordinator.MarkKnownNotSent(fence, proof); err != nil {
		t.Fatal(err)
	}
	next, err := coordinator.AllocateNextSendTry(fence)
	if err != nil {
		t.Fatal(err)
	}
	if next.AttemptID != prepared.AttemptID || next.SendTryOrdinal != 2 || next.State != AttemptPrepared {
		t.Fatalf("retry changed attempt instead of send try: %+v", next)
	}
	second, err := coordinator.ArmSend(fence, attemptBinding("request-try-two", "payload"))
	if err != nil {
		t.Fatal(err)
	}
	if second.AttemptID != first.AttemptID || second.SendTryOrdinal != 2 || second.SendTryID == first.SendTryID || second.RequestPayloadSHA256 != first.RequestPayloadSHA256 {
		t.Fatalf("same-attempt retry lineage invalid: first=%+v second=%+v", first, second)
	}
}

func TestAmbiguousSendCannotRetryWithoutProof(t *testing.T) {
	_, _, store, coordinator := newAttemptTestCoordinator(t)
	defer store.Close()
	_, fence, lineage := armedAttemptForTest(t, coordinator, 2)
	unknown, err := coordinator.MarkDeliveryUnknown(fence, lineage, DeliveryAmbiguity{Code: "TIMEOUT", EvidenceRef: "adapter-timeout-001"})
	if err != nil {
		t.Fatal(err)
	}
	if unknown.State != AttemptDeliveryUnknown {
		t.Fatalf("ambiguous send state = %s", unknown.State)
	}
	liveProof, err := NewLiveKnownNotSentProof(lineage, "TIME_ELAPSED", "clock-only")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := coordinator.MarkKnownNotSent(fence, liveProof); !errors.Is(err, ErrAttemptProof) {
		t.Fatalf("elapsed-time proof error = %v, want proof rejection", err)
	}
	if _, err := coordinator.AllocateNextSendTry(fence); !errors.Is(err, ErrAttemptTransition) {
		t.Fatalf("unknown delivery allocated retry: %v", err)
	}
}

func TestBoundNotSentReconciliationAllowsNextTry(t *testing.T) {
	_, _, store, coordinator := newAttemptTestCoordinator(t)
	defer store.Close()
	prepared, fence, lineage := armedAttemptForTest(t, coordinator, 2)
	if _, err := coordinator.MarkDeliveryUnknown(fence, lineage, DeliveryAmbiguity{Code: "EOF", EvidenceRef: "adapter-eof-001"}); err != nil {
		t.Fatal(err)
	}
	proof, err := NewBoundNotSentReconciliation(lineage, "lookup-proof-001", "operator-continuation-001")
	if err != nil {
		t.Fatal(err)
	}
	known, err := coordinator.MarkKnownNotSent(fence, proof)
	if err != nil {
		t.Fatal(err)
	}
	if known.State != AttemptKnownNotSent {
		t.Fatalf("reconciled state = %s", known.State)
	}
	next, err := coordinator.AllocateNextSendTry(fence)
	if err != nil {
		t.Fatal(err)
	}
	if next.AttemptID != prepared.AttemptID || next.SendTryOrdinal != 2 {
		t.Fatalf("bound reconciliation did not preserve attempt: %+v", next)
	}
}

func TestCorrelatedLateResponseMapsWithoutRecreate(t *testing.T) {
	_, _, store, coordinator := newAttemptTestCoordinator(t)
	defer store.Close()
	prepared, fence, lineage := armedAttemptForTest(t, coordinator, 2)
	if _, err := coordinator.MarkDeliveryUnknown(fence, lineage, DeliveryAmbiguity{Code: "CRASH_AFTER_ARM", EvidenceRef: "reopen-001"}); err != nil {
		t.Fatal(err)
	}
	recoveryFence, err := coordinator.Claim(prepared.AttemptID, "worker-recovery", attemptTestNow.Add(2*time.Minute), time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	proof, err := NewCorrelatedLateSessionProof(lineage, "late-session", digestHex([]byte("late-response")), "late-call-return-001")
	if err != nil {
		t.Fatal(err)
	}
	createCalls := 0
	mapped, err := coordinator.CorrelateLateSession(recoveryFence, proof)
	if err != nil {
		t.Fatal(err)
	}
	if createCalls != 0 || mapped.State != AttemptSessionKnown || mapped.SessionID != "late-session" || mapped.AttemptID != prepared.AttemptID {
		t.Fatalf("late response did not map without create: calls=%d snapshot=%+v", createCalls, mapped)
	}
	duplicate, err := coordinator.CorrelateLateSession(recoveryFence, proof)
	if err != nil || duplicate.SessionID != "late-session" {
		t.Fatalf("exact duplicate mapping was not inert: %+v, %v", duplicate, err)
	}
	conflict, err := NewCorrelatedLateSessionProof(lineage, "conflicting-session", digestHex([]byte("other-response")), "late-call-return-002")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := coordinator.CorrelateLateSession(recoveryFence, conflict); !errors.Is(err, ErrAttemptSessionConflict) {
		t.Fatalf("conflicting session error = %v", err)
	}
	blocked, err := coordinator.Snapshot(prepared.AttemptID)
	if err != nil {
		t.Fatal(err)
	}
	if blocked.State != AttemptBlocked || blocked.SessionID != "late-session" {
		t.Fatalf("conflict replaced mapping or failed to block: %+v", blocked)
	}
}

func TestAttemptCancelBlockAndAcknowledgementRequireTypedEvidence(t *testing.T) {
	t.Run("cancel and block", func(t *testing.T) {
		_, _, store, coordinator := newAttemptTestCoordinator(t)
		defer store.Close()
		prepared, fence, lineage := armedAttemptForTest(t, coordinator, 1)
		if _, err := coordinator.MapSession(fence, lineage, "session-cancel", digestHex([]byte("response"))); err != nil {
			t.Fatal(err)
		}
		cancelled, err := coordinator.RequestCancel(fence, "session-cancel", "cancel-authority-001")
		if err != nil {
			t.Fatal(err)
		}
		if cancelled.State != AttemptCancelRequested {
			t.Fatalf("cancel state = %s", cancelled.State)
		}
		blocked, err := coordinator.Block(fence, "CANCELLED_WITHOUT_TERMINAL", "stream-observation-001")
		if err != nil {
			t.Fatal(err)
		}
		if blocked.State != AttemptBlocked || blocked.AttemptID != prepared.AttemptID {
			t.Fatalf("blocked state = %+v", blocked)
		}
	})

	t.Run("acknowledgement", func(t *testing.T) {
		_, _, store, coordinator := newAttemptTestCoordinator(t)
		defer store.Close()
		prepared, fence, lineage := armedAttemptForTest(t, coordinator, 1)
		if _, err := coordinator.MapSession(fence, lineage, "session-ack", digestHex([]byte("response"))); err != nil {
			t.Fatal(err)
		}
		if _, err := coordinator.Acknowledge(fence, TerminalAdmissionProof{}); !errors.Is(err, ErrAttemptProof) {
			t.Fatalf("empty admission proof error = %v", err)
		}
		admissionKey := taggedDigest("terminal-key-001")
		unbound, err := NewTerminalAdmissionProof(prepared.AttemptID, "session-ack", admissionKey, 9)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := coordinator.Acknowledge(fence, unbound); !errors.Is(err, ErrAttemptProof) {
			t.Fatalf("unbound admission proof error = %v", err)
		}
		terminalResponse := durableAppliedResponse("terminal-stream", "terminal-cursor", "")
		runtime, err := NewDurableRuntime(&scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
			return terminalResponse, nil
		}}, localCompilation(), store)
		if err != nil {
			t.Fatal(err)
		}
		rawTerminal := []byte("terminal-event")
		response, err := runtime.Reduce(context.Background(), KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "terminal-stream", RawAcceptedEvent: rawTerminal})
		if err != nil {
			t.Fatal(err)
		}
		semanticSequence, err := findSemanticCommitSequence(store, digestHex(rawTerminal), response.AcceptedEventIdentity)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := appendClosedTerminalRecord(store, terminalAdmissionRecord{
			AdmissionKey: admissionKey, AttemptID: prepared.AttemptID, SessionID: "session-ack",
			OutputSHA256: taggedDigest("terminal-output"), AcceptedEventIdentity: response.AcceptedEventIdentity,
			SemanticCommitSequence: semanticSequence,
		}); err != nil {
			t.Fatal(err)
		}
		proof, err := NewTerminalAdmissionProof(prepared.AttemptID, "session-ack", admissionKey, semanticSequence)
		if err != nil {
			t.Fatal(err)
		}
		acknowledged, err := coordinator.Acknowledge(fence, proof)
		if err != nil {
			t.Fatal(err)
		}
		if acknowledged.State != AttemptAcknowledged {
			t.Fatalf("acknowledged state = %s", acknowledged.State)
		}
	})
}

func newAttemptTestCoordinator(t *testing.T) (string, DurableStoreHeader, *DurableStore, *AttemptCoordinator) {
	t.Helper()
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableRuntimeHeader()
	store := openDurableStoreForTest(t, path, header)
	runtime, err := NewDurableRuntime(&scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
		return attemptTestCommandResponse, nil
	}}, localCompilation(), store)
	if err != nil {
		store.Close()
		t.Fatal(err)
	}
	if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("attempt-stream", "attempt-event")); err != nil {
		store.Close()
		t.Fatal(err)
	}
	coordinator, err := NewAttemptCoordinator(store)
	if err != nil {
		store.Close()
		t.Fatal(err)
	}
	return path, header, store, coordinator
}

func prepareAttemptForTest(t *testing.T, coordinator *AttemptCoordinator, maxSendTries uint64) AttemptSnapshot {
	t.Helper()
	prepared, err := coordinator.Prepare(AttemptPreparation{
		CommandIntentIdentity: attemptTestCommandResponse.CommandIntentIdentity,
		AdapterProfile:        "eve-leaf-v1",
		AttemptOrdinal:        1,
		MaxSendTries:          maxSendTries,
	})
	if err != nil {
		t.Fatal(err)
	}
	return prepared
}

func claimAttemptForTest(t *testing.T, coordinator *AttemptCoordinator, attemptID, owner string, now time.Time) AttemptFence {
	t.Helper()
	fence, err := coordinator.Claim(attemptID, owner, now, time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	return fence
}

func armedAttemptForTest(t *testing.T, coordinator *AttemptCoordinator, maxSendTries uint64) (AttemptSnapshot, AttemptFence, SendTryLineage) {
	t.Helper()
	prepared := prepareAttemptForTest(t, coordinator, maxSendTries)
	fence := claimAttemptForTest(t, coordinator, prepared.AttemptID, "worker-a", attemptTestNow)
	lineage, err := coordinator.ArmSend(fence, attemptBinding("request-try-one", "payload"))
	if err != nil {
		t.Fatal(err)
	}
	return prepared, fence, lineage
}

func attemptBinding(request, payload string) RequestBinding {
	return RequestBinding{RequestFingerprint: digestHex([]byte(request)), RequestPayloadSHA256: digestHex([]byte(payload))}
}

func closeAttemptStore(t *testing.T, store *DurableStore) {
	t.Helper()
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
}
