---
node_type: robot-talks-findings
status: accepted
date: 2026-08-10
topic: superinterviewer-repository-foundation
---

# Findings — Superinterviewer Repository Foundation

## Direct Result

The smallest defensible foundation is a product-owned research repository with explicit separation
between product authority, research context, research planning, bounded investigations, evidence,
and decisions. It should begin below the weight of a complete `mint`, treat execution systems as
external peers/providers, and integrate repositories and tools through pinned references and narrow
contracts rather than wholesale inheritance. These are Robot-Talks findings, not authorization to
create the repository.

## Evidence Coverage

| investigator | concern | report |
|---|---|---|
| Product and Research Authority | Product identity and research hierarchy | `reports/01-product-research-authority.md` |
| Authority and Scaffold | Scaffold, authority mold, casting, closure, and executable precedents | `reports/02-authority-scaffold.md` |
| Integration and Execution Boundary | Ownership, dependencies, execution, observability, and provenance | `reports/03-integration-execution-boundary.md` |

All three investigators returned evidence-backed findings. They worked across overlapping corpora
from distinct concerns; no report was partitioned by repository.

## Cross-Layer Tensions

### T1 — Product authority versus research-program authority

- **Product layer holds:** the Superinterviewer must remain the primary interface and intellectual
  partner; it cannot become merely a consumer of a generic framing or research framework.
- **Research layer requires:** a large, revisable program whose findings may challenge the original
  frame, without silently rewriting product identity.
- **Impact:** HIGH. A single undifferentiated founding document would either freeze hypotheses as
  product law or allow research prose to mutate product commitments without a decision.
- **Evidence:** `reports/01-product-research-authority.md`, Key Findings 1, 3 and 4; Local Tensions
  “Primary interface vs. research-program owner” and “Master authority vs. informational artifact.”
- **Candidate correction:** separate a product charter, master informational context,
  `research-plan`, scoped investigations/findings, and an explicit decision register with declared
  precedence and mutation rules.
- **Acceptance test:** a branch finding can contradict the current product frame without modifying
  the charter until a named decision accepts, rejects, or reframes it.

### T2 — Clean new repository versus untested necessity

- **Current direction holds:** the Superinterviewer needs a clean starting point outside
  `cyberalchemy-orchestrator`.
- **Evidence layer shows:** no comparison has yet falsified lighter isolation mechanisms; the new
  repository is well motivated but not empirically necessary.
- **Impact:** MEDIUM. Calling the repo boundary “proven” would overstate evidence, while treating it
  as wholly open would ignore the owner's stated direction.
- **Evidence:** `reports/01-product-research-authority.md`, Key Finding 2 and Gaps 4.
- **Candidate correction:** record “new repository” as an explicit owner decision with a named
  rationale and revisit condition, not as a research result.
- **Acceptance test:** the founding decision states what cleanliness protects and what evidence
  would justify consolidation or migration later.

### T3 — Research-first protection versus empirical prototypes

- **Research governance holds:** implementation must not answer open questions accidentally.
- **Product evidence requires:** minimal experiments and a real prototype will eventually be needed
  to distinguish a partner from a persuasive chatbot with memory.
- **Impact:** HIGH. A permanent no-code posture prevents product evidence; premature architecture
  launders implementation choices into conclusions.
- **Evidence:** `reports/01-product-research-authority.md`, Key Finding 5 and Local Tension
  “Research-first vs. empirical learning.”
- **Candidate correction:** make research-first an evidence gate: no architectural commitment before
  a question, discriminating experiment, expected evidence, and acceptance decision are explicit.
- **Acceptance test:** every prototype names the uncertainty it tests and cannot promote its own
  implementation choices into product authority.

### T4 — Complete `mint` authority spine versus proportional bootstrap

- **Governance machinery holds:** `mint` offers a useful mold/casting distinction and provenance
  discipline.
- **Execution evidence shows:** `mint` is not shipped or proven end-to-end; available witnesses are
  manual, scratch-only, incomplete, or leave authority unratified.
- **Impact:** HIGH. A full casting would import salience and taxonomy before the research discovers
  local needs, while claiming an operational foundation that has not been demonstrated.
- **Evidence:** `reports/02-authority-scaffold.md`, all Key Findings; Local Tensions “Casting mínimo
  vs closure obrigatória” and “Gate-first vs programa de pesquisa.”
- **Candidate correction:** reuse the mold/casting boundary, provenance, default-deny posture, and
  source attribution; begin with a minimal local casting rather than the Universal Governance
  Baseline or a full inherited vault.
- **Acceptance test:** every initial authority artifact has an immediate consumer and no copied
  object-level kind is binding merely because it existed upstream.

### T5 — “Subordinate infrastructure” versus peer product boundary

- **Superinterviewer framing holds:** execution capabilities serve the human-facing partner.
- **SWI's own product model holds:** `subagent-work-infrastructure` is a unified product with its own
  Workflow, Dispatch, Run, communication, observability, and recovery authorities—not an internal
  module of the Superinterviewer.
- **Impact:** HIGH. Treating SWI as subordinate erases its authority; importing its ontology as the
  Superinterviewer's core lets a peer product prematurely delimit the research model.
- **Evidence:** `reports/03-integration-execution-boundary.md`, Key Finding 2 and Local Tension
  “Produto Superinterviewer vs. produto SWI.”
- **Candidate correction:** treat SWI as a peer/provider candidate behind an anti-corruption edge.
  The Superinterviewer owns intent, product behavior, research questions, evaluation, and acceptance;
  SWI may own generic execution contracts when a stable interface exists.
- **Acceptance test:** either side can evolve its internal ontology while a narrow mapping connects a
  local research action to an external execution and returns evidence plus identity.

### T6 — Exact lineage versus accidental architectural inheritance

- **Evidence governance requires:** sources, executions, and results must be reproducibly attributable.
- **Repository boundaries require:** broad submodules, copied frameworks, local junctions, and runtime
  hooks must not become the project's architecture by default.
- **Impact:** HIGH. Loose paths lose reproducibility; wholesale imports create authority, drift, and
  portability costs.
- **Evidence:** `reports/02-authority-scaffold.md`, Local Tension “Clone-safe vs reuse vivo”;
  `reports/03-integration-execution-boundary.md`, Key Findings 1, 3–5 and Local Tension “Lineage exata
  vs desacoplamento.”
- **Candidate correction:** use dependency-by-concern with `repository + revision/digest + path +
  selector`; snapshot only when no durable licensed locator exists. Add a minimal execution-link
  contract without requiring a ledger, scheduler, database, or host hooks at inception.
- **Acceptance test:** every load-bearing external claim resolves reproducibly, while removing an
  execution provider does not erase the product or research authority.

## Rejected Conclusions

- The Superinterviewer repository should inherit DomainSpec, `domainspec-core`, Arcanum, Lean, or SWI
  wholesale.
- A closed universal authority taxonomy is required before research begins.
- A completed dispatch or observable receipt is itself accepted research evidence.
- Research-first means prototypes are permanently forbidden.
- The Prompt-Mestre, master initial definitions, and research plan are one document with one authority.

## Human Gate

| decision | proposed disposition | human disposition |
|---|---|---|
| Create a new clean repository | Record as an owner decision with rationale and revisit condition | Accepted 2026-08-10 |
| Separate charter, master context, research plan, investigations, findings, and decisions | Accept as the founding authority split | Accepted 2026-08-10 |
| Bootstrap through full `mint` | Reject for inception; reuse only evidenced mold elements | Accepted 2026-08-10 |
| Relationship to SWI | Treat as peer/provider candidate, not subordinate module | Accepted 2026-08-10 |
| Initial dependency policy | Narrow pinned references and contracts; default-deny broad imports | Accepted 2026-08-10 |
| First implementation | Permit only after a discriminating research/experiment gate | Accepted 2026-08-10 |

The user accepted all six dispositions on 2026-08-10. This authorizes planning the research and
bootstrap; it does not by itself authorize repository creation or implementation.
