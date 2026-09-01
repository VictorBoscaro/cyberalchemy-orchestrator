package rwosidecar

import (
	"bufio"
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"strconv"
	"strings"
)

type EveSendClass string

const (
	EveKnownNotSent     EveSendClass = "known_not_sent"
	EveMayHaveSent      EveSendClass = "may_have_been_sent"
	EveSessionKnown     EveSendClass = "session_known"
	defaultEveMaxBody                = 1 << 20
	defaultEveMaxLine                = 256 << 10
	defaultEveMaxStream              = 4 << 20
)

var (
	ErrEveLeafConfiguration = errors.New("invalid Eve leaf configuration")
	ErrEveLeafProtocol      = errors.New("invalid Eve leaf response")
	ErrEveLeafStream        = errors.New("invalid Eve NDJSON stream")
)

type EveCreateResult struct {
	StatusCode     int
	SessionID      string
	ResponseBytes  []byte
	ResponseSHA256 string
	SendClass      EveSendClass
}

type EveCancelResult struct {
	StatusCode    int
	ResponseBytes []byte
}

// EveRawLineSink must durably persist line before returning nil. EveLeafAdapter
// performs no JSON or terminal interpretation before invoking it.
type EveRawLineSink func(context.Context, string, []byte) error

type EveLeafAdapter struct {
	baseURL        *url.URL
	client         *http.Client
	maxBodyBytes   int64
	maxLineBytes   int
	maxStreamBytes int64
}

func NewEveLeafAdapter(rawBaseURL string, client *http.Client) (*EveLeafAdapter, error) {
	parsed, err := url.Parse(rawBaseURL)
	if err != nil || parsed.Scheme == "" || parsed.Host == "" || parsed.User != nil ||
		(parsed.Scheme != "http" && parsed.Scheme != "https") ||
		(parsed.Path != "" && parsed.Path != "/") || parsed.RawQuery != "" || parsed.Fragment != "" {
		return nil, fmt.Errorf("%w: absolute loopback HTTP(S) base URL required", ErrEveLeafConfiguration)
	}
	ip := net.ParseIP(parsed.Hostname())
	if ip == nil || !ip.IsLoopback() {
		return nil, fmt.Errorf("%w: numeric loopback host required", ErrEveLeafConfiguration)
	}
	if client == nil {
		client = http.DefaultClient
	}
	boundedClient := *client
	boundedClient.CheckRedirect = func(*http.Request, []*http.Request) error {
		return errors.New("Eve leaf redirects are disabled")
	}
	parsed.Path = ""
	return &EveLeafAdapter{
		baseURL: parsed, client: &boundedClient, maxBodyBytes: defaultEveMaxBody,
		maxLineBytes: defaultEveMaxLine, maxStreamBytes: defaultEveMaxStream,
	}, nil
}

func (adapter *EveLeafAdapter) Create(ctx context.Context, requestBytes []byte) (EveCreateResult, error) {
	result := EveCreateResult{SendClass: EveKnownNotSent}
	if adapter == nil || adapter.client == nil || adapter.baseURL == nil {
		return result, ErrEveLeafConfiguration
	}
	if err := ValidateEveTaskRequest(requestBytes); err != nil {
		return result, err
	}
	if err := ctx.Err(); err != nil {
		return result, err
	}
	request, err := http.NewRequestWithContext(ctx, http.MethodPost, adapter.endpoint("/eve/v1/session"), bytes.NewReader(requestBytes))
	if err != nil {
		return result, fmt.Errorf("%w: build create request: %v", ErrEveLeafConfiguration, err)
	}
	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("Accept", "application/json")

	response, err := adapter.client.Do(request)
	if err != nil {
		result.SendClass = EveMayHaveSent
		return result, err
	}
	defer response.Body.Close()
	result.StatusCode = response.StatusCode
	result.SendClass = EveMayHaveSent
	result.ResponseBytes, err = readBounded(response.Body, adapter.maxBodyBytes)
	if err != nil {
		return result, fmt.Errorf("%w: read create response: %v", ErrEveLeafProtocol, err)
	}
	result.ResponseSHA256 = digestHex(result.ResponseBytes)
	if response.StatusCode != http.StatusAccepted {
		return result, fmt.Errorf("%w: create status %d", ErrEveLeafProtocol, response.StatusCode)
	}
	var body struct {
		SessionID string `json:"sessionId"`
	}
	if err := decodeClosedJSON(result.ResponseBytes, &body); err != nil || body.SessionID == "" {
		return result, fmt.Errorf("%w: 202 response requires one sessionId", ErrEveLeafProtocol)
	}
	result.SessionID = body.SessionID
	result.SendClass = EveSessionKnown
	return result, nil
}

func (adapter *EveLeafAdapter) Stream(ctx context.Context, sessionID, afterEventID string, sink EveRawLineSink) error {
	if adapter == nil || adapter.client == nil || adapter.baseURL == nil || sessionID == "" || sink == nil {
		return fmt.Errorf("%w: adapter, session, and persistence sink are required", ErrEveLeafConfiguration)
	}
	streamURL, err := url.Parse(adapter.endpoint("/eve/v1/session/" + url.PathEscape(sessionID) + "/stream"))
	if err != nil {
		return fmt.Errorf("%w: build stream URL: %v", ErrEveLeafConfiguration, err)
	}
	if afterEventID != "" {
		query := streamURL.Query()
		query.Set("afterEventId", afterEventID)
		streamURL.RawQuery = query.Encode()
	}
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, streamURL.String(), nil)
	if err != nil {
		return fmt.Errorf("%w: build stream request: %v", ErrEveLeafConfiguration, err)
	}
	request.Header.Set("Accept", "application/x-ndjson")
	response, err := adapter.client.Do(request)
	if err != nil {
		return err
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		_, _ = readBounded(response.Body, adapter.maxBodyBytes)
		return fmt.Errorf("%w: stream status %d", ErrEveLeafProtocol, response.StatusCode)
	}
	if !validNDJSONContentType(response.Header.Get("Content-Type")) {
		return fmt.Errorf("%w: stream content type %q", ErrEveLeafProtocol, response.Header.Get("Content-Type"))
	}

	reader := bufio.NewReaderSize(response.Body, adapter.maxLineBytes+1)
	var total int64
	for {
		line, readErr := reader.ReadBytes('\n')
		if len(line) > adapter.maxLineBytes {
			return fmt.Errorf("%w: line exceeds %d bytes", ErrEveLeafStream, adapter.maxLineBytes)
		}
		if len(line) != 0 {
			if line[len(line)-1] != '\n' {
				return fmt.Errorf("%w: final NDJSON line lacks LF", ErrEveLeafStream)
			}
			total += int64(len(line))
			if total > adapter.maxStreamBytes {
				return fmt.Errorf("%w: stream exceeds %d bytes", ErrEveLeafStream, adapter.maxStreamBytes)
			}
			// The callback is the persistence boundary. This package does not
			// inspect event IDs or JSON before the exact bytes are accepted.
			if err := sink(ctx, sessionID, bytes.Clone(line)); err != nil {
				return err
			}
		}
		if errors.Is(readErr, io.EOF) {
			return nil
		}
		if readErr != nil {
			return readErr
		}
	}
}

func (adapter *EveLeafAdapter) Cancel(ctx context.Context, sessionID string) (EveCancelResult, error) {
	if adapter == nil || adapter.client == nil || adapter.baseURL == nil || sessionID == "" {
		return EveCancelResult{}, fmt.Errorf("%w: adapter and session are required", ErrEveLeafConfiguration)
	}
	request, err := http.NewRequestWithContext(ctx, http.MethodPost, adapter.endpoint("/eve/v1/session/"+url.PathEscape(sessionID)+"/cancel"), nil)
	if err != nil {
		return EveCancelResult{}, fmt.Errorf("%w: build cancel request: %v", ErrEveLeafConfiguration, err)
	}
	request.Header.Set("Accept", "application/json")
	response, err := adapter.client.Do(request)
	if err != nil {
		return EveCancelResult{}, err
	}
	defer response.Body.Close()
	body, readErr := readBounded(response.Body, adapter.maxBodyBytes)
	result := EveCancelResult{StatusCode: response.StatusCode, ResponseBytes: body}
	if readErr != nil {
		return result, fmt.Errorf("%w: read cancel response: %v", ErrEveLeafProtocol, readErr)
	}
	if response.StatusCode < 200 || response.StatusCode >= 300 {
		return result, fmt.Errorf("%w: cancel status %d", ErrEveLeafProtocol, response.StatusCode)
	}
	return result, nil
}

func (adapter *EveLeafAdapter) endpoint(path string) string {
	copyURL := *adapter.baseURL
	copyURL.Path = path
	return copyURL.String()
}

func readBounded(reader io.Reader, limit int64) ([]byte, error) {
	if limit <= 0 {
		return nil, errors.New("positive body limit required")
	}
	body, err := io.ReadAll(io.LimitReader(reader, limit+1))
	if err != nil {
		return nil, err
	}
	if int64(len(body)) > limit {
		return nil, errors.New("body exceeds " + strconv.FormatInt(limit, 10) + " bytes")
	}
	return body, nil
}

func validNDJSONContentType(value string) bool {
	return value == "" || strings.HasPrefix(value, "application/x-ndjson") || strings.HasPrefix(value, "application/ndjson")
}
