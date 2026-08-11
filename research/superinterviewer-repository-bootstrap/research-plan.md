---
artifact_kind: research-plan
status: proposed
version: 0.1.0
date: 2026-08-10
subject: superinterviewer
---

# Research Plan — Superinterviewer

## 1. Purpose and authority

This plan governs how the Superinterviewer founding research is decomposed, sequenced, stopped,
synthesized, and connected to decisions. It covers two coupled but distinct horizons:

1. **Repository bootstrap:** prepare, review, create, and hand off a clean product-owned research
   repository.
2. **Product research program:** determine where the Superinterviewer is a distinct, useful,
   governable product and what evidence should change its design or existence.

This document is `PROPOSED`. Its first acceptance is **planning authorization**: it authorizes
preparation of the founding package inside `cyberalchemy-orchestrator`. After package review, a
separate **founding-plan ratification** must name the accepted version and digest installed in the
new repository. Ratification supersedes this planning copy as governing authority and is recorded in
the transfer manifest. Neither event authorizes creating another Git repository, provisioning a
remote, installing runtimes, or implementing the product.

The authority split is:

| artifact | authority |
|---|---|
| Product charter | Product identity, boundaries, and interaction protections |
| Master research initial definitions | Informational context, confirmed constraints, baseline, and known gaps |
| Research plan | Sequencing, evidence standards, gates, dependencies, and stopping conditions |
| Scoped initial definitions | One bounded refinable research question and its context |
| Research findings | Cited support, counterevidence, typed negatives, and remaining uncertainty |
| Decision record | Binding acceptance, rejection, reframing, authorization, or supersession |
| Execution receipt or signal | Generated evidence about a run, never an accepted decision by itself |

Findings may contradict the charter immediately as evidence, but only a named decision may change
the charter or authorize implementation.

## 2. Confirmed decisions

The plan treats these as accepted constraints, not hypotheses to be repeatedly re-proven:

1. The Superinterviewer is the product: the person's primary interface and intellectual partner,
   not a generic framing framework or question-only chatbot.
2. It may ask, bring information, suggest, and propose or test reframings and lenses. Completeness
   and separability of these moves remain open.
3. A clean repository will be created outside `cyberalchemy-orchestrator`; this is an owner decision
   with a revisit condition, not an empirical product result.
4. Product charter, master context, plan, investigations, findings, and decisions remain distinct.
5. The complete `mint` package will not be used at inception; only evidenced mold elements may be
   reused proportionally.
6. `subagent-work-infrastructure` is a peer/provider candidate, not a subordinate module or product
   authority.
7. Dependencies begin as narrow pinned references or contracts; broad imports are default-denied.
8. Product implementation requires a prior discriminating research or experiment gate.
9. Reframing cannot silently replace the person's intention; changes must be attributable,
   explainable, contestable, and reversible where appropriate.
10. Claims may not exceed their evidence; mathematical analogies are not product facts.

## 3. Mother question

> Under what observable and governable conditions does the Superinterviewer help a person transform
> an incomplete, changing, or contradictory intention into sufficient clarity for an appropriate
> next step, better than simpler alternatives, without silently replacing that intention or
> degrading autonomy?

“Better,” “sufficient clarity,” “appropriate,” and “autonomy” are research variables. They must be
refined for a context and population before comparative claims are tested.

The product thesis must be reframed or abandoned if no context produces a witness distinct from a
memory assistant, search interface, requirements interview, coaching conversation, or competent
human partner.

## 4. Planning discipline

A research branch enters the plan only when it declares:

1. the consuming decision and blocking uncertainty;
2. incompatible alternatives, including a simple baseline;
3. evidence capable of discriminating them;
4. a `result → action` table including an inconclusive result;
5. a falsifier or kill criterion;
6. an evidence source independent of the material that generated the hypothesis, when validation is claimed;
7. the strongest claim the method can support;
8. dependencies, bounded effort, and stop condition;
9. output authority and promotion path.

If a proposed branch only says “explore,” “map,” or “investigate” and cannot name a decision it may
change, it remains a topic in the question inventory rather than scheduled work.

Research found upstream is a positive result: cite the owner and use `build-from-owned` or
`already-deployed`. Only `no-witness` and `tautological` are terminal negative types.

## 5. Two-horizon critical path

```text
Approved Robot-Talks dispositions
              │
              ▼
Horizon A — founding package prepared here
              │
              ▼
Independent review of charter, plan, authority, provenance, and scaffold
              │
              ▼
Explicit repository-creation authorization
              │
              ▼
Create and validate clean repository; transfer canonical ownership
              │
              ▼
Horizon B — Wave 0 research constitution
              │
              ▼
Historical corpus + product comparators + intention witnesses
              │
              ▼
Discriminating low-commitment experiments
              │
              ├── restrict/reframe/abandon
              └── authorize bounded prototype
```

Horizon A enables Horizon B but may not decide the product model through directory layout, schemas,
providers, or governance machinery. Horizon B must not keep two editable master authorities alive
after ownership is transferred to the new repository.

## 6. Horizon A — Repository bootstrap

### A0 — Accept this plan

Acceptance authorizes only preparation of the founding package in this repository.

Parameters deliberately left for the repository-creation gate:

- canonical repository name and exact local path;
- remote owner/URL, visibility, and whether a remote is created immediately;
- license;
- default branch;
- initial signer/author and protection policy.

### A1 — Prepare the founding package

Create `TRANSFER-MANIFEST.md` first as the sole bootstrap carrier, initially containing candidate
rows rather than installed files. Before creating any other candidate file, its row must name the
immediate consumer, consuming decision, why an existing artifact cannot serve it, binding status,
and removal test. The owner approves or rejects these rows as an A1 sub-gate; a file without an
accepted row is not created. The following tree is a candidate package, not a prescribed scaffold:

```text
founding-package/
├── TRANSFER-MANIFEST.md
├── README.md
├── product/
│   └── CHARTER.md
├── research/
│   ├── research-initial-definitions.md
│   └── research-plan.md
├── authority/
│   ├── AUTHORITY-MODEL.md
│   └── DEFINITIONS.md
├── decisions/
│   └── 0001-create-separate-repository.md
├── policies/
│   └── DEPENDENCIES-AND-PROVENANCE.md
├── manifests/
│   ├── sources.yaml
│   └── dependencies.yaml
├── contracts/
│   └── execution-link.md
└── .gitignore
```

Every created file must pass that consumer test. Do not add empty taxonomies, a Universal Governance
Baseline, constitution packs, a vault, copied frameworks, broad submodules, host-specific skill
mirrors, runtime code, CI, database, ledger, scheduler, or product implementation.

The transfer manifest records destination, status (`DRAFT` or `ACCEPTED`), digest, source, and
installation order. It must disclose that the current bootstrap corpus is untracked until a durable
commit or explicit snapshot fixes it.

### A2 — Review the founding package

Run an independent persisted `review` over the frozen package. The review must test:

1. whether the charter preserves the Superinterviewer as partner/interface rather than framework;
2. whether each authority has one owner and a non-overlapping mutation rule;
3. whether findings can contradict the frame without silently changing it;
4. whether every external claim has reproducible provenance;
5. whether every file and defined term has an immediate consumer;
6. whether providers remain external and replaceable;
7. whether the execution-link contract preserves lineage without requiring a runtime stack;
8. whether a clean clone can understand and validate the foundation without sibling paths.

The review loop is bounded: freeze digest → review → correct only accepted blockers → re-freeze.
Run at most one initial review and two corrective re-reviews. Material changes outside accepted
blockers start a fresh explicitly authorized review cycle. If blockers remain after the ceiling, the
owner must choose to change the package, accept a documented residual, or stop/reframe the bootstrap.

A2 closes only when the owner explicitly accepts the charter, authority model, decision `0001`,
research plan, and frozen transfer manifest, and records the **founding-plan ratification** with
version and digest. Review acceptance and plan ratification do not authorize repository creation.

### A3 — Repository-creation gate

Before mutating outside this repository, obtain explicit authorization for the unresolved parameters
from A0 and the exact digest of the accepted transfer manifest. Local repo creation and remote
provisioning are separate permissions.

### A4 — Create and validate the repository

Only after A3:

1. resolve and verify the exact target is new or empty;
2. initialize Git with the accepted branch;
3. install only transfer-manifest destinations;
4. run V1–V6 below and record `PASS|FAIL|N/A`, command or inspection evidence, and a reason for every
   `N/A`;
5. commit the accepted package as the **foundation commit**;
6. clean-clone the foundation commit and run V7;
7. add `decisions/0002-bootstrap-receipt.md` in a **closure commit**, recording authorization,
   manifest digest, foundation commit, emitted files, validation evidence, and deviations;
8. create/push a remote only if separately authorized and then run V8;
9. use the closure commit for A5 handoff while the receipt preserves the foundation commit identity.

Validation checklist:

- **V1 Manifest:** installed files and digests exactly match the accepted transfer manifest.
- **V2 Provenance:** every source pin resolves or has a justified snapshot; dirty/untracked material
  is not represented as belonging to `HEAD`.
- **V3 Portability:** a scratch copy does not require absolute sibling paths, local junctions, or
  machine-specific symlinks to read its authorities.
- **V4 Authority:** charter, context, plan, findings, decisions, and proposals have non-overlapping
  owners and states; proposals are not binding.
- **V5 Boundary:** no broad submodule, copied framework, mandatory hook, runtime database, credential,
  or unapproved provider entered silently.
- **V6 Git hygiene and repeatability:** branch, ignore rules, license decision, line endings, secrets,
  no-clobber behavior, status, and diff are reviewed; emission repeats safely in a scratch target.
- **V7 Clean clone:** V1–V5 pass from the foundation commit and README resolves the authority map
  without runtime installation.
- **V8 Remote, when authorized:** URL, visibility, default branch, and observed remote commit match A3.

V1–V7 must pass. V8 is required only when remote provisioning is authorized.

### A5 — Transfer canonical ownership

After human acceptance of the created foundation:

- the new repository becomes canonical owner of the charter and research program;
- this bootstrap corpus becomes a pinned antecedent, not a second editable master;
- transferred, rejected, and retained questions are recorded;
- this repository receives a closure pointer to the new repository and commit;
- the first branch opens in the new repo with its own scoped initial definitions.

### Bootstrap completion condition

Bootstrap is complete only when the created repository passes validation, has a creation receipt,
is explicitly accepted, and the handoff leaves one canonical editable authority. It does not deliver
a runtime, agent platform, complete ontology, or implemented Superinterviewer.

## 7. Horizon B — Product research workstreams

WS0–WS8 are topic containers, not executable branches. A wave may activate a workstream only through
one or more scoped branch records satisfying all nine admission fields in section 4. Producing a map,
schema, glossary, or literature sweep does not complete a workstream unless its branch changes or
closes the declared consuming decision.

### WS0 — Historical lineage and case corpus

Reconstruct the evolution from question game to Superinterviewer using observed episodes. Preserve:
prior state, intervention, signal, distinction, reframing, intention change, enabled next step, and
remaining residue. Use this corpus to generate hypotheses and an observation schema, never as its
own validation set.

### WS1 — Product identity, users, jobs, and comparators

Identify contexts in which a partner is preferable to direct answer, search, coaching, facilitation,
or execution. Produce a refutable product thesis, context × job × alternative map, precedent owners,
and explicit non-use contexts.

### WS2 — Intention, state, change, and validation

Distinguish declared, inferred, revised, and operational intention; goals, values, constraints, and
the system's intervention intent. Find concrete witnesses of change and determine who validates it.

### WS3 — Intervention dynamics

Test asking, informing, suggesting, reframing, waiting, and advancing as candidate moves. Determine
whether they are distinguishable, hybrid, or better represented by dimensions. Produce cases,
counterexamples, failure modes, and a candidate—not implemented—selection policy.

### WS4 — Evaluation, causal attribution, and discriminating experiments

Define outcomes and guardrails before instruments. Separate influence, uncertainty, controllability,
value of information, and decision sensitivity. Compare with simple assistants and competent humans
where appropriate.

### WS5 — Autonomy, framing power, and governance

Threat-model induction, dependence, persuasion, omission, anthropomorphism, and capture. Determine
which decisions require explanation, consent, contestability, or human authorization. DAO remains a
candidate, not an architectural commitment.

### WS6 — Locality, lenses, memory, and typed residue

Distinguish meanings of “local,” test marginal context value, lens conflict and order effects, and
preserve unexplained material as typed residue. Determine when local-first must escalate or be
forbidden.

### WS7 — Evidence, execution, and dependency boundaries

Define narrow return-of-evidence and execution-link semantics without selecting a runtime. Maintain
provider replaceability and pinned source identity. SWI, DomainSpec, Arcanum, Lean, and this
orchestrator remain reference/provider candidates until separate dependency gates.

### WS8 — Formalization with consequence

Open only after WS2–WS6 produce observable witnesses. Compare simple typed graphs, causal models,
constraints, and probabilistic models against category-theoretic candidates. Promote a formalism
only if it changes a prediction, test, impossibility result, or decision.

## 8. Research dependency graph

```text
WS0 ──▶ WS1 ──┐
 │             ├──▶ WS3 ──┐
 └────▶ WS2 ──┤           │
               ├──▶ WS5   ├──▶ WS4 ──▶ discriminating prototype gate
               └──▶ WS6 ──┘

WS7 supports all workstreams without owning product semantics.
WS2 + WS3 + WS4 + WS6 ── witness gate ──▶ WS8
```

WS4 may design evidence early but cannot stabilize metrics before WS1 and WS2 define the phenomenon.
WS8 never blocks empirical product research.

## 9. Research waves and gates

### Wave 0 — Minimum epistemic constitution

Outputs:

- accepted mother question;
- claim/refutation map;
- epistemic status and promotion rules;
- branch opening/return contract;
- protected-questions register;
- T1–T6 registered as residual tensions.

Gate B0 passes when each founding claim resolves to a decision, evidence, hypothesis, analogy, or
open question; external sources are pin-able; and findings can contradict the thesis without editing
the charter. B0 also freezes a versioned register of principal claims for the founding phase. New
principal claims require a new plan version rather than silently extending the phase.

### Wave 1 — Witness the phenomenon before architecting it

Candidate containers: WS0, WS1, and WS2. None becomes active until conforming branch records satisfy
section 4.

Outputs: annotated corpus, independent validation set design, honest comparators, operational
glossary, observation schema, counterexamples, and non-use contexts.

Gate B1 passes only if traceable episodes show an intervention changing a relevant distinction and
enabling or correcting a next step, with a plausible contrast against a simple baseline. Otherwise
reframe or stop “intention refinement.”

### Wave 2 — Mechanisms, precedents, and risks

Candidate containers: WS1–WS3 and WS5–WS7; WS4 may design evaluation. None becomes active until
conforming branch records satisfy section 4.

Outputs: ownership matrix, candidate intervention taxonomy, signal/probe/lens/residue model, threat
model, outcomes, and guardrails.

Gate B2 tests definitional soundness: owned work is cited; re-skinning is demoted or killed.

Gate B3 tests evaluability: at least one product claim has a contrast, unit of analysis, outcomes,
guardrails, evidence source, and a result that would weaken it.

### Wave 3 — Low-commitment discriminating experiments

Prefer replay, blinded coding, Wizard-of-Oz, manual comparison, and non-executable interaction
mockups before the prototype gate. Each experiment predeclares alternatives, outcome, safety
guardrails, stopping rule, and architecture questions it is forbidden to decide. No Wave 3 branch
becomes active until its record satisfies section 4.

Gate B4 authorizes one bounded prototype only when it names a discriminating uncertainty, simple
baseline, expected evidence, risks, kill criterion, and discard/revision path.

Only after B4 may that bounded product prototype be created or run.

Gate B4a adjudicates observed results before any principal-claim decision. It requires the frozen
protocol identity, observed comparison with the baseline, threshold and guardrail results,
application of the predeclared `result → action` table, a typed inconclusive outcome when needed, and
an explicit proposed claim update. B6 may accept or reject that evidence-backed disposition; it may
not substitute preference for missing adjudication.

### Wave 4 — Consolidation and selective formalization

Outputs: strongest defensible formulation, limits of use, accepted/rejected decision proposals,
formal candidates promoted or demoted, reordered backlog, and revised mother question.

Gate B5 admits a formalism only when it has operational consequence; otherwise it remains analogy.

Gate B6 accepts, restricts, reframes, or abandons each principal claim through a human decision.

The founding product-research phase completes only when every claim frozen at B0 has a B6
disposition, all required result-action tables have been applied, no blocking branch remains open,
residual questions are explicitly deferred with reopen triggers, and the cycle emits: the strongest
defensible formulation, most fragile hypotheses, smallest next discriminating test, and reasons to
restrict, reframe, or abandon. New principal claims begin a new versioned phase.

## 10. Protected questions

Before any scaffold, schema, metric, adapter, or prototype can become binding, preserve as open:

- whether “primary interface” means exclusive, default, or continuous;
- what “companion” requires beyond interaction style;
- whether candidate intervention classes are complete or separable;
- what object is refined and who validates operational intention;
- what a next step is and whether advancing recommends, hands off, or executes;
- when to infer, ask, preserve ambiguity, return, branch, or stay silent;
- whether lenses and residues are persistent product objects or analytical instruments;
- which objectives select interventions and which rights remain hard constraints;
- which baseline and outcomes distinguish benefit from confidence, speed, or coherence;
- what consent, refusals, events, and sensitive data may be recorded;
- whether DAO is useful at all;
- whether any provider, formalism, memory model, or locality definition is necessary.

Experimental artifacts must reference protected-question IDs, state incorporated choices, declare an
expiry/review point, and prohibit automatic promotion.

## 11. Source, dependency, and execution-link policy

Each load-bearing source reference records at least: `id`, `role`, `repository_url` or durable
locator, `revision`, `worktree_state`, `path`, `selector`, `sha256`, `captured_at`,
`license_or_access`, and `snapshot_path` when needed. Snapshot only when no durable licensed locator
exists.

A dirty or untracked file must not be represented as contained by `HEAD`. Local sibling paths may be
recorded as `observed_at`, never as clone-safe canonical locators.

Executable dependencies record: `id`, `concern`, concrete consumer, `provider`,
`interface_or_capability`, `version_or_revision`, `artifact_digest`, `compatibility`, `optional`,
`allowed_surface`, `status`, and removal test. At day zero, SWI,
DomainSpec, `domainspec-core`, Lean, and this orchestrator are reference-only. Arcanum becomes a
dependency only when an accepted validation or workflow actually invokes it.

The minimum execution link records local question/artifact identity, executor/profile/version,
external run IDs when present, exact input/output digests, timestamps, execution state, limitations,
and local acceptance state. External success never substitutes for local evidence acceptance.

## 12. Branch return contract

Every completed or stopped branch returns:

1. the question and claim version addressed;
2. corpus, sources, revisions, method, and limits;
3. cited answer, strongest counterevidence, typed negative when applicable, and remaining uncertainty;
4. effect on dependencies and the residue/contradiction register;
5. applied `result → action` row;
6. the decision it may inform, without taking that decision implicitly.

Scoped initial definitions return refinements of question, confirmed constraints, and gaps as a
versioned context delta; they do not promote claims or alter the charter. Findings update the
evidence matrix and residue register immediately, but only a decision record may accept, reject,
reframe, authorize implementation, or change binding authority.

## 13. Stopping, splitting, and reframing

### Stop a branch when

- the predeclared decision condition is satisfied and more evidence has low marginal value;
- a suitable owner is found and the work can be built from owned precedent;
- no witness exists under the bounded corpus/test;
- the concept collapses definitionally;
- a prerequisite fails;
- the method cannot support the required claim strength;
- the baseline wins within the predeclared threshold.

“More literature exists” is not sufficient reason to continue.

### Split work when

the consuming decision, method, evidence, or authority differs. Required separations include:
bootstrap vs. product; product authority vs. research governance; conversation behavior vs. runtime;
outcome vs. telemetry; empirical research vs. formalization; user governance vs. DAO; source
provenance vs. run observability.

Do not split merely by discipline or source repository.

### Reframe or abandon when

- simpler baselines match outcomes with lower cost or risk;
- users prefer direct answers without material loss;
- intention refinement cannot be observed without unacceptable induction;
- reframing raises dependence or manipulation without decision benefit;
- local-first hides decisive global risks;
- lenses do not outperform simpler prompts or adapters;
- selecting probes costs as much as the broad model it was meant to avoid;
- governance requirements make interaction impractical;
- no distinct phenomenon survives comparison with memory, search, elicitation, coaching, or competent conversation.

## 14. Plan evolution

The plan is revised by explicit delta:

1. previous question or dependency;
2. new evidence or decision;
3. contradiction or residue;
4. proposed change;
5. downstream work cancelled, added, split, or demoted;
6. approving decision when binding authority changes.

Every cycle ends with:

- strongest currently defensible formulation;
- most fragile hypotheses;
- smallest next discriminating test;
- reasons to restrict, reframe, or abandon;
- updated critical path and deferred work.

Document count, number of agents, turns, probes, or dispatches is not progress. Progress is explicit
reduction of an uncertainty that changes a decision while preserving remaining residue.

## 15. Immediate next work after planning authorization

1. Prepare the A1 founding package in this repository.
2. Freeze it with a transfer manifest and reproducible source pins.
3. Run the independent persisted review at A2.
4. Correct blocking findings and obtain explicit acceptance of charter, authority model, decision
   `0001`, frozen transfer manifest, and the founding-plan version/digest; record this as
   ratification, which supersedes the planning-authorized copy.
5. Return for the A3 repository-creation authorization with exact name, path, remote, visibility,
   license, branch, signer, and accepted manifest digest.

In parallel only where it does not pre-commit product structure, prepare the Wave 0 claim/refutation
map and protected-questions register as draft inputs to the founding package. Do not begin a product
prototype before B4.

## 16. Planning basis

This plan synthesizes:

- `research-initial-definitions.md`;
- accepted Robot-Talks `dialogue.md`, `findings.md`, and three independent reports;
- `planning/inputs/01-research-program.md`;
- `planning/inputs/02-repository-bootstrap.md`;
- `planning/inputs/03-plan-adversary.md`;
- the supplied Prompt-Mestre.

The planning inputs are planning basis and critique, not parallel plan authorities. Claims within
them retain the epistemic status and source of their underlying support.
