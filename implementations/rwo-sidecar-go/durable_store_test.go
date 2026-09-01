package rwosidecar

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"testing"
)

const durableStoreTestRecordType DurableRecordType = 1

type durableStoreTestRecord struct {
	Kind         string `json:"kind"`
	OpaqueBase64 string `json:"opaque_base64"`
}

func (durableStoreTestRecord) DurableRecordType() DurableRecordType {
	return durableStoreTestRecordType
}

func TestDurableStoreAppendReopenRebuildsExactPrefix(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableStoreTestHeader()
	store := openDurableStoreForTest(t, path, header)

	next, previous, err := store.Tip()
	if err != nil {
		t.Fatal(err)
	}
	if next != 1 || previous != zeroFrameSHA256 {
		t.Fatalf("unexpected empty tip: sequence=%d hash=%q", next, previous)
	}
	cursorOne := []byte("opaque-cursor-one")
	first := durableStoreTestRecord{Kind: "semantic_commit", OpaqueBase64: "b3BhcXVl"}
	ref, err := store.Append(AppendExpectation{
		ExpectedSequence:            next,
		ExpectedPreviousFrameSHA256: previous,
		Cursor: &CursorTransition{
			StreamKey:              "graph\x00stream-a",
			ExpectedPreviousSHA256: EmptyCursorSHA256,
			NextSHA256:             digestHex(cursorOne),
		},
	}, first)
	if err != nil {
		t.Fatal(err)
	}
	if ref.Sequence != 1 || ref.Offset <= 0 || ref.FrameSHA256 == zeroFrameSHA256 {
		t.Fatalf("unexpected first reference: %+v", ref)
	}
	next, previous, err = store.Tip()
	if err != nil {
		t.Fatal(err)
	}
	second := durableStoreTestRecord{Kind: "physical_observation", OpaqueBase64: "dHdv"}
	if _, err := store.Append(AppendExpectation{
		ExpectedSequence:            next,
		ExpectedPreviousFrameSHA256: previous,
	}, second); err != nil {
		t.Fatal(err)
	}

	before, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if len(before.Records) != 2 || before.LastSequence != 2 {
		t.Fatalf("unexpected live snapshot: %+v", before)
	}
	if before.CursorSHA256ByStreamKey["graph\x00stream-a"] != digestHex(cursorOne) {
		t.Fatalf("cursor projection was not published exactly: %+v", before.CursorSHA256ByStreamKey)
	}
	// Prove the snapshot is defensive rather than a mutable projection handle.
	before.Records[0].Body[0] ^= 0xff
	before.CursorSHA256ByStreamKey["graph\x00stream-a"] = zeroFrameSHA256
	before, err = store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}

	reopened := openDurableStoreForTest(t, path, header)
	defer reopened.Close()
	after, err := reopened.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(before, after) {
		t.Fatalf("projection changed across reopen:\nbefore=%+v\nafter=%+v", before, after)
	}
	var decoded durableStoreTestRecord
	if err := decodeClosedJSON(after.Records[0].Body, &decoded); err != nil {
		t.Fatal(err)
	}
	if decoded != first {
		t.Fatalf("record bytes changed across reopen: got %+v want %+v", decoded, first)
	}
}

func TestDurableStoreExclusiveLockRejectsSecondWriter(t *testing.T) {
	if runtime.GOOS != "linux" {
		t.Skip("candidate requires Linux flock")
	}
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableStoreTestHeader()
	first := openDurableStoreForTest(t, path, header)
	defer first.Close()
	second, err := OpenDurableStore(path, header)
	if second != nil {
		_ = second.Close()
		t.Fatal("second store unexpectedly acquired the same file")
	}
	if !errors.Is(err, ErrDurableStoreLocked) {
		t.Fatalf("second open error = %v, want ErrDurableStoreLocked", err)
	}
}

func TestDurableStoreTornSemanticTailTruncatesToVerifiedPrefix(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableStoreTestHeader()
	store := openDurableStoreForTest(t, path, header)
	appendDurableStoreTestRecord(t, store, "verified")
	snapshot, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	verifiedInfo, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}

	body, err := jsonRecordEnvelope(durableStoreTestRecord{Kind: "torn", OpaqueBase64: "dG9ybg=="}, nil)
	if err != nil {
		t.Fatal(err)
	}
	previous, err := parseDigest(snapshot.LastFrameSHA256)
	if err != nil {
		t.Fatal(err)
	}
	frame, _ := encodeDurableFrame(durableStoreTestRecordType, 2, previous, body)
	appendFile, err := os.OpenFile(path, os.O_WRONLY|os.O_APPEND, 0)
	if err != nil {
		t.Fatal(err)
	}
	cut := len(frame) / 2
	if cut < durableFramePrefixSize() {
		cut = durableFramePrefixSize()
	}
	if _, err := appendFile.Write(frame[:cut]); err != nil {
		_ = appendFile.Close()
		t.Fatal(err)
	}
	if err := appendFile.Sync(); err != nil {
		_ = appendFile.Close()
		t.Fatal(err)
	}
	if err := appendFile.Close(); err != nil {
		t.Fatal(err)
	}

	reopened := openDurableStoreForTest(t, path, header)
	defer reopened.Close()
	after, err := reopened.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(snapshot, after) {
		t.Fatalf("torn tail changed verified projection:\nbefore=%+v\nafter=%+v", snapshot, after)
	}
	repairedInfo, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	if repairedInfo.Size() != verifiedInfo.Size() {
		t.Fatalf("repaired size = %d, want verified prefix %d", repairedInfo.Size(), verifiedInfo.Size())
	}
}

func TestDurableStoreInteriorCorruptionBlocksOpen(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	header := durableStoreTestHeader()
	store := openDurableStoreForTest(t, path, header)
	appendDurableStoreTestRecord(t, store, "first")
	appendDurableStoreTestRecord(t, store, "second")
	snapshot, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	before, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	corruptOffset := snapshot.Records[0].Ref.Offset + int64(durableFramePrefixSize()) + 3
	file, err := os.OpenFile(path, os.O_RDWR, 0)
	if err != nil {
		t.Fatal(err)
	}
	byteAtOffset := []byte{before[corruptOffset] ^ 0x40}
	if _, err := file.WriteAt(byteAtOffset, corruptOffset); err != nil {
		_ = file.Close()
		t.Fatal(err)
	}
	if err := file.Sync(); err != nil {
		_ = file.Close()
		t.Fatal(err)
	}
	if err := file.Close(); err != nil {
		t.Fatal(err)
	}

	opened, err := OpenDurableStore(path, header)
	if opened != nil {
		_ = opened.Close()
		t.Fatal("corrupt store unexpectedly opened")
	}
	if !errors.Is(err, ErrDurableStoreCorrupt) {
		t.Fatalf("open error = %v, want ErrDurableStoreCorrupt", err)
	}
	after, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if len(after) != len(before) {
		t.Fatalf("corrupt complete store was truncated: before=%d after=%d", len(before), len(after))
	}
}

func TestDurableStoreStaleSequenceHashAndCursorRejectWithoutAppend(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	store := openDurableStoreForTest(t, path, durableStoreTestHeader())
	defer store.Close()
	appendDurableStoreTestRecord(t, store, "first")
	before, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	next, previous, err := store.Tip()
	if err != nil {
		t.Fatal(err)
	}
	record := durableStoreTestRecord{Kind: "rejected", OpaqueBase64: "eA=="}
	cases := []struct {
		name        string
		expectation AppendExpectation
	}{
		{
			name: "sequence",
			expectation: AppendExpectation{
				ExpectedSequence:            next - 1,
				ExpectedPreviousFrameSHA256: previous,
			},
		},
		{
			name: "frame hash",
			expectation: AppendExpectation{
				ExpectedSequence:            next,
				ExpectedPreviousFrameSHA256: zeroFrameSHA256,
			},
		},
		{
			name: "cursor",
			expectation: AppendExpectation{
				ExpectedSequence:            next,
				ExpectedPreviousFrameSHA256: previous,
				Cursor: &CursorTransition{
					StreamKey:              "graph\x00stream-a",
					ExpectedPreviousSHA256: digestHex([]byte("stale")),
					NextSHA256:             digestHex([]byte("next")),
				},
			},
		},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			if _, err := store.Append(test.expectation, record); !errors.Is(err, ErrDurableStoreExpectation) {
				t.Fatalf("Append error = %v, want expectation mismatch", err)
			}
			after, err := store.Snapshot()
			if err != nil {
				t.Fatal(err)
			}
			if !reflect.DeepEqual(before, after) {
				t.Fatalf("rejected CAS changed projection:\nbefore=%+v\nafter=%+v", before, after)
			}
		})
	}
}

func TestDurableStoreWriteOrSyncFailurePoisonsUntilVerifiedReopen(t *testing.T) {
	t.Run("partial write", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "runtime.rwolog")
		header := durableStoreTestHeader()
		injected := errors.New("injected partial write")
		called := false
		store, err := OpenDurableStore(path, header, WithDurableStoreFailureHooks(DurableStoreFailureHooks{
			WriteFrame: func(file *os.File, frame []byte) (int, error) {
				if called {
					return file.Write(frame)
				}
				called = true
				cut := len(frame) / 2
				count, writeErr := file.Write(frame[:cut])
				if writeErr != nil {
					return count, writeErr
				}
				return count, injected
			},
		}))
		if err != nil {
			t.Fatal(err)
		}
		next, previous, err := store.Tip()
		if err != nil {
			t.Fatal(err)
		}
		_, err = store.Append(AppendExpectation{
			ExpectedSequence:            next,
			ExpectedPreviousFrameSHA256: previous,
		}, durableStoreTestRecord{Kind: "uncertain", OpaqueBase64: "eA=="})
		if !errors.Is(err, ErrDurableStoreNeedsReopen) || !errors.Is(err, injected) {
			t.Fatalf("Append error = %v, want injected needs-reopen error", err)
		}
		assertDurableStorePoisoned(t, store)
		if err := store.Close(); err != nil {
			t.Fatal(err)
		}
		reopened := openDurableStoreForTest(t, path, header)
		defer reopened.Close()
		snapshot, err := reopened.Snapshot()
		if err != nil {
			t.Fatal(err)
		}
		if snapshot.LastSequence != 0 || len(snapshot.Records) != 0 {
			t.Fatalf("partial unacknowledged frame reached projection: %+v", snapshot)
		}
	})

	t.Run("sync uncertainty", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "runtime.rwolog")
		header := durableStoreTestHeader()
		injected := errors.New("injected sync uncertainty")
		store, err := OpenDurableStore(path, header, WithDurableStoreFailureHooks(DurableStoreFailureHooks{
			SyncFrame: func(*os.File) error { return injected },
		}))
		if err != nil {
			t.Fatal(err)
		}
		next, previous, err := store.Tip()
		if err != nil {
			t.Fatal(err)
		}
		_, err = store.Append(AppendExpectation{
			ExpectedSequence:            next,
			ExpectedPreviousFrameSHA256: previous,
		}, durableStoreTestRecord{Kind: "possibly-synced", OpaqueBase64: "eA=="})
		if !errors.Is(err, ErrDurableStoreNeedsReopen) || !errors.Is(err, injected) {
			t.Fatalf("Append error = %v, want injected needs-reopen error", err)
		}
		assertDurableStorePoisoned(t, store)
		if err := store.Close(); err != nil {
			t.Fatal(err)
		}
		reopened := openDurableStoreForTest(t, path, header)
		defer reopened.Close()
		snapshot, err := reopened.Snapshot()
		if err != nil {
			t.Fatal(err)
		}
		if snapshot.LastSequence != 1 || len(snapshot.Records) != 1 {
			t.Fatalf("complete uncertain frame was not decided by verified reopen: %+v", snapshot)
		}
	})
}

func TestDurableStoreIncompleteOrMismatchedHeaderBlocks(t *testing.T) {
	t.Run("incomplete canonical header", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "runtime.rwolog")
		if err := os.WriteFile(path, durableHeaderMagic[:4], 0o600); err != nil {
			t.Fatal(err)
		}
		store, err := OpenDurableStore(path, durableStoreTestHeader())
		if store != nil {
			_ = store.Close()
			t.Fatal("incomplete canonical header unexpectedly opened")
		}
		if !errors.Is(err, ErrDurableStoreHeader) {
			t.Fatalf("open error = %v, want header error", err)
		}
	})

	t.Run("exact graph and tuple binding", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "runtime.rwolog")
		header := durableStoreTestHeader()
		store := openDurableStoreForTest(t, path, header)
		if err := store.Close(); err != nil {
			t.Fatal(err)
		}
		wrongGraph := header
		wrongGraph.GraphIdentity = "sha256:wrong-graph"
		if opened, err := OpenDurableStore(path, wrongGraph); opened != nil || !errors.Is(err, ErrDurableStoreHeader) {
			if opened != nil {
				_ = opened.Close()
			}
			t.Fatalf("wrong graph open = %v, %v; want header rejection", opened, err)
		}
		wrongTuple := header
		wrongTuple.Tuple.ProfileVersion = "99.0.0"
		if opened, err := OpenDurableStore(path, wrongTuple); opened != nil || !errors.Is(err, ErrDurableStoreHeader) {
			if opened != nil {
				_ = opened.Close()
			}
			t.Fatalf("wrong tuple open = %v, %v; want header rejection", opened, err)
		}
	})
}

func durableStoreTestHeader() DurableStoreHeader {
	return DurableStoreHeader{
		StoreFormat:          DurableStoreFormatV1,
		GraphIdentity:        "graphv1:sha256:" + digestHex([]byte("compiled-graph")),
		RawCompositionSHA256: digestHex([]byte("raw-composition")),
		Tuple: VersionTuple{
			ContractID:      "RWO-SEMANTIC-CONTRACT",
			ContractVersion: "0.2.0",
			ProfileID:       "RWO-COMPOSITION-PROFILE",
			ProfileVersion:  "0.2.0",
			SchemaID:        "RWO-COMPOSITION-SCHEMA",
			SchemaVersion:   "0.2.0",
			ValueType:       "RecursiveWorkGraph",
		},
		StoreInstanceID: "store-test-instance-001",
	}
}

func openDurableStoreForTest(t *testing.T, path string, header DurableStoreHeader) *DurableStore {
	t.Helper()
	store, err := OpenDurableStore(path, header)
	if err != nil {
		t.Fatal(err)
	}
	return store
}

func appendDurableStoreTestRecord(t *testing.T, store *DurableStore, kind string) DurableRecordRef {
	t.Helper()
	next, previous, err := store.Tip()
	if err != nil {
		t.Fatal(err)
	}
	ref, err := store.Append(AppendExpectation{
		ExpectedSequence:            next,
		ExpectedPreviousFrameSHA256: previous,
	}, durableStoreTestRecord{Kind: kind, OpaqueBase64: fmt.Sprintf("opaque-%s", kind)})
	if err != nil {
		t.Fatal(err)
	}
	return ref
}

func jsonRecordEnvelope(record DurableRecord, cursor *CursorTransition) ([]byte, error) {
	body, err := json.Marshal(record)
	if err != nil {
		return nil, err
	}
	return json.Marshal(persistedRecordEnvelope{
		BodyBase64: base64.StdEncoding.EncodeToString(body),
		Cursor:     cursor,
	})
}

func assertDurableStorePoisoned(t *testing.T, store *DurableStore) {
	t.Helper()
	if _, _, err := store.Tip(); !errors.Is(err, ErrDurableStoreNeedsReopen) {
		t.Fatalf("Tip after uncertainty = %v, want needs reopen", err)
	}
	if _, err := store.Snapshot(); !errors.Is(err, ErrDurableStoreNeedsReopen) {
		t.Fatalf("Snapshot after uncertainty = %v, want needs reopen", err)
	}
	if _, err := store.CursorSHA256("graph\x00stream"); !errors.Is(err, ErrDurableStoreNeedsReopen) {
		t.Fatalf("CursorSHA256 after uncertainty = %v, want needs reopen", err)
	}
	if _, err := store.Append(AppendExpectation{
		ExpectedSequence:            1,
		ExpectedPreviousFrameSHA256: zeroFrameSHA256,
	}, durableStoreTestRecord{Kind: "must-not-append", OpaqueBase64: "eA=="}); !errors.Is(err, ErrDurableStoreNeedsReopen) {
		t.Fatalf("Append after uncertainty = %v, want needs reopen", err)
	}
}

func TestDurableStoreDigestAndRecordCopiesRemainExact(t *testing.T) {
	path := filepath.Join(t.TempDir(), "runtime.rwolog")
	store := openDurableStoreForTest(t, path, durableStoreTestHeader())
	defer store.Close()
	record := durableStoreTestRecord{Kind: "closed-json", OpaqueBase64: "AAEC"}
	appendDurableStoreTestRecord(t, store, record.Kind)
	snapshot, err := store.Snapshot()
	if err != nil {
		t.Fatal(err)
	}
	if len(snapshot.LastFrameSHA256) != 64 || bytes.Equal(snapshot.Records[0].Body, nil) {
		t.Fatalf("invalid durable snapshot: %+v", snapshot)
	}
}
