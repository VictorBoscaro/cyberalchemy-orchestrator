# Validation receipt

Status: SPEC Recheck 3 `KEEP`; this receipt does not approve the separate implementation SWU.

## Checks

```text
python validate_artifacts.py
PASS: schemas, positive identity projection, Ed25519 evidence, singular other, and structural future role
PASS: frozen two-document pool v0.6 fixture verified and losslessly projected to current canonical v0.7 (414 ordered entries)
PASS: 41/41 typed negative vectors with exact paths
LIMIT: this validator checks SPEC fixtures and compares the frozen v0.6 fixture with the current production pool; other production consumers, compiler behavior, registrar, and telemetry require separate implementation evidence

python -m py_compile validate_artifacts.py
PASS

repaired-target whitespace/final-newline audit (excluding immutable review.md)
PASS

feature Craft ledger parse/index audit at SPEC Recheck 3
PASS: 114/114 then-current index targets resolved; the later implementation ledger has separate validation evidence

git diff --check -- <feature CRAFT> <feature ledger>
PASS (Git emitted only its LF/CRLF working-copy warning)

stale-text scan across repaired package and feature Craft surfaces
PASS: no superseded vector-count or pre-review status wording outside immutable review.md

bounded migration-surface scan
PASS: 28 selector/version files, 13 broad role-literal files and 7 governed-pool files classified

immutable review.md SHA-256 after SPEC Recheck 3 KEEP
PASS: 285B4636739DE898607A9F49A898649D754D525ED809DC68597207357CE4BA1F
```

Draft 2020-12 meta-validation runs for every loaded schema. YAML uses a SafeLoader variant that
rejects duplicate mapping keys and preserves date scalars as strings. Fixture evidence uses a real
Ed25519 verification path with the public key in `allocator-trust.json`; the deterministic private
seed exists only in the conformance harness and makes no production key-service claim. Digests are
sorted-key compact UTF-8 JSON for this bounded fixture profile, not a general RFC 8785 claim.

## What is proven

- the frozen v0.6 source fixture parses as the exact two-document/414-row stream pinned by the
  migration authority;
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

- SPEC Recheck 3 returned `KEEP`; implementation approval is a separate gate.
- This validator alone does not prove the production consumers, registrar, compiler or telemetry.
  Separate IMPL evidence reports the current v0.7 pool, v2 dispatch/ledger package, data-selected
  role registry, compiler integration and telemetry consumers; that implementation remains gated
  on its own independent recheck.
- No allocator key service, runtime graph ingestion/launch, scheduler, provider/tool execution or
  downstream autonomous ExecutionGraph execution is proven by this SPEC or the bounded IMPL SWU.
- The implementation re-ran the 19 bootstrap/handoff tests: 14 pass and five cases remain red
  (four assertion failures and one empty-slot error), classified as handoff residue rather than
  identity/role conformance.
