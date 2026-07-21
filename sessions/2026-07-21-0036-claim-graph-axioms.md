---
tags: [ontology, vault, category-theory, anti-bias, dispatch, ledger]
node_type: premise
is_session: true
layer: ontology, domain
nature: explanatory
status: active
created: 2026-07-21
timestamp: 2026-07-21T00:36:21-03:00
expires: 2026-09-19
conversation_id: unknown
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "Anchors two new axioms and a new assertion-typing hypothesis at the epistemic root of the vault, and repairs a veracity-aggregation error (BET-VERACITY-PROP vs BET-√N) that downstream correctness depends on — but changes no code and leaves the README reconciliation open."
---

# HYP-CLAIM-GRAPH + the axiom layer

## Summary

The session began as a high-level read of the repo (what it is, its theses, whether it coheres)
and became co-design that surfaced and registered new vault structure. It established that the
repo's root thesis is epistemological — the scientific-process / `claim ≤ proof` loop (T0) — of
which decision-science, category theory, and portability are three instances. Two genuinely new
ideas were identified: an **assertion-granularity typing layer** (the [[ontology-conventions]]
edge catalog pushed down to the atomic claim) and a **process-decompositor** (a functor *into*
`ORCH`, a verb that generates residue) that populates it — one machine, ingestion ↔ schema —
authored as [[claim-graph]] (HYP-CLAIM-GRAPH, `premise`). Two foundational commitments were
promoted to an axiom layer in a new [[axioms]]: AX-1 (debiasing is worth pursuing — a value
commitment) and AX-2 (the scientific method is the operating method), with AX-3 recording A6. A
tensioned review dispatch (2 evaluators, attack-vector axis conventions ⊥ epistemic-honesty) was
registered and run; its skeptic found one blocker and several majors. The nodes were revised: the
biggest fix reconciled BET-VERACITY-PROP with BET-√N (veracity aggregates *upward* across
independent premises, not ≤ each premise), and the "dual of H-PORT-6" and "three faces meet"
claims were downgraded to conditional-on-OBL-E3/BET-DECOMP-CHEAP/BET-THALER; analogy-as-identity,
a dead path, and unscoped falsifiers were corrected. On the one decision reserved for the user,
AX-1's agent-transfer half was kept as a testable premise (P-AGENT-TRANSFER) rather than
axiomatized — the user confirmed "premise, to test it." The review dispatch was closed in the
ledger (resolved, 2 agents), closing the A6 self-instance loop.

## Contradictions

- `contradicts` [`README.md`](../README.md) — AX-1 promotes the debiasing-value to a
  commitment/axiom while the README still frames the founding claim as a falsifiable hypothesis;
  reconciliation deferred, blocks promotion of [[axioms]] past `draft`.

## Next steps

1. Reconcile the README "What is this?" paragraph with AX-1 (resolve the open `contradicts` edge)
   — split the founding claim into the value-commitment (axiom) and the agent-transfer/efficacy
   (premises), neither side presupposed as yielding. In `README.md`.
2. Graduate `P-AGENT-TRANSFER` from an inline premise in [[axioms]] to its own hypothesis node and
   design an `experiment` against its falsifier (no countermeasure beats the single-agent
   baseline on a shared base model). In `vault/hypothesis/` (e.g. `p-agent-transfer.md`).

## Recommendation

Attack step 1 first: it is the one open `contradicts` edge, it is cheap, and resolving it unblocks
promotion of [[axioms]] past `draft` — licensed by the contradiction recorded above. Step 2 is
the higher-value but heavier arc (it needs a real experiment); it should follow, not precede, the
README reconciliation.

## Files touched

- vault/axioms.md
- vault/hypothesis/claim-graph.md
- telemetry/agents/subagents-dispatch.yaml
