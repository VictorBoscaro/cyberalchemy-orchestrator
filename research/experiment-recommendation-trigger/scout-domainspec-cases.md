# DomainSpec-core historical cases: research-to-action transitions

## Scope and method

This is a bounded, read-only reconstruction of transition episodes in
`C:/Users/victo/domainspec-core`. It uses the append-only dispatch ledger as the
starting index, then checks the linked findings, specifications, run results,
validation receipts, and implementation artifacts. Repository sources were not
modified and commands or tests described by historical receipts were not rerun.

The current ledger is strongly asymmetric: a mechanical count of opening rows
finds 190 `research`, 89 `review`, four `experiment`, one `code`, and one `plan`
dispatch. Consequently, absence of a `code` row is not credible evidence that
nothing was built. The single `code` row is
`2026-06-15-research-md-lean-permguard-edit`; the four experiment rows are the
three Mint rows around [the first criterion and run](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1739)
and the later [intent-population run](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3769).

## Direct answer

The corpus supports recommending an experiment after research, but not from a
dispatch count or the absence of `code`. The strongest historical pattern is:

1. linked research narrows a load-bearing claim rather than merely closing;
2. a surviving uncertainty is expressed as a falsifiable criterion;
3. a named decision would change under either result;
4. prerequisite owners, inputs, and claim ceilings are settled; and
5. no current artifact or prior run has already answered the question.

If (4) is false, the recommendation should be the missing decision, specification,
or build step required to make the experiment admissible. If (5) is unknown, the
system should abstain and ask for or perform an artifact-state check. The cases
below are evidence for that distinction.

## Episode 1 — Machine-map research to a falsifying Mint experiment

**Originating objective.** The `2026-06-24-machine-map-and-moat` research asked
for a reconciled system map, first-build sequence, and moat verdict
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1505)).
It corrected the original framing: the “foundry” claim depends on keeping outer
meta-authority distinct from the minted domain's object-authority
([findings](../../../domainspec-core/development/machine-map/findings.md#L39)),
and the overall machine remained a roadmap, “mostly unbuilt”
([findings](../../../domainspec-core/development/machine-map/findings.md#L15)).

**Research sequence and epistemic advance.** The advance was not closure alone:
the research converted a broad “make the machine” thesis into a narrower,
discriminating claim about whether Mint actually preserves the meta/object
boundary. The following experiment froze one hypothesis and explicitly rejected
self-confirming evidence such as “files exist in the right folders”
([criterion](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L62),
[circularity guard](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L75)).

**Next action and build state.** The criterion was preregistered before the run
([criterion](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md#L23));
the run then minted and scored three domain spines. It falsified the strong
uniform foundry-boundary claim because the research domain failed Obs-A
([run findings](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md#L16),
[verdict](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md#L23)).
A corrected content-autonomy criterion later survived all nine cells while
retaining an explicit weakness in one lexical discriminator
([second run](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md#L109),
[caveat](../../../domainspec-core/cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md#L116)).
Concrete minted artifacts were built inside the experiment folders, but this was
experimental evidence, not a shipped runtime.

**Linkage quality: high but not ledger-native.** The criterion cites the
machine-map synthesis and the experiment follows it chronologically; neither row
contains a machine-readable parent/objective edge. The linkage is therefore
artifact-backed, not derivable from row type and time alone.

**Plausible counterinterpretation.** This is evidence that an experiment was a
productive next step, not evidence that the ledger itself could have known when
to suggest it. The decisive bridge—the falsifiable foundry-boundary claim—lives
in artifacts.

## Episode 2 — Two high-attention researches to a specification, not yet a run

**Originating objective.** The first research asked whether small-parameter
models can have unusually large usable context and requested testable hypotheses
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L1726)).
Its substantive result separated visible context from usable context and selected
a parameter-normalized measurement harness as the best lane
([findings](../../../domainspec-core/research/high-attention-low-parameter-models/findings.md#L7),
[verdict](../../../domainspec-core/research/high-attention-low-parameter-models/findings.md#L38)).

**Research sequence and epistemic advance.** A second research dispatch explicitly
started from the first one's unresolved methodology and sought a reproducible,
resource-bounded protocol
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3548)).
It selected concrete comparison families, fixture classes, controls, measures,
and a staged escalation policy. Its own verdict is unusually useful telemetry:
the research is “decision-ready input” for a later specification, while the
runnable-witness gate is KILL and execution remains blocked
([protocol findings](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol-research/findings.md#L7),
[verdict matrix](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol-research/findings.md#L86)).

**Next action and build state.** A complete specification/work-pack package was
subsequently authored, but it declares `executionReadiness: blocked`
([spec](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol/SPEC.md#L4))
and lists immutable artifacts and human decisions required before a run
([execution boundary](../../../domainspec-core/research/high-attention-low-parameter-models/experiment-protocol/SPEC.md#L136)).
No executable experiment result was found in this bounded folder.

**Linkage quality: high.** The second goal names the existing findings, its folder
is nested below the first, and the specification points back to the research as
its discovery artifact. Again, that continuity is visible in prose and paths,
not a parent field.

**Plausible counterinterpretation.** “Several resolved researches and no code”
would suggest an experiment too early here. The evidence-backed recommendation at
the second close was to author/freeze the specification and resolve owner choices,
not to run. The later specification still says the run is blocked.

## Episode 3 — IOLM research led to implementation without a `code` dispatch

**Originating objective.** `2026-07-22-iolm-workable-example-research` asked for
the fastest governed route to a runnable local graph UI while preserving the
blocked compiler proof boundary
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3710)).

**Epistemic advance.** The findings selected an exact fixture-backed SWU, write
boundary, input bundle, native-web stack, and claim ceiling. At research close it
said the UI did not yet exist and could be built after proposal approval
([findings](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-22-iolm-workable-example/findings.md#L7),
[verdict](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-22-iolm-workable-example/findings.md#L17)).

**Next action and build state.** The implementation now exists at the exact
selected path, with server, HTML/CSS/ES modules, binding schemas, Python and Node
tests, and run receipts. Its README provides runnable commands and preserves the
non-authority boundary
([README](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/README.md#L1),
[checks](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/README.md#L30)).
`git log -- <research-folder> <implementation-folder>` attributes both surfaces
to commit `3e31c8e79` on 2026-07-23, immediately after the research. A later replay
is currently BLOCK because the pinned source fixture drifted, which is evidence
that something was built and later became stale—not that nothing was built
([validation receipt](../../../domainspec-core/cyberAlchemy-v2/development/iolm-workable-example/generated/runs/20260722T182915Z-firefox-replay/validation-summary.json)).

**Linkage quality: high.** Exact path and interface correspondence plus a shared
commit connect findings to implementation. There is no corresponding `code`
opening in the ledger.

**Plausible counterinterpretation.** The later BLOCK could be mistaken for
“unbuilt.” It actually reports a fail-closed hash mismatch in an existing system.
Recommending an experiment from ledger-type absence would be strictly worse than
recommending repair/revalidation.

## Episode 4 — Research contract to an admitted experiment and owner decision

**Originating objective.** `2026-07-22-agent-reasoning-engine-contract` began as
research into the smallest non-vacuous pre-action reasoning-engine contract
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3723)).
The later experiment row explicitly records that definition, experiment design,
planning, and evidence mechanics were complete before the clean rerun
([experiment](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L3769)).

**Epistemic advance and next action.** The pre-registered 15-sample population
run executed rather than merely proposing a witness. All 15 source locks and
structural validations passed, including 3/3 unchanged-rule holdouts
([result](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L11)).
It exposed consequential missingness in 15/15 records and replacement risk in
11/15, then stopped at an explicit owner gate rather than promoting its result
([pressure findings](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L38),
[next gate](../../../domainspec-core/cyberAlchemy-v2/development/agent-reasoning-engine/experiments/intent-schema/runs/2026-07-22-intent-schema-02/RESULT.md#L67)).
The experiment folder contains the populated records, manifests, reducer, audit
script, metrics, evidence cards, and adjudication packet.

**Linkage quality: medium-high.** The experiment context names completion of the
upstream stages, but the ledger does not persist their individual artifact links
or a parent ID. The result itself provides strong executed evidence.

**Plausible counterinterpretation.** A clean structural pass might look like
validation of the schema. The result explicitly limits itself to bounded shape
evidence and leaves schema selection pending; the experiment recommended a human
decision, not implementation.

## Episode 5 — Ontology research advanced, but owner selection and build came first

**Originating objective.** The July 26 gap research asked for the smallest
defensible working ontology prototype and a falsifiable acceptance contract
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L4054)).

**Research sequence and epistemic advance.** It found that the repository did not
yet contain a working ontology prototype, separated present narrow machinery from
stale bindings, and specified a finite positive/fail/indeterminate witness
([findings](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L7),
[current execution state](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L18)).
Its ordered route begins with contract freeze and implementation of a closed-world
validator, not an experiment run
([build slices](../../../domainspec-core/cyberAlchemy-v2/development/research/2026-07-26-ontology-working-prototype-gap/findings.md#L136)).

Four days later, ontology-runtime API research narrowed the reusable runtime
contract further. It classified every endpoint as designed and owner-absent and
blocked implementation until runtime-contract and implementation owners are
selected
([findings](../../../domainspec-core/cyberAlchemy-v2/ontology/development/2026-07-30-ontology-runtime-api-research/findings.md#L30),
[endpoint boundary](../../../domainspec-core/cyberAlchemy-v2/ontology/development/2026-07-30-ontology-runtime-api-research/findings.md#L357)).
The folder then accumulated Define/Design/Plan/Work-Pack artifacts, but the
research itself says these do not authorize or prove a runtime.

**Next action and build state.** The justified next action was owner selection and
bounded implementation of the finite witness. Suggesting “run an experiment” at
the first or second research close would skip the missing apparatus and owner.

**Linkage quality: medium.** Topic, sources, and dates support a chain, but no
machine-readable parent/objective edge proves that the two dispatches are the
same lineage. A trigger must not silently infer identity from “ontology” words.

**Plausible counterinterpretation.** The finite witness could itself be called an
experiment in casual language. In this repository's typed workflow it is first a
validator/runtime implementation with acceptance tests; relabeling it would
collapse `code` and `experiment` rather than improve routing.

## Episode 6 — Research after an existing build

**Originating objective.** The Body War gap research explicitly opened after the
SuggestedTrack API/UI and validation already existed
([ledger](../../../domainspec-core/telemetry/agents/subagents-dispatch.yaml#L4268)).

**Epistemic advance.** It distinguished a current fake-provider developer path
from consent, route-binding, retry, hosted-provider, and participant evidence.
The attached current-validation receipt records successful build/validation,
unit, Postgres e2e, and Chromium runs
([receipt](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md#L13))
while sharply limiting what those passes prove
([proof ceiling](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md#L37)).

**Next action and build state.** The findings select LP-01, a bounded product fix,
before moderated local participant sessions; they explicitly do not authorize or
execute it
([findings](../../../domainspec-core/projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/findings.md#L24)).
Something substantial was already built even though no `code` dispatch describes
that build in this ledger.

**Linkage quality: high for current state, low for original build provenance.**
The receipt binds tests to commit `b7d60c96...`; the ledger does not explain the
build's complete history.

**Plausible counterinterpretation.** Multiple research rows around Body War might
look like pre-build analysis when they are actually post-build gap analysis.
After LP-01 passes, a bounded participant test may be appropriate, but the correct
recommendation before that is implementation.

## Counterexamples to the proposed shortcut

The rule “multiple resolved research dispatches plus no code dispatch means
recommend experiment” fails in at least four distinct ways:

| Failure mode | Concrete case | What the shortcut gets wrong |
|---|---|---|
| Build exists without `code` telemetry | IOLM and Body War | Infers non-construction from a nearly unused dispatch type. |
| Research is decision-ready but execution apparatus is absent | High-attention protocol | Recommends a run before owner decisions, fixtures, scorer, runtime, and admission. |
| The next uncertainty is an implementation/ownership gap | Ontology prototype/runtime | Calls acceptance-contract construction an experiment and skips the owner gate. |
| A prior experiment already answered or narrowed the claim | Mint; intent-population | Risks recommending a duplicate run instead of consuming the result and routing its residue. |

`resolved` is also too weak: it says the dispatch closed successfully, not that a
claim survived, a decision became ready, or the same objective continued. The
high-attention findings expose richer local states—`decision-ready`, runnable
witness `KILL`, and execution `blocked`—that are absent from the close row.

## Candidate transition signals, ranked

### 1. Explicit decision-bearing experiment handoff — strongest

**Signal.** A linked research artifact names (a) one surviving falsifiable claim,
(b) the decision owner, (c) outcomes that would change the decision, (d) frozen or
admissible inputs, and (e) a recommendation to test. Mint and the intent-population
run are the positive precedents.

**Why strong.** It observes epistemic readiness and action relevance directly,
rather than inferring them from counts.

**Strongest invalidator.** Any required criterion, owner, input lock, admission
gate, or claim ceiling is still unresolved. In that case recommend the missing
precondition, not the experiment.

### 2. Surviving claim plus closed negative and an unspent decision — strong

**Signal.** Reviewer/auditor artifacts preserve a non-vacuous claim, state its
collapse-test, and show that no existing run or implementation evidence answers
it. Both possible outcomes have explicit downstream consequences.

**Why strong.** It distinguishes “research accumulated” from “research produced a
testable fork.”

**Strongest invalidator.** A current artifact, prior run, or accepted owner
decision already resolves the fork; recommend consuming/revalidating that evidence
instead.

### 3. Explicit research-to-specification readiness with prerequisites satisfied — medium-strong

**Signal.** Findings mark research as decision-ready for an experiment
specification, and the later specification's readiness/admission checklist is now
fully satisfied.

**Why not stronger.** High-attention shows that decision-ready research and a
written specification can coexist with a blocked run. The trigger needs the later
state, not only the research close.

**Strongest invalidator.** The current specification still says `blocked`,
`decision-gated`, `NOT_RUN`, or lists unresolved human choices.

### 4. Repeated linked research with stable objective and diminishing new residue — medium

**Signal.** Two or more research artifacts share an explicit objective/parent,
each consumes the previous result, the surviving claim remains stable, and later
work mostly refines test mechanics rather than opening new conceptual questions.

**Why only medium.** The present ledger lacks reliable lineage fields; folder
nesting, wording, and temporal adjacency can misjoin unrelated work.

**Strongest invalidator.** The later dispatch changes the objective, introduces a
new owner boundary, or records materially new open questions. Continued research
may then be productive rather than inertial.

### 5. No current construction found after artifact-level verification — weak supporting signal

**Signal.** A bounded current-byte check across the declared write surface and
linked repositories finds no implementation, run receipt, or accepted witness.

**Why weak.** It can support signals 1–4 but cannot justify a recommendation by
itself. IOLM and Body War show why ledger-type absence is insufficient.

**Strongest invalidator.** Any unregistered, cross-repository, externally hosted,
stale-but-real, or differently typed build is found.

### Rejected signal: count/time threshold

“N resolved researches” or “T days without `code`” has no defensible evidential
rank in this corpus. Its strongest invalidator is already observed: successful
builds exist without `code` rows, while long research sequences can correctly end
in owner decisions, specifications, or further research.

## Implication for a future recommendation trigger

The ledger can cheaply nominate candidates, but artifact evidence must adjudicate
them. A defensible trigger would therefore be two-stage:

1. **Nominate:** cluster explicitly linked research under the same objective and
detect a surviving experiment-shaped handoff.
2. **Adjudicate:** read the latest findings/spec/result plus declared write surfaces
to confirm decision relevance, readiness, no prior answer, and no existing build
that changes the route.

The recommendation should carry its evidence and abstention reason, for example:
“Research R1/R2 leaves hypothesis H untested; criterion C is frozen; decision D
changes under either outcome; no run receipt was found. Suggest experiment E.”
If any clause is unsupported, the system should name the missing evidence rather
than imply that an experiment is due.
