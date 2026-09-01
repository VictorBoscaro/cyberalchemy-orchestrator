package rwosidecar

import (
	"context"
	"errors"
	"sync"
	"testing"
)

type scriptedReducer struct {
	mu        sync.Mutex
	requests  []KernelRequest
	originals [][]byte
	reduce    func([]byte, KernelRequest) (KernelResponse, error)
}

func (reducer *scriptedReducer) ReduceCompiled(_ context.Context, _ string, original []byte, request KernelRequest) (KernelResponse, error) {
	reducer.mu.Lock()
	defer reducer.mu.Unlock()
	reducer.requests = append(reducer.requests, request)
	reducer.originals = append(reducer.originals, cloneBytes(original))
	return reducer.reduce(original, request)
}

func localCompilation() CompileResponse {
	return CompileResponse{Outcome: "Compiled", GraphHandle: "graph-1", GraphIdentity: "sha256:graph"}
}

func TestLocalRuntimeCommitsOnlyVerifiedAppliedTransition(t *testing.T) {
	reducer := &scriptedReducer{reduce: func(original []byte, request KernelRequest) (KernelResponse, error) {
		if request.StreamIDHint == "never-applied" {
			return KernelResponse{Outcome: "Rejected", ValidatedStreamID: "other-stream", NextCursor: cloneBytes(original), DefectCodes: []string{"STREAM_ID_MISMATCH"}}, nil
		}
		if len(original) == 0 {
			return KernelResponse{
				Outcome: "Applied", ValidatedStreamID: request.StreamIDHint, NextCursor: []byte("cursor-1"),
				CommandIntent: []byte("command-1"), CommandIntentIdentity: "sha256:command-1",
			}, nil
		}
		return KernelResponse{Outcome: "Rejected", ValidatedStreamID: "other-stream", NextCursor: cloneBytes(original), DefectCodes: []string{"STREAM_ID_MISMATCH"}}, nil
	}}
	runtime, err := NewLocalRuntime(reducer, localCompilation())
	if err != nil {
		t.Fatal(err)
	}
	request := KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: []byte("raw-event")}
	first, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	if first.Outcome != "Applied" {
		t.Fatalf("unexpected first response: %#v", first)
	}
	cursor, outbox, exists := runtime.snapshot("stream-1")
	if !exists || string(cursor) != "cursor-1" || string(outbox["sha256:command-1"]) != "command-1" {
		t.Fatalf("unexpected committed volatile state: %q %#v %t", cursor, outbox, exists)
	}
	second, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	if second.Outcome != "Rejected" {
		t.Fatalf("unexpected second response: %#v", second)
	}
	cursor, outbox, exists = runtime.snapshot("stream-1")
	if !exists || string(cursor) != "cursor-1" || len(outbox) != 1 {
		t.Fatalf("non-applied result mutated volatile state: %q %#v %t", cursor, outbox, exists)
	}

	other := KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "never-applied", RawAcceptedEvent: []byte("raw-event")}
	if _, err := runtime.Reduce(context.Background(), other); err != nil {
		t.Fatal(err)
	}
	if _, _, exists := runtime.snapshot("never-applied"); exists {
		t.Fatal("rejected stream must not create a cursor or outbox map entry")
	}
}

func TestLocalRuntimeRejectsInvalidChildOutputWithoutCommit(t *testing.T) {
	reducer := &scriptedReducer{reduce: func(_ []byte, request KernelRequest) (KernelResponse, error) {
		return KernelResponse{Outcome: "Applied", ValidatedStreamID: "different", NextCursor: []byte("forbidden")}, nil
	}}
	runtime, err := NewLocalRuntime(reducer, localCompilation())
	if err != nil {
		t.Fatal(err)
	}
	_, err = runtime.Reduce(context.Background(), KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: []byte("raw")})
	if !errors.Is(err, ErrInvalidKernelResponse) {
		t.Fatalf("expected invalid child output, got %v", err)
	}
	if _, _, exists := runtime.snapshot("stream-1"); exists {
		t.Fatal("invalid applied response must not commit state")
	}
}

func TestLocalRuntimeSerializesSameStreamAndEmitsAtMostOneCommand(t *testing.T) {
	reducer := &scriptedReducer{reduce: func(original []byte, request KernelRequest) (KernelResponse, error) {
		if len(original) == 0 {
			return KernelResponse{
				Outcome: "Applied", ValidatedStreamID: request.StreamIDHint, NextCursor: []byte("cursor-1"),
				CommandIntent: []byte("command-1"), CommandIntentIdentity: "sha256:command-1",
			}, nil
		}
		return KernelResponse{Outcome: "Duplicate", ValidatedStreamID: request.StreamIDHint, NextCursor: cloneBytes(original)}, nil
	}}
	runtime, err := NewLocalRuntime(reducer, localCompilation())
	if err != nil {
		t.Fatal(err)
	}
	request := KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: []byte("raw")}
	results := make(chan KernelResponse, 2)
	errors := make(chan error, 2)
	for range 2 {
		go func() {
			response, err := runtime.Reduce(context.Background(), request)
			results <- response
			errors <- err
		}()
	}
	for range 2 {
		if err := <-errors; err != nil {
			t.Fatal(err)
		}
		<-results
	}
	cursor, outbox, exists := runtime.snapshot("stream-1")
	if !exists || string(cursor) != "cursor-1" || len(outbox) != 1 {
		t.Fatalf("same-stream concurrent reductions broke atomicity: %q %#v", cursor, outbox)
	}
}

func TestNewLocalRuntimeRequiresSuccessfulCompilation(t *testing.T) {
	_, err := NewLocalRuntime(&scriptedReducer{}, CompileResponse{Outcome: "Rejected"})
	if !errors.Is(err, ErrMalformedEnvelope) {
		t.Fatalf("expected malformed compilation binding, got %v", err)
	}
}

func TestServiceMapsRuntimeUncertaintyToOneUnknownWithoutState(t *testing.T) {
	reducer := &scriptedReducer{reduce: func(_ []byte, _ KernelRequest) (KernelResponse, error) {
		return KernelResponse{}, errors.New("child EOF")
	}}
	runtime, err := NewLocalRuntime(reducer, localCompilation())
	if err != nil {
		t.Fatal(err)
	}
	observation, err := (Service{Kernel: runtime}).Reduce(context.Background(), fixtureEnvelope([]byte("raw")))
	if err != nil {
		t.Fatal(err)
	}
	if observation.Status != "unknown" || observation.UncertaintyReason != "KERNEL_UNAVAILABLE_OR_UNCERTAIN" {
		t.Fatalf("runtime uncertainty invented a retry or result: %#v", observation)
	}
	if _, _, exists := runtime.snapshot("stream-1"); exists {
		t.Fatal("uncertain child call must not create volatile runtime state")
	}
}
