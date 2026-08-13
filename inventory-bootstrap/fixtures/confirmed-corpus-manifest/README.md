# ConfirmedCorpusManifest fixture

This directory closes only R1 from `08-execution-sheet-reaudit.md`. It defines and checks the
host-owned, pre-write manifest for the frozen D1 corpus. It does not run the Inventory bootstrap,
write `.arcanum/inventory/`, update expected hashes, or interpret any source.

## Contract

`confirmed-corpus-manifest.schema.json` freezes `confirmed-corpus-manifest@1`. Every file identity
contains a normalized repository-relative `path`, lowercase SHA-256 `sha256`, byte `size`, and the
40-character Git `revision`. The manifest also binds:

- its intended exact repository-relative output path;
- the semantic authority (`04-execution-sheet.md`);
- the mechanically extracted external row source (`d1-dispatch-sheet.md`);
- the ordered 22-row corpus with `entire-file` selectors;
- the ordered C1-C8 controls.

The JSON serialization is UTF-8, key-sorted, compact, and newline-terminated. No timestamp or host
path is included, so identical repository state and intended output path produce identical bytes.

The verifier requires the physical input file to resolve exactly to its declared
`confirmed_manifest_path`, requires canonical bytes, reconstructs the expected manifest from the bound files and repository state, proves
the external rows equal the frozen table row-for-row, and then requires field-level equality. It
fails on omissions, additions, reordering, changed selectors/hashes/sizes/revisions, changed
controls, source drift, authority drift, or an output path outside the repository.

## Commands

Run tests (read-only apart from Python's disposable cache files):

```powershell
python -m unittest discover -s inventory-bootstrap/fixtures/confirmed-corpus-manifest -p 'test_*.py' -v
```

Preview canonical manifest bytes on stdout without writing a manifest:

```powershell
python inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed_corpus_manifest.py `
  --repo-root . materialize `
  --manifest-path internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/inventory-bootstrap/runs/<run-id>/confirmed-corpus-manifest.json
```

At an authorized exact-run gate, the host may redirect those bytes to the exact allowlisted run
path. This fixture itself never performs that write. Verify a separately materialized manifest:

```powershell
python inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed_corpus_manifest.py `
  --repo-root . verify <exact-manifest-path>
```

Success prints `CONFIRMED_CORPUS_MANIFEST_VERIFIED`. Any mismatch exits non-zero with a typed
`BLOCK/...` reason. Hashes are never rewritten or accepted from the manifest under test.

## Inventory projection contract

`d1-lens-use-corpus-manifest.schema.json` defines the distinct writer-owned projection intended for
`.arcanum/inventory/raw/d1-lens-use-corpus.manifest.json`. The projection copies the verified,
ordered `sources` and `controls`, binds the canonical host manifest by path/hash/size/revision, and
adds the fixed denominator `{22 sources, 8 controls, 176 cells}`. It contains no interpretation.
Projection equivalence is exact field equality against a fresh deterministic projection of the
verified physical host manifest.

Preview projection bytes on stdout without writing Inventory:

```powershell
python inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed_corpus_manifest.py `
  --repo-root . project-inventory <exact-manifest-path>
```

Verify a separately written projection without modifying it:

```powershell
python inventory-bootstrap/fixtures/confirmed-corpus-manifest/confirmed_corpus_manifest.py `
  --repo-root . verify-inventory-projection <exact-manifest-path> <projection-path>
```

Success prints `INVENTORY_PROJECTION_VERIFIED`. Omitted, extra, reordered, or semantically changed
fields fail closed.
