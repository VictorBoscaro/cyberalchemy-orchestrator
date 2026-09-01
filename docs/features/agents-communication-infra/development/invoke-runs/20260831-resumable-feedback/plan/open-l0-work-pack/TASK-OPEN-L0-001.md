# TASK-OPEN-L0-001 — non-authoritative audit-opening projection oracle

## Status and decision question

- **State:** `planned-blocked-on-independent-work-pack-review`
- **Layer:** OPEN L0 only
- **Decision question:** After this task, do two structurally independent pure implementations
  reproduce the same synthetic unstamped 0.6.4-shaped row and expose every declared preservation
  and loss without creating any execution or opening authority?
- **Controlling design:** [TECH-OPEN-D0](../TECH-OPEN-D0.md)
- **Design review:** [TECH-D0-REVIEW](../evidence/TECH-D0-REVIEW.md)

The work is an experiment, not an opening writer. Its output is a hypothesis fixture. It cannot be
used to append a dispatch, satisfy OPEN, advance a Run or Group, preserve a Seat/session, claim an
effect, or authorize a worker/provider.

## Minimum working unit

Implement two pure Python projections over one closed synthetic input:

1. `projector.py` produces canonical unstamped opening-row bytes, ordered operation bindings and a
   canonical discrepancy report.
2. `independent_oracle.py` independently reproduces the same outputs without importing the
   projector or sharing projection/canonicalization helpers.

The implementations may share only Python standard-library primitives and the immutable fixture
bytes. Independence is a code-dependency property; it is not a claim that two people authored the
implementations.

## Exact experimental input choices

These values are reversible test hypotheses, not product defaults or approved role semantics:

- synthetic dispatch type/route: `review` / installed legacy-managed `review` capability;
- candidate role mapping: runtime `author -> writer`, runtime `reviewer -> auditor`;
- unique audit group IDs: `audit_author_turn_0`, `audit_reviewer_turn_0`,
  `audit_author_turn_1`;
- explicit `invoked_by`: `synthetic@example.invalid`;
- `anti_bias_mode=disabled`, `max_loops=1`, `output_mode=inline`;
- all model, prompt, goal, context and budget values are visibly prefixed or named `synthetic`.

The candidate route must bind the pinned current registry and installed review capability, but the
output must label it `candidate` and `authority=none`. Mechanically valid legacy shape is not
launch authority.

## Exact future code write scope

1. `implementations/experiments/aci_open_l0/projector.py`
2. `implementations/experiments/aci_open_l0/independent_oracle.py`
3. `implementations/experiments/aci_open_l0/fixtures/synthetic-input.json`
4. `implementations/experiments/aci_open_l0/fixtures/expected-unstamped-row.json`
5. `implementations/experiments/aci_open_l0/fixtures/expected-discrepancy-report.json`
6. `implementations/tests/experiments/test_aci_open_l0_projection.py`

No existing file is in write scope. No package initializer is required; the test loads the two
modules by exact path. The implementation agent must use `domainspec-implement`; the independent
verifier must use `review` and must not edit the implementation.

## Required behavior

- Accept only the closed experimental input and exact three-operation order.
- Require three unique operation-scoped audit group IDs and explicit candidate role mappings.
- Require explicit `invoked_by`; reject caller-supplied `created` anywhere in the projected row.
- Emit canonical UTF-8 JSON bytes with sorted object keys, compact separators, NFC strings and no
  trailing newline. Array order is semantic; object-key input order is not.
- Compute lowercase `sha256:` digests over exact output bytes.
- Emit discrepancies for at least: runtime-managed versus legacy-managed authority, role-vocabulary
  substitution, logical Group reuse versus unique audit groups, shared author Seat/session loss,
  continuation-key loss, and inability of `layers=2` to preserve reviewer interposition.
- Treat direct legacy roles `author`/`reviewer`, duplicate `group_authoring`, missing/extra fields,
  reordered operation/group/connection arrays and drifted candidate-route digests as rejection.
- Show that a consistently recomputed candidate route, registry, capability, tool-profile or role
  change alters the experimental digest without granting authority.
- Expose no filesystem writer, subprocess, network, SQLite, journal, service, appender, provider,
  worker, effect or runtime mutation interface.

## Done criteria

Both implementations reproduce the same frozen bytes/digests; mutation tests reject every declared
closed-shape violation; static reachability shows no production consumer; the full runtime
regression signature is unchanged; and an independent reviewer returns `PASS/KEEP` against the
exact descriptor bytes.

## Local experimental test obligations

These IDs are local evidence and must not be added to canonical ACI traceability or presented as
OPEN evidence.

| ID | Required proof |
|---|---|
| `OPEN-L0-T1` | Projector and independent oracle produce byte-identical row, bindings, discrepancy documents and digests. |
| `OPEN-L0-T2` | Unknown/missing keys and missing/extra/reordered semantic arrays reject; object-key reordering canonicalizes without drift. |
| `OPEN-L0-T3` | Direct `author`/`reviewer` roles, duplicate `group_authoring`, wrong bindings and `layers=2` substitution reject. |
| `OPEN-L0-T4` | Discrepancies witness loss of shared Seat/session, continuation, logical Group reuse and reviewer interposition. |
| `OPEN-L0-T5` | Route-digest mismatch rejects; consistently recomputed route/registry/capability/tool-profile/role drift changes the experimental digest but grants no authority. |
| `OPEN-L0-T6` | Caller-supplied `created` and missing/empty/ambient `invoked_by` reject. |
| `OPEN-L0-T7` | Modules neither import one another nor production/appender code and expose no I/O or mutation primitive. |
| `OPEN-L0-T8` | A bounded repository scan finds no production consumer or appender/effect/OPEN/Run/Group/worker/provider call. |
| `OPEN-L0-T9` | Existing runtime discovery remains green with an unchanged signature. |

## Stop conditions

Stop before code if the descriptor, pinned design/review, appender or registry bytes drift. Stop
during implementation if satisfying any test requires importing or calling production runtime or
appender code, editing an existing file, registering a schema, changing CONF bytes, writing a
ledger row, creating an OPEN/effect/transition, or selecting A/B/C. Record the mismatch instead of
widening scope.

## Validation commands

```text
python -B -m unittest implementations.tests.experiments.test_aci_open_l0_projection -v
python -B -m compileall implementations/experiments/aci_open_l0 implementations/tests/experiments/test_aci_open_l0_projection.py
python -B -m unittest discover -s implementations/tests/runtime -t .
git diff --check
```

## Promotion boundary

L0 completion returns only to the unresolved A/B/C authority gate. It cannot promote itself to L1
or authorize an authoritative opening path.
