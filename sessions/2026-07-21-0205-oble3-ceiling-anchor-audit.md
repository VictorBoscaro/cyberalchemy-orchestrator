---
tags: [category-theory, residue-functor, obl-e3, synthesis-under-tension, cross-repo-pinning, ontology-governance, dispatch-ledger]
node_type: audit
is_session: true
layer: ontology, architecture
nature: technical
status: active
created: 2026-07-21
timestamp: 2026-07-21T02:05:45-03:00
expires: 2026-09-19
conversation_id: c4fa472b-a6c1-4423-8339-a1bcebea2518
decisions_made: true
contradictions_found: true
specs_updated: [README.md, OBLIGATIONS.md, MAPPING.md, definitions/DEFINITIONS.md, FRAMINGS.md, PLAN.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Corrected a real overclaim across six governing docs about what OBL-E3 sub-3 closes, and opened a concretely-scoped next target (synthesis as the second residue instance) pinned by reference rather than copy."
---

# OBL-E3 ceiling correction + residue-anchor audit

## Summary

The session began as an evaluation request: read the README and judged the orchestrator's proposal, separating the runnable substrate (dispatch discipline, ledger, control plane) from the unproven category-theory thesis. To ground the verdict, subagents swept three sibling repos (domainspec, business-philosopher, domainspec-lean-formalization) to test whether the CT grounding is rigorous or metaphorical. The finding: the residue functor (`FunctorialResidueStructure`, sorry-free) genuinely anchors "residue = shadow ⊕ structure" and proves the thin⇒count / enrich-C⇒separate lever, but only on the diamond toy, and a second morphism-level instance is an OPEN prize in `PRIZES.md`. We decided the highest-value move is proving synthesis-under-tension as that second instance, which would also discharge OBL-E3 sub-3. Two writer subagents authored a two-part brief into the sibling repo `../domainspec-lean-formalization/TO-ME/oble3-synthesis-as-second-residue-instance/` (00 motivation, 01 technical Lean design). The technical writer corrected two overclaims: the refinement orientation (`synth ≤ concat`), and that synthesis clears only the *separation* bar — not the *invariant-factor* prize (closed-negative over concrete `Ab`). We decided to anchor by pinned reference (`domainspec-lean-formalization @ 6edb664`), never to copy Lean files, honoring single-writer + portability. Six repo docs were then corrected to stop implying OBL-E3 sub-3 closes the prize; two opposed reviewers caught inherited broken anchors and README/PLAN/FRAMINGS leaks. I verified the true line numbers via grep (`:97→:120`, `:513→:545`, `tierC_pigeonhole_not_injective` in `DiamondResidueInvariantFactors.lean:408`) and applied a full corrective pass, consolidating the ceiling mechanism single-source in OBLIGATIONS sub-3. All dispatches were registered and closed in the ledger; the only unpaid claim left is "sorry-free", hedged as not build-gate-verified this session.

## Contradictions

- questions OBLIGATIONS.md (OBL-E3 sub-3) — found and fixed an overclaim implying sub-3 closes the invariant-factor prize; it only clears the separation bar, and the closed-negative-over-`Ab` prize (`PRIZES.md:67`) stays open.
- validates definitions/DEFINITIONS.md (DEF-ORCH-001) — the sibling sweep confirmed "residue = shadow ⊕ structure" is anchored to a real, sorry-free decl (`FunctorialResidueStructure @ 6edb664`), though proven only on the diamond toy; the anchor was line-corrected and SHA-pinned, with the sorry-free status hedged as true per source + repo audit but **not** build-gate-verified this session.
- questions README.md — carried the pre-ceiling framing ("half the way to discharging sub-3"); added the separation-vs-invariant-factor caveat.
- questions PLAN.md — carried the pre-ceiling collapse-test framing; added the separation-bar-only pointer to OBL-E3 sub-3.
- questions FRAMINGS.md — inherited stale Lean anchors (`:97→:120`, `:513→:545`, `ofAntitoneSet :162→:189`) with no SHA pin; corrected.

## Open questions

- Is the orchestration `synthesis` fibre (`AgentOut`) a *real register*, or another toy like the diamond's `Bool` fibres? This is the anti-toy condition that decides whether a `SynthesisResidue` instance is a genuine second morphism-level residue rather than a `MergeResidue` reskin — undecided, and it lives or dies on the fibre's actual structure.

## Next steps

1. Run `lake build` + `#print axioms` in `domainspec-lean-formalization @ 6edb664` and replace the "sorry-free per source" hedge with "verified @ 6edb664" across the six anchors (OBLIGATIONS/DEFINITIONS/MAPPING/FRAMINGS).
2. Execute `../domainspec-lean-formalization/TO-ME/oble3-synthesis-as-second-residue-instance/01-technical-approach.md`: write `SynthesisResidue.lean` — the `Paths`-category sequential fragment (sub-1/sub-2, free) plus the synthesis separation-bar instance mirroring the diamond (sub-3).

## Recommendation

The keystone is Next step 1: the build-gate verification is cheap and licensed — Contradictions edge 2 records the DEF-ORCH-001 anchor as accurate and sorry-free per source + repo audit, with only the build-gate re-verify pending. Do it first to close the last `claim ≤ proof` gap. Then attempt Next step 2, whose live risk is exactly the Open question above; self-labeled hunch (from the technical brief, not a landed proof) that synthesis clears the *separation* bar but not the invariant-factor prize.

## Files touched

- README.md
- OBLIGATIONS.md
- MAPPING.md
- definitions/DEFINITIONS.md
- FRAMINGS.md
- PLAN.md
- telemetry/agents/subagents-dispatch.yaml
