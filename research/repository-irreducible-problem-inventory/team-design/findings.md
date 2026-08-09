---
tags: [irreducible-problems, research-team, subagents, candidate-inventory]
artifact_kind: findings
layer: project
status: proposed
version: 0.1.0
created_at: 2026-08-06
updated_at: 2026-08-06
---

# Team Design — Repository Irreducible Problem Inventory

## Decision frame

The next stage should produce a useful, evidence-linked inventory of candidate problems and
relationships. It may state hypotheses and unresolved alternatives. It does not need to prove
irreducibility, minimality, or completeness.

The exploration already supplied three broad perspectives and a candidate family structure. The
largest evidence gap is not another unrestricted local scan: it is the under-sampled authority
material in `../domainspec-core`. The second need is a structurally different analysis that tests
the existing candidates for category errors and explanatory overlap without turning those tests
into a promotion gate.

Success is demonstrated by: (1) new candidates or negative findings from the previously
under-sampled sibling corpus; (2) explicit evidence and authority standing for every candidate;
(3) a relation map that distinguishes possible dependency, overlap, symptom, response, and open
relationship; and (4) visible uncertainty rather than forced closure.

## Recommended research seats

### Seat 1 — Sibling authority candidate scout

**Role and distinct lens:** Evidence discovery in the sibling authority system. This seat asks what
problem formulations become visible when the previously under-sampled governed corpus is read as
a source of candidate failures, not as authority over this repository. It does not run collapse
tests or design architecture.

**Exact corpus boundary:**

- `../domainspec-core/AGENTS.md` and `../domainspec-core/README.md` for repository-level standing;
- every Markdown file directly under `../domainspec-core/cyberAlchemy-v2/authority/`;
- every Markdown file under `../domainspec-core/cyberAlchemy-v2/authority/definitions/`;
- every Markdown file under `../domainspec-core/cyberAlchemy-v2/authority/decisions/`;
- every Markdown file under `../domainspec-core/cyberAlchemy-v2/authority/constitutions/`;
- all four files under `../domainspec-core/cyberAlchemy-v2/disciplines/cards/`;
- the current research brief and both exploration artifacts in this repository.

`../domainspec-core/cyberAlchemy-v2/authority/imports/` is explicitly excluded. Its 536 imported
files would turn a bounded authority reading into an uncontrolled source-history survey. Runtime,
implementation, test, and private validation material are also excluded unless one of the files in
scope directly identifies a specific item as necessary to understand a candidate; any such
exception must be named and justified before use.

**Question:** Which distinct failure candidates, boundary conditions, or counterexamples are
actually stated or entailed by the sibling's governed authority corpus, and which merely name
responses, desired properties, or governance mechanisms?

**Expected return:** One compact candidate ledger. Each row should contain: candidate name; failure
statement; concrete negative case; source path and selector; source status/scope; candidate standing
(`observed`, `source-claimed`, or `analyst-hypothesis`); nearest exploration family; whether it is
new, refines an existing candidate, contradicts one, or supplies no material change. End with a
short coverage statement and a list of deliberately excluded evidence. Do not claim completeness
or local governing authority.

**Rough budget:** 18k–24k tokens. The larger budget belongs here because the task closes the main
known corpus-coverage gap.

### Seat 2 — Candidate relation and category-error analyst

**Role and distinct lens:** Adversarial conceptual analysis over the evidence already gathered.
This seat tries to explain candidates through one another, construct counterexamples, and separate
problem, symptom, property, response, and mechanism. It does not discover or survey new repository
areas and does not judge whether the candidate set is complete.

**Exact corpus boundary:**

- `research/repository-irreducible-problem-inventory/research-initial-definitions.md`;
- `research/repository-irreducible-problem-inventory/stages/exploration/research.md`;
- `research/repository-irreducible-problem-inventory/stages/exploration/findings.md`;
- `sessions/2026-08-04-1730-repository-irreducible-problem-exploration.md`;
- only the source selectors already cited by those four artifacts, and only when needed to verify
  the wording or standing of a load-bearing claim.

This seat must not open sibling authority directories wholesale; that is Seat 1's boundary.

**Question:** For the candidates already on record, which relations are supported by an explicit
counterexample or dependency, which proposed collapses remain plausible, and which entries are
category errors because they name a response or terminal outcome rather than a failure mechanism?

**Expected return:** A relation table using only `may-depend-on`, `may-overlap`, `possible-symptom-of`,
`counterexample-separates`, `category-error`, and `relationship-open`. Every non-open relation must
include its counterexample or derivation and citation. Include a small candidate dependency graph,
a list of the strongest rival explanations, and the minimum questions that synthesis cannot answer
from current evidence. Labels such as `irreducible`, `complete`, and `final` are forbidden.

**Rough budget:** 10k–14k tokens.

## Topology and dependencies

Seats 1 and 2 should run in parallel. Their corpus boundaries and questions are deliberately
orthogonal: Seat 1 expands evidence; Seat 2 challenges the structure of existing evidence. Neither
depends on the other's return, which protects independent judgment and avoids a serial framing
effect.

After both return, the parent should perform synthesis. A third synthesis seat would mostly repeat
the parent's unavoidable ownership work and would add a handoff without adding a new evidence lens.
The parent should:

1. normalize both returns into one candidate ledger without erasing source-specific vocabulary;
2. merge only exact duplicates and retain disputed relations as alternatives;
3. add Seat 1's new candidates to the relation map without inventing tests that neither seat ran;
4. produce candidate and hypothesis conclusions with explicit standing and coverage limits;
5. keep architecture, ownership, and implementation recommendations outside the research verdict;
6. hand the synthesized artifact to an independent reviewer that did not participate in either
   research seat.

The reviewer is a downstream gate, not a third research seat. Its useful lenses are corpus-boundary
violations, unsupported authority transfer, hidden category changes, missing rival hypotheses, and
claims stronger than the evidence. Review should not reject the work merely because minimality or
completeness remains unproved.

## Duplication controls

- Seat 1 owns new sibling-authority evidence; Seat 2 owns relations among existing candidates.
- Neither seat writes the final inventory or makes architecture decisions.
- Neither seat repeats the three original exploration perspectives as an unrestricted survey.
- Source citations are preserved verbatim enough to audit, but source language is not automatically
  adopted as this repository's canonical vocabulary.
- A candidate appearing in both returns is not independent corroboration when both rely on the same
  cited source; synthesis must record shared provenance.
- Mechanisms such as inventories, ledgers, gates, typed edges, validators, or observability remain
  excluded from the problem set unless expressed as a concrete failure case.

## Conditional third seat

Do not launch a third research seat by default. Add a narrowly scoped translator only if synthesis
finds at least three load-bearing candidate pairs whose apparent agreement depends on incompatible
definitions across the two repositories. Its sole corpus would be the exact source passages for
those disputed pairs plus the two seat returns. Its return would state what each translation
preserves, collapses, and leaves unexplained. Budget: 6k–8k tokens.

## Lean fallback

If only one research seat is affordable, run Seat 1 and let the parent perform a lightweight
relation pass over the existing exploration. This closes the largest known evidence gap while
accepting weaker independence in the conceptual analysis. Budget: 18k–24k for the seat and roughly
6k–8k for parent synthesis.

## Recommendation

Use two parallel research seats — the sibling authority candidate scout and the candidate relation
and category-error analyst — followed by parent-owned synthesis and an independent review. The main
trade-off is deliberate asymmetry: most research capacity goes to the under-sampled sibling corpus,
while local evidence is challenged rather than re-surveyed. This is lean and minimizes duplicated
work, but it can miss a candidate that exists only in an uninspected local repository area; that
risk should remain an explicit coverage limitation, not be disguised as completeness.
