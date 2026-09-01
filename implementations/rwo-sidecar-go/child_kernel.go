package rwosidecar

import (
	"context"
	"encoding/base64"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strconv"
	"sync"
)

const localKernelProtocolVersion = "rwo-local-kernel/1"

var (
	// ErrKernelProtocol means the private local child did not honor its framed
	// control protocol. The caller must not guess whether semantic work ran.
	ErrKernelProtocol = errors.New("invalid RWO local kernel protocol response")
	// ErrKernelClosed means the one long-lived child is unavailable. This
	// prototype deliberately does not restart or replay it automatically.
	ErrKernelClosed = errors.New("RWO local kernel child is closed")
)

// CompileRequest is the one raw composition boundary sent to the Rust child.
// The Go host only base64-wraps the bytes; it never decodes or normalizes the
// semantic composition itself.
type CompileRequest struct {
	Tuple          VersionTuple
	RawComposition []byte
}

// CompileResponse describes a graph retained only by the child process. Its
// handle has no meaning after that process exits.
type CompileResponse struct {
	Outcome       string
	GraphHandle   string
	GraphIdentity string
	DefectCodes   []string
}

// ChildKernelConfig supplies the explicit local process boundary. It has no
// network address, retry policy, persistence setting, or external adapter.
type ChildKernelConfig struct {
	ExecutablePath string
	RegistryPath   string
	MaxFrameBytes  uint32
}

func (config ChildKernelConfig) validate() error {
	if config.ExecutablePath == "" || config.RegistryPath == "" || config.MaxFrameBytes == 0 {
		return fmt.Errorf("%w: executable_path, registry_path, and max_frame_bytes are required", ErrMalformedEnvelope)
	}
	return nil
}

// ChildKernel owns one private, long-lived Rust child. Calls serialize at the
// process protocol boundary, while LocalRuntime owns its own per-stream commit
// locks above this layer.
type ChildKernel struct {
	mu            sync.Mutex
	command       *exec.Cmd
	stdin         io.WriteCloser
	stdout        io.ReadCloser
	maxFrameBytes uint32
	nextRequestID uint64
	closed        bool
}

// ProcessKernel names the Go-owned process/protocol role used in the Work
// Pack. It remains an alias because the implementation is deliberately one
// narrow child-process bridge, not a second semantic kernel.
type ProcessKernel = ChildKernel

// StartChildKernel starts a local executable with exactly the Rust child's
// private arguments. It intentionally uses no shell and does not consult the
// network.
func StartChildKernel(config ChildKernelConfig) (*ChildKernel, error) {
	if err := config.validate(); err != nil {
		return nil, err
	}
	command := exec.Command(
		config.ExecutablePath,
		"--registry", config.RegistryPath,
		"--max-frame-bytes", strconv.FormatUint(uint64(config.MaxFrameBytes), 10),
	)
	stdin, err := command.StdinPipe()
	if err != nil {
		return nil, fmt.Errorf("open local kernel stdin: %w", err)
	}
	stdout, err := command.StdoutPipe()
	if err != nil {
		_ = stdin.Close()
		return nil, fmt.Errorf("open local kernel stdout: %w", err)
	}
	// Child stderr is diagnostic only. Keeping it on the host stderr prevents a
	// full diagnostic pipe from blocking the private protocol stream.
	command.Stderr = os.Stderr
	if err := command.Start(); err != nil {
		_ = stdin.Close()
		_ = stdout.Close()
		return nil, fmt.Errorf("start local kernel child: %w", err)
	}
	return &ChildKernel{
		command:       command,
		stdin:         stdin,
		stdout:        stdout,
		maxFrameBytes: config.MaxFrameBytes,
	}, nil
}

// StartProcessKernel is the Work-Pack-facing constructor for the same local
// child bridge. It adds no behavior beyond StartChildKernel.
func StartProcessKernel(config ChildKernelConfig) (*ProcessKernel, error) {
	return StartChildKernel(config)
}

// Close stops the volatile child. It does not flush, persist, retry, or replay
// any request. A later caller must explicitly start and compile a new child.
func (child *ChildKernel) Close() error {
	if child == nil {
		return nil
	}
	child.mu.Lock()
	defer child.mu.Unlock()
	return child.stopLocked()
}

func (child *ChildKernel) stopLocked() error {
	if child.closed {
		return nil
	}
	child.closed = true
	var failures []error
	if child.stdin != nil {
		if err := child.stdin.Close(); err != nil {
			failures = append(failures, err)
		}
	}
	if child.command != nil && child.command.Process != nil {
		if err := child.command.Process.Kill(); err != nil && !errors.Is(err, os.ErrProcessDone) {
			failures = append(failures, err)
		}
		if err := child.command.Wait(); err != nil {
			// A nonzero exit is expected after an explicit local stop.
			if _, ok := err.(*exec.ExitError); !ok {
				failures = append(failures, err)
			}
		}
	}
	return errors.Join(failures...)
}

// Compile sends opaque composition bytes to Rust and returns only child-owned
// graph identity metadata. A failed protocol exchange closes the child to
// prevent a later response from being mistaken for another request.
func (child *ChildKernel) Compile(ctx context.Context, request CompileRequest) (CompileResponse, error) {
	if child == nil {
		return CompileResponse{}, ErrKernelClosed
	}
	if err := request.Tuple.validate(); err != nil {
		return CompileResponse{}, err
	}
	if len(request.RawComposition) == 0 {
		return CompileResponse{}, fmt.Errorf("%w: raw composition is required", ErrMalformedEnvelope)
	}
	response, err := child.exchange(ctx, childRequest{
		Operation:            "CompileV1",
		Tuple:                request.Tuple,
		RawCompositionBase64: base64.StdEncoding.EncodeToString(request.RawComposition),
	})
	if err != nil {
		return CompileResponse{}, err
	}
	if response.ResponseKind != "semantic" || (response.Outcome != "Compiled" && response.Outcome != "Rejected") {
		return CompileResponse{}, fmt.Errorf("%w: invalid compile response", ErrKernelProtocol)
	}
	result := CompileResponse{
		Outcome:       response.Outcome,
		GraphHandle:   response.GraphHandle,
		GraphIdentity: response.GraphIdentity,
		DefectCodes:   response.defectCodes(),
	}
	if result.Outcome == "Compiled" && (result.GraphHandle == "" || result.GraphIdentity == "") {
		return CompileResponse{}, fmt.Errorf("%w: compiled response lacks graph handle or identity", ErrKernelProtocol)
	}
	return result, nil
}

// ReduceCompiled uses a graph handle retained by this exact child process. The
// original cursor and raw event remain opaque bytes to Go.
func (child *ChildKernel) ReduceCompiled(
	ctx context.Context,
	graphHandle string,
	originalCursor []byte,
	request KernelRequest,
) (KernelResponse, error) {
	if child == nil {
		return KernelResponse{}, ErrKernelClosed
	}
	if graphHandle == "" {
		return KernelResponse{}, fmt.Errorf("%w: graph handle is required", ErrMalformedEnvelope)
	}
	if err := request.validate(); err != nil {
		return KernelResponse{}, err
	}
	var originalCursorBase64 json.RawMessage
	if originalCursor != nil {
		originalCursorBase64, _ = json.Marshal(base64.StdEncoding.EncodeToString(originalCursor))
	} else {
		originalCursorBase64 = json.RawMessage("null")
	}
	response, err := child.exchange(ctx, childRequest{
		Operation:              "ReduceV1",
		Tuple:                  request.Tuple,
		GraphHandle:            graphHandle,
		StreamIDHint:           request.StreamIDHint,
		RawAcceptedEventBase64: base64.StdEncoding.EncodeToString(request.RawAcceptedEvent),
		OriginalCursorBase64:   originalCursorBase64,
	})
	if err != nil {
		return KernelResponse{}, err
	}
	if response.ResponseKind != "semantic" || !validOutcome(response.Outcome) {
		return KernelResponse{}, fmt.Errorf("%w: invalid reduce response", ErrKernelProtocol)
	}
	cursor, err := decodeOptionalBase64(response.CursorBase64)
	if err != nil {
		return KernelResponse{}, err
	}
	command, err := decodeOptionalBase64(response.CommandBase64)
	if err != nil {
		return KernelResponse{}, err
	}
	return KernelResponse{
		Outcome:               response.Outcome,
		NextCursor:            cursor,
		CommandIntent:         command,
		ValidatedStreamID:     response.ValidatedStreamID,
		AcceptedEventIdentity: response.AcceptedEventIdentity,
		EventPayloadDigest:    response.EventPayloadDigest,
		CommandIntentIdentity: response.CommandIntentIdentity,
		CommandPayloadDigest:  response.CommandPayloadDigest,
		DefectCodes:           response.defectCodes(),
	}, nil
}

type childRequest struct {
	ProtocolVersion        string          `json:"protocol_version"`
	RequestID              string          `json:"request_id"`
	Operation              string          `json:"operation"`
	Tuple                  VersionTuple    `json:"tuple"`
	RawCompositionBase64   string          `json:"raw_composition_base64,omitempty"`
	GraphHandle            string          `json:"graph_handle,omitempty"`
	StreamIDHint           string          `json:"stream_id_hint,omitempty"`
	RawAcceptedEventBase64 string          `json:"raw_accepted_event_base64,omitempty"`
	OriginalCursorBase64   json.RawMessage `json:"original_cursor_base64,omitempty"`
}

type childDefect struct {
	Code string `json:"code"`
}

type childError struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

type childResponse struct {
	ProtocolVersion       string        `json:"protocol_version"`
	RequestID             *string       `json:"request_id"`
	Operation             *string       `json:"operation"`
	ResponseKind          string        `json:"response_kind"`
	Outcome               string        `json:"outcome"`
	GraphHandle           string        `json:"graph_handle"`
	GraphIdentity         string        `json:"graph_identity"`
	ValidatedStreamID     string        `json:"validated_stream_id"`
	CursorBase64          *string       `json:"cursor_base64"`
	CommandBase64         *string       `json:"command_base64"`
	AcceptedEventIdentity string        `json:"accepted_event_identity"`
	EventPayloadDigest    string        `json:"event_payload_digest"`
	CommandIntentIdentity string        `json:"command_intent_identity"`
	CommandPayloadDigest  string        `json:"command_payload_digest"`
	Defects               []childDefect `json:"defects"`
	Error                 *childError   `json:"error"`
}

func (response childResponse) defectCodes() []string {
	codes := make([]string, 0, len(response.Defects))
	for _, defect := range response.Defects {
		if defect.Code != "" {
			codes = append(codes, defect.Code)
		}
	}
	return codes
}

func decodeOptionalBase64(value *string) ([]byte, error) {
	if value == nil {
		return nil, nil
	}
	decoded, err := base64.StdEncoding.DecodeString(*value)
	if err != nil {
		return nil, fmt.Errorf("%w: semantic byte payload is not base64", ErrKernelProtocol)
	}
	return decoded, nil
}

func (child *ChildKernel) exchange(ctx context.Context, request childRequest) (childResponse, error) {
	child.mu.Lock()
	defer child.mu.Unlock()
	if child.closed {
		return childResponse{}, ErrKernelClosed
	}
	child.nextRequestID++
	request.ProtocolVersion = localKernelProtocolVersion
	request.RequestID = strconv.FormatUint(child.nextRequestID, 10)
	payload, err := json.Marshal(request)
	if err != nil {
		return childResponse{}, fmt.Errorf("marshal child request: %w", err)
	}
	if len(payload) == 0 || len(payload) > int(child.maxFrameBytes) {
		return childResponse{}, fmt.Errorf("%w: request frame exceeds configured maximum", ErrKernelProtocol)
	}
	if err := writeChildFrame(child.stdin, payload); err != nil {
		_ = child.stopLocked()
		return childResponse{}, fmt.Errorf("write child request: %w", err)
	}
	type received struct {
		response childResponse
		err      error
	}
	result := make(chan received, 1)
	go func() {
		bytes, err := readChildFrame(child.stdout, child.maxFrameBytes)
		if err != nil {
			result <- received{err: err}
			return
		}
		var response childResponse
		if err := json.Unmarshal(bytes, &response); err != nil {
			result <- received{err: fmt.Errorf("decode child response: %w", err)}
			return
		}
		result <- received{response: response}
	}()
	select {
	case <-ctx.Done():
		_ = child.stopLocked()
		<-result // consume the terminated read before another process is possible
		return childResponse{}, ctx.Err()
	case outcome := <-result:
		if outcome.err != nil {
			_ = child.stopLocked()
			return childResponse{}, fmt.Errorf("read child response: %w", outcome.err)
		}
		if outcome.response.ProtocolVersion != localKernelProtocolVersion ||
			outcome.response.RequestID == nil || *outcome.response.RequestID != request.RequestID ||
			outcome.response.Operation == nil || *outcome.response.Operation != request.Operation {
			_ = child.stopLocked()
			return childResponse{}, fmt.Errorf("%w: response correlation mismatch", ErrKernelProtocol)
		}
		if outcome.response.ResponseKind == "protocol_error" {
			_ = child.stopLocked()
			if outcome.response.Error == nil {
				return childResponse{}, fmt.Errorf("%w: child protocol error lacks detail", ErrKernelProtocol)
			}
			return childResponse{}, fmt.Errorf("%w: %s", ErrKernelProtocol, outcome.response.Error.Code)
		}
		return outcome.response, nil
	}
}

func writeChildFrame(writer io.Writer, payload []byte) error {
	var header [4]byte
	binary.BigEndian.PutUint32(header[:], uint32(len(payload)))
	if _, err := writer.Write(header[:]); err != nil {
		return err
	}
	_, err := writer.Write(payload)
	return err
}

func readChildFrame(reader io.Reader, maximum uint32) ([]byte, error) {
	var header [4]byte
	if _, err := io.ReadFull(reader, header[:]); err != nil {
		return nil, err
	}
	length := binary.BigEndian.Uint32(header[:])
	if length == 0 || length > maximum {
		return nil, fmt.Errorf("frame length %d is outside configured bounds", length)
	}
	payload := make([]byte, length)
	if _, err := io.ReadFull(reader, payload); err != nil {
		return nil, err
	}
	return payload, nil
}
