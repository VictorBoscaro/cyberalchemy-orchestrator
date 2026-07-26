---
tags: [agents, architecture, mathematics, lean, invariants, review]
node_type: review
status: proposed
version: 0.1.0
last_updated: 2026-07-25
related_plan: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
stream_id: R1
reviews: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/CANDIDATE-INVARIANTS.md
evidence: ../../../domainspec-lean-formalization/lean-engineer/cyberalchemy-orchestrator/agent-language/
authority: research-input-only
---

# Lean mechanization probe — `CANDIDATE-INVARIANTS.md` K1–K7

## 1. Status, and what this is not

This is **out-of-sequence evidence.** The subplan sequences Lean as step 9, after the staged
two-reviewer review at step 8 ([PLAN.md](../../plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md)
:409-413), and the system-view appendix closes by naming "immediate Lean implementation" as
specifically what the next step is *not*
([agent-language-system-view.md](../../docs/architecture/agent-language-system-view.md):790-792).
That review has not run. This probe was authored at repository-owner direction, ahead of the gate.

It is therefore **Lean-as-notation-aid** — role 1 of the three the subplan requires be kept
separate (`PLAN.md`:104-107). It is not the accepted dependency cone. **It moves no proposition
off `open`**, and it is not a product-architecture verdict.

The probe targets `CANDIDATE-INVARIANTS.md` (v0.4.1, `status: proposed`,
`authority: research-input-only`) rather than the §16 appendix ledger, because the appendix's
`P-01…P-15` numbering does not appear in this node's bound sources at all — see §6.

## 2. Build evidence — which proof-status gate items are discharged

[findings.md](findings.md#proof-status-gate) sets a seven-item gate before any claim reaches
`machine-checked-currently`. Four are now discharged, three are not.

| # | Gate item | Status |
|---|---|---|
| 1 | Lean project and toolchain | **discharged** — `domainspec-lean-formalization/lean-engineer/`, `leanprover/lean4:v4.30.0-rc2`, Mathlib pinned `388f44f89d70fbad0e1accb8fd62fc8c97714a85` |
| 2 | Exact build target and dependency cone | **discharged** — five `lean_lib` targets: `AgentLanguageCore`, `AgentLanguageKernel`, `AgentLanguageIndependence`, `AgentLanguageComposition`, `AgentLanguageLineage`. Cone is Mathlib + `Mathlib.Data.List.Basic`; no category theory, no `Finset`, nothing from the sibling's `lean-formalization/` residue package |
| 3 | Successful build output | **discharged** — `lake build` of all five: 469 jobs, exit 0. The pre-existing package also rebuilt green (941 jobs, exit 0) |
| 4 | `sorry` and axiom audit | **discharged** — zero `sorry` in source; `#print axioms` on every main theorem reports only `propext`, `Classical.choice`, `Quot.sound` |
| 5 | Theorem and source digests | **NOT discharged** — the files are uncommitted working-tree state; no rev exists to pin |
| 6 | Correspondence review | **NOT discharged** — correspondence to the ACI named types (`ConfirmedDispatch`, `RuntimeEventEnvelope`, `ExecutionAuthorityFence`) is recorded as `noCorrespondence`; no engineer view exists to own it |
| 7 | Relationship to runtime validators | **NOT discharged** |

**Consequently nothing here is `machine-checked-currently`.** Items 5–7 are unmet, and item 6
cannot be met until an engineer view exists. The honest status of every result below is *a
machine-checked fact about a model*, which is a different object from a fact about the candidate
laws or about the product.

Targets are deliberately excluded from the package's `defaultTargets`, so the `permguard` /
`agentguard` extraction surface is untouched.

## 3. Findings that survived adversarial review

Two survived an adversarial vacuity pass and a subset-rule audit run as separate agents.

### PF-01 — A uniform invariant-registration mechanism defeats K7

**The finding.** Model the registration mechanism as a flat registry in which kernel laws and
user laws are entries of the same kind, and the user supplies a scope assignment saying in which
states each entry is evaluated. Under that mechanism, a reasonable user-level policy — *evaluate
this only while describing, i.e. only in states carrying no effect yet* — switches K4 off exactly
in the states where K4 is load-bearing, since K4 is the law about effect boundaries. The result is
a state that the kernel law set rejects and the composed registry accepts. **K7 fails.**

The failure is not a user law admitting anything. The kernel law is still registered; it is
simply never evaluated. A safety argument resting on "user invariants can only narrow the valid
state space" does not reach this case, because that argument is about the *append* operator and
this is a different operator.

**Not mere vacuity.** The witness is targeted, not global: an assignment that scopes away K4
alone, leaving every other law universal, admits the violation, while the same registry
demonstrably still enforces K1 on a K1-violating state.

**Stated repair.** Kernel entries must be **present and in scope** at every state, for every user
configuration. Pinning kernel laws to universal scope while leaving user laws subject to the
user's scope assignment satisfies this for *every* scope assignment. Proved **sufficient**, not
necessary; no converse was attempted.

**Disabling is the same hole through a different door.** Deactivating a kernel entry (removing it
from the registry) fails the same condition for the presence reason rather than the scope reason.
The consequence for design is that hardening the scope field alone is insufficient — the
activation/lifecycle decision is a second enforcement point. A third door, `retiring`, was not
modelled; by the source's own text retiring a kernel law is a versioned kernel change, but if the
product's retire path runs through the same registry API as the user path, this probe says nothing
about it.

**What this means for the product intent.** `CANDIDATE-INVARIANTS.md` grants the user five verbs:
adding, disabling, scoping, composing, retiring. *Adding* and *composing* are safe. *Disabling* and
*scoping* are not. The design consequence is that kernel entries need **a different type at the
registration boundary** — a documented convention that kernel invariants "should not" be scoped is
not sufficient, because the mechanism as modelled cannot tell the two kinds of entry apart.

**Collapse test.** If the product's registration API already types kernel entries distinctly from
user entries — so that no user-supplied scope assignment or activation decision can reach a kernel
entry — this finding contributes nothing and should be recorded as already-satisfied.

### PF-02 — K1 and K2 *as formalised* admit rootless cycles

**The finding.** A state satisfying all six formalised kernel laws exists in which every grant
derives its authority from another grant in a closed cycle (no rooted grant anywhere), and every
fact is a correction of another fact (no original). Both laws' lookups are local existential
checks — *the referenced grant/fact is present in the list* — which do not force well-foundedness.

This is the prose failure the source names: *"Content cannot assert its own authority"* (K1) and
*"correction adds a new fact or explicit supersession rather than silently rewriting accepted
history"* (K2). A closed delegation cycle is authority asserting itself; a correction chain with
no original is history with nothing underneath it.

**Demotion applied.** This is a fact about **the encoding in `AgentLanguageKernel`**, not about
the prose laws. The prose was not proved to have the hole; a different formalisation might not.
And "the laws need an acyclicity clause" is a design inference — no theorem shows such a clause
would be sufficient to carry the prose content.

**Collapse test.** If the product's grant and fact stores enforce well-foundedness structurally
(e.g. a materialised root, or an append-only chain that cannot close), the finding reduces to a
gap in this probe's encoding and contributes nothing to the candidate laws.

## 4. What did not survive — recorded, not hidden

The adversarial pass found more than it confirmed. These are recorded because the alternative is
a register that drifts.

**N-01 — No transition system. Nothing here is shown to be an invariant.** The source defines an
invariant as a predicate preserved by every valid transition. The probe encodes that definition
faithfully and then **never instantiates it** at the kernel state type: the preservation predicate
has zero uses. Every K1–K6 result is a **satisfiability** fact, not a **preservation** fact. These
are different questions. K6 is worst affected — "replayable, idempotent transitions" is not
under-modelled but *unstatable* in a state type with no dynamics, as are K2's "acceptance is
recorded before acknowledgement" and K4's "before a consequential effect". **This is the probe's
principal limitation and it undercuts its framing as a model of an invariant set.**

**N-02 — The independence result is field privacy, not logical independence.** Each formalised law
owns at least one field no other law reads, so the countermodels are automatic: *any* predicate on
the grants list alone comes out "independent" of the other five. As an answer to minimality test 2
its value is close to nil. The reduction cuts deeper than first reported: the six laws instantiate
only three schemas — referential integrity (×4), identity-uniqueness (×2), field-value constraint
(×3). Whether they collapse under a uniform entity table is **not modelled** and remains a live
minimality objection, not a result.

**N-03 — Retracted: "K7 is of a different logical type, so the candidate set is heterogeneous."**
This was asserted in the probe's own module documentation and does not survive. The type split is
an artefact of choosing a state type with no registry field; the reviewer rebuilt the alternative
(state carrying its registry, K7 as an ordinary state predicate, count seven) in about ten lines.
The observation is real about *that encoding* and is not evidence about `CANDIDATE-INVARIANTS.md`.
**No claim about the heterogeneity of the candidate set is made or supported.**

**N-04 — The probe's own non-vacuity template is vacuous.** The record/semantics separation
theorem was designated the template for the whole library and is two unrelated existentials: the
governance-record type has no field naming a predicate, so the connection is not expressible. The
statement provably decomposes into "records can be well-formed" and, separately, "systems can
break predicates". It separates nothing.

**N-05 — The lineage non-transmission witness is an empty world.** The four capability predicates
fail for the child because the underlying record lists are empty, not because inheritance was
blocked — and the *parent* has none of the four either. The collapse test that matters ("child
launches from ancestry alone") requires a well-endowed parent. The reviewer constructed that
version and confirmed it works; the probe did not state it. Formally true, evidentially near-empty.

## 5. Precedent and ownership

**No novelty is claimed anywhere in this probe.** Per the trigger discipline, owners are named:

- The **stratification shape** in PF-01 — mandatory laws that a discretionary layer cannot weaken —
  is owned twice over. Externally: XACML / Cedar mandatory-vs-discretionary policy layering.
  In-package: `AgentPermissionKernelComposition.append_restricts_left` / `append_restricts_right`
  in the same Lean package already prove the append-restricts-both-sides shape. PF-01's
  contribution is not the shape but its **application to invariant registration**, and the
  observation that the source's own verb list grants the user the operator under which it fails.
- **Independence by countermodel** (§4, N-02) is Hilbert (1899) / Huntington (1904). Standard.
- The probe imports nothing from the sibling's `lean-formalization/` residue package and makes no
  typed-residue claim. It sits in `lean-engineer/`, whose binding honest typing is *engineering on
  owned foundations, not a novelty or typed-residue claim*.

## 6. Effect on this node's existing findings

- **F-07** (existing Lean assets are narrow precedents, `proof-present-in-bound-source`) is
  unchanged for the three previously cited files. This probe adds new artifacts at a *higher*
  evidentiary level for gate items 1–4 but a *lower* one for 5–7, so it does not raise F-07.
- **F-08** (countermodels are the first acceptance tests) is supported in method. PF-01 and PF-02
  are both countermodels, and both survived review; every positive result did not.
- **F-05** (deep structure does not require deep runtime authority) is *not* advanced. N-05 records
  that the lineage witness is evidentially near-empty.
- **No finding F-01…F-11 is reversed or promoted by this probe.**
- The `P-01…P-15` ledger in the system-view appendix has **no counterpart in this node's bound
  sources** — a search of `research.md`, `findings.md` and `research-initial-definitions.md`
  returns zero occurrences of that numbering. The sources sustain an eight-item proposed
  proposition set and eight countermodels. This is recorded as a bookkeeping observation, not a
  defect claim against the appendix.

## 7. Open Questions

| ID | Question | Status | History |
|---|---|---|---|
| ALF-OQ-016 | Does the product's invariant-registration API type kernel entries distinctly from user entries, across scope assignment *and* activation/lifecycle? | open | Opened 2026-07-25 from PF-01. This is the finding's collapse test. |
| ALF-OQ-017 | Does `retiring` reach kernel entries through the same registry path as the user verbs? Not modelled. | open | Opened 2026-07-25 from PF-01. |
| ALF-OQ-018 | Do K1 and K2 require an explicit well-foundedness clause, and is such a clause sufficient to carry their prose content? | open | Opened 2026-07-25 from PF-02; sufficiency unproved. |
| ALF-OQ-019 | Under a uniform entity/identity table, do the six candidate laws reduce to fewer than six? Three schemas were observed; no model was built. | open | Opened 2026-07-25 from N-02. |
| ALF-OQ-020 | What transition relation makes K1–K6 statable as *preservation* rather than satisfaction, and does independence survive re-derivation over it? | open | Opened 2026-07-25 from N-01. **This blocks any minimality claim.** |
| ALF-OQ-021 | Is `KernelAlwaysInScope` necessary as well as sufficient for K7 under scoping? | open | Opened 2026-07-25; no converse attempted. |

`ALF-OQ-001` through `ALF-OQ-011` and `ALF-OQ-013` through `ALF-OQ-015` are untouched by this probe
and remain as recorded in [findings.md](findings.md#open-questions).

## 8. Recommendation

The staged review at step 8 remains the correct next step and this probe does not substitute for
it. Two concrete inputs are offered to it:

1. **PF-01 is actionable independently of everything else here.** It does not depend on the
   transition system that N-01 says is missing, and it bears directly on a product decision — the
   type of a registration API — that is cheap now and expensive later.
2. **N-01 should be closed before any minimality claim is made.** Independence of satisfiability is
   not independence of invariance, and the minimality question the source poses is about the latter.
