package rwosidecar

import (
	"bytes"
	"context"
	"errors"
	"net"
	"testing"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func startFixtureRuntime(t *testing.T) *LocalRuntime {
	t.Helper()
	manifest := localManifest(t)
	composition := localFixture(t, manifest, "explicitComposition")
	child := startFixtureChild(t)
	compiled, err := child.Compile(context.Background(), CompileRequest{
		Tuple: tupleForFixture(composition, "ExplicitComposition"), RawComposition: rawFixture(t, composition),
	})
	if err != nil {
		t.Fatal(err)
	}
	runtime, err := NewRuntimeKernel(child, compiled)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := runtime.Close(); err != nil {
			t.Errorf("close runtime: %v", err)
		}
	})
	return runtime
}

func TestRuntimeGRPCBufconnUsesRealRustChildAndVolatileCommit(t *testing.T) {
	manifest := localManifest(t)
	event := localFixture(t, manifest, "matchingEvent")
	runtime := startFixtureRuntime(t)
	client, cleanup := newBufconnGRPCClient(t, Service{Kernel: runtime})
	defer cleanup()

	raw := rawFixture(t, event)
	firstInput := EventEnvelope{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", CorrelationID: "correlation-a", RawAcceptedEvent: raw,
		Delivery: DeliveryContext{AdapterName: "bufconn", PhysicalAttemptID: "delivery-a"},
	}
	first, err := client.Reduce(context.Background(), firstInput)
	if err != nil {
		t.Fatal(err)
	}
	if first.Status != "reduced" || first.Outcome != "Applied" || first.ValidatedStreamID != "stream-1" || len(first.NextCursor) == 0 || len(first.CommandIntent) == 0 {
		t.Fatalf("unexpected first observation: %#v", first)
	}
	cursor, outbox, exists := runtime.snapshot("stream-1")
	if !exists || !bytes.Equal(cursor, first.NextCursor) || len(outbox) != 1 {
		t.Fatalf("first gRPC call did not make one volatile transition: %q %#v", cursor, outbox)
	}

	secondInput := firstInput
	secondInput.CorrelationID = "correlation-b"
	secondInput.Delivery = DeliveryContext{AdapterName: "same-local-adapter", PhysicalAttemptID: "delivery-b"}
	second, err := client.Reduce(context.Background(), secondInput)
	if err != nil {
		t.Fatal(err)
	}
	if second.Outcome != "Duplicate" || !bytes.Equal(second.NextCursor, first.NextCursor) || len(second.CommandIntent) != 0 {
		t.Fatalf("changed metadata changed semantic duplicate behavior: %#v", second)
	}
	cursor, outbox, exists = runtime.snapshot("stream-1")
	if !exists || !bytes.Equal(cursor, first.NextCursor) || len(outbox) != 1 {
		t.Fatalf("duplicate created an extra local effect: %q %#v", cursor, outbox)
	}
}

func TestRuntimeCloseDropsVolatileState(t *testing.T) {
	manifest := localManifest(t)
	event := localFixture(t, manifest, "matchingEvent")
	runtime := startFixtureRuntime(t)
	_, err := runtime.Reduce(context.Background(), KernelRequest{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, event),
	})
	if err != nil {
		t.Fatal(err)
	}
	if _, _, exists := runtime.snapshot("stream-1"); !exists {
		t.Fatal("fixture transition was not volatile state")
	}
	if err := runtime.Close(); err != nil {
		t.Fatal(err)
	}
	if _, _, exists := runtime.snapshot("stream-1"); exists {
		t.Fatal("Close must drop volatile cursor/outbox maps")
	}
}

func TestRuntimeRecordsNoMatchWithoutInventingCommand(t *testing.T) {
	runtime := startFixtureRuntime(t)
	noMatch := map[string]any{
		"contract_id": "RWO-SEMANTIC-CONTRACT", "contract_version": "1.0.0",
		"profile_id": "RWO-JCS-IJSON-SAFEINT", "profile_version": "1.0.0",
		"schema_id": "AcceptedEventView", "schema_version": "1.0.0",
		"stream_id": "stream-no-match", "event_id": "event-no-match", "event_type": "NoMatch",
		"source_node_id": "source", "payload": map[string]any{"job_id": "job-no-match"},
	}
	response, err := runtime.Reduce(context.Background(), KernelRequest{
		Tuple: tupleForFixture(noMatch, "AcceptedEventView"), StreamIDHint: "stream-no-match", RawAcceptedEvent: rawFixture(t, noMatch),
	})
	if err != nil {
		t.Fatal(err)
	}
	if response.Outcome != "Applied" || len(response.NextCursor) == 0 || len(response.CommandIntent) != 0 {
		t.Fatalf("no-match must advance only a cursor: %#v", response)
	}
	cursor, outbox, exists := runtime.snapshot("stream-no-match")
	if !exists || !bytes.Equal(cursor, response.NextCursor) || len(outbox) != 0 {
		t.Fatalf("no-match state mismatch: %q %#v", cursor, outbox)
	}
}

func TestRuntimeLeavesStateUntouchedForDivergentAndMalformedEvents(t *testing.T) {
	manifest := localManifest(t)
	event := localFixture(t, manifest, "matchingEvent")
	runtime := startFixtureRuntime(t)
	request := KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, event)}
	first, err := runtime.Reduce(context.Background(), request)
	if err != nil {
		t.Fatal(err)
	}
	beforeCursor, beforeOutbox, _ := runtime.snapshot("stream-1")
	divergent := localFixture(t, manifest, "matchingEvent")
	divergent["payload"] = map[string]any{"job_id": "job-2"}
	response, err := runtime.Reduce(context.Background(), KernelRequest{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, divergent),
	})
	if err != nil {
		t.Fatal(err)
	}
	if response.Outcome != "DivergentDuplicate" || !bytes.Equal(response.NextCursor, first.NextCursor) || len(response.CommandIntent) != 0 {
		t.Fatalf("unexpected divergent response: %#v", response)
	}
	afterCursor, afterOutbox, _ := runtime.snapshot("stream-1")
	if !bytes.Equal(beforeCursor, afterCursor) || len(beforeOutbox) != len(afterOutbox) {
		t.Fatalf("divergent event changed state: %q %#v -> %q %#v", beforeCursor, beforeOutbox, afterCursor, afterOutbox)
	}
	malformed, err := runtime.Reduce(context.Background(), KernelRequest{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: []byte("{not-json"),
	})
	if err != nil {
		t.Fatal(err)
	}
	if malformed.Outcome != "Rejected" || len(malformed.CommandIntent) != 0 || !bytes.Equal(malformed.NextCursor, beforeCursor) {
		t.Fatalf("unexpected malformed raw event response: %#v", malformed)
	}
	afterMalformedCursor, afterMalformedOutbox, _ := runtime.snapshot("stream-1")
	if !bytes.Equal(beforeCursor, afterMalformedCursor) || len(beforeOutbox) != len(afterMalformedOutbox) {
		t.Fatal("malformed raw event changed volatile state")
	}
}

func TestFreshRuntimeHasNoRecoveryState(t *testing.T) {
	manifest := localManifest(t)
	event := localFixture(t, manifest, "matchingEvent")
	firstRuntime := startFixtureRuntime(t)
	request := KernelRequest{Tuple: fixtureTuple(), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, event)}
	first, err := firstRuntime.Reduce(context.Background(), request)
	if err != nil || first.Outcome != "Applied" {
		t.Fatalf("first volatile host transition: %#v %v", first, err)
	}
	if err := firstRuntime.Close(); err != nil {
		t.Fatal(err)
	}
	secondRuntime := startFixtureRuntime(t)
	if _, _, exists := secondRuntime.snapshot("stream-1"); exists {
		t.Fatal("fresh runtime must not recover prior cursor or outbox state")
	}
	second, err := secondRuntime.Reduce(context.Background(), request)
	if err != nil || second.Outcome != "Applied" || len(second.CommandIntent) == 0 {
		t.Fatalf("fresh volatile host did not independently apply: %#v %v", second, err)
	}
}

func TestRuntimeGRPCLoopbackSmokeStopsCleanly(t *testing.T) {
	manifest := localManifest(t)
	event := localFixture(t, manifest, "matchingEvent")
	runtime := startFixtureRuntime(t)
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	if address := listener.Addr().(*net.TCPAddr).IP; !address.IsLoopback() {
		t.Fatalf("smoke listener escaped loopback: %s", address)
	}
	server := NewGRPCServer(Service{Kernel: runtime})
	serveDone := make(chan error, 1)
	go func() { serveDone <- server.Serve(listener) }()
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	connection, err := grpc.DialContext(ctx, listener.Addr().String(), grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock(), grpc.WithDisableRetry())
	if err != nil {
		server.Stop()
		_ = listener.Close()
		t.Fatal(err)
	}
	client := NewGRPCClient(connection)
	observation, err := client.Reduce(ctx, EventEnvelope{
		Tuple: fixtureTuple(), StreamIDHint: "stream-1", CorrelationID: "loopback-smoke", RawAcceptedEvent: rawFixture(t, event),
		Delivery: DeliveryContext{AdapterName: "loopback-smoke", PhysicalAttemptID: "one"},
	})
	if err != nil {
		t.Fatal(err)
	}
	if observation.Outcome != "Applied" || len(observation.NextCursor) == 0 {
		t.Fatalf("unexpected local smoke observation: %#v", observation)
	}
	_ = connection.Close()
	server.Stop()
	_ = listener.Close()
	select {
	case serveErr := <-serveDone:
		if serveErr != nil && !errors.Is(serveErr, grpc.ErrServerStopped) {
			t.Fatalf("loopback server shutdown: %v", serveErr)
		}
	case <-time.After(5 * time.Second):
		t.Fatal("loopback server did not stop")
	}
}
