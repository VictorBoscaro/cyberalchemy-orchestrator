---
tags: [investigation, falsifier, claim-proof, enum-drift, obl-e3, repo-standing]
node_type: audit
is_session: false
layer: architecture, domain
nature: explanatory
status: exploratory
veracity: high
conviction: high
version: 0.1.0
last_updated: 2026-07-21
---

# Investigator — the Falsifier (claim ≤ proof, applied without mercy)

**Vector:** the gap between what the repo *claims* and what it has *demonstrated*.
Every line below cites the file it rests on.

## The master signal: the discipline leaks on its own checkable facts

The repo's loudest claim is that a *validated, single-writer, append-only* dispatch
discipline "runs for real" (`README.md:20`). Three cracks show the discipline does
not actually hold to `claim ≤ proof` in practice:

1. **The enum-drift is a live refutation of the repo's integrity spine, still
   untraced.** Two 2026-07-18 close rows carry out-of-enum `exit_reason: "success"`
   that "cannot have passed the appender" (`vault/audit/ledger-enum-drift-finding.md:36-41`).
   EG-1 ("one validated writer") is therefore *false as stated* and sits at
   `veracity: medium` (`engine-constitution.md:153-155`). The finding's own repair
   path is **OPEN** — "reproduce how the two rows entered" — and is named the
   "keystone next step for Phase 2" (`ledger-enum-drift-finding.md:53-57`). It was
   found 2026-07-19 and is not traced as of 2026-07-21. An append-only *hook* is
   claimed (`README.md:108`) yet was bypassed — the enforcement claim exceeds the proof.
2. **The repo cannot reconcile its own headline count.** `PLAN.md:232` says the agent
   pool has **414** entries; `README.md:136,474` says **419**. A trivially checkable
   number drifts across the two front-door documents. Small, but it is the same failure
   mode as the enum-drift one layer up: no single validated source for a stated fact.

These are not cosmetic. EG-1 is the load-bearing invariant that Phase 2 (the write
button), the bus-as-projection claim (`orchestration-infra`, cited
`ledger-enum-drift-finding.md:44-47`), and the whole "engine constitution ratifies
earned practice" posture (`engine-constitution.md:404`) all lean on. The spine is
currently unproven and is contradicted by data on disk.

## Claims masquerading as results

- **The category-theory front (Front 2) is scaffolding, not result — and its proof
  has not even been re-verified to exist.** OBL-E3 is **OPEN** (`OBLIGATIONS.md:50`);
  "nothing is typed in Lean *in this repo*" (`PLAN.md:6`, `README.md:16`). Every
  "strong candidate" row in `MAPPING.md` (probe→Yoneda, zig-zag, synthesis→pushout,
  ~16 rows) rests on Lean decls in a *sibling* repo whose "**build gate re-verify
  [is] pending**" (`MAPPING.md:25`) and whose build is flagged "**build unverified**"
  (`PLAN.md:282`). So these are candidates resting on proof no one in this repo has
  re-run. Honestly labeled — but it is the single largest block of *unproven surface*
  in the repo, and the README itself says so: "until OBL-E3 is discharged … everything
  in this vault is a typed candidate, not a result" (`README.md:453`).
- **The anti-noise thesis's flagship theorem rests on an unconstructed object.** The
  `bias ⊕ noise` split is "conditional, not free" (`PLAN.md:78`); it holds only under
  a Legendre potential `F` that is "**asserted by naming, not constructed**"
  (`anti-noise-orchestration.md:54,504-508`). All five registered bets are `in-test`
  or "candidate — not yet survived"; nothing is `operational`
  (`anti-noise-orchestration.md:325,587`). The Front-1 table is mostly **PENDING**
  (`PLAN.md:123-128`).
- **"Droppable into any repo" is a slogan with no discharged test.** H-PORT-1..6 are
  all undischarged hypotheses (`README.md:298-332`); the substrate is "hardwired to one
  Windows operator … not demonstrated on a second machine" (`PLAN.md:245-247`).

## What must be killed / de-scoped (unproven surface with no live path)

1. **HYP-ORCH-FRACTAL — its own pre-registered falsifier already FIRED.** The audit
   `close-row-enrich-c.md:15,54` proves "no close enriches `C`" from the appender
   schema, so "the current-design instance of this hypothesis is **falsified**"
   (`framework-self-similarity.md:74-80`). What survives is "conditional on BL-3," a
   typed-graph ledger that does not exist. It is **double-gated** — below OBL-E3 *and*
   BL-3 (`framework-self-similarity.md:28`) — i.e. it rests on two artifacts, neither
   built. By `claim ≤ proof` it should be explicitly shelved (its own retirement
   trigger, OQ-4, `:139`), not carried as a live "private proof target." De-scope now.
2. **Freeze the CT candidate layer's expansion.** No new MAPPING/FRAMINGS/DEFINITIONS
   rows should be authored until (a) the sibling Lean build is re-verified green and
   (b) OBL-E3 is *attempted*. Adding candidate rows on an unverified base grows unproven
   surface while claiming rigor.

## The single artifact that most reduces unproven surface

Two answers, by criterion:

- **Most urgent (do first): the drift trace / reproduction.** It is cheap, decidable,
  and it resolves a *known live counterexample* to the repo's headline invariant. It is
  the only thing that can move EG-1 off `medium` — either to `high` (a scoped-writer
  guard) or to an amended rule (`engine-constitution.md:388-392`) — and it is the sole
  precondition the repo itself places on Phase 2. Until it exists, "the discipline runs
  for real" is unproven and everything built on EG-1 is provisional.
- **Largest surface reduced per artifact: attempt OBL-E3.** A single Lean session
  collapses the *entire* Front-2 candidate layer (MAPPING, FRAMINGS, DEFINITIONS,
  FRACTAL, faces-instance) into either result or "decoration for the sequential
  fragment" (`OBLIGATIONS.md:38-43`). It "depends on nothing external — dischargeable
  now" (`OBLIGATIONS.md:47`). That it is dischargeable now and has *not been attempted*
  is itself the tell: the thesis layer is carried at candidate precisely because the
  one test that would grade it is deferred.

**Verdict.** The repo is unusually honest in *labeling* its unproven surface — but
honesty of labeling is not proof, and two facts (the untraced enum-drift, the 414/419
count-drift) show the discipline leaks even where verification is trivial. Next action
by proof: (1) trace the drift, (2) attempt OBL-E3, (3) shelve FRACTAL. Everything else
is thesis until those three move.

## Connections

| Document | Type | Description |
|---|---|---|
| [[ledger-enum-drift-finding]] | `derives-from` | The live counterexample this report treats as the master signal that the discipline leaks; its repair path is still OPEN. |
| [[engine-constitution]] | `contradicts` | EG-1's "one validated writer" is refuted on disk; this report ranks tracing the drift above all else to resolve it. |
| `OBLIGATIONS.md` | `grounds` | OBL-E3 (OPEN, dischargeable now) is named the single largest unproven-surface reducer; its non-attempt is the central tell. |
| `MAPPING.md` | `contradicts` | The "strong candidate" CT rows rest on a sibling Lean build flagged build-unverified; the report freezes this layer's expansion. |
| [[framework-self-similarity]] | `contradicts` | Its own falsifier 1 fired; this report recommends explicit shelving rather than carrying it as a live proof target. |
| [[anti-noise-orchestration]] | `contextualizes` | Flagship `bias ⊕ noise` split rests on an unconstructed `F`; cited as a claim masquerading as a near-result. |

