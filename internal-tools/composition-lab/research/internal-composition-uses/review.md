# Review — Internal Uses of Composition: Research Initial Definitions

Target: `research-initial-definitions.md`

## Coverage

| attacker | lens | target coverage | findings raised | zero-findings defence |
|---|---|---|---:|---|
| reviewer 1 | boundary / contract | Entire target | 3 MAJOR | Not applicable |
| reviewer 2 | fidelity / evidence | Entire target | 1 MINOR | Not applicable |

Both reviewers attacked the complete target. The boundary / contract review tested the separation
of context, constraints, evidence, and gaps; searched for embedded methods, corpus choices,
hypotheses, outputs, gates, agent topology, tests, success or stopping criteria, solutions, and
unsupported reduction or generalization from lenses. The fidelity / evidence review tested the
broad objective, the status of lenses as an anchor case, absence of premature research design or
external categories, treatment of gaps as unknowns, separation of evidence kinds, and reference
integrity.

## Resolved findings

| # | file | evidence | severity | correction applied | state |
|---|---|---|---|---|---|
| 1 | `research-initial-definitions.md` | Quoted pre-fix evidence: “The Composition Lab needs to understand these existing uses before composition can be represented, supported, evaluated, or governed more intentionally.” This text no longer appears in the final target. | MAJOR | Removed the research direction from `Context`; the final `Context` only describes the local phenomenon and unresolved distinction. | resolved |
| 2 | `research-initial-definitions.md` | Quoted pre-fix evidence: “The internal comparison includes lenses, skills, workflows, artifacts and knowledge, and interfaces as distinct domains of use.” This text no longer appears in the final target. | MAJOR | Removed the prescribed corpus enumeration from the constraints. | resolved |
| 3 | `research-initial-definitions.md` | Quoted pre-fix evidence: “Existing internal advice identifies skills, workflows, artifacts and knowledge, and interfaces as necessary contrasts to the lens case.” This text no longer appears in the final target. | MAJOR | Removed the normative comparison claim from the evidence baseline. | resolved |
| 4 | `research-initial-definitions.md` | “The repository already treats lens composition as a comparatively rich local case involving distributed perspectives, information boundaries, confrontation of results, and synthesis.” | MINOR | Added the supporting citation `([Research program — “Por que começar com lentes”](../../research-program.md))`. | resolved |

Verification after correction found no regression and no surviving finding.

## `research-initial-definitions.md`

No CRITICAL, MAJOR, or MINOR finding survives verification.

**Verdict:** KEEP

## Change requests

None.

## Close

- `exit_reason`: resolved — all raised findings were corrected and independently rechecked; no
  finding survives.
- `final_approval`: APPROVE — accepted by a dedicated final approver.
- `agents_spawned`: 5 — one author, two independent reviewers (boundary / contract and fidelity /
  evidence), one review writer, and one dedicated final approver.
