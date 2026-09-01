package rwosidecar

import (
	"bytes"
	"context"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
)

var fakeEveLines = [][]byte{
	[]byte("{\"eventId\":\"eve-event-1\",\"sessionId\":\"session-1\",\"type\":\"session.started\"}\n"),
	[]byte("{\"eventId\":\"eve-event-2\",\"output\":{\"answer\":\"bounded result\"},\"sessionId\":\"session-1\",\"type\":\"task.output\"}\n"),
	[]byte("{\"eventId\":\"eve-event-3\",\"sessionId\":\"session-1\",\"type\":\"session.completed\"}\n"),
}

func TestRequestPolicyMustBeExactAndToolFree(t *testing.T) {
	prepared := testPreparedEveRequest(t)
	mutations := []struct {
		name   string
		mutate func([]byte) []byte
	}{
		{name: "requestInput", mutate: func(value []byte) []byte {
			return bytes.Replace(value, []byte(`"requestInput":false`), []byte(`"requestInput":true`), 1)
		}},
		{name: "tools", mutate: addEveRequestField(`"tools":[]`)},
		{name: "delegation", mutate: addEveRequestField(`"delegation":true`)},
		{name: "workflow", mutate: addEveRequestField(`"workflow":{}`)},
		{name: "agent", mutate: addEveRequestField(`"agent":"built-in"`)},
		{name: "callback", mutate: addEveRequestField(`"callback":"http://127.0.0.1/cb"`)},
		{name: "shell", mutate: addEveRequestField(`"shell":true`)},
		{name: "write", mutate: addEveRequestField(`"write":true`)},
		{name: "web", mutate: addEveRequestField(`"web":true`)},
		{name: "arbitrary network", mutate: addEveRequestField(`"network":true`)},
	}
	for _, mutation := range mutations {
		t.Run(mutation.name, func(t *testing.T) {
			var creates int
			server := httptest.NewServer(http.HandlerFunc(func(http.ResponseWriter, *http.Request) { creates++ }))
			defer server.Close()
			adapter, err := NewEveLeafAdapter(server.URL, server.Client())
			if err != nil {
				t.Fatal(err)
			}
			result, err := adapter.Create(context.Background(), mutation.mutate(prepared.RequestBytes))
			if !errors.Is(err, ErrEveRequestPolicy) || result.SendClass != EveKnownNotSent || creates != 0 {
				t.Fatalf("policy mutation result=%#v err=%v creates=%d", result, err, creates)
			}
		})
	}
	if _, err := NewEveLeafAdapter("https://example.com", nil); !errors.Is(err, ErrEveLeafConfiguration) {
		t.Fatalf("non-loopback URL error = %v", err)
	}
}

func TestEveLeafCreatesOneSessionAndPersistsExactRawLines(t *testing.T) {
	server := newFakeEveServer(t)
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	prepared := testPreparedEveRequest(t)
	created, err := adapter.Create(context.Background(), prepared.RequestBytes)
	if err != nil {
		t.Fatalf("create: %v", err)
	}
	if created.SendClass != EveSessionKnown || created.SessionID != "session-1" || created.StatusCode != http.StatusAccepted {
		t.Fatalf("create result = %#v", created)
	}
	var persisted [][]byte
	err = adapter.Stream(context.Background(), created.SessionID, "", func(_ context.Context, sessionID string, line []byte) error {
		if sessionID != created.SessionID {
			t.Fatalf("sink session = %q", sessionID)
		}
		persisted = append(persisted, bytes.Clone(line))
		return nil
	})
	if err != nil {
		t.Fatalf("stream: %v", err)
	}
	if !equalRawLines(persisted, fakeEveLines) {
		t.Fatalf("persisted lines changed\n got: %q\nwant: %q", persisted, fakeEveLines)
	}
	state := server.State()
	if state.Creates != 1 || state.Streams != 1 || state.Cancels != 0 || !bytes.Equal(state.CreateBody, prepared.RequestBytes) {
		t.Fatalf("fake Eve observations = %#v", state)
	}
}

func TestSessionKnownReopensByReconnectWithoutSecondCreate(t *testing.T) {
	server := newFakeEveServer(t)
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	created, err := adapter.Create(context.Background(), testPreparedEveRequest(t).RequestBytes)
	if err != nil {
		t.Fatal(err)
	}
	var first [][]byte
	if err := adapter.Stream(context.Background(), created.SessionID, "", collectRawLines(&first)); err != nil {
		t.Fatal(err)
	}
	var reconnect [][]byte
	if err := adapter.Stream(context.Background(), created.SessionID, "eve-event-3", collectRawLines(&reconnect)); err != nil {
		t.Fatal(err)
	}
	state := server.State()
	if state.Creates != 1 || state.Streams != 2 || len(reconnect) != 0 || state.AfterEventID != "eve-event-3" {
		t.Fatalf("reconnect observations = %#v, lines=%q", state, reconnect)
	}
	if !equalRawLines(first, fakeEveLines) {
		t.Fatalf("first stream changed: %q", first)
	}
}

func TestEveLeafCancelUsesKnownSessionEndpoint(t *testing.T) {
	server := newFakeEveServer(t)
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	result, err := adapter.Cancel(context.Background(), "session-1")
	if err != nil || result.StatusCode != http.StatusAccepted {
		t.Fatalf("cancel result=%#v err=%v", result, err)
	}
	if state := server.State(); state.Cancels != 1 || state.Creates != 0 {
		t.Fatalf("cancel observations = %#v", state)
	}
}

func TestEveLeafDoesNotInterpretBeforePersistence(t *testing.T) {
	line := []byte("not-json-but-still-raw\n")
	server := httptest.NewServer(http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("Content-Type", "application/x-ndjson")
		_, _ = writer.Write(line)
	}))
	defer server.Close()
	adapter, err := NewEveLeafAdapter(server.URL, server.Client())
	if err != nil {
		t.Fatal(err)
	}
	var persisted []byte
	if err := adapter.Stream(context.Background(), "session-1", "", func(_ context.Context, _ string, raw []byte) error {
		persisted = bytes.Clone(raw)
		return nil
	}); err != nil {
		t.Fatalf("transport interpreted raw bytes: %v", err)
	}
	if !bytes.Equal(persisted, line) {
		t.Fatalf("raw persistence changed: %q", persisted)
	}
}

type fakeEveState struct {
	Creates      int
	Streams      int
	Cancels      int
	CreateBody   []byte
	AfterEventID string
}

type fakeEveServer struct {
	*httptest.Server
	mu    sync.Mutex
	state fakeEveState
}

func newFakeEveServer(t *testing.T) *fakeEveServer {
	t.Helper()
	fake := &fakeEveServer{}
	fake.Server = httptest.NewServer(http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		fake.mu.Lock()
		defer fake.mu.Unlock()
		switch {
		case request.Method == http.MethodPost && request.URL.Path == "/eve/v1/session":
			fake.state.Creates++
			body, _ := io.ReadAll(request.Body)
			fake.state.CreateBody = bytes.Clone(body)
			if err := ValidateEveTaskRequest(body); err != nil {
				http.Error(writer, err.Error(), http.StatusBadRequest)
				return
			}
			writer.Header().Set("Content-Type", "application/json")
			writer.WriteHeader(http.StatusAccepted)
			_, _ = writer.Write([]byte(`{"sessionId":"session-1"}`))
		case request.Method == http.MethodGet && request.URL.Path == "/eve/v1/session/session-1/stream":
			fake.state.Streams++
			fake.state.AfterEventID = request.URL.Query().Get("afterEventId")
			writer.Header().Set("Content-Type", "application/x-ndjson")
			if fake.state.AfterEventID == "" {
				for _, line := range fakeEveLines {
					_, _ = writer.Write(line)
				}
			}
		case request.Method == http.MethodPost && request.URL.Path == "/eve/v1/session/session-1/cancel":
			fake.state.Cancels++
			writer.WriteHeader(http.StatusAccepted)
			_, _ = writer.Write([]byte(`{"status":"cancel_requested"}`))
		default:
			http.NotFound(writer, request)
		}
	}))
	return fake
}

func (fake *fakeEveServer) State() fakeEveState {
	fake.mu.Lock()
	defer fake.mu.Unlock()
	copy := fake.state
	copy.CreateBody = bytes.Clone(copy.CreateBody)
	return copy
}

func testPreparedEveRequest(t *testing.T) PreparedEveTaskRequest {
	t.Helper()
	prepared, err := PrepareEveTaskRequest(testCommandBytes(t, "seat", testSeatAddress), taggedTestDigest("command"), "attempt-1", 1, testSeatCatalog(t, fixtureMaterialRoot(t)))
	if err != nil {
		t.Fatal(err)
	}
	return prepared
}

func addEveRequestField(field string) func([]byte) []byte {
	return func(value []byte) []byte {
		trimmed := bytes.TrimSpace(value)
		return append(append(append([]byte(nil), trimmed[:len(trimmed)-1]...), ','), append([]byte(field), '}')...)
	}
}

func collectRawLines(target *[][]byte) EveRawLineSink {
	return func(_ context.Context, _ string, line []byte) error {
		*target = append(*target, bytes.Clone(line))
		return nil
	}
}

func equalRawLines(left, right [][]byte) bool {
	if len(left) != len(right) {
		return false
	}
	for index := range left {
		if !bytes.Equal(left[index], right[index]) {
			return false
		}
	}
	return true
}
