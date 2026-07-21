---
tags: [ontology, vault, category-theory, dispatch, ledger, anti-bias]
node_type: premise
is_session: true
layer: ontology, domain, architecture
nature: explanatory, reference
status: active
created: 2026-07-21
timestamp: 2026-07-21T23:50:00-03:00
expires: 2026-09-19
conversation_id: 6a204ec8-df5e-462a-b153-8e363cebcb91
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "Restructures the axiom layer into method-invariants/telos/design-stance (fixes AX-2, adds AX-4 independent-check and AX-5 fallibilism) and retires H-META-1 for the successor H-META-1', landing changes at the epistemic root the whole vault derives from."
---

# Axiom invariants and the meta-ontology M

## Summary

The session opened by orienting a newcomer to the repo, then turned to a design question: how to
ground the orchestrator's domain-independence, which the README's H-PORT-6 bridge could not carry
through category theory. It proposed a **meta-ontology `M`** and fixed its shape — four substrates
(domain, documents, a ledger of epistemic units, an operational trace) bound by a provenance spine,
with the ledger recast as a typed knowledge-graph *separate* from the dispatch trace. Two read-only
sweeps of the sibling repo `domainspec-core` (cav2 authority / CANONICAL-KINDS; the ledger family)
were distilled into `research/meta-ontology/SEED.md` + `SOURCES.md`, and `BACKLOG.md` gained BL-1..4.
The owner corrected a fixed-meta-level claim; a locate→review→apply→review dispatch pipeline
propagated it, retiring **H-META-1 (fixed meta-level) → H-META-1'** (governance recursion; no fixed
content level; convergence a candidate, not a fact). The owner then proposed that the fixed layer is
"scientific process + anti-bias"; this was red-teamed, and the red-team itself reviewed by three
opposed agents. The reconciled landing: the hypothesis survives in **normative form** — the anti-bias
*norm* (independent check) and the accountability *form* are invariants, while mechanisms,
articulations, and the empirical label are demoted; generation is pre-methodological; "one motor" is
retired for a structured-plural warrant (`proof ∘ falsification` + stipulation + procedure). Acting on
that, `vault/axioms/axioms.md` was restructured into method-invariants (§1: AX-2 fixed to
type-appropriate warrant + new AX-4 independent-check + new AX-5 fallibilism), a value/telos (AX-1),
and a design stance (AX-3) — an instance of BL-2 applied to the axiom layer. All subagent work ran
through the repo's own dispatch discipline (check-tension → register → close), dogfooding the machinery.

## Contradictions

- validates `vault/axioms/axioms.md` — the axiom-layer red-team's reconciled landing (anti-bias *norm*
  and accountability *form* survive as invariants; mechanisms/articulations and the empirical label
  demoted) licensed the restructure into §1/§2/§3, the AX-2 fix, and new AX-4/AX-5.
- contradicts `README.md` — AX-1 promotes the debiasing-value to a §2 commitment while README still
  frames the founding claim as a falsifiable hypothesis; edge pre-existing in axioms.md, unresolved.
- contradicts `BACKLOG.md` (BL-1) — H-META-1 (fixed/universal meta-level) failed its own
  collapse-test (a) and was retired for the governance-recursion successor H-META-1'.
- validates `BACKLOG.md` (BL-2) — the axioms.md restructure (splitting method-invariant/value/
  design-stance out of one `axiom` label) is a concrete instance of BL-2's de-fusion thesis.
- questions `vault/audit/faces-instance-frozen-map.md` — its deferred decision-moving disjunct
  (*must BL-3's close step enrich `C`?*) is left unbound; scoping BL-3 (below) will force it.

## Next steps

1. Reconcile `README.md` (debiasing framed as a falsifiable hypothesis) with `vault/axioms/axioms.md`
   AX-1 (debiasing as a §2 value commitment) — neither presupposed as the side that yields — before
   either moves up a level.
2. Scope **BL-3** (ledger v-next: typed epistemic-unit graph + provenance spine + `supersede` event) —
   the redesign whose close-step design forces the deferred P-FACES-INSTANCE disjunct (see Contradictions).

## Recommendation

Attack the **README ↔ AX-1 reconciliation** (step 1) first. It is a named, pre-existing contradiction
edge, now reaffirmed by the restructure (the licensing fact: axioms.md's §2 promotion of the
debiasing-value), it blocks either side from moving up a level, and it is cheap next to BL-3 — whose
larger structural work is itself gated by the still-deferred P-FACES-INSTANCE disjunct. Doing the
reconciliation first unblocks the axiom layer's own promotion without waiting on the ledger redesign.

## Files touched

- research/meta-ontology/SEED.md
- research/meta-ontology/SOURCES.md
- research/meta-ontology/axiom-layer-redteam.md
- BACKLOG.md
- README.md
- vault/axioms/axioms.md
- telemetry/agents/subagents-dispatch.yaml
