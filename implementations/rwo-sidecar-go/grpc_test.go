package rwosidecar

import (
	"bytes"
	"context"
	"errors"
	"net"
	"reflect"
	"testing"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
	"google.golang.org/grpc/test/bufconn"
)

func newBufconnGRPCClient(t *testing.T, service Service) (GRPCClient, func()) {
	t.Helper()

	listener := bufconn.Listen(1024 * 1024)
	server := NewGRPCServer(service)
	serveDone := make(chan error, 1)
	go func() {
		serveDone <- server.Serve(listener)
	}()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	connection, err := grpc.DialContext(
		ctx,
		"bufnet",
		grpc.WithContextDialer(func(ctx context.Context, _ string) (net.Conn, error) {
			return listener.DialContext(ctx)
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
		grpc.WithDisableRetry(),
	)
	cancel()
	if err != nil {
		server.Stop()
		_ = listener.Close()
		t.Fatalf("dial bufconn gRPC sidecar: %v", err)
	}

	cleanup := func() {
		_ = connection.Close()
		server.Stop()
		_ = listener.Close()
		select {
		case err := <-serveDone:
			if err != nil && !errors.Is(err, grpc.ErrServerStopped) {
				t.Errorf("serve bufconn gRPC sidecar: %v", err)
			}
		case <-time.After(5 * time.Second):
			t.Error("bufconn gRPC server did not stop")
		}
	}
	return NewGRPCClient(connection), cleanup
}

func TestGRPCBufconnPreservesRawBytesAndDeliveryBoundary(t *testing.T) {
	raw := []byte(" {\n  \"event_id\": \"event-1\", \"duplicate\": 1, \"duplicate\": 2\n}\t")
	kernel := &recordingKernel{response: KernelResponse{Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor")}}
	client, cleanup := newBufconnGRPCClient(t, Service{Kernel: kernel})
	defer cleanup()

	first := fixtureEnvelope(raw)
	first.Delivery = DeliveryContext{AdapterName: "grpc-bufconn", PhysicalAttemptID: "delivery-1"}
	firstObservation, err := client.Reduce(context.Background(), first)
	if err != nil {
		t.Fatal(err)
	}
	if kernel.calls != 1 {
		t.Fatalf("expected one kernel call, got %d", kernel.calls)
	}
	if !bytes.Equal(kernel.request.RawAcceptedEvent, raw) {
		t.Fatalf("gRPC changed raw event bytes: %q", kernel.request.RawAcceptedEvent)
	}
	if kernel.request.Tuple != fixtureTuple() || kernel.request.StreamIDHint != first.StreamIDHint {
		t.Fatalf("gRPC changed semantic request: %#v", kernel.request)
	}
	if firstObservation.Delivery != first.Delivery || firstObservation.Outcome != "Applied" {
		t.Fatalf("gRPC lost delivery observation: %#v", firstObservation)
	}

	second := first
	second.Delivery = DeliveryContext{AdapterName: "grpc-bufconn", PhysicalAttemptID: "delivery-2"}
	secondObservation, err := client.Reduce(context.Background(), second)
	if err != nil {
		t.Fatal(err)
	}
	if kernel.calls != 2 {
		t.Fatalf("expected two kernel calls, got %d", kernel.calls)
	}
	if !reflect.DeepEqual(kernel.requests[0], kernel.requests[1]) {
		t.Fatalf("delivery metadata leaked into kernel requests: %#v != %#v", kernel.requests[0], kernel.requests[1])
	}
	if secondObservation.Delivery != second.Delivery {
		t.Fatalf("second delivery metadata was not retained in observation: %#v", secondObservation)
	}
}

func TestGRPCBufconnKernelUncertaintyIsNotRetried(t *testing.T) {
	kernel := &recordingKernel{err: errors.New("lost response")}
	client, cleanup := newBufconnGRPCClient(t, Service{Kernel: kernel})
	defer cleanup()

	observation, err := client.Reduce(context.Background(), fixtureEnvelope([]byte("{}")))
	if err != nil {
		t.Fatal(err)
	}
	if kernel.calls != 1 {
		t.Fatalf("kernel uncertainty must not create a retry; got %d calls", kernel.calls)
	}
	if observation.Status != "unknown" || observation.UncertaintyReason != "KERNEL_UNAVAILABLE_OR_UNCERTAIN" {
		t.Fatalf("unexpected uncertainty observation: %#v", observation)
	}
	if observation.Outcome != "" || len(observation.CommandIntent) != 0 {
		t.Fatalf("uncertainty invented a semantic output: %#v", observation)
	}
}

func TestGRPCBufconnMapsMalformedEnvelopeToInvalidArgument(t *testing.T) {
	client, cleanup := newBufconnGRPCClient(t, Service{Kernel: &recordingKernel{response: KernelResponse{Outcome: "Applied", ValidatedStreamID: "stream-1", NextCursor: []byte("cursor")}}})
	defer cleanup()

	_, err := client.Reduce(context.Background(), EventEnvelope{})
	if status.Code(err) != codes.InvalidArgument {
		t.Fatalf("expected InvalidArgument for malformed gRPC envelope, got %v", err)
	}
}
