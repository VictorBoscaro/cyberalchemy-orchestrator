# Context pack — SWU-ACI-EXECUTION-POLICY-DENIAL-002

## Context Pack Summary

- Task: [`TASK-POLICY-002`](../tasks/TASK-POLICY-002.md)
- Descriptor: [`SWU-ACI-EXECUTION-POLICY-DENIAL-002`](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json)
- Mode: `deep`, link-first, strict obligation coverage
- Files selected: 18
- Obligation coverage: 100% for workpack context
- Runtime handoff: none
- Code entry: **BLOCK** until a separate exact code-readiness receipt returns `PASS`
- Lean bridge: excluded from evidence, dependencies and execution
- Unresolved product or technical decision: none inside the bounded L2 question

This pack is a repository-local planning aid. It does not replace the task, descriptor, readiness
receipt or implementation review and grants no code, runtime, production or external-action
authority.

## Objective and minimum useful proof

Prove that the exact reopened, non-executable POLICY-001 package can route each of twelve closed
scalar test selectors to one byte-identical durable package-level denial. The proof may add one
test-only SQLite table and one row in a caller-supplied temporary file-backed database. It must not
attempt the named action, mutate POLICY-001 evidence, create production authority or claim
POLICY-003/L3 host enforcement.

## Authority precedence

1. The current [task](../tasks/TASK-POLICY-002.md) owns the decision question, exact write scope,
   obligations, validation commands and stop conditions.
2. The current [descriptor](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json) owns exact pins,
   symbols, capability denies and the promotion ceiling.
3. Current DomainSpec contracts own receipt semantics and T-ACI-POL2-1 through T-ACI-POL2-8.
4. Frozen reviews and inventories explain accepted planning judgments but do not override current
   task, descriptor or normative bytes.
5. Existing POLICY-000 and POLICY-001 code is read-only evidence and dependency surface.

Any conflict, missing pin or required write outside the descriptor stops the task. Historical pins
embedded in earlier reports do not substitute for the current descriptor pins.

## Obligation coverage

| Obligation | Status | Selected evidence | Required resolution |
|---|---|---|---|
| `ENTRY` | `covered / code blocked` | [Task § Entry predicates](../tasks/TASK-POLICY-002.md#entry-predicates-and-stop-conditions), [descriptor `entry_gate_status`](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json) | Rehash all pins, prove all three outputs absent and obtain a separate `PASS` readiness receipt before mutation. |
| `T-ACI-POL2-1` | `covered` | [TEST-SPEC § T-ACI-POL2-1](../../specs/TEST-SPEC.md#t-aci-pol2-1--exact-fake-denial-receipt), [domain § ExecutionPolicyFakeDenialReceipt](../../specs/domain.md#executionpolicyfakedenialreceipt) | Oracle independently freezes exact preimage/receipt bytes, ordered reasons and both digests. |
| `T-ACI-POL2-2` | `covered` | [Task § T-ACI-POL2-1 through T-ACI-POL2-8](../tasks/TASK-POLICY-002.md#t-aci-pol2-1-through-t-aci-pol2-8), [alignment § Required negative coverage](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-ALIGNMENT-LAYERING-AUDIT.md#required-negative-coverage) | Reopen and fully revalidate L1 before the denial transaction; every drift/positive authority case leaves zero L2 rows. |
| `T-ACI-POL2-3` | `covered` | [Task § Closed implementation contract](../tasks/TASK-POLICY-002.md#closed-implementation-contract), [TEST-SPEC § T-ACI-POL2-3](../../specs/TEST-SPEC.md#t-aci-pol2-3--decision-reasons-and-attempt-labels-are-closed) | Exactly 12 unique scalar selectors; label never enters receipt, row, digest, identity or authority. |
| `T-ACI-POL2-4` | `covered` | [Persistence inventory § Failpoints and atomicity](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md#failpoints-and-atomicity) | Three pre-commit failpoints roll back; post-commit lost response leaves one row and converges on retry. |
| `T-ACI-POL2-5` | `covered` | [Persistence inventory § Replay, conflict and corruption classification](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md#replay-conflict-and-corruption-classification) | Both uniqueness axes resolve under one writer transaction; drift conflicts without mutation. |
| `T-ACI-POL2-6` | `covered` | [TEST-SPEC § T-ACI-POL2-6](../../specs/TEST-SPEC.md#t-aci-pol2-6--file-backed-reopen-reproduces-denial) | Fresh database, L1 and L2 handles reproduce exact source binding, bytes and digests; memory-only SQLite rejects. |
| `T-ACI-POL2-7` | `covered` | [TEST-SPEC § T-ACI-POL2-7](../../specs/TEST-SPEC.md#t-aci-pol2-7--every-attempt-label-denies-with-zero-external-action) | All labels run independently while every external/workload boundary spy remains zero. |
| `T-ACI-POL2-8` | `covered` | [TEST-SPEC § T-ACI-POL2-8](../../specs/TEST-SPEC.md#t-aci-pol2-8--production-and-l3-firewall), [capability § POLICY-002/L2 fake-denial invariants](../../specs/capabilities/execution-policy-authority.md#policy-002l2-fake-denial-invariants) | Preserve L1 exactly; add one L2 table/row only; production authority/effect rows and L3 evidence remain empty. |
| `SCOPE` | `covered` | [Task § Exact write scope](../tasks/TASK-POLICY-002.md#exact-write-scope), [descriptor `current_write_scope`](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json) | Only the three named test paths may change; all other paths are read-only. |

Strict context coverage: **PASS**. Executable handoff: **BLOCK pending readiness**.

## Selected sources and exact pins

| Source | Selector purpose | SHA-256 |
|---|---|---|
| [Task](../tasks/TASK-POLICY-002.md) | Primary obligations, scope, commands and stop conditions | `9e7d32981c028df50bb89c2f113e85cfb9121bbcbed38a8af10443627b1d7f80` |
| [Descriptor](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json) | Exact authority, capability and dependency envelope | `b6853f2026f4a3881fc08b253dd7c5a2f2ef81e4f018f151b0875df68725a73e` |
| [TECH-POLICY-D0](../../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md) | Layer allocation and L2/L3 boundary | `522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` |
| [POLICY-002 DomainSpec review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-DOMAINSPEC-REVIEW.md) | Planning-only integrated contract verdict | `1a758c0d0223f6a26b2408a32c2f7ba087a456a26b80c6e0fd38b7f053497ff9` |
| [POLICY-002 persistence inventory](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md) | One-table transaction, replay, reopen and corruption pattern | `2319202dc75eb09306523e54623a2c20f60b4be35fd1e62c4538743116d3d869` |
| [POLICY-002 alignment audit](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-ALIGNMENT-LAYERING-AUDIT.md) | Three-path topology and layer-leakage controls | `34ece0e88c7a67a4065285d476d8143a617a111a579daa0ba6713d5bf811e8a3` |
| [POLICY-001 implementation review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-IMPLEMENTATION-REVIEW.md) | Independently reviewed L1 prerequisite | `cbb9c03460ae755f39d194b58d0db2f8ca531bc8572f27ec4bf2949deeef885b` |
| [L1 harness](../../../../../implementations/tests/runtime/policy_lineage_harness.py) | Public `reopen_synthetic_lineage` seam | `8f8d74d4f02d89392e853e14d48acdc7317c9dd17b0fbd91e49c5f90683b812b` |
| [L1 oracle](../../../../../implementations/tests/runtime/execution_policy_lineage_oracle_v1.json) | Exact source fixture | `9cc5ffd931a911b2c6fb5dcaaf5d5f0e336514663dbd8866209218e67084952b` |
| [L1 tests](../../../../../implementations/tests/runtime/test_execution_policy_lineage.py) | Existing reopen/firewall evidence | `fd82c46ffbc6ac36656c646bdb1dffe3b7cc34f36920e1c27725d47688dd8e75` |
| [Domain](../../specs/domain.md) | Closed denial receipt and canonical vectors | `978e5c018e8aaa97d277cbd403594c0dca511aa395cb603a0496cb567ba91f9c` |
| [SPEC](../../specs/SPEC.md) | Feature registration and exclusions | `319130e802af1d85aec2373517b3f9d72f79f6a68a221154c6691c47e2620c60` |
| [Capability](../../specs/capabilities/execution-policy-authority.md) | L0–L2 ownership and authority firewall | `8b8fa86efbd49ed74dd49da9cd05e33ed183e5194d4c3c27f2d0a08d8f7f241a` |
| [TEST-SPEC](../../specs/TEST-SPEC.md) | T-ACI-POL2-1 through T-ACI-POL2-8 | `bfd080bc0ec4860d7c5b9f3f028b8bbd0560786e9e61a83ce51168b0d21b985d` |
| [Rules](../../specs/rules.md) | ACI-R23 | `eeac22fe4dc0edc3a31a2f9cbf94aea7d976cda1e61e1ce793fe66e0fc758225` |
| [Interfaces](../../specs/interfaces.md) | Scalar test-only denial boundary | `c5e055ef443a3f3a1391b49e20b1f74b0bc7e5c523ca54295bf496037e70f028` |
| [Architecture](../../specs/architecture.md) | One-table L2 topology and L3 firewall | `6991ebb1b470733b8044a9f081ba5284ce87f127671e12db0b9a2e205c381832` |
| [Glossary](../../specs/glossary.md) | Selector/denial/authority distinctions | `f8c561b7d69a0eaf4dbd404d6d7ec01d9ddfaa67adf45a264e97d89e98de3efb` |

## Exact write scope

1. `implementations/tests/runtime/policy_denial_harness.py`
2. `implementations/tests/runtime/execution_policy_denial_oracle_v1.json`
3. `implementations/tests/runtime/test_execution_policy_denial.py`

The L2 harness consumes L1 only through
`SyntheticPolicyLineageHarness.reopen_synthetic_lineage(...)`. It may use the existing canonical,
database and error helpers, but must not import L1 private SQL, tables or validators. Production
modules are allowed only as read-only rejection/spy targets in tests.

## Constraints, non-goals and fallback

- `ExecutionPolicyFakeDenialHarness` exposes only `deny_synthetic_attempt(...)` and
  `reopen_fake_denial(...)` as the required public test seam.
- One scalar label is a routing selector only. It is absent from canonical bytes, persisted rows,
  identity, replay and authority.
- Exactly one table, `test_execution_policy_fake_denial_receipts`, is admitted. No artifact,
  migration, journal record, runtime aggregate, event, effect or production export is admitted.
- POLICY-003, product policy values, production fence, provider launch, host enforcement, cutover,
  commit, push and deploy remain deferred.
- Broad repository exploration is allowed only after naming an uncovered obligation. If satisfying
  it requires another write path or changes the claim, stop and return the gap to planning.

## Validation surface

Use exactly the five commands frozen in the task and descriptor after readiness passes. The curated
runtime command excludes `test_agent_continuation_lean_bridge.py`; that bridge is not evidence for
this workpack. Successful commands are implementation evidence only and require subsequent
independent review.

## Next actions

1. Author and independently validate the exact readiness receipt against the task, descriptor,
   current pins, absent outputs and denied capabilities.
2. Only after readiness `PASS`, implement the three-path scaffold.
3. Run the frozen validation surface and obtain independent implementation review without
   promoting the result beyond POLICY-002/L2 test-only evidence.
