# Runtime Handoff Pack: RWO Domain Recovery Model

## Identity

- Task/SWU: `refine-20260805T184601Z-rwo-domain-recovery-model:s01`
- Source task/work-pack: `REFINE-SEED-PROPOSAL.md` and `REFINE-DISPATCH.json`
- Session/run id: `20260805T184601Z-rwo-domain-recovery-model`
- Session evidence path: `context-builder/`
- Runtime handoff: `runtime`
- Target repository revision: `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`
- Umbrella repository revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Evidence date: `2026-08-05`

## Obligation Coverage

| Obligation | Status | Selected evidence | Resolution |
| --- | --- | --- | --- |
| `O1-IDENTITY` | covered | `DESIGN.md` §4.1–4.2, §6.1; findings implementation matrix | Definition, run, node path, attempt, message, correlation, causation, and idempotency identities are distinct. |
| `O2-RECOVERY-TAXONOMY` | covered | `DESIGN.md` §5.6, §11; accepted findings smallest contract and negative controls | Existing semantics distinguish bounded repeat, same-key redelivery, duplicate conflict, restart, stale attempt, cancellation, and compensation; the missing closed taxonomy is the refinement target. |
| `O3-DOMAIN-BOUNDARY` | covered | `DESIGN.md` §6.3, §7–8; ontology inference shields | Domain event names and domain state remain work-owned; kernel event classifications and cursor are structural only. |
| `O4-CLASSIFIER-AND-POLICY` | resolved | seed exact-model questions; `DESIGN.md` RWO-I04, I06, I12 | No existing classifier contract exists. The run may design a candidate deterministic classifier, but owner selection and implementation remain deferred. |
| `O5-REPLAY-RESUME-REVALIDATE` | covered | `DESIGN.md` I11 and §11; findings RWO/ARE matrix; bridge replay/revalidation rows | Restart/resume rebuilds from accepted history; historical replay is immutable and side-effect-free; current revalidation creates a new run. |
| `O6-EFFECT-UNCERTAINTY` | covered | `DESIGN.md` I10 and §11; ontology no-idempotency-effect-proof shield; bridge exact-effect/effect-lifecycle rows | Message idempotency is not effect idempotency. Unknown outcome stays honest unknown and requires the exact-effect/effect owner path before another attempt. |
| `O7-RWO-ARE-ACI` | covered | accepted findings exact matrix and topology verdicts; bridge conditional stage map and non-collapse constraints | RWO coordinates; ARE derives semantics; ACI accepts lifecycle/effect intents and owns one journal; separate owners admit artifacts and exact effects. |
| `O8-ONTOLOGY-DELTA` | covered | ontology §6–8, §12–13; graph nodes; validation receipt | The current graph is structurally valid and non-authoritative, but contains zero recovery/retry/reconciliation-labelled nodes. Any delta remains a proposed later owner route. |
| `O9-OUTPUT-AND-SCOPE` | covered | seed required deliverables/write scope; dispatch s01–s10 and gates g05/g07 | The run must produce exact candidate design and non-executed planning evidence only inside this folder. |

Strict coverage: `pass`

## Selected Sources

- `REFINE-SEED-PROPOSAL.md`
  - Selectors: Current Evidence Boundary; Problem To Refine; Exact-Model Questions; Required Model Deliverables; Done Criteria.
  - Obligations: O1–O9.
  - Evidence summary: fixes the intended distinctions, counterexamples, proof ceiling, write scope, and forbidden mutations.
- `REFINE-DISPATCH.json`
  - Selectors: route menu; overlays; subagent strategy; steps s01–s10; gates g01–g08.
  - Obligations: O1–O9.
  - Evidence summary: validated execution order, technique trace, receipt expectations, helper boundary, and promotion guardrails.
- `../../../DESIGN.md`
  - Selectors: §4.1–4.2; §5.6; §6.1–6.3; §7–8; §10–11; §14–15.
  - Obligations: O1–O6, O8.
  - Evidence summary: immutable definition/run identity, delivery baseline, event classifications, state ownership, routing algorithm, invariants, and partial recovery semantics.
- `../../../ontology/ONTOLOGY.md`
  - Selectors: §6–8; §12–13.
  - Obligations: O3, O5, O6, O8.
  - Evidence summary: non-collapse shields, observation ceilings, retry/rework/completion residue, cross-owner gaps, and current validation posture.
- `../../../ontology/nodes/nodes.json`
  - Selectors: case-insensitive label/id query for `recover|retry|reconcil`.
  - Obligations: O8.
  - Evidence summary: query result count is zero; current ontology has no materialized recovery-specific node family.
- `../../../../../../../../ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/findings.md`
  - Selectors: Proposal-only RWO; implementation matrix; exact RWO/ARE matrix; topology verdicts; smallest safe contract; negative controls; residue.
  - Obligations: O1, O2, O5–O8.
  - Evidence summary: current target precedents are partial, redelivery must be split from new attempt, and RWO/ARE/ACI/effect boundaries remain separate and mostly unimplemented.
- `../../../../../../../../cyberAlchemy-v2/development/agent-reasoning-engine/design/rwo-integration/ONTOLOGY-BRIDGE.md`
  - Selectors: Boundary; conditional stage map; required sequence; topology dispositions; non-collapse constraints; F1–F8; open questions.
  - Obligations: O5–O7.
  - Evidence summary: private documentation candidate defining conditional semantic/effect seams, honest unknown outcomes, replay/revalidation split, and unresolved owners.
- `../../../ontology/receipts/CURRENT-STATE-2026-08-05-VALIDATION.json`
  - Selectors: validation results and authority effect.
  - Obligations: O8.
  - Evidence summary: current ontology graph validation evidence; it is not proof of recovery semantics or runtime behavior.

## Architecture Guidance

- Model recovery as a decision over typed facts, declared policy, and accepted history; do not put domain semantics into the RWO kernel.
- Preserve six different identity transitions: same message, new Attempt, new repeat round, new WorkRun, replay/resume without new execution, and separate effect reconciliation/compensation work.
- Apply fail-closed precedence before scheduling. Conflict, stale observation, restart, and unknown external effect must be handled before ordinary retry eligibility.
- A domain may map its event to domain meaning and recovery category, but it cannot allocate attempts, bypass budgets/fences, authorize effects, rewrite journal truth, or turn ARE output into routing permission.
- ARE may evaluate admitted immutable semantic inputs. It does not own WorkRun/Attempt lifecycle, ACI acceptance, artifact admission, exact-effect authority, or effect attempts.
- Keep all produced terms candidate-local until design review and later ontology/definition owner routes.

## Related Feature Context

The current RWO design already models WorkDefinition, WorkRun, Attempt,
BoundedRepeat, WorkProtocol, Journal, OrchestrationCursor, ExecutorAdapter, and
AuthorityReference. The refinement fills the semantic gap between a domain
failure observation and one structurally safe treatment; it does not replace
those objects.

## Constraints And Non-Goals

- No exactly-once business-effect claim.
- No second scheduler or integrated journal.
- No domain-status, semantic-judgment, or effect-authority ownership in RWO.
- No lifecycle route from a projection, recommendation, route label, or stale observation.
- No runtime compatibility, host binding, schema acceptance, or implementation claim.
- No canonical definition or ontology promotion.

## Write Scope

- `docs/features/recursive-work-orchestrator/development/refinement-runs/20260805T184601Z-rwo-domain-recovery-model/`

## Validation Surface

- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py <run>/REFINE-DISPATCH.json --json`
- JSON parse and cross-reference checks for every structured artifact and receipt.
- Decision-table coverage for every disposition and precedence branch.
- Negative scenarios for unknown effect, divergent duplicate, stale attempt, replay side effects, changed authority/input, and ambiguous mapping.
- Final Interrogation verdict before Refine synthesis.

## Gaps And Blockers

- `G1-JOURNAL-OWNERSHIP` — deferred owner decision: accepted history versus domain source-of-truth affects reconciliation but does not block a candidate interface that preserves both references.
- `G2-EFFECT-OWNER` — deferred owner decision: exact-effect and reconciliation owners are absent; candidate contracts must represent the missing owner as a block.
- `G3-ARE-CONFORMANCE` — deferred: no executable RWO-to-ARE seam exists; design may specify a boundary but must not claim compatibility.
- `G4-DESIGN-SELECTION-VALIDATOR` — the full Invoke Design denominator/selection runtime is not established for this target-local refine run. The design can reach `authored-complete`, but normal mutation-capable Plan handoff remains blocked unless the evidence state becomes `design-validator-pass`.

No gap requires external research. All are local owner, contract, or execution-evidence gaps.

## Authority Precedence

1. Direct owner sources and accepted evidence receipts.
2. Current RWO design proposal.
3. Current RWO ontology as a non-authoritative explanatory view.
4. Refine-run candidate artifacts.
5. Projections and helper criticism, which never create authority.

## Fallback Exploration Rule

Broad repository exploration is allowed only for a gap named above or a new
obligation gap recorded before exploration. Extra sources must be added to the
context index with the obligation they close.

## Provenance

- Target revision: `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`
- Umbrella revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- `DESIGN.md`: `sha256:28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
- `ontology/ONTOLOGY.md`: `sha256:b0b83ea540c0f805208b93e068816c45cb928d4f08eea50eca8ba4178843d9e1`
- `ontology/nodes/nodes.json`: `sha256:ef78619eb5626cfca41fdfcdcf7dfc9a03ebd93f5d98f5e880c71e2807d74195`
- accepted findings: `sha256:734a3122359f8cefd0c13fee36b6b2caabf5d158693b588a3678f138bd1941c1`
- private bridge: `sha256:fa85aeccd36069531f57674204b3da51aa1fbd0433e9f69579035ec574424e97`
- ontology validation receipt: `sha256:b18128258a143c94908960324fde803815a32b05a21c444ccca68fb87e1544fd`
- seed: `sha256:b6800f4090cd635f9c675b98653dbf2cce873d1f0918983b3b689f356967979f`
- dispatch: `sha256:65d93921b564fe82ed1da4471e31a82ff39781cc6d56294eead664b3482f58c4`
- Builder mode: `standard`, strict, emit both, runtime handoff.

## Output Paths

- Markdown: `context-builder/context-pack.md`
- JSON/index: `context-builder/context-pack.json`

