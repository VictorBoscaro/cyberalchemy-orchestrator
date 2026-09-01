package rwosidecar

import (
	"bytes"
	"context"
	"errors"
	"os"
	"path/filepath"
	"reflect"
	"sync"
	"testing"
)

func TestDurableRuntimeCommitsRustResponseAndRebuildsExactly(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	store := openDurableRuntimeStore(t, path)
	response := durableAppliedResponse("stream-1", "cursor-one", "command-one")
	reducer := &scriptedReducer{reduce: func(original []byte, request KernelRequest) (KernelResponse, error) {
		if len(original) != 0 || request.StreamIDHint != "stream-1" {
			t.Fatalf("unexpected reducer input: cursor=%q request=%+v", original, request)
		}
		return response, nil
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	request := durableRuntimeRequest("stream-1", "raw-event-one")
	got, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	if !kernelResponsesEqual(got, response) {
		t.Fatalf("durable response changed Rust evidence: got=%+v want=%+v", got, response)
	}
	snapshot := runtime.Snapshot("stream-1")
	if !snapshot.Exists || snapshot.SemanticCommitCount != 1 || snapshot.CommittedReplayCount != 0 ||
		!bytes.Equal(snapshot.Cursor, response.NextCursor) || !bytes.Equal(snapshot.Outbox[response.CommandIntentIdentity], response.CommandIntent) {
		t.Fatalf("unexpected live projection: %+v", snapshot)
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
	after := rebuilt.Snapshot("stream-1")
	if !bytes.Equal(after.Cursor, snapshot.Cursor) || len(after.Outbox) != 1 ||
		!bytes.Equal(after.Outbox[response.CommandIntentIdentity], response.CommandIntent) || after.SemanticCommitCount != 1 {
		t.Fatalf("projection drift after reopen: before=%+v after=%+v", snapshot, after)
	}
}

func TestCommittedReplayPreservesRustOutcomeWithoutSecondOutbox(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	store := openDurableRuntimeStore(t, path)
	defer store.Close()
	calls := 0
	response := durableAppliedResponse("stream-1", "cursor-one", "command-one")
	reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
		calls++
		return response, nil
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	request := durableRuntimeRequest("stream-1", "same-raw-event")
	first, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	second, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	if calls != 1 {
		t.Fatalf("committed replay called Rust %d times, want 1", calls)
	}
	if second.Outcome != "Applied" || !kernelResponsesEqual(first, second) {
		t.Fatalf("Go synthesized a different replay result: first=%+v second=%+v", first, second)
	}
	snapshot := runtime.Snapshot("stream-1")
	if snapshot.SemanticCommitCount != 1 || snapshot.CommittedReplayCount != 1 || len(snapshot.Outbox) != 1 {
		t.Fatalf("replay changed semantic counts: %+v", snapshot)
	}
	storeSnapshot, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if len(storeSnapshot.Records) != 2 || storeSnapshot.Records[0].Type != RecordTypeSemanticCommitV1 || storeSnapshot.Records[1].Type != RecordTypeCommittedReplayV1 {
		t.Fatalf("unexpected record sequence: %+v", storeSnapshot.Records)
	}
}

func TestDurableRuntimeCrashBeforeSemanticAppendLeavesNoState(t *testing.T) {
	store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
	defer store.Close()
	reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
		return KernelResponse{}, errors.New("child stopped before response")
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw")); err == nil {
		t.Fatal("uncertain child call unexpectedly committed")
	}
	if runtime.Snapshot("stream-1").Exists {
		t.Fatal("pre-append crash created a projection")
	}
	snapshot, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if len(snapshot.Records) != 0 {
		t.Fatalf("pre-append crash wrote records: %+v", snapshot.Records)
	}
}

func TestSyncedSemanticCommitBeforeAckReplaysOneRustOutcome(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableRuntimeHeader()
	injected := errors.New("caller cannot know sync result")
	store, err := OpenDurableStore(path, header, WithDurableStoreFailureHooks(DurableStoreFailureHooks{
		SyncFrame: func(*os.File) error { return injected },
	}))
	if err != nil {
		t.Fatal(err)
	}
	response := durableAppliedResponse("stream-1", "cursor-one", "command-one")
	reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) { return response, nil }}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw")); !errors.Is(err, ErrDurableStoreNeedsReopen) {
		t.Fatalf("uncertain sync error = %v, want needs reopen", err)
	}
	_ = store.Close()

	reopened := openDurableRuntimeStore(t, path)
	defer reopened.Close()
	rebuilt, err := NewDurableRuntime(reducer, localCompilation(), reopened)
	if err != nil {
		t.Fatal(err)
	}
	snapshot := rebuilt.Snapshot("stream-1")
	if snapshot.SemanticCommitCount != 1 || len(snapshot.Outbox) != 1 || !bytes.Equal(snapshot.Cursor, response.NextCursor) {
		t.Fatalf("verified reopen did not decide the complete frame: %+v", snapshot)
	}
	got, err := rebuilt.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw"))
	if err != nil || !kernelResponsesEqual(got, response) {
		t.Fatalf("replay after uncertain acknowledgement: %+v %v", got, err)
	}
	if after := rebuilt.Snapshot("stream-1"); after.SemanticCommitCount != 1 || len(after.Outbox) != 1 {
		t.Fatalf("replay duplicated committed output: %+v", after)
	}
}

func TestFabricatedOrChangedCommandCannotCommit(t *testing.T) {
	cases := []KernelResponse{
		{
			Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor"), CommandIntent: []byte("command"),
			AcceptedEventIdentity: taggedDigest("event"), EventPayloadDigest: taggedDigest("event-payload"),
		},
		{
			Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor"), CommandIntent: []byte("command"),
			AcceptedEventIdentity: taggedDigest("event"), EventPayloadDigest: taggedDigest("event-payload"),
			CommandIntentIdentity: taggedDigest("command"), CommandPayloadDigest: "not-a-rust-digest",
		},
	}
	for index, response := range cases {
		t.Run(string(rune('a'+index)), func(t *testing.T) {
			store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
			defer store.Close()
			reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) { return response, nil }}
			runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
			if err != nil {
				t.Fatal(err)
			}
			if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw")); !errors.Is(err, ErrInvalidKernelResponse) {
				t.Fatalf("invalid Rust evidence error = %v", err)
			}
			if runtime.Snapshot("stream-1").Exists {
				t.Fatal("invalid command evidence committed")
			}
		})
	}

	t.Run("committed identity cannot change bytes", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "runtime.rwolog")
		store := openDurableRuntimeStore(t, path)
		identity := taggedDigest("stable-command-identity")
		responses := []KernelResponse{
			{
				Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor-one"),
				CommandIntent: []byte("command-one"), CommandIntentIdentity: identity,
				CommandPayloadDigest: taggedDigest("command-one"), AcceptedEventIdentity: taggedDigest("event-one"),
				EventPayloadDigest: taggedDigest("event-payload-one"),
			},
			{
				Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor-two"),
				CommandIntent: []byte("command-two"), CommandIntentIdentity: identity,
				CommandPayloadDigest: taggedDigest("command-two"), AcceptedEventIdentity: taggedDigest("event-two"),
				EventPayloadDigest: taggedDigest("event-payload-two"),
			},
		}
		calls := 0
		reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
			response := responses[calls]
			calls++
			return response, nil
		}}
		runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw-one")); err != nil {
			t.Fatal(err)
		}
		before, err := store.Snapshot()
		if err != nil {
			t.Fatal(err)
		}
		if _, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw-two")); !errors.Is(err, ErrInvalidKernelResponse) {
			t.Fatalf("conflicting command error = %v", err)
		}
		after, err := store.Snapshot()
		if err != nil {
			t.Fatal(err)
		}
		if !reflect.DeepEqual(before, after) {
			t.Fatal("conflicting command appended before rejection")
		}
		if err := store.Close(); err != nil {
			t.Fatal(err)
		}
		reopened := openDurableRuntimeStore(t, path)
		defer reopened.Close()
		rebuilt, err := NewDurableRuntime(reducer, localCompilation(), reopened)
		if err != nil {
			t.Fatalf("verified reopen after rejected conflict: %v", err)
		}
		projection := rebuilt.Snapshot("stream-1")
		if projection.SemanticCommitCount != 1 || !bytes.Equal(projection.Outbox[identity], []byte("command-one")) {
			t.Fatalf("conflict changed committed projection: %+v", projection)
		}
	})
}

func TestDurableRuntimeNonAppliedAndMissingRustAreInert(t *testing.T) {
	t.Run("missing Rust", func(t *testing.T) {
		store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
		defer store.Close()
		if _, err := NewDurableRuntime(nil, localCompilation(), store); !errors.Is(err, ErrMalformedEnvelope) {
			t.Fatalf("nil Rust owner error = %v", err)
		}
	})
	for _, outcome := range []string{"Rejected", "Duplicate", "DivergentDuplicate"} {
		t.Run(outcome, func(t *testing.T) {
			store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
			defer store.Close()
			reducer := &scriptedReducer{reduce: func(original []byte, request KernelRequest) (KernelResponse, error) {
				return KernelResponse{Outcome: outcome, ValidatedStreamID: request.StreamIDHint, NextCursor: cloneBytes(original), DefectCodes: []string{"NON_APPLIED"}}, nil
			}}
			runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
			if err != nil {
				t.Fatal(err)
			}
			response, err := runtime.Reduce(context.Background(), durableRuntimeRequest("stream-1", "raw"))
			if err != nil || response.Outcome != outcome {
				t.Fatalf("non-applied outcome changed: %+v %v", response, err)
			}
			if runtime.Snapshot("stream-1").Exists {
				t.Fatal("non-applied response created durable state")
			}
			snapshot, err := store.Snapshot()
			if err != nil || len(snapshot.Records) != 0 {
				t.Fatalf("non-applied response wrote durable state: records=%d err=%v", len(snapshot.Records), err)
			}
		})
	}
}

func TestDurableRuntimeIndependentStreamsShareOneWriter(t *testing.T) {
	store := openDurableRuntimeStore(t, filepath.Join(t.TempDir(), "runtime.rwolog"))
	defer store.Close()
	reducer := &scriptedReducer{reduce: func(_ []byte, request KernelRequest) (KernelResponse, error) {
		return durableAppliedResponse(request.StreamIDHint, "cursor-"+request.StreamIDHint, "command-"+request.StreamIDHint), nil
	}}
	runtime, err := NewDurableRuntime(reducer, localCompilation(), store)
	if err != nil {
		t.Fatal(err)
	}
	var wait sync.WaitGroup
	errorsChannel := make(chan error, 2)
	for _, stream := range []string{"stream-a", "stream-b"} {
		wait.Add(1)
		go func(stream string) {
			defer wait.Done()
			_, err := runtime.Reduce(context.Background(), durableRuntimeRequest(stream, "raw-"+stream))
			errorsChannel <- err
		}(stream)
	}
	wait.Wait()
	close(errorsChannel)
	for err := range errorsChannel {
		if err != nil {
			t.Fatal(err)
		}
	}
	for _, stream := range []string{"stream-a", "stream-b"} {
		if snapshot := runtime.Snapshot(stream); snapshot.SemanticCommitCount != 1 || len(snapshot.Outbox) != 1 {
			t.Fatalf("stream %s projection: %+v", stream, snapshot)
		}
	}
}

func TestDurableRuntimeRealRustChildPersistsImmutableCommand(t *testing.T) {
	manifest := localManifest(t)
	composition := localFixture(t, manifest, "explicitComposition")
	event := localFixture(t, manifest, "matchingEvent")
	compositionBytes := rawFixture(t, composition)
	child := startFixtureChild(t)
	compiled, err := child.Compile(context.Background(), CompileRequest{
		Tuple: tupleForFixture(composition, "ExplicitComposition"), RawComposition: compositionBytes,
	})
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := DurableStoreHeader{
		StoreFormat: DurableStoreFormatV1, GraphIdentity: compiled.GraphIdentity,
		RawCompositionSHA256: digestHex(compositionBytes), Tuple: tupleForFixture(composition, "ExplicitComposition"),
		StoreInstanceID: "real-rust-durable-test",
	}
	store, err := OpenDurableStore(path, header)
	if err != nil {
		t.Fatal(err)
	}
	runtime, err := NewDurableRuntime(child, compiled, store)
	if err != nil {
		t.Fatal(err)
	}
	raw := rawFixture(t, event)
	response, err := runtime.Reduce(context.Background(), KernelRequest{
		Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "stream-1", RawAcceptedEvent: raw,
	})
	if err != nil {
		t.Fatal(err)
	}
	if response.Outcome != "Applied" || len(response.CommandIntent) == 0 || !isTaggedSHA256(response.CommandIntentIdentity) {
		t.Fatalf("real Rust child did not produce immutable evidence: %+v", response)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	reopened, err := OpenDurableStore(path, header)
	if err != nil {
		t.Fatal(err)
	}
	defer reopened.Close()
	rebuilt, err := NewDurableRuntime(child, compiled, reopened)
	if err != nil {
		t.Fatal(err)
	}
	snapshot := rebuilt.Snapshot("stream-1")
	if snapshot.SemanticCommitCount != 1 || len(snapshot.Outbox) != 1 ||
		!bytes.Equal(snapshot.Outbox[response.CommandIntentIdentity], response.CommandIntent) {
		t.Fatalf("real Rust command did not survive reopen: %+v", snapshot)
	}
	replayed, err := rebuilt.Reduce(context.Background(), KernelRequest{
		Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "stream-1", RawAcceptedEvent: raw,
	})
	if err != nil || !kernelResponsesEqual(replayed, response) {
		t.Fatalf("real Rust committed replay changed evidence: %+v %v", replayed, err)
	}
}

func durableRuntimeHeader() DurableStoreHeader {
	return DurableStoreHeader{
		StoreFormat: DurableStoreFormatV1, GraphIdentity: localCompilation().GraphIdentity,
		RawCompositionSHA256: digestHex([]byte("composition")), Tuple: fixtureTuple(), StoreInstanceID: "durable-runtime-test",
	}
}

func openDurableRuntimeStore(t *testing.T, path string) *DurableStore {
	t.Helper()
	store, err := OpenDurableStore(path, durableRuntimeHeader())
	if err != nil {
		t.Fatal(err)
	}
	return store
}

func durableRuntimeRequest(stream, raw string) KernelRequest {
	return KernelRequest{Tuple: fixtureTuple(), StreamIDHint: stream, RawAcceptedEvent: []byte(raw)}
}

func durableAppliedResponse(stream, cursor, command string) KernelResponse {
	response := KernelResponse{
		Outcome: "Applied", ValidatedStreamID: stream, NextCursor: []byte(cursor),
		AcceptedEventIdentity: taggedDigest("event-" + stream + "-" + cursor), EventPayloadDigest: taggedDigest("payload-" + stream + "-" + cursor),
	}
	if command != "" {
		response.CommandIntent = []byte(command)
		response.CommandIntentIdentity = taggedDigest("identity-" + command)
		response.CommandPayloadDigest = taggedDigest("payload-" + command)
	}
	return response
}

func taggedDigest(value string) string { return "sha256:" + digestHex([]byte(value)) }

func kernelResponsesEqual(left, right KernelResponse) bool {
	return left.Outcome == right.Outcome && bytes.Equal(left.NextCursor, right.NextCursor) &&
		bytes.Equal(left.CommandIntent, right.CommandIntent) && left.ValidatedStreamID == right.ValidatedStreamID &&
		left.AcceptedEventIdentity == right.AcceptedEventIdentity && left.EventPayloadDigest == right.EventPayloadDigest &&
		left.CommandIntentIdentity == right.CommandIntentIdentity && left.CommandPayloadDigest == right.CommandPayloadDigest &&
		bytes.Equal([]byte(joinStrings(left.DefectCodes)), []byte(joinStrings(right.DefectCodes)))
}

func joinStrings(values []string) string {
	var result string
	for _, value := range values {
		result += "\x00" + value
	}
	return result
}
