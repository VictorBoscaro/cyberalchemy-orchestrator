package rwosidecar

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func localContractRoot(t *testing.T) string {
	t.Helper()
	return filepath.Join("..", "..", "docs", "features", "recursive-work-orchestrator", "development", "decision-gates", "20260807T173437Z-rwo-language-contract-v2")
}

func childExecutable(t *testing.T) string {
	t.Helper()
	path := os.Getenv("RWO_KERNEL_CHILD")
	if path == "" {
		t.Skip("set RWO_KERNEL_CHILD to exercise the real local Rust child")
	}
	return path
}

func localManifest(t *testing.T) map[string]any {
	t.Helper()
	bytes, err := os.ReadFile(filepath.Join(localContractRoot(t), "vectors", "CONFORMANCE-MANIFEST.json"))
	if err != nil {
		t.Fatal(err)
	}
	var document map[string]any
	if err := json.Unmarshal(bytes, &document); err != nil {
		t.Fatal(err)
	}
	return document
}

func localFixture(t *testing.T, manifest map[string]any, name string) map[string]any {
	t.Helper()
	fixtures := manifest["fixtures"].(map[string]any)
	return fixtures[name].(map[string]any)
}

func rawFixture(t *testing.T, fixture map[string]any) []byte {
	t.Helper()
	bytes, err := json.Marshal(fixture)
	if err != nil {
		t.Fatal(err)
	}
	return bytes
}

func tupleForFixture(fixture map[string]any, valueType string) VersionTuple {
	return VersionTuple{
		ContractID: fixture["contract_id"].(string), ContractVersion: fixture["contract_version"].(string),
		ProfileID: fixture["profile_id"].(string), ProfileVersion: fixture["profile_version"].(string),
		SchemaID: fixture["schema_id"].(string), SchemaVersion: fixture["schema_version"].(string), ValueType: valueType,
	}
}

func startFixtureChild(t *testing.T) *ChildKernel {
	t.Helper()
	child, err := StartChildKernel(ChildKernelConfig{
		ExecutablePath: childExecutable(t),
		RegistryPath:   filepath.Join(localContractRoot(t), "schemas", "registry.json"),
		MaxFrameBytes:  1 << 20,
	})
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := child.Close(); err != nil {
			t.Errorf("close child: %v", err)
		}
	})
	return child
}

func TestChildKernelCompilesAndReducesThroughPrivateFraming(t *testing.T) {
	manifest := localManifest(t)
	composition := localFixture(t, manifest, "explicitComposition")
	event := localFixture(t, manifest, "matchingEvent")
	child := startFixtureChild(t)

	compiled, err := child.Compile(context.Background(), CompileRequest{
		Tuple: tupleForFixture(composition, "ExplicitComposition"), RawComposition: rawFixture(t, composition),
	})
	if err != nil {
		t.Fatal(err)
	}
	if compiled.Outcome != "Compiled" || compiled.GraphHandle == "" || compiled.GraphIdentity == "" {
		t.Fatalf("unexpected compilation: %#v", compiled)
	}
	first, err := child.ReduceCompiled(context.Background(), compiled.GraphHandle, nil, KernelRequest{
		Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, event),
	})
	if err != nil {
		t.Fatal(err)
	}
	if first.Outcome != "Applied" || first.ValidatedStreamID != "stream-1" || len(first.NextCursor) == 0 || len(first.CommandIntent) == 0 {
		t.Fatalf("unexpected first reduction: %#v", first)
	}
	duplicate, err := child.ReduceCompiled(context.Background(), compiled.GraphHandle, first.NextCursor, KernelRequest{
		Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "stream-1", RawAcceptedEvent: rawFixture(t, event),
	})
	if err != nil {
		t.Fatal(err)
	}
	if duplicate.Outcome != "Duplicate" || string(duplicate.NextCursor) != string(first.NextCursor) || len(duplicate.CommandIntent) != 0 {
		t.Fatalf("unexpected duplicate reduction: %#v", duplicate)
	}
}

func TestChildKernelPreservesSemanticRejectionWithoutHostCommitSignal(t *testing.T) {
	manifest := localManifest(t)
	composition := localFixture(t, manifest, "explicitComposition")
	event := localFixture(t, manifest, "matchingEvent")
	child := startFixtureChild(t)
	compiled, err := child.Compile(context.Background(), CompileRequest{
		Tuple: tupleForFixture(composition, "ExplicitComposition"), RawComposition: rawFixture(t, composition),
	})
	if err != nil {
		t.Fatal(err)
	}
	rejected, err := child.ReduceCompiled(context.Background(), compiled.GraphHandle, nil, KernelRequest{
		Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "wrong-stream", RawAcceptedEvent: rawFixture(t, event),
	})
	if err != nil {
		t.Fatal(err)
	}
	if rejected.Outcome != "Rejected" || len(rejected.CommandIntent) != 0 || len(rejected.DefectCodes) != 1 || rejected.DefectCodes[0] != "STREAM_ID_MISMATCH" {
		t.Fatalf("unexpected stream-hint rejection: %#v", rejected)
	}
}
