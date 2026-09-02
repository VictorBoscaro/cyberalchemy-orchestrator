# Task session — SPEC-ACI-DRAFT-GRAPH-001

## Task Session Result

- Task: `SPEC-ACI-DRAFT-GRAPH-001`
- Route: bounded specification/conformance design; no runtime or compiler implementation
- Result: `PASS`; dedicated Recheck 3 returned aggregate `KEEP`
- Objective served: make the LLM-authored boundary small and closed while preserving one complete,
  user-confirmed ExecutionGraph authority.
- Runtime: local documentation work
- Adapter: none
- Handoff pack: none; runtime delegation was not requested
- Strict coverage: pass for the worker scope
- Fallback search: none; all controlling sources existed
- Gate verdict: original F1-F6, later R1-R2 and S1 were repaired; dedicated Recheck 3 returned
  aggregate `KEEP` and opened the bounded successor implementation gate.
- Subagent closeout: `pass`; the worker spawned no agents, and the parent-owned dedicated reviewer
  completed Recheck 3 with aggregate `KEEP`.
- Experiment harness: not applicable
- Synchronized records: this file, `VALIDATION.md`, and the successor `WORK-PACK.md`; the final
  closeout is recorded in the implementation follow-up. Feature `CRAFT.md`, `.craft/ledger.yml`
  and canonical specs were intentionally not changed.

## Context pack

Mode was standard with strict obligation coverage. The repair added `review.md` as the tenth
explicit source. Markdown
sources were limited to controlling decisions/status/acceptance selectors; the complete proposed
schema and toy JSON were necessary because the task requires field-complete ownership and fixture
derivation.

| Source | Controlling selectors | Obligations |
|---|---|---|
| `sessions/2026-09-01-1524-aci-execution-graph-refinement.md` | summary, open questions, next steps, recommendation | O1, O2, O9 |
| refinement `RESULT.md` | conclusion, tested boundary, residue | O1, O8, O9 |
| `execution-graph-v2.proposed.schema.json` | complete structure and all 105 leaf paths | O2, O3, O4 |
| `ARCHITECTURE.md` | authority/evidence namespaces, sequence, content/secrets, material change | O1, O4, O5 |
| `review-correct-verify-toy-graph.json` | complete source fixture | O2, O3, O6 |
| `DESIGN-REVIEW.md` | repaired defects, toy evidence ceiling, placeholder-ref residue | O4, O6, O8 |
| stage-09 `WORK-PACK.md` | acceptance, negatives, stop conditions, non-goals | O4, O7, O9 |
| feature `CRAFT.md` | current boundary and active contract gap only | O1, O9 |
| feature `.craft/ledger.yml` | canonical graph decision and active gap rows only | O1, O9 |
| local `review.md` | F1-F6 and Recheck R1-R2/S1 evidence, consequences and change requests | O1-O12 repair coverage |

### Obligation matrix

| ID | Obligation | Evidence produced | Status |
|---|---|---|---|
| O1 | Preserve one non-authoritative draft and one authoritative EG | compilation boundary and task record | covered |
| O2 | Classify every relevant EG field | `FIELD-OWNERSHIP.md`, 105-leaf inventory | covered |
| O3 | Produce a closed Draft 2020-12 schema and derived draft | schema + positive draft validation | covered |
| O4 | Specify exact deterministic compilation and errors | `COMPILATION-CONTRACT.md` | covered |
| O5 | Make policy monotone: restrict/reject, never widen | policy fixture, contract and subset checks | covered |
| O6 | Supply explicit frozen context/policy/catalog/resource fixtures and expected EG | `fixtures/` + expected graph | covered |
| O7 | Cover required negative cases | `NEGATIVE-VECTORS.md`, precondition checks | covered |
| O8 | State the evidence ceiling and actual validation | `VALIDATION.md` and explicit no-compiler claim | covered |
| O9 | Define gated next SWU without changing canonical/ledger state | local `WORK-PACK.md` | covered |
| O10 | Synchronize successor inputs, vectors/results and KEEP/FIX gate vocabulary | repaired `WORK-PACK.md` | covered |
| O11 | Prove output-field pointer existence and scalar schema admission on draft and emitted EG | contract, N19/N20 and permanent attacks | covered |
| O12 | Require literal exact object/array ancestor types and reject typeless/nullable traversal symmetrically | contract, N21-N24 and permanent scalar/null attacks | covered |

## Decisions and assumptions

| ID | Classification | Selection | Reason / review concern |
|---|---|---|---|
| D1 | inherited decision | derive the draft from the current JSON | owner direction; avoids a competing model |
| D2 | technical decision | draft uses exact symbolic keys; catalog supplies immutable refs | prevents the LLM from inventing refs/digests |
| D3 | technical decision | system allocator owns frozen dispatch identity/revision; local aliases map only subordinate graph IDs | removes LLM control over the authority pair |
| D4 | inherited/refined decision | node inputs own data mapping; data edges are derived | removes duplicate authoritative mappings |
| D5 | technical decision | numeric components restrict first, then all effective node reservations must fit effective global limits | makes 30k/24k a typed failure and prevents rebalancing |
| D6 | technical decision | semantics and audit constants come from policy; content/refs from explicit fixtures | gives every output field one source |
| D7 | review-needed assumption | proposed `aci-cjson-1` is RFC 8785 UTF-8 JCS | necessary to make bytes deterministic; not proven or promoted here |
| D8 | inherited assumption | all current EG bytes, including display names, affect authority | matches conservative material-change rule; canonical-v2 review may remove presentation-only fields |
| D9 | boundary clarification | `objective.done_when` remains purpose prose, not executable control | runtime control is only closed predicates, per-node validation rules and lifecycle |
| D10 | fail-closed repair | DraftGraph v1 supports only command deny/empty | no complete argv/cwd/environment admission case exists |
| D11 | semantic repair | success predicates may prove only required validated outputs | failure predicates remain stop/failure-only |
| D12 | fail-closed semantic repair | output-field pointers walk only explicit properties/items and directly provable type/const/enum schemas | missing, composite or incompatible values cannot become control |
| D13 | exact-ancestor-type repair | every object/array traversal ancestor must declare literal exact `type`; absent, union and nullable types are unprovable | applicator keywords alone do not constrain scalar/null instances |

No blocker-level product choice was discovered. D7 and D8 are explicit independent-review targets;
they do not authorize promotion or code entry.

## Gates

- Dependencies: pass; all ten controlling artifacts existed.
- Write scope: pass; every new file is under the assigned follow-up directory.
- Preexisting changes: preserved; feature CRAFT/ledger and unrelated dirty files were not edited.
- Authority boundary: pass at proposal level; draft is never confirmed or consumed by runtime.
- Deterministic sources: pass for the fixture; every ref/content value is explicit and digest checked.
- Validation path: pass; Python 3.12.2 with `jsonschema` 4.21.1 was available.
- Independent review: final Recheck 3 is aggregate `KEEP`; F1-F6, R1-R2 and S1 are resolved within
  the review's bounded evidence ceiling.

## Produced evidence

- `FIELD-OWNERSHIP.md`
- `draft-graph-v1.proposed.schema.json`
- `review-correct-verify.draft.json`
- `review-correct-verify.expected.execution.json`
- `COMPILATION-CONTRACT.md`
- `fixtures/catalog.json`
- `fixtures/compilation-context.json`
- `fixtures/policy.json`
- `fixtures/resources.json`
- `NEGATIVE-VECTORS.md`
- `VALIDATION.md`
- `validate_artifacts.py`
- `WORK-PACK.md`

## Remaining residue

- This specification SWU itself ran no compiler; the separately reviewed successor now provides a
  fixture-backed pure compiler and conformance evidence without promoting canonical v2.
- This specification SWU itself did not prove RFC 8785 canonicalization; the successor implements
  only the reviewed bounded adapter used by its conformance corpus, not general RFC 8785 coverage.
- Policy/catalog/resource fixture formats were closed here by contract prose; their implementation
  schemas belong to the separately reviewed successor package.
- Credential resolution remains specified without a positive fixture. Commands are deliberately
  unsupported and structurally denied in DraftGraph v1; a future allowlist needs its own full-tuple
  spec and positive/negative conformance package.
- DraftGraph v1 deliberately rejects composite/ref-based output-pointer proof and traversal through
  absent, union or nullable ancestor types; extending beyond direct exact-type properties/items plus
  type/const/enum needs a separately reviewed resolver contract.
- The canonical v2 graph/view/confirmation/ingestion specification and CONF v1 cutover remain open.

## Decision Gate Result

- Target scope: this worker SWU
- Result: `n/a`
- Decisions resolved: 0 product decisions; 10 bounded technical selections/clarifications recorded
- Blockers remaining: 0 for this specification SWU; successor code entry passed and the bounded
  implementation later received its own aggregate `KEEP`
- Decision artifact: none
- Next step: use the reviewed SPEC+IMPL corpus only as input to the still-open canonical-v2
  specification work; do not infer projector, confirmation, persistence or runtime readiness
