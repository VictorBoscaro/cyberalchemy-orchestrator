package rwosidecar

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

const (
	directionClientToServer = "client-to-server"
	directionServerToClient = "server-to-client"
)

type CodexContractReport struct {
	ProfileID           string
	NamespaceMembers    int
	WireScenarios       int
	WireMessages        int
	ExplicitResults     int
	ExplicitErrors      int
	UsedNamespaceMember int
}

type codexWireRecord struct {
	Sequence  int             `json:"sequence"`
	Direction string          `json:"direction"`
	Message   json.RawMessage `json:"message"`
}

type pendingCodexRequest struct {
	method string
	path   string
	line   int
}

type codexScenarioReport struct {
	messages        int
	explicitResults int
	explicitErrors  int
	usedMembers     map[string]struct{}
}

func LoadAndValidateCodexContractCapsule(root string) (CodexContractReport, error) {
	var profile CodexContractProfile
	if err := loadStrictJSON(filepath.Join(root, "profile.json"), &profile); err != nil {
		return CodexContractReport{}, err
	}
	if err := validateCodexProfile(profile); err != nil {
		return CodexContractReport{}, err
	}

	var namespace CodexNamespace
	if err := loadStrictJSON(filepath.Join(root, profile.NamespaceRef), &namespace); err != nil {
		return CodexContractReport{}, err
	}
	memberIndex, err := validateCodexNamespace(namespace)
	if err != nil {
		return CodexContractReport{}, err
	}

	scenarios := append([]CodexScenario(nil), profile.Scenarios...)
	sort.Slice(scenarios, func(i, j int) bool { return scenarios[i].Name < scenarios[j].Name })
	report := CodexContractReport{
		ProfileID:        profile.ProfileID,
		NamespaceMembers: len(namespace.Members),
	}
	usedMembers := make(map[string]struct{})
	for _, scenario := range scenarios {
		if scenario.Name == "namespace" {
			continue
		}
		scenarioReport, validateErr := validateCodexWireScenario(filepath.Join(root, scenario.Path), memberIndex)
		if validateErr != nil {
			return CodexContractReport{}, validateErr
		}
		report.WireScenarios++
		report.WireMessages += scenarioReport.messages
		report.ExplicitResults += scenarioReport.explicitResults
		report.ExplicitErrors += scenarioReport.explicitErrors
		for member := range scenarioReport.usedMembers {
			usedMembers[member] = struct{}{}
		}
	}
	if len(usedMembers) != len(memberIndex) {
		unused := make([]string, 0)
		for key := range memberIndex {
			if _, used := usedMembers[key]; !used {
				unused = append(unused, key)
			}
		}
		sort.Strings(unused)
		return CodexContractReport{}, codexError("capability-expansion", "namespace.json", fmt.Sprintf("namespace members without fixture evidence: %v", unused))
	}
	report.UsedNamespaceMember = len(usedMembers)
	return report, nil
}

func loadStrictJSON(path string, target any) error {
	payload, err := os.ReadFile(path)
	if err != nil {
		return codexError("fixture-read-failed", filepath.Base(path), err.Error())
	}
	decoder := json.NewDecoder(bytes.NewReader(payload))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(target); err != nil {
		return codexError("fixture-json-invalid", filepath.Base(path), err.Error())
	}
	if err := requireJSONEOF(decoder); err != nil {
		return codexError("fixture-json-invalid", filepath.Base(path), err.Error())
	}
	return nil
}

func requireJSONEOF(decoder *json.Decoder) error {
	var trailing any
	err := decoder.Decode(&trailing)
	if err == io.EOF {
		return nil
	}
	if err == nil {
		return fmt.Errorf("trailing JSON value")
	}
	return err
}

func validateCodexNamespace(namespace CodexNamespace) (map[string]CodexNamespaceMember, error) {
	if namespace.SchemaVersion != codexNamespaceSchema {
		return nil, codexError("namespace-contract-mismatch", "namespace.json", fmt.Sprintf("schema_version must equal %q", codexNamespaceSchema))
	}
	memberIndex := make(map[string]CodexNamespaceMember, len(namespace.Members))
	for _, member := range namespace.Members {
		if member.Method == "" || member.Owner == "" {
			return nil, codexError("namespace-member-invalid", "namespace.json", "method and owner are required")
		}
		if !validCodexDirection(member.Direction) {
			return nil, codexError("namespace-member-invalid", "namespace.json", fmt.Sprintf("invalid direction %q", member.Direction))
		}
		if member.Kind != "request" && member.Kind != "notification" {
			return nil, codexError("namespace-member-invalid", "namespace.json", fmt.Sprintf("invalid kind %q", member.Kind))
		}
		key := codexMemberKey(member.Direction, member.Method)
		if _, duplicate := memberIndex[key]; duplicate {
			return nil, codexError("duplicate-namespace-member", "namespace.json", key)
		}
		memberIndex[key] = member
	}
	if len(memberIndex) == 0 {
		return nil, codexError("missing-namespace-member", "namespace.json", "namespace is empty")
	}

	requiredPointers := map[string]struct{}{
		"/error": {}, "/id": {}, "/jsonrpc": {}, "/method": {}, "/params": {}, "/result": {},
	}
	owners := make(map[string]string, len(namespace.FieldOwners))
	for _, fieldOwner := range namespace.FieldOwners {
		if fieldOwner.Pointer == "" || fieldOwner.Owner == "" {
			return nil, codexError("field-owner-invalid", "namespace.json", "pointer and owner are required")
		}
		if previous, duplicate := owners[fieldOwner.Pointer]; duplicate {
			return nil, codexError("duplicate-owner-field", "namespace.json", fmt.Sprintf("%s owned by both %q and %q", fieldOwner.Pointer, previous, fieldOwner.Owner))
		}
		owners[fieldOwner.Pointer] = fieldOwner.Owner
	}
	for pointer := range requiredPointers {
		if _, present := owners[pointer]; !present {
			return nil, codexError("missing-owner-field", "namespace.json", pointer)
		}
	}
	return memberIndex, nil
}

func validateCodexWireScenario(path string, members map[string]CodexNamespaceMember) (codexScenarioReport, error) {
	handle, err := os.Open(path)
	if err != nil {
		return codexScenarioReport{}, codexError("fixture-read-failed", filepath.Base(path), err.Error())
	}
	defer handle.Close()

	report := codexScenarioReport{usedMembers: make(map[string]struct{})}
	pending := make(map[string]pendingCodexRequest)
	scanner := bufio.NewScanner(handle)
	scanner.Buffer(make([]byte, 64*1024), 1024*1024)
	expectedSequence := 1
	for scanner.Scan() {
		line := scanner.Bytes()
		if len(bytes.TrimSpace(line)) == 0 {
			return codexScenarioReport{}, &codexContractError{Code: "empty-wire-record", Path: filepath.Base(path), Sequence: expectedSequence, Detail: "blank JSONL records are forbidden"}
		}
		var record codexWireRecord
		decoder := json.NewDecoder(bytes.NewReader(line))
		decoder.DisallowUnknownFields()
		if err := decoder.Decode(&record); err != nil {
			return codexScenarioReport{}, &codexContractError{Code: "wire-record-invalid", Path: filepath.Base(path), Sequence: expectedSequence, Detail: err.Error()}
		}
		if err := requireJSONEOF(decoder); err != nil {
			return codexScenarioReport{}, &codexContractError{Code: "wire-record-invalid", Path: filepath.Base(path), Sequence: expectedSequence, Detail: err.Error()}
		}
		if record.Sequence != expectedSequence {
			return codexScenarioReport{}, &codexContractError{Code: "wire-sequence-invalid", Path: filepath.Base(path), Sequence: expectedSequence, Detail: fmt.Sprintf("got %d", record.Sequence)}
		}
		if !validCodexDirection(record.Direction) {
			return codexScenarioReport{}, &codexContractError{Code: "wire-direction-invalid", Path: filepath.Base(path), Sequence: expectedSequence, Detail: record.Direction}
		}
		if err := validateCodexWireMessage(filepath.Base(path), record, members, pending, &report); err != nil {
			return codexScenarioReport{}, err
		}
		report.messages++
		expectedSequence++
	}
	if err := scanner.Err(); err != nil {
		return codexScenarioReport{}, codexError("fixture-read-failed", filepath.Base(path), err.Error())
	}
	if report.messages == 0 {
		return codexScenarioReport{}, codexError("empty-wire-scenario", filepath.Base(path), "scenario has no messages")
	}
	if len(pending) != 0 {
		ids := make([]string, 0, len(pending))
		for id := range pending {
			ids = append(ids, id)
		}
		sort.Strings(ids)
		return codexScenarioReport{}, codexError("unresolved-request", filepath.Base(path), fmt.Sprintf("pending responses: %v", ids))
	}
	return report, nil
}

func validateCodexWireMessage(path string, record codexWireRecord, members map[string]CodexNamespaceMember, pending map[string]pendingCodexRequest, report *codexScenarioReport) error {
	var fields map[string]json.RawMessage
	if err := json.Unmarshal(record.Message, &fields); err != nil {
		return &codexContractError{Code: "wire-message-invalid", Path: path, Sequence: record.Sequence, Detail: err.Error()}
	}
	allowed := map[string]struct{}{
		"error": {}, "id": {}, "jsonrpc": {}, "method": {}, "params": {}, "result": {},
	}
	for field := range fields {
		if field == "output" || field == "inferred_output" {
			return &codexContractError{Code: "inferred-output", Path: path, Sequence: record.Sequence, Detail: fmt.Sprintf("field %q is forbidden", field)}
		}
		if _, known := allowed[field]; !known {
			return &codexContractError{Code: "unknown-wire-field", Path: path, Sequence: record.Sequence, Detail: field}
		}
	}
	var version string
	if raw, present := fields["jsonrpc"]; !present || json.Unmarshal(raw, &version) != nil || version != codexJSONRPCVersion {
		return &codexContractError{Code: "jsonrpc-version-invalid", Path: path, Sequence: record.Sequence, Detail: "jsonrpc must equal 2.0"}
	}
	methodRaw, hasMethod := fields["method"]
	idRaw, hasID := fields["id"]
	_, hasResult := fields["result"]
	_, hasError := fields["error"]

	if hasMethod {
		if hasResult || hasError {
			return &codexContractError{Code: "inferred-output", Path: path, Sequence: record.Sequence, Detail: "method messages cannot carry result or error"}
		}
		var method string
		if err := json.Unmarshal(methodRaw, &method); err != nil || method == "" {
			return &codexContractError{Code: "wire-method-invalid", Path: path, Sequence: record.Sequence, Detail: "method must be a non-empty string"}
		}
		memberKey := codexMemberKey(record.Direction, method)
		member, known := members[memberKey]
		if !known {
			return &codexContractError{Code: "missing-namespace-member", Path: path, Sequence: record.Sequence, Detail: memberKey}
		}
		report.usedMembers[memberKey] = struct{}{}
		if member.Kind == "request" && !hasID {
			return &codexContractError{Code: "request-id-missing", Path: path, Sequence: record.Sequence, Detail: method}
		}
		if member.Kind == "notification" && hasID {
			return &codexContractError{Code: "notification-id-forbidden", Path: path, Sequence: record.Sequence, Detail: method}
		}
		if hasID {
			id, err := canonicalCodexID(idRaw)
			if err != nil {
				return &codexContractError{Code: "request-id-invalid", Path: path, Sequence: record.Sequence, Detail: err.Error()}
			}
			responseKey := oppositeCodexDirection(record.Direction) + "\x00" + id
			if _, duplicate := pending[responseKey]; duplicate {
				return &codexContractError{Code: "duplicate-request-id", Path: path, Sequence: record.Sequence, Detail: id}
			}
			pending[responseKey] = pendingCodexRequest{method: method, path: path, line: record.Sequence}
		}
		return nil
	}

	if !hasID {
		return &codexContractError{Code: "response-id-missing", Path: path, Sequence: record.Sequence, Detail: "response has no id"}
	}
	if hasResult == hasError {
		return &codexContractError{Code: "response-output-invalid", Path: path, Sequence: record.Sequence, Detail: "response must carry exactly one explicit result or error"}
	}
	id, err := canonicalCodexID(idRaw)
	if err != nil {
		return &codexContractError{Code: "response-id-invalid", Path: path, Sequence: record.Sequence, Detail: err.Error()}
	}
	pendingKey := record.Direction + "\x00" + id
	if _, present := pending[pendingKey]; !present {
		return &codexContractError{Code: "unmatched-response", Path: path, Sequence: record.Sequence, Detail: id}
	}
	delete(pending, pendingKey)
	if hasResult {
		report.explicitResults++
	} else {
		report.explicitErrors++
	}
	return nil
}

func canonicalCodexID(raw json.RawMessage) (string, error) {
	trimmed := bytes.TrimSpace(raw)
	if len(trimmed) == 0 || bytes.Equal(trimmed, []byte("null")) {
		return "", fmt.Errorf("id must be a string or number")
	}
	var scalar any
	decoder := json.NewDecoder(bytes.NewReader(trimmed))
	decoder.UseNumber()
	if err := decoder.Decode(&scalar); err != nil {
		return "", err
	}
	switch scalar.(type) {
	case string, json.Number:
	default:
		return "", fmt.Errorf("id must be a string or number")
	}
	buffer := new(bytes.Buffer)
	if err := json.Compact(buffer, trimmed); err != nil {
		return "", err
	}
	return buffer.String(), nil
}

func validCodexDirection(direction string) bool {
	return direction == directionClientToServer || direction == directionServerToClient
}

func oppositeCodexDirection(direction string) string {
	if direction == directionClientToServer {
		return directionServerToClient
	}
	return directionClientToServer
}

func codexMemberKey(direction, method string) string {
	return strings.Join([]string{direction, method}, "\x00")
}
