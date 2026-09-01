package rwosidecar

import (
	"bytes"
	"context"
	"fmt"
	"sync"
)

// compiledReducer is the smallest private contract LocalRuntime needs from a
// child. It deliberately exposes only opaque byte reduction, never a Go
// implementation of semantic admission, compilation, or reduction.
type compiledReducer interface {
	ReduceCompiled(context.Context, string, []byte, KernelRequest) (KernelResponse, error)
}

// LocalRuntime owns only volatile host state for one child-owned compiled
// graph. A restart means constructing another runtime: this type deliberately
// contains no journal, checkpoint, retry queue, recovery, or delivery logic.
type LocalRuntime struct {
	child         compiledReducer
	graphHandle   string
	graphIdentity string

	locksMu     sync.Mutex
	streamLocks map[string]*sync.Mutex
	streamsMu   sync.Mutex
	streams     map[string]*volatileStream
}

// RuntimeKernel names the configured stateful Kernel role at the transport
// boundary. It is an alias for LocalRuntime so no second state machine exists.
type RuntimeKernel = LocalRuntime

type volatileStream struct {
	cursor []byte
	outbox map[string][]byte
}

// NewLocalRuntime binds one already-compiled graph to volatile Go-owned state.
// A rejected compilation cannot be turned into a runtime by this constructor.
func NewLocalRuntime(child compiledReducer, compilation CompileResponse) (*LocalRuntime, error) {
	if child == nil {
		return nil, fmt.Errorf("%w: compiled reducer is required", ErrMalformedEnvelope)
	}
	if compilation.Outcome != "Compiled" || compilation.GraphHandle == "" || compilation.GraphIdentity == "" {
		return nil, fmt.Errorf("%w: a successful child compilation is required", ErrMalformedEnvelope)
	}
	return &LocalRuntime{
		child:         child,
		graphHandle:   compilation.GraphHandle,
		graphIdentity: compilation.GraphIdentity,
		streamLocks:   make(map[string]*sync.Mutex),
		streams:       make(map[string]*volatileStream),
	}, nil
}

// NewRuntimeKernel is the Work-Pack-facing constructor for a volatile runtime.
func NewRuntimeKernel(child *ProcessKernel, compilation CompileResponse) (*RuntimeKernel, error) {
	return NewLocalRuntime(child, compilation)
}

// Close clears all volatile state and closes the underlying child when it is a
// ProcessKernel. There is intentionally no persistence or recovery path.
func (runtime *LocalRuntime) Close() error {
	if runtime == nil {
		return nil
	}
	runtime.streamsMu.Lock()
	runtime.streams = make(map[string]*volatileStream)
	runtime.streamsMu.Unlock()
	if child, ok := runtime.child.(*ChildKernel); ok {
		return child.Close()
	}
	return nil
}

// Reduce calls Rust with the last volatile cursor for the stream hint, then
// commits only an Applied response which Rust verified to the same stream. The
// state transition and optional immutable command append share one per-stream
// critical section. All other outcomes leave host maps unchanged.
func (runtime *LocalRuntime) Reduce(ctx context.Context, request KernelRequest) (KernelResponse, error) {
	if runtime == nil || runtime.child == nil {
		return KernelResponse{}, ErrKernelClosed
	}
	if err := request.validate(); err != nil {
		return KernelResponse{}, err
	}
	key := runtime.streamKey(request.StreamIDHint)
	streamLock := runtime.lockFor(key)
	streamLock.Lock()
	defer streamLock.Unlock()

	runtime.streamsMu.Lock()
	stream := runtime.streams[key]
	var original []byte
	if stream != nil {
		original = cloneBytes(stream.cursor)
	}
	runtime.streamsMu.Unlock()
	response, err := runtime.child.ReduceCompiled(ctx, runtime.graphHandle, original, request)
	if err != nil {
		// A transport/control uncertainty is intentionally not a recovery or
		// retry signal. Service maps it to one unknown observation.
		return KernelResponse{}, err
	}
	if !validOutcome(response.Outcome) {
		return KernelResponse{}, fmt.Errorf("%w: %q", ErrInvalidKernelResponse, response.Outcome)
	}

	if response.Outcome != "Applied" {
		if len(response.CommandIntent) != 0 {
			return KernelResponse{}, fmt.Errorf("%w: command on %s", ErrInvalidKernelResponse, response.Outcome)
		}
		if !bytes.Equal(response.NextCursor, original) {
			return KernelResponse{}, fmt.Errorf("%w: non-applied response changed cursor", ErrInvalidKernelResponse)
		}
		// Rust may expose the admitted stream from a rejected stream-hint
		// mismatch. That remains non-committing; all other non-applied results
		// must agree with the locked routing key.
		if response.Outcome != "Rejected" && response.ValidatedStreamID != request.StreamIDHint {
			return KernelResponse{}, fmt.Errorf("%w: non-applied response changed stream", ErrInvalidKernelResponse)
		}
		return cloneKernelResponse(response), nil
	}

	if response.ValidatedStreamID == "" || response.ValidatedStreamID != request.StreamIDHint {
		return KernelResponse{}, fmt.Errorf("%w: applied response stream mismatch", ErrInvalidKernelResponse)
	}
	if len(response.NextCursor) == 0 {
		return KernelResponse{}, fmt.Errorf("%w: applied response lacks cursor", ErrInvalidKernelResponse)
	}
	if len(response.CommandIntent) != 0 {
		if response.CommandIntentIdentity == "" {
			return KernelResponse{}, fmt.Errorf("%w: command lacks immutable identity", ErrInvalidKernelResponse)
		}
	}

	runtime.streamsMu.Lock()
	if stream == nil {
		stream = &volatileStream{outbox: make(map[string][]byte)}
		runtime.streams[key] = stream
	}
	if len(response.CommandIntent) != 0 {
		if existing, exists := stream.outbox[response.CommandIntentIdentity]; exists && !bytes.Equal(existing, response.CommandIntent) {
			runtime.streamsMu.Unlock()
			return KernelResponse{}, fmt.Errorf("%w: command intent identity conflicts with bytes", ErrInvalidKernelResponse)
		}
	}
	stream.cursor = cloneBytes(response.NextCursor)
	if len(response.CommandIntent) != 0 {
		if _, exists := stream.outbox[response.CommandIntentIdentity]; !exists {
			stream.outbox[response.CommandIntentIdentity] = cloneBytes(response.CommandIntent)
		}
	}
	runtime.streamsMu.Unlock()
	return cloneKernelResponse(response), nil
}

func (runtime *LocalRuntime) streamKey(streamIDHint string) string {
	return runtime.graphIdentity + "\x00" + streamIDHint
}

func (runtime *LocalRuntime) lockFor(key string) *sync.Mutex {
	runtime.locksMu.Lock()
	defer runtime.locksMu.Unlock()
	if lock := runtime.streamLocks[key]; lock != nil {
		return lock
	}
	lock := new(sync.Mutex)
	runtime.streamLocks[key] = lock
	return lock
}

// snapshot is test-only evidence of the volatile map. It returns copies so a
// caller cannot mutate runtime state. No durable export is provided.
func (runtime *LocalRuntime) snapshot(streamIDHint string) (cursor []byte, outbox map[string][]byte, exists bool) {
	if runtime == nil {
		return nil, nil, false
	}
	key := runtime.streamKey(streamIDHint)
	streamLock := runtime.lockFor(key)
	streamLock.Lock()
	defer streamLock.Unlock()
	runtime.streamsMu.Lock()
	stream := runtime.streams[key]
	if stream == nil {
		runtime.streamsMu.Unlock()
		return nil, nil, false
	}
	copyOutbox := make(map[string][]byte, len(stream.outbox))
	for identity, command := range stream.outbox {
		copyOutbox[identity] = cloneBytes(command)
	}
	cursor = cloneBytes(stream.cursor)
	runtime.streamsMu.Unlock()
	return cursor, copyOutbox, true
}

func cloneKernelResponse(response KernelResponse) KernelResponse {
	response.NextCursor = cloneBytes(response.NextCursor)
	response.CommandIntent = cloneBytes(response.CommandIntent)
	response.DefectCodes = append([]string(nil), response.DefectCodes...)
	return response
}

func cloneBytes(value []byte) []byte {
	if value == nil {
		return nil
	}
	return append([]byte(nil), value...)
}
