// Package rwosidecar defines a lossless, transport-neutral RWO boundary.
package rwosidecar

import (
	"context"
	"errors"
	"fmt"
)

var (
	// ErrMalformedEnvelope means the adapter did not provide enough information
	// to make a semantic kernel request. It is not a retry decision.
	ErrMalformedEnvelope = errors.New("malformed RWO sidecar envelope")
	// ErrInvalidKernelResponse means an implementation broke the closed RWO
	// outcome vocabulary. The sidecar refuses to invent a recovery action.
	ErrInvalidKernelResponse = errors.New("invalid RWO kernel response")
)

// VersionTuple must accompany every raw semantic payload sent to a kernel.
// It intentionally mirrors the seven registered semantic tuple members rather
// than trusting a transport-specific content-type or schema name.
type VersionTuple struct {
	ContractID      string `json:"contract_id"`
	ContractVersion string `json:"contract_version"`
	ProfileID       string `json:"profile_id"`
	ProfileVersion  string `json:"profile_version"`
	SchemaID        string `json:"schema_id"`
	SchemaVersion   string `json:"schema_version"`
	ValueType       string `json:"value_type"`
}

func (tuple VersionTuple) validate() error {
	if tuple.ContractID == "" || tuple.ContractVersion == "" ||
		tuple.ProfileID == "" || tuple.ProfileVersion == "" ||
		tuple.SchemaID == "" || tuple.SchemaVersion == "" || tuple.ValueType == "" {
		return fmt.Errorf("%w: complete version tuple required", ErrMalformedEnvelope)
	}
	return nil
}

// DeliveryContext belongs to an adapter. None of these fields reach the pure
// kernel request, because physical delivery does not alter semantic identity.
type DeliveryContext struct {
	AdapterName       string `json:"adapter_name"`
	PhysicalAttemptID string `json:"physical_attempt_id"`
}

// EventEnvelope is the boundary input. RawAcceptedEvent is intentionally bytes
// rather than decoded JSON: an ingress adapter must retain raw number lexemes,
// duplicate-name evidence, whitespace, and any later admission defect.
type EventEnvelope struct {
	Tuple VersionTuple `json:"tuple"`
	// StreamIDHint is a Go-owned volatile routing selector. Rust admits the
	// opaque event bytes and verifies that its semantic stream_id agrees before
	// any runtime state can be committed.
	StreamIDHint     string          `json:"stream_id_hint"`
	CorrelationID    string          `json:"correlation_id"`
	RawAcceptedEvent []byte          `json:"raw_accepted_event"`
	Delivery         DeliveryContext `json:"delivery"`
}

func (envelope EventEnvelope) validate() error {
	if err := envelope.Tuple.validate(); err != nil {
		return err
	}
	if envelope.CorrelationID == "" {
		return fmt.Errorf("%w: correlation_id is required", ErrMalformedEnvelope)
	}
	if envelope.StreamIDHint == "" {
		return fmt.Errorf("%w: stream_id_hint is required", ErrMalformedEnvelope)
	}
	if len(envelope.RawAcceptedEvent) == 0 {
		return fmt.Errorf("%w: raw_accepted_event is required", ErrMalformedEnvelope)
	}
	return nil
}

// KernelRequest is deliberately smaller than EventEnvelope. It proves that
// adapter delivery metadata cannot leak into a deterministic reduce call.
type KernelRequest struct {
	Tuple            VersionTuple
	StreamIDHint     string
	RawAcceptedEvent []byte
}

func (request KernelRequest) validate() error {
	if err := request.Tuple.validate(); err != nil {
		return err
	}
	if request.StreamIDHint == "" {
		return fmt.Errorf("%w: stream_id_hint is required", ErrMalformedEnvelope)
	}
	if len(request.RawAcceptedEvent) == 0 {
		return fmt.Errorf("%w: raw_accepted_event is required", ErrMalformedEnvelope)
	}
	return nil
}

// KernelResponse uses the RWO closed outcome vocabulary. A command is one
// immutable byte payload or absent, matching the at-most-one intent invariant.
type KernelResponse struct {
	Outcome               string
	NextCursor            []byte
	CommandIntent         []byte
	ValidatedStreamID     string
	AcceptedEventIdentity string
	EventPayloadDigest    string
	CommandIntentIdentity string
	CommandPayloadDigest  string
	DefectCodes           []string
}

// Kernel is the only dependency the Go boundary has on a kernel process or
// library. Rust, a local in-memory fixture, a Unix socket, or a future gRPC
// client can implement it without changing transport semantics here.
type Kernel interface {
	Reduce(context.Context, KernelRequest) (KernelResponse, error)
}

// IngressAdapter converts any transport message into the stable EventEnvelope
// shape. It does not grant journal acceptance or perform raw admission.
type IngressAdapter interface {
	Name() string
	Decode(context.Context, []byte) (EventEnvelope, error)
}

// CommandEnvelope is the outbound boundary shape. It is separate from a
// physical delivery operation: RWO emits an intent, while another owner may
// later decide delivery, retry, acknowledgement, or reconciliation.
type CommandEnvelope struct {
	LogicalMessageID string
	CommandIntent    []byte
}

// CommandAdapter maps one immutable command intent to transport bytes. It is
// intentionally not called by Service.Reduce.
type CommandAdapter interface {
	Name() string
	Encode(context.Context, CommandEnvelope) ([]byte, error)
}

// Observation is the sidecar result. Unknown means the boundary did not learn
// whether a kernel request completed; it never means retry the semantic work.
type Observation struct {
	Status                string          `json:"status"`
	CorrelationID         string          `json:"correlation_id"`
	Delivery              DeliveryContext `json:"delivery"`
	Outcome               string          `json:"outcome,omitempty"`
	ValidatedStreamID     string          `json:"validated_stream_id,omitempty"`
	NextCursor            []byte          `json:"next_cursor,omitempty"`
	CommandIntent         []byte          `json:"command_intent,omitempty"`
	AcceptedEventIdentity string          `json:"accepted_event_identity,omitempty"`
	EventPayloadDigest    string          `json:"event_payload_digest,omitempty"`
	CommandIntentIdentity string          `json:"command_intent_identity,omitempty"`
	CommandPayloadDigest  string          `json:"command_payload_digest,omitempty"`
	DefectCodes           []string        `json:"defect_codes,omitempty"`
	UncertaintyReason     string          `json:"uncertainty_reason,omitempty"`
}

// Service connects a transport boundary to one kernel implementation. It is
// stateless, concurrency-safe as long as its Kernel implementation is.
type Service struct {
	Kernel Kernel
}

// Reduce forwards a defensive copy of the raw event bytes, never decoded or
// re-serialized. Transport metadata stays in Observation only.
func (service Service) Reduce(ctx context.Context, envelope EventEnvelope) (Observation, error) {
	if err := envelope.validate(); err != nil {
		return Observation{}, err
	}
	if service.Kernel == nil {
		return Observation{}, fmt.Errorf("%w: kernel is required", ErrMalformedEnvelope)
	}

	request := KernelRequest{
		Tuple:            envelope.Tuple,
		StreamIDHint:     envelope.StreamIDHint,
		RawAcceptedEvent: append([]byte(nil), envelope.RawAcceptedEvent...),
	}
	response, err := service.Kernel.Reduce(ctx, request)
	if err != nil {
		return Observation{
			Status:            "unknown",
			CorrelationID:     envelope.CorrelationID,
			Delivery:          envelope.Delivery,
			UncertaintyReason: "KERNEL_UNAVAILABLE_OR_UNCERTAIN",
		}, nil
	}
	if !validOutcome(response.Outcome) {
		return Observation{}, fmt.Errorf("%w: %q", ErrInvalidKernelResponse, response.Outcome)
	}
	if response.Outcome != "Applied" && len(response.CommandIntent) != 0 {
		return Observation{}, fmt.Errorf("%w: command on %s", ErrInvalidKernelResponse, response.Outcome)
	}
	if response.Outcome == "Applied" && (response.ValidatedStreamID == "" || len(response.NextCursor) == 0) {
		return Observation{}, fmt.Errorf("%w: applied response lacks verified stream or cursor", ErrInvalidKernelResponse)
	}
	return Observation{
		Status:                "reduced",
		CorrelationID:         envelope.CorrelationID,
		Delivery:              envelope.Delivery,
		Outcome:               response.Outcome,
		ValidatedStreamID:     response.ValidatedStreamID,
		NextCursor:            append([]byte(nil), response.NextCursor...),
		CommandIntent:         append([]byte(nil), response.CommandIntent...),
		AcceptedEventIdentity: response.AcceptedEventIdentity,
		EventPayloadDigest:    response.EventPayloadDigest,
		CommandIntentIdentity: response.CommandIntentIdentity,
		CommandPayloadDigest:  response.CommandPayloadDigest,
		DefectCodes:           append([]string(nil), response.DefectCodes...),
	}, nil
}

func validOutcome(outcome string) bool {
	switch outcome {
	case "Applied", "Duplicate", "DivergentDuplicate", "Rejected":
		return true
	default:
		return false
	}
}
