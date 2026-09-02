# Validation receipt

Status: `ready_for_recheck`, not self-approved.

## Checks

```text
python validate_artifacts.py
PASS: schemas, positive identity projection, Ed25519 evidence, singular other, and structural future role
PASS: real two-document pool v0.6 verified and losslessly projected to canonical v0.7 shape (414 entries)
PASS: 41/41 typed negative vectors with exact paths
LIMIT: specification fixtures only; production pool, consumers, registrar, compiler, and telemetry are unchanged

python -m py_compile validate_artifacts.py
PASS

repaired-target whitespace/final-newline audit (excluding immutable review.md)
PASS

feature Craft ledger parse/index audit
PASS: 114/114 index targets resolve

git diff --check -- <feature CRAFT> <feature ledger>
PASS (Git emitted only its LF/CRLF working-copy warning)

stale-text scan across repaired package and feature Craft surfaces
PASS: no superseded vector-count or pre-review status wording outside immutable review.md

bounded migration-surface scan
PASS: 28 selector/version files, 13 broad role-literal files and 7 governed-pool files classified

immutable review.md SHA-256 after Recheck 2
PASS: FF27533D10B5D0DDD3190C3E5D0928185470182D3ED7F708B3BA416DCD8F68A1
```

Draft 2020-12 meta-validation runs for every loaded schema. YAML uses a SafeLoader variant that
rejects duplicate mapping keys and preserves date scalars as strings. Fixture evidence uses a real
Ed25519 verification path with the public key in `allocator-trust.json`; the deterministic private
seed exists only in the conformance harness and makes no production key-service claim. Digests are
sorted-key compact UTF-8 JSON for this bounded fixture profile, not a general RFC 8785 claim.

## What is proven

- the real pool authority bytes parse as the actual two-document/414-row v0.6 stream;
- the deterministic migration projection preserves all non-identity roster data/order and produces
  canonical v0.7 `agent_name` rows;
- role registry v1 is exactly eight enabled roles and a same-version byte change fails against its
  trusted digest;
- assignment/ref tamper, forged signature, replay, stale/conflicting evidence and ref drift have
  distinct reachable errors;
- 41 normalization, source-authority, registry, context, evidence and assignment attacks return
  exact codes/paths, including raw-only pool substitution, registry reorder/name substitution and a
  future-only role rejected under v1;
- an illustrative unaccepted registry v2 can carry `researcher` through the unchanged structural
  pool schema when its role set is explicitly supplied; this proves schema extensibility, not v2
  authority or production support;
- DraftGraph cannot author `display_name`; final projection uses signed assignments; singular
  `other` is admitted only with explicit signed role-fit override.

## Residue

- Independent recheck has not yet returned `KEEP`.
- The production pool is still v0.6 `name`; direct consumers and registrar still use stale shapes,
  ledger schema `0.6.4` and hard-coded seven-role enums. No dispatch-type registry v2 or telemetry
  row `0.7.0` exists; `other` therefore is not yet production-valid.
- No production migration, loader, allocator key service, compiler integration, telemetry schema
  bump, runtime launch or downstream ExecutionGraph consumption is proven.
- Recheck 2 reports a selected 19-test production suite with 5 failures and 1 error. This repair did
  not rerun or diagnose that suite. It remains an unresolved validation limit; there is no claim
  that those outcomes pre-existed this work or were caused by this specification package.
