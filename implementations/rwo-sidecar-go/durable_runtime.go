package rwosidecar

import (
	"bytes"
	"context"
	"encoding/base64"
	"errors"
	"fmt"
	"strings"
	"sync"
)

const (
	// RecordTypeSemanticCommitV1 is one Rust-authored cursor transition and its
	// optional immutable command, committed as one durable frame.
	RecordTypeSemanticCommitV1 DurableRecordType = 0x0201
	// RecordTypeCommittedReplayV1 is a physical observation that an exact raw
	// event was answered from an already-synced Rust result.
	RecordTypeCommittedReplayV1 DurableRecordType = 0x0202
)

// SemanticCommitV1 stores opaque Rust output. Go validates the closed response
// shape, but never decodes the cursor or derives a semantic identity.
type SemanticCommitV1 struct {
	GraphIdentity         string   `json:"graph_identity"`
	StreamID              string   `json:"stream_id"`
	RawEventSHA256        string   `json:"raw_event_sha256"`
	RawEventBase64        string   `json:"raw_event_base64"`
	Outcome               string   `json:"outcome"`
	PreviousCursorSHA256  string   `json:"previous_cursor_sha256"`
	NextCursorSHA256      string   `json:"next_cursor_sha256"`
	NextCursorBase64      string   `json:"next_cursor_base64"`
	CommandIntentBase64   string   `json:"command_intent_base64,omitempty"`
	AcceptedEventIdentity string   `json:"accepted_event_identity"`
	EventPayloadDigest    string   `json:"event_payload_digest"`
	CommandIntentIdentity string   `json:"command_intent_identity,omitempty"`
	CommandPayloadDigest  string   `json:"command_payload_digest,omitempty"`
	DefectCodes           []string `json:"defect_codes"`
}

func (SemanticCommitV1) DurableRecordType() DurableRecordType {
	return RecordTypeSemanticCommitV1
}

// CommittedReplayV1 is deliberately physical evidence. It names the exact
// stored semantic record and does not introduce a Go-authored outcome.
type CommittedReplayV1 struct {
	GraphIdentity          string `json:"graph_identity"`
	StreamID               string `json:"stream_id"`
	RawEventSHA256         string `json:"raw_event_sha256"`
	SemanticCommitSequence uint64 `json:"semantic_commit_sequence"`
}

func (CommittedReplayV1) DurableRecordType() DurableRecordType {
	return RecordTypeCommittedReplayV1
}

type durableCommittedResult struct {
	rawEvent []byte
	response KernelResponse
	sequence uint64
}

type durableRuntimeStream struct {
	cursor  []byte
	outbox  map[string][]byte
	replays map[string]durableCommittedResult
}

// DurableRuntimeSnapshot is a defensive physical projection for tests and
// later coordinator layers. It exposes Rust-owned bytes without interpreting
// them.
type DurableRuntimeSnapshot struct {
	Cursor               []byte
	Outbox               map[string][]byte
	SemanticCommitCount  int
	CommittedReplayCount int
	Exists               bool
}

// DurableRuntime binds one compiled Rust graph to one verified DurableStore.
// The caller owns the child process and the store lifetime.
type DurableRuntime struct {
	child         compiledReducer
	store         *DurableStore
	graphHandle   string
	graphIdentity string

	locksMu      sync.Mutex
	streamLocks  map[string]*sync.Mutex
	projectionMu sync.Mutex
	streams      map[string]*durableRuntimeStream
	commitCount  map[string]int
	replayCount  map[string]int
	appendMu     sync.Mutex
}

// NewDurableRuntime rebuilds projections only from the verified store prefix.
func NewDurableRuntime(child compiledReducer, compilation CompileResponse, store *DurableStore) (*DurableRuntime, error) {
	if child == nil {
		return nil, fmt.Errorf("%w: compiled reducer is required", ErrMalformedEnvelope)
	}
	if store == nil {
		return nil, fmt.Errorf("%w: durable store is required", ErrMalformedEnvelope)
	}
	if compilation.Outcome != "Compiled" || compilation.GraphHandle == "" || compilation.GraphIdentity == "" {
		return nil, fmt.Errorf("%w: a successful child compilation is required", ErrMalformedEnvelope)
	}
	snapshot, err := store.Snapshot()
	if err != nil {
		return nil, err
	}
	if snapshot.Header.GraphIdentity != compilation.GraphIdentity {
		return nil, fmt.Errorf("%w: compiled graph does not match durable header", ErrDurableStoreHeader)
	}
	runtime := &DurableRuntime{
		child:         child,
		store:         store,
		graphHandle:   compilation.GraphHandle,
		graphIdentity: compilation.GraphIdentity,
		streamLocks:   make(map[string]*sync.Mutex),
		streams:       make(map[string]*durableRuntimeStream),
		commitCount:   make(map[string]int),
		replayCount:   make(map[string]int),
	}
	if err := runtime.rebuild(snapshot); err != nil {
		return nil, err
	}
	return runtime, nil
}

// NewDurableRuntimeKernel is the concrete-child convenience constructor. It
// does not transfer child ownership to the runtime.
func NewDurableRuntimeKernel(child *ProcessKernel, compilation CompileResponse, store *DurableStore) (*DurableRuntime, error) {
	return NewDurableRuntime(child, compilation, store)
}

// Close intentionally does not close the injected child or store. Their owner
// decides ordering, which avoids a double-close during reopen tests.
func (runtime *DurableRuntime) Close() error { return nil }

// Reduce serializes one stream from cursor read through Rust and the synced
// semantic frame. Exact committed raw replay returns stored Rust evidence.
func (runtime *DurableRuntime) Reduce(ctx context.Context, request KernelRequest) (KernelResponse, error) {
	if runtime == nil || runtime.child == nil || runtime.store == nil {
		return KernelResponse{}, ErrKernelClosed
	}
	if err := request.validate(); err != nil {
		return KernelResponse{}, err
	}
	key := runtime.streamKey(request.StreamIDHint)
	lock := runtime.lockFor(key)
	lock.Lock()
	defer lock.Unlock()

	rawDigest := digestHex(request.RawAcceptedEvent)
	runtime.projectionMu.Lock()
	stream := runtime.streams[key]
	if stream != nil {
		if committed, ok := stream.replays[rawDigest]; ok && bytes.Equal(committed.rawEvent, request.RawAcceptedEvent) {
			response := cloneKernelResponse(committed.response)
			runtime.projectionMu.Unlock()
			if err := runtime.appendReplay(key, request.StreamIDHint, rawDigest, committed.sequence); err != nil {
				return KernelResponse{}, err
			}
			return response, nil
		}
	}
	var original []byte
	if stream != nil {
		original = cloneBytes(stream.cursor)
	}
	runtime.projectionMu.Unlock()

	response, err := runtime.child.ReduceCompiled(ctx, runtime.graphHandle, original, request)
	if err != nil {
		return KernelResponse{}, err
	}
	if err := validateDurableKernelResponse(response, original, request.StreamIDHint); err != nil {
		return KernelResponse{}, err
	}
	if response.Outcome != "Applied" {
		return cloneKernelResponse(response), nil
	}
	// A Rust command identity is immutable within one stream. Detect a
	// conflicting response before the semantic frame is appended; discovering
	// it only while updating the in-memory projection would leave a synced frame
	// that necessarily fails the next verified reopen.
	if len(response.CommandIntent) != 0 {
		runtime.projectionMu.Lock()
		stream = runtime.streams[key]
		if stream != nil {
			if existing, ok := stream.outbox[response.CommandIntentIdentity]; ok && !bytes.Equal(existing, response.CommandIntent) {
				runtime.projectionMu.Unlock()
				return KernelResponse{}, fmt.Errorf("%w: command identity conflicts with committed bytes", ErrInvalidKernelResponse)
			}
		}
		runtime.projectionMu.Unlock()
	}

	record := SemanticCommitV1{
		GraphIdentity:         runtime.graphIdentity,
		StreamID:              response.ValidatedStreamID,
		RawEventSHA256:        rawDigest,
		RawEventBase64:        base64.StdEncoding.EncodeToString(request.RawAcceptedEvent),
		Outcome:               response.Outcome,
		PreviousCursorSHA256:  digestHex(original),
		NextCursorSHA256:      digestHex(response.NextCursor),
		NextCursorBase64:      base64.StdEncoding.EncodeToString(response.NextCursor),
		CommandIntentBase64:   encodeOptionalBase64(response.CommandIntent),
		AcceptedEventIdentity: response.AcceptedEventIdentity,
		EventPayloadDigest:    response.EventPayloadDigest,
		CommandIntentIdentity: response.CommandIntentIdentity,
		CommandPayloadDigest:  response.CommandPayloadDigest,
		DefectCodes:           append([]string(nil), response.DefectCodes...),
	}
	ref, err := runtime.appendSemantic(key, record)
	if err != nil {
		return KernelResponse{}, err
	}
	runtime.projectionMu.Lock()
	stream = runtime.ensureStreamLocked(key)
	if len(response.CommandIntent) != 0 {
		stream.outbox[response.CommandIntentIdentity] = cloneBytes(response.CommandIntent)
	}
	stream.cursor = cloneBytes(response.NextCursor)
	stream.replays[rawDigest] = durableCommittedResult{
		rawEvent: cloneBytes(request.RawAcceptedEvent), response: cloneKernelResponse(response), sequence: ref.Sequence,
	}
	runtime.commitCount[key]++
	runtime.projectionMu.Unlock()
	return cloneKernelResponse(response), nil
}

func (runtime *DurableRuntime) appendSemantic(streamKey string, record SemanticCommitV1) (DurableRecordRef, error) {
	runtime.appendMu.Lock()
	defer runtime.appendMu.Unlock()
	next, previous, err := runtime.store.Tip()
	if err != nil {
		return DurableRecordRef{}, err
	}
	return runtime.store.Append(AppendExpectation{
		ExpectedSequence: next, ExpectedPreviousFrameSHA256: previous,
		Cursor: &CursorTransition{
			StreamKey: streamKey, ExpectedPreviousSHA256: record.PreviousCursorSHA256, NextSHA256: record.NextCursorSHA256,
		},
	}, record)
}

func (runtime *DurableRuntime) appendReplay(streamKey, streamID, rawDigest string, sequence uint64) error {
	runtime.appendMu.Lock()
	defer runtime.appendMu.Unlock()
	next, previous, err := runtime.store.Tip()
	if err != nil {
		return err
	}
	_, err = runtime.store.Append(AppendExpectation{ExpectedSequence: next, ExpectedPreviousFrameSHA256: previous}, CommittedReplayV1{
		GraphIdentity: runtime.graphIdentity, StreamID: streamID, RawEventSHA256: rawDigest, SemanticCommitSequence: sequence,
	})
	if err != nil {
		return err
	}
	runtime.projectionMu.Lock()
	runtime.replayCount[streamKey]++
	runtime.projectionMu.Unlock()
	return nil
}

func (runtime *DurableRuntime) rebuild(snapshot DurableStoreSnapshot) error {
	for _, stored := range snapshot.Records {
		switch stored.Type {
		case RecordTypeSemanticCommitV1:
			var record SemanticCommitV1
			if err := decodeClosedJSON(stored.Body, &record); err != nil {
				return fmt.Errorf("%w: semantic commit %d: %v", ErrDurableStoreCorrupt, stored.Ref.Sequence, err)
			}
			response, raw, err := validateStoredSemanticCommit(record, runtime.graphIdentity, stored.Cursor)
			if err != nil {
				return fmt.Errorf("%w: semantic commit %d: %v", ErrDurableStoreCorrupt, stored.Ref.Sequence, err)
			}
			key := runtime.streamKey(record.StreamID)
			stream := runtime.ensureStreamLocked(key)
			if digestHex(stream.cursor) != record.PreviousCursorSHA256 {
				return fmt.Errorf("%w: semantic cursor projection at sequence %d", ErrDurableStoreCorrupt, stored.Ref.Sequence)
			}
			if len(response.CommandIntent) != 0 {
				if existing, ok := stream.outbox[response.CommandIntentIdentity]; ok && !bytes.Equal(existing, response.CommandIntent) {
					return fmt.Errorf("%w: command projection at sequence %d", ErrDurableStoreCorrupt, stored.Ref.Sequence)
				}
				stream.outbox[response.CommandIntentIdentity] = cloneBytes(response.CommandIntent)
			}
			stream.cursor = cloneBytes(response.NextCursor)
			if previous, ok := stream.replays[record.RawEventSHA256]; ok && !bytes.Equal(previous.rawEvent, raw) {
				return fmt.Errorf("%w: raw replay digest collision", ErrDurableStoreCorrupt)
			}
			stream.replays[record.RawEventSHA256] = durableCommittedResult{rawEvent: raw, response: response, sequence: stored.Ref.Sequence}
			runtime.commitCount[key]++
		case RecordTypeCommittedReplayV1:
			var record CommittedReplayV1
			if err := decodeClosedJSON(stored.Body, &record); err != nil {
				return fmt.Errorf("%w: committed replay %d: %v", ErrDurableStoreCorrupt, stored.Ref.Sequence, err)
			}
			key := runtime.streamKey(record.StreamID)
			stream := runtime.streams[key]
			committed, ok := stream.replays[record.RawEventSHA256]
			if record.GraphIdentity != runtime.graphIdentity || !ok || committed.sequence != record.SemanticCommitSequence {
				return fmt.Errorf("%w: replay does not bind a semantic commit", ErrDurableStoreCorrupt)
			}
			runtime.replayCount[key]++
		}
	}
	return nil
}

func validateStoredSemanticCommit(record SemanticCommitV1, graphIdentity string, cursor *CursorTransition) (KernelResponse, []byte, error) {
	if record.GraphIdentity != graphIdentity || record.Outcome != "Applied" || record.StreamID == "" {
		return KernelResponse{}, nil, errors.New("semantic binding mismatch")
	}
	raw, err := base64.StdEncoding.Strict().DecodeString(record.RawEventBase64)
	if err != nil || len(raw) == 0 || digestHex(raw) != record.RawEventSHA256 {
		return KernelResponse{}, nil, errors.New("raw event binding mismatch")
	}
	next, err := base64.StdEncoding.Strict().DecodeString(record.NextCursorBase64)
	if err != nil || len(next) == 0 || digestHex(next) != record.NextCursorSHA256 {
		return KernelResponse{}, nil, errors.New("cursor binding mismatch")
	}
	command, err := decodeOptionalStrictBase64(record.CommandIntentBase64)
	if err != nil {
		return KernelResponse{}, nil, errors.New("command bytes invalid")
	}
	if cursor == nil || cursor.ExpectedPreviousSHA256 != record.PreviousCursorSHA256 || cursor.NextSHA256 != record.NextCursorSHA256 {
		return KernelResponse{}, nil, errors.New("store cursor transition mismatch")
	}
	response := KernelResponse{
		Outcome: record.Outcome, NextCursor: next, CommandIntent: command, ValidatedStreamID: record.StreamID,
		AcceptedEventIdentity: record.AcceptedEventIdentity, EventPayloadDigest: record.EventPayloadDigest,
		CommandIntentIdentity: record.CommandIntentIdentity, CommandPayloadDigest: record.CommandPayloadDigest,
		DefectCodes: append([]string(nil), record.DefectCodes...),
	}
	if err := validateDurableKernelResponse(response, nil, record.StreamID); err != nil {
		return KernelResponse{}, nil, err
	}
	return response, raw, nil
}

func validateDurableKernelResponse(response KernelResponse, original []byte, streamID string) error {
	if !validOutcome(response.Outcome) {
		return fmt.Errorf("%w: %q", ErrInvalidKernelResponse, response.Outcome)
	}
	if response.Outcome != "Applied" {
		if len(response.CommandIntent) != 0 || !bytes.Equal(response.NextCursor, original) {
			return fmt.Errorf("%w: non-applied result changed state", ErrInvalidKernelResponse)
		}
		if response.Outcome != "Rejected" && response.ValidatedStreamID != streamID {
			return fmt.Errorf("%w: non-applied stream mismatch", ErrInvalidKernelResponse)
		}
		return nil
	}
	if response.ValidatedStreamID != streamID || len(response.NextCursor) == 0 {
		return fmt.Errorf("%w: applied stream or cursor mismatch", ErrInvalidKernelResponse)
	}
	if !isTaggedSHA256(response.AcceptedEventIdentity) || !isTaggedSHA256(response.EventPayloadDigest) {
		return fmt.Errorf("%w: applied response lacks Rust identity evidence", ErrInvalidKernelResponse)
	}
	if len(response.CommandIntent) == 0 {
		if response.CommandIntentIdentity != "" || response.CommandPayloadDigest != "" {
			return fmt.Errorf("%w: absent command has identity evidence", ErrInvalidKernelResponse)
		}
		return nil
	}
	if !isTaggedSHA256(response.CommandIntentIdentity) || !isTaggedSHA256(response.CommandPayloadDigest) {
		return fmt.Errorf("%w: command lacks immutable Rust identity evidence", ErrInvalidKernelResponse)
	}
	return nil
}

func (runtime *DurableRuntime) streamKey(streamID string) string {
	return runtime.graphIdentity + "\x00" + streamID
}

func (runtime *DurableRuntime) lockFor(key string) *sync.Mutex {
	runtime.locksMu.Lock()
	defer runtime.locksMu.Unlock()
	if lock := runtime.streamLocks[key]; lock != nil {
		return lock
	}
	lock := new(sync.Mutex)
	runtime.streamLocks[key] = lock
	return lock
}

func (runtime *DurableRuntime) ensureStreamLocked(key string) *durableRuntimeStream {
	stream := runtime.streams[key]
	if stream == nil {
		stream = &durableRuntimeStream{outbox: make(map[string][]byte), replays: make(map[string]durableCommittedResult)}
		runtime.streams[key] = stream
	}
	return stream
}

// Snapshot returns one stream projection without mutable handles.
func (runtime *DurableRuntime) Snapshot(streamID string) DurableRuntimeSnapshot {
	if runtime == nil {
		return DurableRuntimeSnapshot{}
	}
	key := runtime.streamKey(streamID)
	lock := runtime.lockFor(key)
	lock.Lock()
	defer lock.Unlock()
	runtime.projectionMu.Lock()
	defer runtime.projectionMu.Unlock()
	stream := runtime.streams[key]
	if stream == nil {
		return DurableRuntimeSnapshot{}
	}
	outbox := make(map[string][]byte, len(stream.outbox))
	for identity, command := range stream.outbox {
		outbox[identity] = cloneBytes(command)
	}
	return DurableRuntimeSnapshot{
		Cursor: cloneBytes(stream.cursor), Outbox: outbox, SemanticCommitCount: runtime.commitCount[key],
		CommittedReplayCount: runtime.replayCount[key], Exists: true,
	}
}

func encodeOptionalBase64(value []byte) string {
	if len(value) == 0 {
		return ""
	}
	return base64.StdEncoding.EncodeToString(value)
}

func decodeOptionalStrictBase64(value string) ([]byte, error) {
	if value == "" {
		return nil, nil
	}
	return base64.StdEncoding.Strict().DecodeString(value)
}

func isTaggedSHA256(value string) bool {
	return strings.HasPrefix(value, "sha256:") && validateDigest(strings.TrimPrefix(value, "sha256:")) == nil
}
