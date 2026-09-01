package rwosidecar

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"strconv"
	"strings"
	"sync"
	"unicode/utf8"
)

const (
	RecordTypeRawEveLineV1          DurableRecordType = 0x0501
	RecordTypeTerminalCandidateV1   DurableRecordType = 0x0502
	RecordTypeTerminalAdmissionV1   DurableRecordType = 0x0503
	RecordTypeTerminalReplayInertV1 DurableRecordType = 0x0504
	RecordTypeTerminalDivergentV1   DurableRecordType = 0x0505

	defaultTerminalMaxLineBytes   = 256 << 10
	defaultTerminalMaxStreamBytes = 4 << 20
)

var (
	ErrTerminalEvidence   = errors.New("invalid persisted Eve terminal evidence")
	ErrTerminalPolicy     = errors.New("forbidden Eve terminal event")
	ErrTerminalSchema     = errors.New("Eve terminal output does not match the closed schema")
	ErrTerminalDivergence = errors.New("RWO terminal admission diverges")
	ErrTerminalSemantic   = errors.New("Rust did not admit the terminal event")
)

// RawEveLineV1 retains the exact newline-bearing provider bytes. Validation
// reads only these synced records, never a live HTTP buffer.
type RawEveLineV1 struct {
	AttemptID   string `json:"attempt_id"`
	SessionID   string `json:"session_id"`
	LineOrdinal uint64 `json:"line_ordinal"`
	LineSHA256  string `json:"line_sha256"`
	LineBase64  string `json:"line_base64"`
}

func (RawEveLineV1) DurableRecordType() DurableRecordType { return RecordTypeRawEveLineV1 }

type terminalCandidateRecord struct {
	AdmissionKey       string   `json:"admission_key"`
	AttemptID          string   `json:"attempt_id"`
	SessionID          string   `json:"session_id"`
	OutputSHA256       string   `json:"output_sha256"`
	ResultAddress      string   `json:"result_address"`
	CanonicalOutputB64 string   `json:"canonical_output_base64"`
	CanonicalEventB64  string   `json:"canonical_event_base64"`
	RawSequences       []uint64 `json:"raw_sequences"`
}

func (terminalCandidateRecord) DurableRecordType() DurableRecordType {
	return RecordTypeTerminalCandidateV1
}

type terminalAdmissionRecord struct {
	AdmissionKey           string `json:"admission_key"`
	AttemptID              string `json:"attempt_id"`
	SessionID              string `json:"session_id"`
	OutputSHA256           string `json:"output_sha256"`
	AcceptedEventIdentity  string `json:"accepted_event_identity"`
	SemanticCommitSequence uint64 `json:"semantic_commit_sequence"`
}

func (terminalAdmissionRecord) DurableRecordType() DurableRecordType {
	return RecordTypeTerminalAdmissionV1
}

type terminalReplayRecord struct {
	AdmissionKey string `json:"admission_key"`
	OutputSHA256 string `json:"output_sha256"`
}

func (terminalReplayRecord) DurableRecordType() DurableRecordType {
	return RecordTypeTerminalReplayInertV1
}

type terminalDivergentRecord struct {
	AdmissionKey    string `json:"admission_key"`
	CommittedSHA256 string `json:"committed_sha256"`
	ObservedSHA256  string `json:"observed_sha256"`
}

func (terminalDivergentRecord) DurableRecordType() DurableRecordType {
	return RecordTypeTerminalDivergentV1
}

// DurableEveRawWriter is an EveRawLineSink whose return is the sync boundary.
type DurableEveRawWriter struct {
	store     *DurableStore
	attemptID string
	mu        sync.Mutex
	ordinal   uint64
}

func NewDurableEveRawWriter(store *DurableStore, attemptID string) (*DurableEveRawWriter, error) {
	if store == nil || attemptID == "" {
		return nil, fmt.Errorf("%w: store and attempt are required", ErrTerminalEvidence)
	}
	writer := &DurableEveRawWriter{store: store, attemptID: attemptID}
	snapshot, err := store.Snapshot()
	if err != nil {
		return nil, err
	}
	for _, stored := range snapshot.Records {
		if stored.Type != RecordTypeRawEveLineV1 {
			continue
		}
		var record RawEveLineV1
		if err := decodeClosedJSON(stored.Body, &record); err != nil {
			return nil, fmt.Errorf("%w: raw record %d", ErrTerminalEvidence, stored.Ref.Sequence)
		}
		if record.AttemptID == attemptID && record.LineOrdinal > writer.ordinal {
			writer.ordinal = record.LineOrdinal
		}
	}
	return writer, nil
}

func (writer *DurableEveRawWriter) Sink(ctx context.Context, sessionID string, line []byte) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	if writer == nil || writer.store == nil || sessionID == "" || len(line) == 0 || line[len(line)-1] != '\n' {
		return fmt.Errorf("%w: exact LF-bearing line required", ErrTerminalEvidence)
	}
	writer.mu.Lock()
	defer writer.mu.Unlock()
	writer.ordinal++
	record := RawEveLineV1{
		AttemptID: writer.attemptID, SessionID: sessionID, LineOrdinal: writer.ordinal,
		LineSHA256: digestHex(line), LineBase64: base64.StdEncoding.EncodeToString(line),
	}
	if _, err := appendClosedTerminalRecord(writer.store, record); err != nil {
		writer.ordinal--
		return err
	}
	return nil
}

type TerminalValidationInput struct {
	GraphIdentity      string
	StreamID           string
	CommandIdentity    string
	AttemptID          string
	SessionID          string
	TerminalClass      string
	SourceNodeID       string
	Tuple              VersionTuple
	OutputSchemaBytes  []byte
	OutputSchemaSHA256 string
	PolicySHA256       string
	MaxLineBytes       int
	MaxStreamBytes     int
}

type TerminalCandidate struct {
	AdmissionKey       string
	AttemptID          string
	SessionID          string
	OutputSHA256       string
	ResultAddress      string
	CanonicalOutput    []byte
	CanonicalEvent     []byte
	RawRecordSequences []uint64
	Tuple              VersionTuple
	StreamID           string
}

type terminalStreamEvent struct {
	EventID   string          `json:"eventId"`
	Output    json.RawMessage `json:"output,omitempty"`
	SessionID string          `json:"sessionId"`
	Type      string          `json:"type"`
}

type terminalOutput struct {
	Answer string `json:"answer"`
}

type terminalAcceptedEvent struct {
	ContractID      string                    `json:"contract_id"`
	ContractVersion string                    `json:"contract_version"`
	EventID         string                    `json:"event_id"`
	EventType       string                    `json:"event_type"`
	Payload         ExecuteBoundedSeatPayload `json:"payload"`
	ProfileID       string                    `json:"profile_id"`
	ProfileVersion  string                    `json:"profile_version"`
	SchemaID        string                    `json:"schema_id"`
	SchemaVersion   string                    `json:"schema_version"`
	SourceNodeID    string                    `json:"source_node_id"`
	StreamID        string                    `json:"stream_id"`
}

// ValidatePersistedTerminal derives one candidate solely from verified raw
// records. Provider event IDs and JSON formatting do not enter K or D.
func ValidatePersistedTerminal(store *DurableStore, input TerminalValidationInput) (TerminalCandidate, error) {
	if store == nil || input.GraphIdentity == "" || input.StreamID == "" || input.CommandIdentity == "" ||
		input.AttemptID == "" || input.SessionID == "" || input.TerminalClass == "" || input.SourceNodeID == "" ||
		!isTaggedSHA256(input.OutputSchemaSHA256) || !isTaggedSHA256(input.PolicySHA256) || input.Tuple.validate() != nil {
		return TerminalCandidate{}, fmt.Errorf("%w: complete terminal binding required", ErrTerminalEvidence)
	}
	if "sha256:"+digestHex(input.OutputSchemaBytes) != input.OutputSchemaSHA256 {
		return TerminalCandidate{}, fmt.Errorf("%w: output schema digest drift", ErrTerminalSchema)
	}
	if err := validateClosedAnswerSchema(input.OutputSchemaBytes); err != nil {
		return TerminalCandidate{}, err
	}
	maxLine := input.MaxLineBytes
	if maxLine == 0 {
		maxLine = defaultTerminalMaxLineBytes
	}
	maxStream := input.MaxStreamBytes
	if maxStream == 0 {
		maxStream = defaultTerminalMaxStreamBytes
	}
	snapshot, err := store.Snapshot()
	if err != nil {
		return TerminalCandidate{}, err
	}
	var rawSequences []uint64
	var output terminalOutput
	var outputSeen, started, completed bool
	lastEventOrdinal := int64(-1)
	total := 0
	for _, stored := range snapshot.Records {
		if stored.Type != RecordTypeRawEveLineV1 {
			continue
		}
		var record RawEveLineV1
		if err := decodeClosedJSON(stored.Body, &record); err != nil {
			return TerminalCandidate{}, fmt.Errorf("%w: raw record %d", ErrTerminalEvidence, stored.Ref.Sequence)
		}
		if record.AttemptID != input.AttemptID || record.SessionID != input.SessionID {
			continue
		}
		line, err := base64.StdEncoding.Strict().DecodeString(record.LineBase64)
		if err != nil || len(line) == 0 || line[len(line)-1] != '\n' || digestHex(line) != record.LineSHA256 || !utf8.Valid(line) {
			return TerminalCandidate{}, fmt.Errorf("%w: invalid raw line at %d", ErrTerminalEvidence, stored.Ref.Sequence)
		}
		total += len(line)
		if len(line) > maxLine || total > maxStream {
			return TerminalCandidate{}, fmt.Errorf("%w: terminal stream bounds exceeded", ErrTerminalEvidence)
		}
		if completed {
			return TerminalCandidate{}, fmt.Errorf("%w: event after terminal", ErrTerminalPolicy)
		}
		var event terminalStreamEvent
		if err := decodeClosedJSON(bytes.TrimSuffix(line, []byte{'\n'}), &event); err != nil {
			return TerminalCandidate{}, fmt.Errorf("%w: malformed event at %d: %v", ErrTerminalEvidence, stored.Ref.Sequence, err)
		}
		if event.SessionID != input.SessionID || event.EventID == "" {
			return TerminalCandidate{}, fmt.Errorf("%w: event correlation", ErrTerminalEvidence)
		}
		ordinal, err := terminalEventOrdinal(event.EventID)
		if err != nil || ordinal <= lastEventOrdinal {
			return TerminalCandidate{}, fmt.Errorf("%w: non-monotonic event ID", ErrTerminalEvidence)
		}
		lastEventOrdinal = ordinal
		switch event.Type {
		case "session.started":
			if started || outputSeen || completed || len(event.Output) != 0 {
				return TerminalCandidate{}, ErrTerminalEvidence
			}
			started = true
		case "task.output":
			if !started || outputSeen || completed || len(event.Output) == 0 {
				return TerminalCandidate{}, ErrTerminalEvidence
			}
			if err := decodeClosedJSON(event.Output, &output); err != nil || output.Answer == "" || !utf8.ValidString(output.Answer) {
				return TerminalCandidate{}, fmt.Errorf("%w: closed answer required", ErrTerminalSchema)
			}
			outputSeen = true
		case "session.completed":
			if !started || !outputSeen || completed || len(event.Output) != 0 {
				return TerminalCandidate{}, ErrTerminalEvidence
			}
			completed = true
		default:
			return TerminalCandidate{}, fmt.Errorf("%w: %s", ErrTerminalPolicy, event.Type)
		}
		rawSequences = append(rawSequences, stored.Ref.Sequence)
	}
	if !started || !outputSeen || !completed {
		return TerminalCandidate{}, fmt.Errorf("%w: terminal triple incomplete", ErrTerminalEvidence)
	}
	canonicalOutput, err := json.Marshal(output)
	if err != nil {
		return TerminalCandidate{}, err
	}
	outputDigest := "sha256:" + digestHex(canonicalOutput)
	keyDigest := sha256.Sum256([]byte("RWO-TERMINAL-ADMISSION-V1\x00" + input.GraphIdentity + input.StreamID + input.CommandIdentity + input.AttemptID + input.SessionID + input.TerminalClass))
	key := "sha256:" + hex.EncodeToString(keyDigest[:])
	eventIDDigest := sha256.Sum256([]byte(key + outputDigest))
	event := terminalAcceptedEvent{
		ContractID: input.Tuple.ContractID, ContractVersion: input.Tuple.ContractVersion,
		EventID: "terminalv1:" + hex.EncodeToString(eventIDDigest[:]), EventType: "SeatTerminalObservedV1",
		Payload:   ExecuteBoundedSeatPayload{JobID: "resultv1:sha256:" + strings.TrimPrefix(outputDigest, "sha256:")},
		ProfileID: input.Tuple.ProfileID, ProfileVersion: input.Tuple.ProfileVersion,
		SchemaID: "AcceptedEventView", SchemaVersion: input.Tuple.SchemaVersion,
		SourceNodeID: input.SourceNodeID, StreamID: input.StreamID,
	}
	eventBytes, err := json.Marshal(event)
	if err != nil {
		return TerminalCandidate{}, err
	}
	return TerminalCandidate{
		AdmissionKey: key, AttemptID: input.AttemptID, SessionID: input.SessionID,
		OutputSHA256: outputDigest, ResultAddress: event.Payload.JobID,
		CanonicalOutput: canonicalOutput, CanonicalEvent: eventBytes, RawRecordSequences: rawSequences,
		Tuple:    VersionTuple{ContractID: input.Tuple.ContractID, ContractVersion: input.Tuple.ContractVersion, ProfileID: input.Tuple.ProfileID, ProfileVersion: input.Tuple.ProfileVersion, SchemaID: "AcceptedEventView", SchemaVersion: input.Tuple.SchemaVersion, ValueType: "AcceptedEventView"},
		StreamID: input.StreamID,
	}, nil
}

type TerminalAdmissionResult struct {
	Status                 string
	AdmissionKey           string
	OutputSHA256           string
	SemanticCommitSequence uint64
	RustResponse           KernelResponse
}

// TerminalCoordinator persists convergence state and routes first admission
// through DurableRuntime. It does not acknowledge the physical attempt.
type TerminalCoordinator struct {
	store   *DurableStore
	runtime *DurableRuntime
	mu      sync.Mutex
}

func NewTerminalCoordinator(store *DurableStore, runtime *DurableRuntime) (*TerminalCoordinator, error) {
	if store == nil || runtime == nil {
		return nil, fmt.Errorf("%w: store and durable Rust runtime required", ErrTerminalSemantic)
	}
	return &TerminalCoordinator{store: store, runtime: runtime}, nil
}

func (coordinator *TerminalCoordinator) Admit(ctx context.Context, candidate TerminalCandidate) (TerminalAdmissionResult, error) {
	coordinator.mu.Lock()
	defer coordinator.mu.Unlock()
	if !isTaggedSHA256(candidate.AdmissionKey) || candidate.AttemptID == "" || candidate.SessionID == "" ||
		!isTaggedSHA256(candidate.OutputSHA256) || len(candidate.CanonicalEvent) == 0 {
		return TerminalAdmissionResult{}, ErrTerminalEvidence
	}
	existingDigest, admittedSequence, existing, err := terminalBinding(coordinator.store, candidate.AdmissionKey, candidate.AttemptID, candidate.SessionID)
	if err != nil {
		return TerminalAdmissionResult{}, err
	}
	if existing {
		if existingDigest != candidate.OutputSHA256 {
			_, _ = appendClosedTerminalRecord(coordinator.store, terminalDivergentRecord{AdmissionKey: candidate.AdmissionKey, CommittedSHA256: existingDigest, ObservedSHA256: candidate.OutputSHA256})
			return TerminalAdmissionResult{}, ErrTerminalDivergence
		}
		if admittedSequence != 0 {
			_, err := appendClosedTerminalRecord(coordinator.store, terminalReplayRecord{AdmissionKey: candidate.AdmissionKey, OutputSHA256: candidate.OutputSHA256})
			return TerminalAdmissionResult{Status: "inert", AdmissionKey: candidate.AdmissionKey, OutputSHA256: candidate.OutputSHA256, SemanticCommitSequence: admittedSequence}, err
		}
	}
	if !existing {
		_, err := appendClosedTerminalRecord(coordinator.store, terminalCandidateRecord{
			AdmissionKey: candidate.AdmissionKey, AttemptID: candidate.AttemptID, SessionID: candidate.SessionID,
			OutputSHA256: candidate.OutputSHA256, ResultAddress: candidate.ResultAddress,
			CanonicalOutputB64: base64.StdEncoding.EncodeToString(candidate.CanonicalOutput), CanonicalEventB64: base64.StdEncoding.EncodeToString(candidate.CanonicalEvent),
			RawSequences: append([]uint64(nil), candidate.RawRecordSequences...),
		})
		if err != nil {
			return TerminalAdmissionResult{}, err
		}
	}
	response, err := coordinator.runtime.Reduce(ctx, KernelRequest{Tuple: candidate.Tuple, StreamIDHint: candidate.StreamID, RawAcceptedEvent: cloneBytes(candidate.CanonicalEvent)})
	if err != nil {
		return TerminalAdmissionResult{}, err
	}
	if response.Outcome != "Applied" || len(response.CommandIntent) != 0 || !isTaggedSHA256(response.AcceptedEventIdentity) {
		return TerminalAdmissionResult{}, fmt.Errorf("%w: outcome=%s command=%d", ErrTerminalSemantic, response.Outcome, len(response.CommandIntent))
	}
	semanticSequence, err := findSemanticCommitSequence(coordinator.store, digestHex(candidate.CanonicalEvent), response.AcceptedEventIdentity)
	if err != nil {
		return TerminalAdmissionResult{}, err
	}
	_, err = appendClosedTerminalRecord(coordinator.store, terminalAdmissionRecord{
		AdmissionKey: candidate.AdmissionKey, AttemptID: candidate.AttemptID, SessionID: candidate.SessionID,
		OutputSHA256:          candidate.OutputSHA256,
		AcceptedEventIdentity: response.AcceptedEventIdentity, SemanticCommitSequence: semanticSequence,
	})
	if err != nil {
		return TerminalAdmissionResult{}, err
	}
	return TerminalAdmissionResult{Status: "admitted", AdmissionKey: candidate.AdmissionKey, OutputSHA256: candidate.OutputSHA256, SemanticCommitSequence: semanticSequence, RustResponse: response}, nil
}

func terminalBinding(store *DurableStore, key, attemptID, sessionID string) (string, uint64, bool, error) {
	snapshot, err := store.Snapshot()
	if err != nil {
		return "", 0, false, err
	}
	var digest string
	var sequence uint64
	for _, stored := range snapshot.Records {
		switch stored.Type {
		case RecordTypeTerminalCandidateV1:
			var record terminalCandidateRecord
			if err := decodeClosedJSON(stored.Body, &record); err != nil {
				return "", 0, false, ErrTerminalEvidence
			}
			if record.AdmissionKey == key {
				if record.AttemptID != attemptID || record.SessionID != sessionID {
					return "", 0, false, ErrTerminalDivergence
				}
				if digest != "" && digest != record.OutputSHA256 {
					return "", 0, false, ErrTerminalDivergence
				}
				digest = record.OutputSHA256
			}
		case RecordTypeTerminalAdmissionV1:
			var record terminalAdmissionRecord
			if err := decodeClosedJSON(stored.Body, &record); err != nil {
				return "", 0, false, ErrTerminalEvidence
			}
			if record.AdmissionKey == key {
				if record.AttemptID != attemptID || record.SessionID != sessionID {
					return "", 0, false, ErrTerminalDivergence
				}
				if digest != "" && digest != record.OutputSHA256 {
					return "", 0, false, ErrTerminalDivergence
				}
				digest, sequence = record.OutputSHA256, record.SemanticCommitSequence
			}
		}
	}
	return digest, sequence, digest != "", nil
}

func findSemanticCommitSequence(store *DurableStore, rawDigest, acceptedIdentity string) (uint64, error) {
	snapshot, err := store.Snapshot()
	if err != nil {
		return 0, err
	}
	for index := len(snapshot.Records) - 1; index >= 0; index-- {
		stored := snapshot.Records[index]
		if stored.Type != RecordTypeSemanticCommitV1 {
			continue
		}
		var record SemanticCommitV1
		if decodeClosedJSON(stored.Body, &record) == nil && record.RawEventSHA256 == rawDigest && record.AcceptedEventIdentity == acceptedIdentity {
			return stored.Ref.Sequence, nil
		}
	}
	return 0, fmt.Errorf("%w: synced semantic commit not found", ErrTerminalSemantic)
}

func appendClosedTerminalRecord(store *DurableStore, record DurableRecord) (DurableRecordRef, error) {
	next, previous, err := store.Tip()
	if err != nil {
		return DurableRecordRef{}, err
	}
	return store.Append(AppendExpectation{ExpectedSequence: next, ExpectedPreviousFrameSHA256: previous}, record)
}

func terminalEventOrdinal(eventID string) (int64, error) {
	component := eventID
	if index := strings.LastIndexByte(eventID, '-'); index >= 0 {
		component = eventID[index+1:]
	}
	return strconv.ParseInt(component, 10, 64)
}

func validateClosedAnswerSchema(raw []byte) error {
	var schema struct {
		Schema               string `json:"$schema"`
		AdditionalProperties bool   `json:"additionalProperties"`
		Properties           struct {
			Answer struct {
				MinLength int    `json:"minLength"`
				Type      string `json:"type"`
			} `json:"answer"`
		} `json:"properties"`
		Required []string `json:"required"`
		Type     string   `json:"type"`
	}
	if err := decodeClosedJSON(raw, &schema); err != nil || schema.Type != "object" || schema.AdditionalProperties ||
		len(schema.Required) != 1 || schema.Required[0] != "answer" || schema.Properties.Answer.Type != "string" || schema.Properties.Answer.MinLength < 1 {
		return fmt.Errorf("%w: unsupported output schema", ErrTerminalSchema)
	}
	return nil
}
