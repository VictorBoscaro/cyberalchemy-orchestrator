# Stage 03 — Interrogation Refine Review

Capability: `interrogation`  
Mode: `refine-review`  
Verdict: FLAG

No user question was required: the confirmed seed fixes the objective, transport
families, research boundary, write scope, and proof ceiling. The review asked
the highest-discrimination questions against the definition.

| Question | Answer | Effect |
| --- | --- | --- |
| Can a single bidirectional port preserve addressed commands versus accepted events? | No; method names do not prevent state/owner collapse. | reject A and unsplit B |
| Is journal acceptance part of the transport adapter? | No; it is a separate collaborating owner. | require independent port |
| Can a transport delivery attempt reuse `attempt_id`? | No; `attempt_id` is ambiguous and must become `work_attempt_id`; delivery gets its own ID. | require closed identity table |
| Is “at least once” mandatory for the core? | No; memory and RPC cannot truthfully provide the same cross-crash redelivery semantics. | move guarantee to capabilities |
| Can a message carry `authority_ref` and thereby be authorized? | No; it is an evidence locator requiring current owner validation. | add non-authorizing rule |
| May an adapter retry automatically? | Only transport-internal transparent behavior that cannot create a second application observation; otherwise it reports evidence for RWO classification. | add retry boundary |
| Does a dead-letter outcome mean Work terminal failure? | No. | observation only |
| Can transport replay substitute for journal replay? | No. | distinguish two cursors and zero-call reconstruction |

## Flags

1. Current `DESIGN.md` leaves RWO-OQ-001 journal/domain truth ownership open.
2. The common envelope overloads `attempt_id`, `sequence`, and `occurred_at`.
3. Named profile bundles could become marketing labels unless backed by atomic
   capability atoms, implementation/configuration digests, and negative tests.
4. Effectful command redelivery requires recipient convergence evidence and an
   independent exact-effect unknown-outcome route.

## Definition Review Verdict

Proceed to the frozen bounded research comparison and Distill. Candidate D is
the only family still viable, but it must be reduced to a minimal contract and
owner-gated before Design.

