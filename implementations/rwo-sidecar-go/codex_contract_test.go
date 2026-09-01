package rwosidecar

import (
	"encoding/json"
	"errors"
	"os"
	"testing"
)

func TestCodexContractCapsule(t *testing.T) {
	t.Run("accepts exact provider-inert fixture capsule", func(t *testing.T) {
		fixtureRoot := os.Getenv("RWO_CODEX_CONTRACT_FIXTURE_ROOT")
		if fixtureRoot == "" {
			fixtureRoot = "testdata/codex-contract-v0"
		}
		report, err := LoadAndValidateCodexContractCapsule(fixtureRoot)
		if err != nil {
			t.Fatalf("validate capsule: %v", err)
		}
		if report.ProfileID != codexProfileID {
			t.Fatalf("profile id = %q, want %q", report.ProfileID, codexProfileID)
		}
		if report.NamespaceMembers != 7 || report.UsedNamespaceMember != 7 {
			t.Fatalf("namespace counts = declared %d used %d, want 7/7", report.NamespaceMembers, report.UsedNamespaceMember)
		}
		if report.WireScenarios != 3 || report.WireMessages != 13 {
			t.Fatalf("wire counts = scenarios %d messages %d, want 3/13", report.WireScenarios, report.WireMessages)
		}
		if report.ExplicitResults != 5 || report.ExplicitErrors != 0 {
			t.Fatalf("explicit outputs = results %d errors %d, want 5/0", report.ExplicitResults, report.ExplicitErrors)
		}
	})

	t.Run("rejects capability expansion", func(t *testing.T) {
		profile := exactTestCodexProfile()
		profile.Capabilities = append(profile.Capabilities, "source-mutation")
		assertCodexErrorCode(t, validateCodexProfile(profile), "capability-expansion")
	})

	t.Run("rejects duplicate owner field", func(t *testing.T) {
		namespace := exactTestCodexNamespace()
		namespace.FieldOwners = append(namespace.FieldOwners, CodexFieldOwner{Pointer: "/result", Owner: "another-owner"})
		_, err := validateCodexNamespace(namespace)
		assertCodexErrorCode(t, err, "duplicate-owner-field")
	})

	t.Run("rejects missing namespace member", func(t *testing.T) {
		record := codexWireRecord{
			Sequence:  1,
			Direction: directionClientToServer,
			Message:   json.RawMessage(`{"jsonrpc":"2.0","id":"x","method":"thread/unknown","params":{}}`),
		}
		report := codexScenarioReport{usedMembers: make(map[string]struct{})}
		err := validateCodexWireMessage("negative.jsonl", record, map[string]CodexNamespaceMember{}, map[string]pendingCodexRequest{}, &report)
		assertCodexErrorCode(t, err, "missing-namespace-member")
	})

	t.Run("rejects inferred output", func(t *testing.T) {
		record := codexWireRecord{
			Sequence:  1,
			Direction: directionServerToClient,
			Message:   json.RawMessage(`{"jsonrpc":"2.0","id":"x","output":{"text":"not explicit result"}}`),
		}
		report := codexScenarioReport{usedMembers: make(map[string]struct{})}
		err := validateCodexWireMessage("negative.jsonl", record, map[string]CodexNamespaceMember{}, map[string]pendingCodexRequest{}, &report)
		assertCodexErrorCode(t, err, "inferred-output")
	})
}

func assertCodexErrorCode(t *testing.T, err error, expected string) {
	t.Helper()
	if err == nil {
		t.Fatalf("expected %s error", expected)
	}
	var contractErr *codexContractError
	if !errors.As(err, &contractErr) {
		t.Fatalf("error type = %T, want *codexContractError: %v", err, err)
	}
	if contractErr.Code != expected {
		t.Fatalf("error code = %q, want %q: %v", contractErr.Code, expected, err)
	}
}

func exactTestCodexProfile() CodexContractProfile {
	return CodexContractProfile{
		SchemaVersion:       codexProfileSchema,
		ProfileID:           codexProfileID,
		Transport:           codexTransport,
		JSONRPCVersion:      codexJSONRPCVersion,
		NamespaceRef:        "namespace.json",
		ProviderLaunch:      codexProviderLaunch,
		OutputPolicy:        codexOutputPolicy,
		UnknownMemberPolicy: codexUnknownMemberPolicy,
		Capabilities: []string{
			"interrupt-observation",
			"permission-observation",
			"raw-wire-observation",
		},
		Scenarios: []CodexScenario{
			{Name: "interrupted", Path: "interrupted.jsonl"},
			{Name: "namespace", Path: "namespace.json"},
			{Name: "permission", Path: "permission.jsonl"},
			{Name: "success", Path: "success.jsonl"},
		},
	}
}

func exactTestCodexNamespace() CodexNamespace {
	return CodexNamespace{
		SchemaVersion: codexNamespaceSchema,
		Members: []CodexNamespaceMember{
			{Method: "initialize", Direction: directionClientToServer, Kind: "request", Owner: "codex-app-server-protocol"},
		},
		FieldOwners: []CodexFieldOwner{
			{Pointer: "/error", Owner: "json-rpc-envelope"},
			{Pointer: "/id", Owner: "json-rpc-envelope"},
			{Pointer: "/jsonrpc", Owner: "json-rpc-envelope"},
			{Pointer: "/method", Owner: "codex-app-server-protocol"},
			{Pointer: "/params", Owner: "codex-app-server-protocol"},
			{Pointer: "/result", Owner: "json-rpc-envelope"},
		},
	}
}
