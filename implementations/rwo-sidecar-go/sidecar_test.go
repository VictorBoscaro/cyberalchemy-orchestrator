package rwosidecar

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"reflect"
	"testing"
)

type recordingKernel struct {
	request  KernelRequest
	requests []KernelRequest
	calls    int
	response KernelResponse
	err      error
}

func (kernel *recordingKernel) Reduce(_ context.Context, request KernelRequest) (KernelResponse, error) {
	kernel.request = request
	kernel.requests = append(kernel.requests, request)
	kernel.calls++
	return kernel.response, kernel.err
}

func fixtureTuple() VersionTuple {
	return VersionTuple{
		ContractID: "RWO-SEMANTIC-CONTRACT", ContractVersion: "1.0.0",
		ProfileID: "RWO-JCS-IJSON-SAFEINT", ProfileVersion: "1.0.0",
		SchemaID: "AcceptedEventView", SchemaVersion: "1.0.0", ValueType: "AcceptedEventView",
	}
}

func fixtureEnvelope(raw []byte) EventEnvelope {
	return EventEnvelope{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", CorrelationID: "correlation-1", RawAcceptedEvent: raw,
		Delivery: DeliveryContext{AdapterName: "memory", PhysicalAttemptID: "attempt-7"},
	}
}

func TestReducePreservesRawBytesAndExcludesDeliveryMetadata(t *testing.T) {
	raw := []byte(" {\n  \"event_id\": \"event-1\", \"safe\": 1\n}\t")
	kernel := &recordingKernel{response: KernelResponse{
		Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor"), CommandIntent: []byte("command"),
	}}
	service := Service{Kernel: kernel}
	observation, err := service.Reduce(context.Background(), fixtureEnvelope(raw))
	if err != nil {
		t.Fatal(err)
	}
	if observation.Status != "reduced" || observation.Outcome != "Applied" {
		t.Fatalf("unexpected observation: %#v", observation)
	}
	if !reflect.DeepEqual(kernel.request.RawAcceptedEvent, raw) {
		t.Fatalf("kernel received changed raw bytes: %q", kernel.request.RawAcceptedEvent)
	}
	if kernel.request.StreamIDHint != "stream-1" || kernel.request.Tuple != fixtureTuple() {
		t.Fatalf("semantic request mismatch: %#v", kernel.request)
	}
	if string(observation.CommandIntent) != "command" || observation.Delivery.PhysicalAttemptID != "attempt-7" {
		t.Fatalf("observation lost boundary data: %#v", observation)
	}
	raw[0] = '!'
	if kernel.request.RawAcceptedEvent[0] == '!' {
		t.Fatal("sidecar retained caller-owned raw byte slice")
	}
}

func TestReduceReturnsUnknownWithoutInventingRetry(t *testing.T) {
	kernel := &recordingKernel{err: errors.New("lost response")}
	observation, err := (Service{Kernel: kernel}).Reduce(context.Background(), fixtureEnvelope([]byte("{}")))
	if err != nil {
		t.Fatal(err)
	}
	if observation.Status != "unknown" || observation.UncertaintyReason != "KERNEL_UNAVAILABLE_OR_UNCERTAIN" {
		t.Fatalf("unexpected uncertainty: %#v", observation)
	}
	if len(observation.CommandIntent) != 0 || observation.Outcome != "" {
		t.Fatalf("unknown observation invented semantic output: %#v", observation)
	}
}

func TestReduceRejectsMalformedEnvelopeAndInvalidKernelOutput(t *testing.T) {
	kernel := &recordingKernel{response: KernelResponse{Outcome: "Duplicate", CommandIntent: []byte("forbidden")}}
	service := Service{Kernel: kernel}
	if _, err := service.Reduce(context.Background(), EventEnvelope{}); !errors.Is(err, ErrMalformedEnvelope) {
		t.Fatalf("expected malformed envelope, got %v", err)
	}
	if _, err := service.Reduce(context.Background(), fixtureEnvelope([]byte("{}"))); !errors.Is(err, ErrInvalidKernelResponse) {
		t.Fatalf("expected invalid kernel response, got %v", err)
	}
}

func TestHTTPReferenceAdapterPreservesBase64RawPayload(t *testing.T) {
	raw := []byte("{\"z\":1, \"a\":2}")
	kernel := &recordingKernel{response: KernelResponse{Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor")}}
	handler := NewHTTPHandler(Service{Kernel: kernel})

	body, err := json.Marshal(fixtureEnvelope(raw))
	if err != nil {
		t.Fatal(err)
	}
	request := httptest.NewRequest(http.MethodPost, "/v1/reduce", bytes.NewReader(body))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if response.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", response.Code)
	}
	if !reflect.DeepEqual(kernel.request.RawAcceptedEvent, raw) {
		t.Fatalf("HTTP adapter changed raw bytes: %q", kernel.request.RawAcceptedEvent)
	}
}
