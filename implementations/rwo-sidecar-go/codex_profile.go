package rwosidecar

import (
	"fmt"
	"sort"
)

const (
	codexProfileSchema       = "rwo.codex-contract-profile/v0"
	codexNamespaceSchema     = "rwo.codex-contract-namespace/v0"
	codexProfileID           = "codex-app-server-observation-v0"
	codexTransport           = "stdio-jsonl"
	codexJSONRPCVersion      = "2.0"
	codexProviderLaunch      = "forbidden"
	codexOutputPolicy        = "explicit-jsonrpc-result-or-error-only"
	codexUnknownMemberPolicy = "reject"
)

var codexRequiredCapabilities = map[string]struct{}{
	"interrupt-observation":  {},
	"permission-observation": {},
	"raw-wire-observation":   {},
}

var codexRequiredScenarios = map[string]string{
	"interrupted": "interrupted.jsonl",
	"namespace":   "namespace.json",
	"permission":  "permission.jsonl",
	"success":     "success.jsonl",
}

type codexContractError struct {
	Code     string
	Path     string
	Sequence int
	Detail   string
}

func (e *codexContractError) Error() string {
	location := e.Path
	if e.Sequence > 0 {
		location = fmt.Sprintf("%s:%d", location, e.Sequence)
	}
	if location == "" {
		return fmt.Sprintf("%s: %s", e.Code, e.Detail)
	}
	return fmt.Sprintf("%s at %s: %s", e.Code, location, e.Detail)
}

func codexError(code, path, detail string) error {
	return &codexContractError{Code: code, Path: path, Detail: detail}
}

type CodexContractProfile struct {
	SchemaVersion       string          `json:"schema_version"`
	ProfileID           string          `json:"profile_id"`
	Transport           string          `json:"transport"`
	JSONRPCVersion      string          `json:"jsonrpc_version"`
	NamespaceRef        string          `json:"namespace_ref"`
	ProviderLaunch      string          `json:"provider_launch"`
	OutputPolicy        string          `json:"output_policy"`
	UnknownMemberPolicy string          `json:"unknown_member_policy"`
	Capabilities        []string        `json:"capabilities"`
	Scenarios           []CodexScenario `json:"scenarios"`
}

type CodexScenario struct {
	Name string `json:"name"`
	Path string `json:"path"`
}

type CodexNamespace struct {
	SchemaVersion string                 `json:"schema_version"`
	Members       []CodexNamespaceMember `json:"members"`
	FieldOwners   []CodexFieldOwner      `json:"field_owners"`
}

type CodexNamespaceMember struct {
	Method    string `json:"method"`
	Direction string `json:"direction"`
	Kind      string `json:"kind"`
	Owner     string `json:"owner"`
}

type CodexFieldOwner struct {
	Pointer string `json:"pointer"`
	Owner   string `json:"owner"`
}

func validateCodexProfile(profile CodexContractProfile) error {
	checks := []struct {
		actual string
		expect string
		name   string
	}{
		{profile.SchemaVersion, codexProfileSchema, "schema_version"},
		{profile.ProfileID, codexProfileID, "profile_id"},
		{profile.Transport, codexTransport, "transport"},
		{profile.JSONRPCVersion, codexJSONRPCVersion, "jsonrpc_version"},
		{profile.NamespaceRef, "namespace.json", "namespace_ref"},
		{profile.ProviderLaunch, codexProviderLaunch, "provider_launch"},
		{profile.OutputPolicy, codexOutputPolicy, "output_policy"},
		{profile.UnknownMemberPolicy, codexUnknownMemberPolicy, "unknown_member_policy"},
	}
	for _, check := range checks {
		if check.actual != check.expect {
			return codexError("profile-contract-mismatch", "profile.json", fmt.Sprintf("%s must equal %q", check.name, check.expect))
		}
	}

	seenCapabilities := make(map[string]struct{}, len(profile.Capabilities))
	for _, capability := range profile.Capabilities {
		if _, supported := codexRequiredCapabilities[capability]; !supported {
			return codexError("capability-expansion", "profile.json", fmt.Sprintf("unsupported capability %q", capability))
		}
		if _, duplicate := seenCapabilities[capability]; duplicate {
			return codexError("duplicate-capability", "profile.json", capability)
		}
		seenCapabilities[capability] = struct{}{}
	}
	if len(seenCapabilities) != len(codexRequiredCapabilities) {
		return codexError("missing-capability", "profile.json", "profile must declare the exact private observation capability set")
	}

	seenScenarios := make(map[string]string, len(profile.Scenarios))
	for _, scenario := range profile.Scenarios {
		expectedPath, required := codexRequiredScenarios[scenario.Name]
		if !required || expectedPath != scenario.Path {
			return codexError("scenario-expansion", "profile.json", fmt.Sprintf("unexpected scenario binding %q -> %q", scenario.Name, scenario.Path))
		}
		if _, duplicate := seenScenarios[scenario.Name]; duplicate {
			return codexError("duplicate-scenario", "profile.json", scenario.Name)
		}
		seenScenarios[scenario.Name] = scenario.Path
	}
	if len(seenScenarios) != len(codexRequiredScenarios) {
		missing := make([]string, 0)
		for name := range codexRequiredScenarios {
			if _, present := seenScenarios[name]; !present {
				missing = append(missing, name)
			}
		}
		sort.Strings(missing)
		return codexError("missing-scenario", "profile.json", fmt.Sprintf("missing %v", missing))
	}
	return nil
}
