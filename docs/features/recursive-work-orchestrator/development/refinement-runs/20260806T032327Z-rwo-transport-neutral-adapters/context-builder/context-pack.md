# Context Pack: Transport-Neutral RWO Adapters

Pack kind: runtime handoff session evidence  
Mode: standard, strict, emit both  
Run ID: `20260806T032327Z-rwo-transport-neutral-adapters`  
Claim ceiling: candidate design and non-executed plan

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Preserve command/event lane separation. | `DESIGN.md` §6 | covered |
| O2 | Separate protocol delivery from journal acceptance. | `DESIGN.md` §6, §7, RWO-OQ-001 | covered; owner gap retained |
| O3 | Define immutable RWO identity versus transport metadata. | `DESIGN.md` §6.1; recovery candidate §7 | covered |
| O4 | Model heterogeneous delivery semantics without false guarantees. | frozen official transport sources in seed | covered |
| O5 | Distinguish reconnect, redelivery, new Work Attempt, repeat, replay, and effect reconciliation. | recovery candidate §§2–7 | covered |
| O6 | Define capability declaration and admission proof. | `DESIGN.md` RWO-I12; seed questions | covered |
| O7 | Keep domain, ARE, ACI, and exact-effect authority outside adapters. | `DESIGN.md` RWO-I10; recovery candidate §§8, 10 | covered |
| O8 | Permit a truthful limited in-memory adapter. | seed; transport comparison | covered |
| O9 | Provide transport-family mappings. | gRPC, Redis, CloudEvents, EventBridge sources | covered at design level |
| O10 | Provide negative conformance fixtures. | seed done criteria; recovery games | covered as planned fixtures |
| O11 | Identify ontology delta without mutating ontology. | `ontology/ONTOLOGY.md` nodes/relations/profiles | covered |
| O12 | Produce a non-executed owner-gated plan. | Refine and Invoke Plan contracts | covered |

Strict coverage: PASS. O2 remains a named downstream owner gate rather than an
uncovered obligation.

## Selected Evidence

| Source | Selectors | Obligations | Why included |
| --- | --- | --- | --- |
| `DESIGN.md` | §§4.3, 6, 6.1, 6.2, 7, 8, 10–15 | O1–O8, O11 | current RWO proposal and open delivery/journal boundary |
| prior recovery `RESULT.md` | treatment, identity, owner-gate summaries | O3, O5, O7 | separates delivery, execution, and effect recovery |
| prior recovery `stages/08-distill-repair.md` | §§2–10, 13 | O2, O3, O5, O7, O10 | exact candidate recovery and atomic acceptance model |
| `ontology/ONTOLOGY.md` | WorkProtocol, Journal, ExecutorAdapter, profiles, shields | O2, O7, O11 | current explanatory graph vocabulary and missing adapter concepts |
| `REFINE-SEED-PROPOSAL.md` | exact questions, deliverables, invariants | O1–O12 | confirmed scope and proof ceiling |
| official source set | exact URLs in seed | O4, O8, O9 | current transport-semantics comparison only |

## Evidence Versus Inference

Evidence establishes that transport families expose different retry,
acknowledgement, ordering, durability, replay, fan-out, and flow-control
behavior. The selected RWO adapter shape is an inference to be tested. No
source selects it, and no source proves runtime conformance.

## Authority Precedence

1. User-confirmed material scope and repository owner contracts.
2. Current `DESIGN.md` for candidate RWO semantics.
3. Prior recovery candidate for internal identity/recovery consistency.
4. Current ontology only as a non-authority explanatory projection.
5. External primary sources only for transport behavior, never RWO ownership.
6. Delegated returns are advisory attacks consumed after design authoring.

## Constraints And Non-Goals

- Writes stay in this run folder except the already-closed dispatch ledger.
- No current design, ontology, runtime, definitions, ARE/ACI, or transport
  implementation is mutated.
- No adapter, broker, profile, or conformance suite is selected as implemented.
- No delivery behavior implies exactly-once business effects.

## Fallback Exploration Rule

If a detail cannot be supported by the selected sources, record an owner gap or
planned fixture. Do not browse beyond the frozen source set, infer authority,
or invent a transport guarantee.

