package rwosidecar

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
)

const (
	testSeatAddress = "seatv1/sha256/7e792eba8811c01d1a2964207c86c30ab630d2f8afe6c7562d2f24fe24d50787"
	testSchemaHash  = "c9c047a65cbe3a70021493137d28d94d8913ea06b6dc7b13ca4254a1909d07bb"
	testInputHash   = "0f8bb97262774eb7471563c503150a0501a72562948f1ede7e2b2c25f90a7c3b"
)

func TestMaterialAddressResolvesExactClosedToolFreeBytes(t *testing.T) {
	root := fixtureMaterialRoot(t)
	catalog := testSeatCatalog(t, root)
	material, err := catalog.Resolve(testSeatAddress, "seat")
	if err != nil {
		t.Fatalf("resolve exact material: %v", err)
	}
	if got := digestTestBytes(material.ManifestBytes); got != strings.TrimPrefix(testSeatAddress, SeatAddressPrefix) {
		t.Fatalf("manifest digest = %s", got)
	}
	if got := digestTestBytes(material.OutputSchemaBytes); got != testSchemaHash {
		t.Fatalf("output schema digest = %s", got)
	}
	if len(material.MountedInputBytes) != 1 || digestTestBytes(material.MountedInputBytes[0]) != testInputHash {
		t.Fatalf("mounted input did not preserve the exact composition bytes")
	}
	if material.Manifest.MaxToolCalls != 0 || !material.Manifest.CapabilityPolicy.disabled() {
		t.Fatalf("material is not the closed zero-tool policy: %#v", material.Manifest)
	}
	if material.Manifest.SeatID != "seat" || material.Manifest.TimeoutMilliseconds != 5000 || material.Manifest.MaxOutputBytes != 4096 {
		t.Fatalf("material bounds changed: %#v", material.Manifest)
	}
}

func TestMaterialAddressRejectsAnyDrift(t *testing.T) {
	tests := []struct {
		name   string
		path   string
		mutate func([]byte) []byte
	}{
		{name: "manifest prompt or policy", path: "seat-manifest.json", mutate: func(value []byte) []byte {
			return bytes.Replace(value, []byte("bounded-worker"), []byte("changed-worker"), 1)
		}},
		{name: "mounted input", path: "composition.json", mutate: func(value []byte) []byte {
			return append(bytes.Clone(value), ' ')
		}},
		{name: "output schema", path: "output-schema.json", mutate: func(value []byte) []byte {
			return bytes.Replace(value, []byte(`"minLength":1`), []byte(`"minLength":2`), 1)
		}},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			root := copyFixtureMaterial(t)
			path := filepath.Join(root, test.path)
			original, err := os.ReadFile(path)
			if err != nil {
				t.Fatal(err)
			}
			if err := os.WriteFile(path, test.mutate(original), 0o600); err != nil {
				t.Fatal(err)
			}
			catalog := testSeatCatalog(t, root)
			if _, err := catalog.Resolve(testSeatAddress, "seat"); !errors.Is(err, ErrSeatMaterialDrift) {
				t.Fatalf("resolve drift error = %v", err)
			}
		})
	}
}

func TestContentAddressRoundTripRejectsDriftWrongSeatAndSubstitution(t *testing.T) {
	root := fixtureMaterialRoot(t)
	catalog := testSeatCatalog(t, root)
	if _, err := catalog.Resolve(testSeatAddress, "another-seat"); !errors.Is(err, ErrSeatMaterialCorrelation) {
		t.Fatalf("wrong seat error = %v", err)
	}

	substituted, err := NewSeatMaterialCatalog(root, []SeatMaterialBinding{{Address: testSeatAddress, RelativePath: "output-schema.json"}})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := substituted.Resolve(testSeatAddress, "seat"); !errors.Is(err, ErrSeatMaterialDrift) {
		t.Fatalf("substitution error = %v", err)
	}

	copyRoot := copyFixtureMaterial(t)
	manifestPath := filepath.Join(copyRoot, "seat-manifest.json")
	manifest, err := os.ReadFile(manifestPath)
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(manifestPath, append(manifest, ' '), 0o600); err != nil {
		t.Fatal(err)
	}
	drifted := testSeatCatalog(t, copyRoot)
	if _, err := drifted.Resolve(testSeatAddress, "seat"); !errors.Is(err, ErrSeatMaterialDrift) {
		t.Fatalf("drift error = %v", err)
	}
}

func TestMaterialAddressRejectsTraversalAndSymlinkEscape(t *testing.T) {
	root := fixtureMaterialRoot(t)
	if _, err := NewSeatMaterialCatalog(root, []SeatMaterialBinding{{Address: testSeatAddress, RelativePath: "../seat-manifest.json"}}); !errors.Is(err, ErrSeatMaterialPath) {
		t.Fatalf("traversal error = %v", err)
	}

	tempRoot := t.TempDir()
	outside := filepath.Join(t.TempDir(), "seat-manifest.json")
	manifest, err := os.ReadFile(filepath.Join(root, "seat-manifest.json"))
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(outside, manifest, 0o600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(outside, filepath.Join(tempRoot, "seat-manifest.json")); err != nil {
		t.Fatal(err)
	}
	catalog, err := NewSeatMaterialCatalog(tempRoot, []SeatMaterialBinding{{Address: testSeatAddress, RelativePath: "seat-manifest.json"}})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := catalog.Resolve(testSeatAddress, "seat"); !errors.Is(err, ErrSeatMaterialPath) {
		t.Fatalf("symlink escape error = %v", err)
	}
}

func TestMaterialAddressBuildsExactClosedEveRequest(t *testing.T) {
	catalog := testSeatCatalog(t, fixtureMaterialRoot(t))
	prepared, err := PrepareEveTaskRequest(testCommandBytes(t, "seat", testSeatAddress), taggedTestDigest("command"), "attempt-1", 1, catalog)
	if err != nil {
		t.Fatalf("prepare: %v", err)
	}
	if prepared.Request.Mode != "task" || prepared.Request.Capabilities.RequestInput {
		t.Fatalf("request policy changed: %#v", prepared.Request)
	}
	if prepared.Request.Message != "Role: bounded-worker\n\n"+prepared.Material.Manifest.Prompt {
		t.Fatalf("message did not preserve exact role/prompt: %q", prepared.Request.Message)
	}
	if !bytes.Equal(bytes.TrimSpace(prepared.Request.OutputSchema), bytes.TrimSpace(prepared.Material.OutputSchemaBytes)) {
		t.Fatalf("outputSchema differs from exact decoded fixture")
	}
	for _, forbidden := range []string{`"tools"`, `"agent"`, `"workflow"`, `"delegation"`, `"callback"`, `"shell"`, `"write"`, `"web"`, `"network"`} {
		if bytes.Contains(bytes.ToLower(prepared.RequestBytes), []byte(forbidden)) {
			t.Fatalf("request contains forbidden transport field %s: %s", forbidden, prepared.RequestBytes)
		}
	}
	if prepared.RequestFingerprint == "" || prepared.RequestSHA256 != digestHex(prepared.RequestBytes) {
		t.Fatalf("request binding missing: %#v", prepared)
	}
}

func TestMaterialAddressColonFormRecordsFrozenRegistryTension(t *testing.T) {
	// The selected design deliberately uses a colon-tagged content address.
	// The adapter address is itself a valid RWO identifier after the v2 repair.
	frozenJobID := regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._/-]*$`)
	if !frozenJobID.MatchString(testSeatAddress) {
		t.Fatalf("seat address does not satisfy the accepted identifier grammar")
	}
}

func fixtureMaterialRoot(t *testing.T) string {
	t.Helper()
	root, err := filepath.Abs(filepath.Join("testdata", "eve-one-seat"))
	if err != nil {
		t.Fatal(err)
	}
	return root
}

func copyFixtureMaterial(t *testing.T) string {
	t.Helper()
	destination := t.TempDir()
	for _, name := range []string{"composition.json", "composition-tuple.json", "authorization-event.json", "seat-manifest.json", "output-schema.json"} {
		value, err := os.ReadFile(filepath.Join(fixtureMaterialRoot(t), name))
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(destination, name), value, 0o600); err != nil {
			t.Fatal(err)
		}
	}
	return destination
}

func testSeatCatalog(t *testing.T, root string) *SeatMaterialCatalog {
	t.Helper()
	catalog, err := NewSeatMaterialCatalog(root, []SeatMaterialBinding{{Address: testSeatAddress, RelativePath: "seat-manifest.json"}})
	if err != nil {
		t.Fatal(err)
	}
	return catalog
}

func testCommandBytes(t *testing.T, target, address string) []byte {
	t.Helper()
	command := ExecuteBoundedSeatCommand{
		ContractID: "RWO-SEMANTIC-CONTRACT", ContractVersion: "1.0.0", ProfileID: "RWO-JCS-IJSON-SAFEINT", ProfileVersion: "1.0.0",
		SchemaID: "CommandIntent", SchemaVersion: "1.0.0", GraphIdentity: taggedTestDigest("graph"), EdgeID: "edge-execute-seat",
		AcceptedEventIdentity: taggedTestDigest("event"), CommandType: "ExecuteBoundedSeat", TargetNodeID: target,
		Payload: ExecuteBoundedSeatPayload{JobID: address},
	}
	value, err := json.Marshal(command)
	if err != nil {
		t.Fatal(err)
	}
	return value
}

func digestTestBytes(value []byte) string {
	digest := sha256.Sum256(value)
	return hex.EncodeToString(digest[:])
}

func taggedTestDigest(value string) string { return "sha256:" + digestTestBytes([]byte(value)) }
