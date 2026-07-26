# Review — Phase-A F4/F5/F6 authoring and code-dispatch package

- Review date: 2026-07-26
- Dispatch: `2026-07-26-phase-a-authoring-review`
- Frozen target corpus: 8/8 SHA-256 bindings matched
- Frozen authority corpus: 11/11 SHA-256 bindings matched
- Output mode: persisted
- Overall verdict: **FIX**

## Coverage

| Attacker | Lens | Findings raised | Zero-findings defence |
|---|---|---:|---|
| Hoare | mechanics / correctness | 5 candidates | n/a |
| Liskov | fidelity / governance | 3 candidates | n/a |
| Parnas | ownership / reference integrity | 10 candidates | n/a |

- Collapse note: the three attackers ran independently without `robot_talks`; their overlapping
  findings converged on confirmation/readiness/source-binding defects while their distinct lenses
  also exposed lifecycle handoff and stale-status defects. There was no premature shared synthesis.
- Lens coverage: every attacker verified all 19 bound hashes and attacked all eight target
  artifacts from its declared lens.
- Verification discipline: the parent reproduced every surviving quotation against the frozen
  targets. Findings aimed only at pre-existing authority artifacts, rather than at the eight
  authored/modified targets, were dropped as outside this review's target corpus.

## `phase-a-authoring-review-proposal-v1.json`

| # | File | Evidence quoted from the artifact | Severity | Proposed fix |
|---|---|---|---|---|
| R1 | `plans/governed-agent-work-infrastructure/workstreams/phase-a-authoring-review-proposal-v1.json` | `"confirmation_mode": "owner-explicit-no-repeat-confirmation"`; the proposal records requests/evidence but no embedded final capability-review PASS and two exact-digest check-tension PASS results. | **CRITICAL** | Replace the invented mode with the recognized `final_only`, bind the user's explicit confirmation evidence, and embed all three gate results on the final proposal digest. |

**Verdict:** FIX

The owner did explicitly authorize the three-agent review without another confirmation. That
authorization can satisfy a recognized `final_only` confirmation when bound to the concrete
proposal; it does not create a fifth confirmation mode.

## `SWU-ACI-HOST-BUS-INTEGRITY-001-code-readiness.json`,
`SWU-ACI-HOST-BUS-INTEGRITY-001.json` and `swu-manifest.md`

| # | File | Evidence quoted from the artifact | Severity | Proposed fix |
|---|---|---|---|---|
| R2 | `docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-HOST-BUS-INTEGRITY-001-code-readiness.json`; descriptor; shared manifest | The receipt says `"status": "PASS"`, while the descriptor says `"planner_preflight": "authoring_complete_readiness_pending"` and `"implementation_status": "specified-readiness-pending"`, and the manifest says `readiness pending`. | **MAJOR** | Complete planner preflight, synchronize descriptor/manifest status, then regenerate every digest-dependent readiness/proposal artifact. Until then, do not register the code dispatch. |

**Verdict:** FIX

## `phase-a-host-bus-integrity-code-proposal-v1.json`

| # | File | Evidence quoted from the artifact | Severity | Proposed fix |
|---|---|---|---|---|
| R3 | `plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-code-proposal-v1.json` | It claims `"projection_schema_version": "aci.concrete-dispatch-proposal/v1"` but its seats contain only ledger-level agent fields; it does not bind an exact structural revision/digest, requested provider/adapter, skill bindings, response contracts, or the final capability/tension gate receipts required by the governing strategy. | **MAJOR** | Rebuild the structural and concrete projections with the complete strategy fields and exact final gate evidence before confirmation/registration. |
| R4 | same | Its exhaustive `"source_bindings"` omits `implementations/server/runtime/reveal_delivery.py` and `implementations/server/runtime/migrations/011_bus_reveal_delivery.sql`, although F6 requires minting exact manifest hashes for both active sources. | **MAJOR** | Add both active files as read-only path/SHA-256 bindings and regenerate the proposal digest. |
| R5 | same | The pinned `.claude/skills/domainspec-implement/SKILL.md` requires reading `domainspec/.agents/skills/domainspec-implement/SKILL.md` and `domainspec/.claude/skills/domainspec-implementation-axioms/SKILL.md`, but neither is frozen in the proposal; the bound operations contract also delegates authority to unbound `SPEC.md`/discovery sources. | **MAJOR** | Bind every mandatory procedural and normative authority needed by the code handoff, including the linked implementation skill, axioms, SPEC and discovery authority. |
| R6 | same | The proposal nests the executable row under `"dispatch_record"`, while the registered appender accepts a top-level dispatch row and the proposal defines no digest-verifying extraction/registration step. | **MAJOR** | Add a deterministic bridge that verifies the concrete proposal digest and extracts exactly the frozen `dispatch_record`, or make the confirmed top-level dispatch row itself the appender input with separate proposal evidence. |

**Verdict:** FIX

## `WORK-PACK.md`

| # | File | Evidence quoted from the artifact | Severity | Proposed fix |
|---|---|---|---|---|
| R7 | `docs/features/agents-communication-infra/WORK-PACK.md` | The selection table still labels `SWU-ACI-BUS-DELIVERY-001` as `implemented-verified`, while the frozen Phase-A review says no completed execution receipt exists and requires downgrade until F3 closes. | **MAJOR** | Downgrade the BUS completion status everywhere until a content-addressed F3 completion receipt exists; keep the new F4/F5/F6 repair status separate. |

**Verdict:** FIX

## Artifacts without surviving findings

- `docs/decisions/worker-b-execution-sequence.md` — preserves Phase-A and ACI-005 prerequisites
  and does not inflate provider execution.
- `docs/features/agents-communication-infra/TEST-SPEC.md` — T-ACI-PHASEA-I1–I3 faithfully encode
  F4/F5/F6 negative evidence and make no implementation-completion claim.
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-030.md` — correctly separates
  prerequisite maintenance from SWU-ACI-008 protocol promotion.

## Change requests

1. **CRITICAL:** repair the review proposal's confirmation mode and embed its exact gate evidence.
2. **MAJOR:** make planner/readiness/manifest state consistent and regenerate dependent digests.
3. **MAJOR:** rebuild the code proposal as a complete concrete projection with its structural
   binding, seat fields and gate receipts.
4. **MAJOR:** freeze the two active F6 sources before code confirmation.
5. **MAJOR:** freeze every mandatory procedural and normative authority consumed by the coder.
6. **MAJOR:** define a digest-verifying concrete-proposal-to-appender handoff.
7. **MAJOR:** downgrade the stale `implemented-verified` BUS claim until F3 completion evidence
   exists.

## Final disposition

The review is accepted as a **FIX** deliverable. No code dispatch may register from the current
readiness receipt or code proposal. The next action is bounded authoring repair followed by a fresh
readiness and proposal-gate cycle.

- `exit_reason`: `resolved`
- `agents_spawned`: three independent review explorers; three proposal-gate helpers

