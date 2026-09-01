package rwosidecar

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"unicode/utf8"
)

const (
	SeatMaterialSchemaV1 = "rwo.seat-manifest/v1"
	SeatAddressPrefix    = "seatv1/sha256/"
)

var (
	ErrSeatMaterialAddress     = errors.New("invalid RWO seat material address")
	ErrSeatMaterialDrift       = errors.New("RWO seat material digest drift")
	ErrSeatMaterialPath        = errors.New("RWO seat material path escapes the allowed root")
	ErrSeatMaterialSchema      = errors.New("invalid RWO seat material schema")
	ErrSeatMaterialPolicy      = errors.New("RWO seat material policy is not tool-free")
	ErrSeatMaterialCorrelation = errors.New("RWO seat material does not match the command target")
	ErrEveCommand              = errors.New("invalid ExecuteBoundedSeat command")
	ErrEveRequestPolicy        = errors.New("invalid Eve task request policy")
)

var seatAddressPattern = regexp.MustCompile(`^seatv1/sha256/([0-9a-f]{64})$`)

// SeatCapabilityPolicy is deliberately closed. The local leaf has no
// capability that can be enabled by omission or an unrecognized extension.
type SeatCapabilityPolicy struct {
	AgentTool        bool `json:"agent_tool"`
	ArbitraryNetwork bool `json:"arbitrary_network"`
	Connections      bool `json:"connections"`
	Delegation       bool `json:"delegation"`
	RequestInput     bool `json:"request_input"`
	Schedules        bool `json:"schedules"`
	Shell            bool `json:"shell"`
	Web              bool `json:"web"`
	Workflow         bool `json:"workflow"`
	Write            bool `json:"write"`
}

func (policy *SeatCapabilityPolicy) UnmarshalJSON(encoded []byte) error {
	var wire struct {
		AgentTool        *bool `json:"agent_tool"`
		ArbitraryNetwork *bool `json:"arbitrary_network"`
		Connections      *bool `json:"connections"`
		Delegation       *bool `json:"delegation"`
		RequestInput     *bool `json:"request_input"`
		Schedules        *bool `json:"schedules"`
		Shell            *bool `json:"shell"`
		Web              *bool `json:"web"`
		Workflow         *bool `json:"workflow"`
		Write            *bool `json:"write"`
	}
	if err := decodeClosedJSON(encoded, &wire); err != nil {
		return err
	}
	if wire.AgentTool == nil || wire.ArbitraryNetwork == nil || wire.Connections == nil ||
		wire.Delegation == nil || wire.RequestInput == nil || wire.Schedules == nil ||
		wire.Shell == nil || wire.Web == nil || wire.Workflow == nil || wire.Write == nil {
		return errors.New("all ten capability-policy members are required")
	}
	*policy = SeatCapabilityPolicy{
		AgentTool: *wire.AgentTool, ArbitraryNetwork: *wire.ArbitraryNetwork,
		Connections: *wire.Connections, Delegation: *wire.Delegation,
		RequestInput: *wire.RequestInput, Schedules: *wire.Schedules,
		Shell: *wire.Shell, Web: *wire.Web, Workflow: *wire.Workflow, Write: *wire.Write,
	}
	return nil
}

func (policy SeatCapabilityPolicy) disabled() bool {
	return !policy.AgentTool && !policy.ArbitraryNetwork && !policy.Connections &&
		!policy.Delegation && !policy.RequestInput && !policy.Schedules &&
		!policy.Shell && !policy.Web && !policy.Workflow && !policy.Write
}

// SeatManifest is the complete physical material contract for the selected
// one-seat prototype. It is not a scheduler input and cannot select a graph
// successor.
type SeatManifest struct {
	SchemaVersion        string               `json:"schema_version"`
	SeatID               string               `json:"seat_id"`
	Role                 string               `json:"role"`
	Prompt               string               `json:"prompt"`
	InputManifestSHA256  string               `json:"input_manifest_sha256"`
	MountedReadOnlyPaths []string             `json:"mounted_read_only_paths"`
	OutputSchemaPath     string               `json:"output_schema_path"`
	OutputSchemaSHA256   string               `json:"output_schema_sha256"`
	MaxOutputBytes       uint64               `json:"max_output_bytes"`
	TimeoutMilliseconds  uint64               `json:"timeout_milliseconds"`
	MaxToolCalls         uint64               `json:"max_tool_calls"`
	CapabilityPolicy     SeatCapabilityPolicy `json:"capability_policy"`
}

func (manifest *SeatManifest) UnmarshalJSON(encoded []byte) error {
	var wire struct {
		SchemaVersion        string                `json:"schema_version"`
		SeatID               string                `json:"seat_id"`
		Role                 string                `json:"role"`
		Prompt               string                `json:"prompt"`
		InputManifestSHA256  string                `json:"input_manifest_sha256"`
		MountedReadOnlyPaths []string              `json:"mounted_read_only_paths"`
		OutputSchemaPath     string                `json:"output_schema_path"`
		OutputSchemaSHA256   string                `json:"output_schema_sha256"`
		MaxOutputBytes       *uint64               `json:"max_output_bytes"`
		TimeoutMilliseconds  *uint64               `json:"timeout_milliseconds"`
		MaxToolCalls         *uint64               `json:"max_tool_calls"`
		CapabilityPolicy     *SeatCapabilityPolicy `json:"capability_policy"`
	}
	if err := decodeClosedJSON(encoded, &wire); err != nil {
		return err
	}
	if wire.MaxOutputBytes == nil || wire.TimeoutMilliseconds == nil || wire.MaxToolCalls == nil || wire.CapabilityPolicy == nil {
		return errors.New("all bounded and capability fields are required")
	}
	*manifest = SeatManifest{
		SchemaVersion: wire.SchemaVersion, SeatID: wire.SeatID, Role: wire.Role, Prompt: wire.Prompt,
		InputManifestSHA256: wire.InputManifestSHA256, MountedReadOnlyPaths: wire.MountedReadOnlyPaths,
		OutputSchemaPath: wire.OutputSchemaPath, OutputSchemaSHA256: wire.OutputSchemaSHA256,
		MaxOutputBytes: *wire.MaxOutputBytes, TimeoutMilliseconds: *wire.TimeoutMilliseconds,
		MaxToolCalls: *wire.MaxToolCalls, CapabilityPolicy: *wire.CapabilityPolicy,
	}
	return nil
}

type SeatMaterialBinding struct {
	Address      string
	RelativePath string
}

// ResolvedSeatMaterial carries exact bytes so later layers do not need to
// re-open mutable filenames after resolution.
type ResolvedSeatMaterial struct {
	Address           string
	ManifestPath      string
	ManifestBytes     []byte
	Manifest          SeatManifest
	MountedInputBytes [][]byte
	OutputSchemaBytes []byte
	PolicySHA256      string
}

type SeatMaterialCatalog struct {
	root     string
	bindings map[string]string
}

func NewSeatMaterialCatalog(root string, bindings []SeatMaterialBinding) (*SeatMaterialCatalog, error) {
	if root == "" || len(bindings) == 0 {
		return nil, fmt.Errorf("%w: allowed root and at least one binding are required", ErrSeatMaterialSchema)
	}
	absRoot, err := filepath.Abs(root)
	if err != nil {
		return nil, fmt.Errorf("%w: %v", ErrSeatMaterialPath, err)
	}
	realRoot, err := filepath.EvalSymlinks(absRoot)
	if err != nil {
		return nil, fmt.Errorf("%w: resolve allowed root: %v", ErrSeatMaterialPath, err)
	}
	info, err := os.Stat(realRoot)
	if err != nil || !info.IsDir() {
		return nil, fmt.Errorf("%w: allowed root must be an existing directory", ErrSeatMaterialPath)
	}

	catalog := &SeatMaterialCatalog{root: realRoot, bindings: make(map[string]string, len(bindings))}
	for _, binding := range bindings {
		if !seatAddressPattern.MatchString(binding.Address) {
			return nil, fmt.Errorf("%w: %q", ErrSeatMaterialAddress, binding.Address)
		}
		if _, exists := catalog.bindings[binding.Address]; exists {
			return nil, fmt.Errorf("%w: duplicate binding for %q", ErrSeatMaterialAddress, binding.Address)
		}
		if err := validateRelativeMaterialPath(binding.RelativePath); err != nil {
			return nil, err
		}
		catalog.bindings[binding.Address] = binding.RelativePath
	}
	return catalog, nil
}

func (catalog *SeatMaterialCatalog) Resolve(address, expectedSeatID string) (ResolvedSeatMaterial, error) {
	if catalog == nil || expectedSeatID == "" {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: catalog and expected seat are required", ErrSeatMaterialCorrelation)
	}
	match := seatAddressPattern.FindStringSubmatch(address)
	if match == nil {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: %q", ErrSeatMaterialAddress, address)
	}
	relativeManifest, exists := catalog.bindings[address]
	if !exists {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: address is not configured", ErrSeatMaterialAddress)
	}
	manifestPath, manifestBytes, err := catalog.readBoundedFile(relativeManifest)
	if err != nil {
		return ResolvedSeatMaterial{}, err
	}
	if digestHex(manifestBytes) != match[1] {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: manifest bytes do not match %s", ErrSeatMaterialDrift, address)
	}

	var manifest SeatManifest
	if err := decodeClosedJSON(manifestBytes, &manifest); err != nil {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: manifest: %v", ErrSeatMaterialSchema, err)
	}
	if err := validateSeatManifest(manifest, expectedSeatID); err != nil {
		return ResolvedSeatMaterial{}, err
	}

	inputs := make([][]byte, 0, len(manifest.MountedReadOnlyPaths))
	for _, inputPath := range manifest.MountedReadOnlyPaths {
		_, inputBytes, readErr := catalog.readBoundedFile(inputPath)
		if readErr != nil {
			return ResolvedSeatMaterial{}, readErr
		}
		inputs = append(inputs, inputBytes)
	}
	// The selected prototype has exactly one mounted input. That makes the
	// declared input digest unambiguous instead of inventing a multi-file hash.
	if len(inputs) != 1 || "sha256:"+digestHex(inputs[0]) != manifest.InputManifestSHA256 {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: mounted input bytes do not match input_manifest_sha256", ErrSeatMaterialDrift)
	}

	_, outputSchema, err := catalog.readBoundedFile(manifest.OutputSchemaPath)
	if err != nil {
		return ResolvedSeatMaterial{}, err
	}
	if "sha256:"+digestHex(outputSchema) != manifest.OutputSchemaSHA256 {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: output schema bytes do not match output_schema_sha256", ErrSeatMaterialDrift)
	}
	if !json.Valid(outputSchema) {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: output schema is not JSON", ErrSeatMaterialSchema)
	}
	policyBytes, err := json.Marshal(manifest.CapabilityPolicy)
	if err != nil {
		return ResolvedSeatMaterial{}, fmt.Errorf("%w: encode capability policy: %v", ErrSeatMaterialSchema, err)
	}

	return ResolvedSeatMaterial{
		Address: address, ManifestPath: manifestPath, ManifestBytes: bytes.Clone(manifestBytes), Manifest: manifest,
		MountedInputBytes: cloneByteSlices(inputs), OutputSchemaBytes: bytes.Clone(outputSchema),
		PolicySHA256: "sha256:" + digestHex(policyBytes),
	}, nil
}

func validateSeatManifest(manifest SeatManifest, expectedSeatID string) error {
	if manifest.SchemaVersion != SeatMaterialSchemaV1 || manifest.SeatID == "" ||
		manifest.Role == "" || manifest.Prompt == "" || !utf8.ValidString(manifest.Role) ||
		!utf8.ValidString(manifest.Prompt) || manifest.MaxOutputBytes == 0 ||
		manifest.TimeoutMilliseconds == 0 || len(manifest.MountedReadOnlyPaths) != 1 ||
		manifest.OutputSchemaPath == "" || !isTaggedSHA256(manifest.InputManifestSHA256) ||
		!isTaggedSHA256(manifest.OutputSchemaSHA256) {
		return fmt.Errorf("%w: incomplete or unsupported one-seat manifest", ErrSeatMaterialSchema)
	}
	if manifest.SeatID != expectedSeatID {
		return fmt.Errorf("%w: manifest seat %q, command target %q", ErrSeatMaterialCorrelation, manifest.SeatID, expectedSeatID)
	}
	if manifest.MaxToolCalls != 0 || !manifest.CapabilityPolicy.disabled() {
		return fmt.Errorf("%w: max_tool_calls must be zero and all ten capabilities false", ErrSeatMaterialPolicy)
	}
	for _, path := range append(append([]string(nil), manifest.MountedReadOnlyPaths...), manifest.OutputSchemaPath) {
		if err := validateRelativeMaterialPath(path); err != nil {
			return err
		}
	}
	return nil
}

func validateRelativeMaterialPath(path string) error {
	if path == "" || filepath.IsAbs(path) || filepath.Clean(path) != path || path == "." ||
		strings.HasPrefix(path, ".."+string(filepath.Separator)) || path == ".." {
		return fmt.Errorf("%w: %q", ErrSeatMaterialPath, path)
	}
	return nil
}

func (catalog *SeatMaterialCatalog) readBoundedFile(relative string) (string, []byte, error) {
	if err := validateRelativeMaterialPath(relative); err != nil {
		return "", nil, err
	}
	candidate := filepath.Join(catalog.root, relative)
	realPath, err := filepath.EvalSymlinks(candidate)
	if err != nil {
		return "", nil, fmt.Errorf("%w: resolve %q: %v", ErrSeatMaterialPath, relative, err)
	}
	rel, err := filepath.Rel(catalog.root, realPath)
	if err != nil || rel == ".." || strings.HasPrefix(rel, ".."+string(filepath.Separator)) || filepath.IsAbs(rel) {
		return "", nil, fmt.Errorf("%w: %q", ErrSeatMaterialPath, relative)
	}
	info, err := os.Stat(realPath)
	if err != nil || !info.Mode().IsRegular() {
		return "", nil, fmt.Errorf("%w: %q is not a regular file", ErrSeatMaterialPath, relative)
	}
	content, err := os.ReadFile(realPath)
	if err != nil {
		return "", nil, fmt.Errorf("%w: read %q: %v", ErrSeatMaterialPath, relative, err)
	}
	return realPath, content, nil
}

// ExecuteBoundedSeatCommand mirrors the Rust-emitted closed CommandIntent
// shape for this adapter only. Unknown fields are rejected.
type ExecuteBoundedSeatCommand struct {
	ContractID            string                    `json:"contract_id"`
	ContractVersion       string                    `json:"contract_version"`
	ProfileID             string                    `json:"profile_id"`
	ProfileVersion        string                    `json:"profile_version"`
	SchemaID              string                    `json:"schema_id"`
	SchemaVersion         string                    `json:"schema_version"`
	GraphIdentity         string                    `json:"graph_identity"`
	EdgeID                string                    `json:"edge_id"`
	AcceptedEventIdentity string                    `json:"accepted_event_identity"`
	CommandType           string                    `json:"command_type"`
	TargetNodeID          string                    `json:"target_node_id"`
	Payload               ExecuteBoundedSeatPayload `json:"payload"`
}

type ExecuteBoundedSeatPayload struct {
	JobID string `json:"job_id"`
}

func DecodeExecuteBoundedSeatCommand(raw []byte) (ExecuteBoundedSeatCommand, error) {
	var command ExecuteBoundedSeatCommand
	if err := decodeClosedJSON(raw, &command); err != nil {
		return command, fmt.Errorf("%w: %v", ErrEveCommand, err)
	}
	if command.ContractID == "" || command.ContractVersion == "" || command.ProfileID == "" ||
		command.ProfileVersion == "" || command.SchemaID != "CommandIntent" || command.SchemaVersion == "" ||
		!isTaggedSHA256(command.GraphIdentity) || !isTaggedSHA256(command.AcceptedEventIdentity) ||
		command.EdgeID == "" || command.CommandType != "ExecuteBoundedSeat" || command.TargetNodeID == "" ||
		!seatAddressPattern.MatchString(command.Payload.JobID) {
		return command, fmt.Errorf("%w: closed ExecuteBoundedSeat fields are required", ErrEveCommand)
	}
	return command, nil
}

type EveRequestCapabilities struct {
	RequestInput bool `json:"requestInput"`
}

func (capabilities *EveRequestCapabilities) UnmarshalJSON(encoded []byte) error {
	var wire struct {
		RequestInput *bool `json:"requestInput"`
	}
	if err := decodeClosedJSON(encoded, &wire); err != nil {
		return err
	}
	if wire.RequestInput == nil {
		return errors.New("requestInput is required")
	}
	capabilities.RequestInput = *wire.RequestInput
	return nil
}

type EveTaskClientContext struct {
	CommandIntentIdentity string `json:"rwoCommandIntentIdentity"`
	AttemptID             string `json:"rwoAttemptId"`
	SendTryOrdinal        uint64 `json:"rwoSendTryOrdinal"`
	SeatMaterialAddress   string `json:"rwoSeatMaterialAddress"`
	TargetNodeID          string `json:"rwoTargetNodeId"`
	InputManifestSHA256   string `json:"rwoInputManifestSha256"`
	OutputSchemaSHA256    string `json:"rwoOutputSchemaSha256"`
	PolicySHA256          string `json:"rwoPolicySha256"`
}

type EveTaskRequest struct {
	Message       string                 `json:"message"`
	Mode          string                 `json:"mode"`
	OutputSchema  json.RawMessage        `json:"outputSchema"`
	Capabilities  EveRequestCapabilities `json:"capabilities"`
	ClientContext EveTaskClientContext   `json:"clientContext"`
}

type PreparedEveTaskRequest struct {
	Command            ExecuteBoundedSeatCommand
	Material           ResolvedSeatMaterial
	Request            EveTaskRequest
	RequestBytes       []byte
	RequestFingerprint string
	RequestSHA256      string
}

func PrepareEveTaskRequest(commandBytes []byte, commandIdentity, attemptID string, sendTryOrdinal uint64, catalog *SeatMaterialCatalog) (PreparedEveTaskRequest, error) {
	if !isTaggedSHA256(commandIdentity) || attemptID == "" || sendTryOrdinal == 0 || catalog == nil {
		return PreparedEveTaskRequest{}, fmt.Errorf("%w: command identity, attempt, send try, and catalog are required", ErrEveCommand)
	}
	command, err := DecodeExecuteBoundedSeatCommand(commandBytes)
	if err != nil {
		return PreparedEveTaskRequest{}, err
	}
	material, err := catalog.Resolve(command.Payload.JobID, command.TargetNodeID)
	if err != nil {
		return PreparedEveTaskRequest{}, err
	}
	request := EveTaskRequest{
		Message: commandMessage(material.Manifest), Mode: "task", OutputSchema: bytes.Clone(material.OutputSchemaBytes),
		Capabilities: EveRequestCapabilities{RequestInput: false},
		ClientContext: EveTaskClientContext{
			CommandIntentIdentity: commandIdentity, AttemptID: attemptID, SendTryOrdinal: sendTryOrdinal,
			SeatMaterialAddress: material.Address, TargetNodeID: command.TargetNodeID,
			InputManifestSHA256: material.Manifest.InputManifestSHA256,
			OutputSchemaSHA256:  material.Manifest.OutputSchemaSHA256, PolicySHA256: material.PolicySHA256,
		},
	}
	requestBytes, err := json.Marshal(request)
	if err != nil {
		return PreparedEveTaskRequest{}, fmt.Errorf("%w: encode request: %v", ErrEveRequestPolicy, err)
	}
	if err := ValidateEveTaskRequest(requestBytes); err != nil {
		return PreparedEveTaskRequest{}, err
	}
	contextBytes, _ := json.Marshal(request.ClientContext)
	fingerprintInput := "RWO-EVE-REQUEST-V1\x00" + commandIdentity + attemptID + strconv.FormatUint(sendTryOrdinal, 10) +
		string(requestBytes) + material.Manifest.OutputSchemaSHA256 + material.PolicySHA256 +
		material.Manifest.InputManifestSHA256 + string(contextBytes)
	return PreparedEveTaskRequest{
		Command: command, Material: material, Request: request, RequestBytes: bytes.Clone(requestBytes),
		RequestFingerprint: digestHex([]byte(fingerprintInput)), RequestSHA256: digestHex(requestBytes),
	}, nil
}

func commandMessage(manifest SeatManifest) string {
	return "Role: " + manifest.Role + "\n\n" + manifest.Prompt
}

// ValidateEveTaskRequest is called immediately before transport. Enabling a
// capability or adding a tool/workflow/callback field is an error, not a field
// the adapter may silently discard.
func ValidateEveTaskRequest(raw []byte) error {
	var wire struct {
		Message       string                  `json:"message"`
		Mode          string                  `json:"mode"`
		OutputSchema  *json.RawMessage        `json:"outputSchema"`
		Capabilities  *EveRequestCapabilities `json:"capabilities"`
		ClientContext *EveTaskClientContext   `json:"clientContext"`
	}
	if err := decodeClosedJSON(raw, &wire); err != nil {
		return fmt.Errorf("%w: %v", ErrEveRequestPolicy, err)
	}
	if wire.OutputSchema == nil || wire.Capabilities == nil || wire.ClientContext == nil {
		return fmt.Errorf("%w: outputSchema, capabilities, and clientContext are required", ErrEveRequestPolicy)
	}
	request := EveTaskRequest{
		Message: wire.Message, Mode: wire.Mode, OutputSchema: *wire.OutputSchema,
		Capabilities: *wire.Capabilities, ClientContext: *wire.ClientContext,
	}
	policyBytes, _ := json.Marshal(SeatCapabilityPolicy{})
	expectedPolicySHA256 := "sha256:" + digestHex(policyBytes)
	if request.Mode != "task" || request.Message == "" || !utf8.ValidString(request.Message) ||
		request.Capabilities.RequestInput || !json.Valid(request.OutputSchema) ||
		!isTaggedSHA256(request.ClientContext.CommandIntentIdentity) || request.ClientContext.AttemptID == "" ||
		request.ClientContext.SendTryOrdinal == 0 || !seatAddressPattern.MatchString(request.ClientContext.SeatMaterialAddress) ||
		request.ClientContext.TargetNodeID == "" || !isTaggedSHA256(request.ClientContext.InputManifestSHA256) ||
		!isTaggedSHA256(request.ClientContext.OutputSchemaSHA256) || request.ClientContext.PolicySHA256 != expectedPolicySHA256 {
		return fmt.Errorf("%w: exact task fields and disabled requestInput are required", ErrEveRequestPolicy)
	}
	return nil
}

func cloneByteSlices(values [][]byte) [][]byte {
	cloned := make([][]byte, len(values))
	for index := range values {
		cloned[index] = bytes.Clone(values[index])
	}
	return cloned
}
