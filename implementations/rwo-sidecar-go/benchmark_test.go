package rwosidecar

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

// BenchmarkLocalRuntime is a single-host, single-child baseline only. It does
// not establish production throughput, an ABI decision, persistence, or any
// effect-delivery property. Run it explicitly with RWO_KERNEL_CHILD set.
func BenchmarkLocalRuntime(b *testing.B) {
	path := os.Getenv("RWO_KERNEL_CHILD")
	if path == "" {
		b.Skip("set RWO_KERNEL_CHILD to benchmark the local Rust child")
	}
	contractRoot := filepath.Join("..", "..", "docs", "features", "recursive-work-orchestrator", "development", "decision-gates", "20260807T173437Z-rwo-language-contract-v2")
	manifestBytes, err := os.ReadFile(filepath.Join(contractRoot, "vectors", "CONFORMANCE-MANIFEST.json"))
	if err != nil {
		b.Fatal(err)
	}
	var manifest map[string]any
	if err := json.Unmarshal(manifestBytes, &manifest); err != nil {
		b.Fatal(err)
	}
	fixtures := manifest["fixtures"].(map[string]any)
	composition := fixtures["explicitComposition"].(map[string]any)
	event := fixtures["matchingEvent"].(map[string]any)
	compositionBytes, err := json.Marshal(composition)
	if err != nil {
		b.Fatal(err)
	}
	eventBytes, err := json.Marshal(event)
	if err != nil {
		b.Fatal(err)
	}
	child, err := StartProcessKernel(ChildKernelConfig{
		ExecutablePath: path,
		RegistryPath:   filepath.Join(contractRoot, "schemas", "registry.json"),
		MaxFrameBytes:  1 << 20,
	})
	if err != nil {
		b.Fatal(err)
	}
	defer child.Close()
	compiled, err := child.Compile(context.Background(), CompileRequest{
		Tuple: tupleForFixture(composition, "ExplicitComposition"), RawComposition: compositionBytes,
	})
	if err != nil {
		b.Fatal(err)
	}
	runtime, err := NewRuntimeKernel(child, compiled)
	if err != nil {
		b.Fatal(err)
	}
	defer runtime.Close()
	request := KernelRequest{Tuple: tupleForFixture(event, "AcceptedEventView"), StreamIDHint: "stream-1", RawAcceptedEvent: eventBytes}
	b.ReportAllocs()
	b.ResetTimer()
	for index := 0; index < b.N; index++ {
		if _, err := runtime.Reduce(context.Background(), request); err != nil {
			b.Fatal(err)
		}
	}
}
