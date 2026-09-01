# BUS-001 — final implementation evidence

## Verdict

`IMPLEMENTED-REVIEWED-PASS / PASS-KEEP` for the bounded official-publication component.

BUS-001 derives the exact preallocated `source_message_id` from one confirmed continuation mapping,
authenticates a persisted candidate/receipt against one journal-backed completed Attempt, and
atomically accepts one official message plus its ordered event pair. Migration 015 adds only
`runtime_attempt_result_acceptances`; it performs no backfill or legacy mutation.

## Group-stream decision

The publication candidate is evidence on the Attempt stream. Official acceptance appends
`attempt.result_accepted` followed by `position.accepted` or `critique.accepted` on the exact Group
stream. The Attempt link is non-transitioning: the completed Attempt and its aggregate head remain
unchanged. The Group advances exactly `+2`; its composite head and generic aggregate head converge
on the second official event.

This is a component proof only. Completed attempts, Group phase and reviewer visibility are
harness-owned prerequisites. No production publisher, service/API route, opening, effective input,
resume, effect, worker, provider/tool or adapter was added or invoked.

## Frozen entry authority

| Artifact | Historical entry digest |
|---|---|
| Descriptor | `sha256:cfc8f64d052f9adc5f85e5ce63985f6b90ed7ce6c55845c7d379ac117f21ca53` |
| Readiness | `sha256:b5d09dd470fd3beeb9d5e5d7be0d28df6f2c5af22baa653c9545afe52bd497e3` |

These are retained as entry authority and are not repinned to final implementation bytes.

## Final integrity evidence

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/confirmed_bus.py` | `sha256:1e4573cbcf7c3c50dbc062bf36d0b07f85630fb1c27c7eca3fc0a39c34c6659f` |
| `implementations/tests/runtime/test_runtime_confirmed_bus.py` | `sha256:80ae84ed0ba2f38c6281f6214eb0bd524be134346a30e50df31df50992b71a3e` |
| Stage-E source manifest | `sha256:e3232eb2b74e201f0a717e1ca42c2814f37ef79c54503b76e6654cc8b31337bd` — `75/75` |
| Stage-E execution receipt | `sha256:17ba25aa400e8d5c387fca09f1df9c1137e1f40bc61c012fef70a939449cd703` |

## Verification

- BUS-001: 23/23 PASS.
- HEADS-001: 8/8 PASS; incident and repair lineage remain preserved in its evidence.
- CONT-001: 9/9 PASS.
- CONF-001: 8/8 PASS.
- ACI traceability: 1/1 PASS.
- Stage-C: 8/8 PASS.
- Orchestration bridge: 18/18 PASS.
- Complete runtime discovery: 200/200 PASS.
- Canonical Control Center discovery: 36/36 PASS.
- Python compileall and `git diff --check`: PASS.
- Independent red-team: `PASS / KEEP`; no open BUS-001 finding remains.

## Promotion boundary

BUS-001 is promoted only to `implemented-reviewed-pass`. CONT-002, OPEN, positive Run transition,
RESUME, WORKER and VERIFY remain unpromoted. PRODUCT-PASS is a hard gate because its missing product
authority changes `confirmed_authority_digest`; real execution therefore requires a new dispatch
identity, a CONF v2 authority package and a new explicit user confirmation. CONF v1 remains a
component fixture.
