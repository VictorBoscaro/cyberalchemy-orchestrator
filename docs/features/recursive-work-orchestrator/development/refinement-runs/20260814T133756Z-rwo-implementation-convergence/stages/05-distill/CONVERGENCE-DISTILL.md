# Convergence Distill — Executable RWO Evidence Boundary

Run ID: `20260814T133756Z-rwo-implementation-convergence`
Mode: `standard`
Budget: one proposal track, two recursive rounds, one reconciliation
Verdict: `pass`
Selected unit: `RWO-CVG-001 executable convergence boundary`
Implementation effect: `none`

## Outcome Brief

The smallest coherent next implementation unit is not a unified service or a
dispatch-to-RWO adapter. It is one executable convergence boundary that locks
the current source/status tuple, runs the existing implementation checks without
sharing an oracle, exposes the seat-address contradiction as a dual-status
negative witness, and emits separate claim axes with no aggregate pass bit.

This is implementation infrastructure rather than lifecycle bookkeeping: it
turns the current Python, Rust, Go, and shared-dispatch evidence into a
repeatable machine-observable boundary. It deliberately does not choose the
semantic repair or fabricate missing dispatch graph/event semantics.

## Objective and target context

- Seed: refine the current CyberAlchemy orchestrator implementation with RWO.
- Target context: the next finite local implementation Work Pack, before any
  semantic-contract change, adapter adoption, lifecycle selection, or external
  compatibility campaign.
- Output artifact: an implementation design for a deterministic local
  convergence verifier and its bounded evidence formats.
- Optimization goal: maximize trustworthy next-step information while keeping
  every authority boundary explicit and every mutation reversible.

## Broad layer map

```text
CyberAlchemy orchestration implementation convergence
  -> evidence and authority convergence
     -> executable claim separation
        -> RWO-CVG-001 executable convergence boundary
           -> exact source/status lock
           -> independent runner observations
           -> formal mismatch and integration-boundary witnesses
           -> per-axis report and claim matrix
```

The selected abstraction level is implementation-conformance infrastructure.
It is below architecture and planning, but above any one language's tests. It
observes implementations and never becomes their semantic or lifecycle owner.

## Candidate split

| Candidate | Closure | Hidden authority | Immediate value | Result |
| --- | --- | --- | --- | --- |
| A. Merge Python, Rust, Go, and shared dispatch into one service | no | collapses semantic, physical, launch, and lifecycle owners | low until several contracts are invented | reject |
| B. Implement a dispatch-to-RWO adapter now | no | invents graph edges, event acceptance, and delivery ownership absent from current dispatch rows | ambiguous | reject |
| C. Repair the colon-form seat address now | narrow but decision-blocked | chooses semantic-contract policy without its owner | high after owner decision | route, not select |
| D. Execute DRT-001 lifecycle adoption | coherent but wrong layer | substitutes lifecycle progress for implementation convergence | narrow | defer to existing continuation |
| E. Build an executable convergence boundary | yes | none if claim axes stay separate | high and reversible | select |

## Role conversation trace

The confirmed dispatch authorizes exactly one native helper for s07. Therefore
the Standard Distill Proposer and Balancer roles are executed as labeled parent
simulation; no additional helper is spawned.

### Round 1

Proposer claim: select a local cross-language test runner that invokes all
current suites and returns one convergence result.

Evidence: each implementation already has meaningful local tests, and a single
entry point would improve repeatability.

Balancer objection — `owner-collapse`: one result would imply equivalent test
meaning, hide skipped or blocked axes, and let shared-dispatch adjacency appear
as integration.

Reconciliation — `revise`: replace the aggregate result with an exact source
lock, independent axis runners, negative boundary witnesses, and a claim matrix.
The package may have an execution-complete field, but never an implementation-
conforms aggregate bit.

### Round 2

Proposer claim: split the source lock, runner, witnesses, and report generator
into four independent first units.

Evidence: each component can be implemented and unit-tested separately.

Balancer objection — `meaning-loss-when-split`: a source lock without executed
observations is inventory; a runner without claim bindings is just a script; a
witness without the dual current/formal status invites accidental repair; and a
report without fail-closed inputs can turn absence into green evidence.

Reconciliation — `accept-selected-boundary`: keep them as four SWUs inside one
coherent delivery unit. The first SWU is the lock schema and validator, but the
unit is not complete until the report binds all four parts.

Cycle guard: further reduction repeats those four names without preserving the
trust property. Stop after the confirmed two-round budget.

## Selected unit contract

### Responsibility

Given an exact local source/status lock and explicit runner descriptors, produce
a deterministic report of what the current implementation evidence supports,
what failed or could not run, and which claims remain unsupported. Fail closed
on source drift, missing tools, command failure, malformed evidence, or a runner
that attempts a forbidden external effect.

### Inputs

1. `rwo-convergence-lock/v1`: repository-relative path, SHA-256, size, role,
   authority posture, lifecycle posture, and allowed observer for every bound
   source.
2. `rwo-convergence-runners/v1`: one exact command descriptor per axis with
   working directory, executable identity/version or discovery rule, bounded
   environment, timeout, isolation path, and expected receipt type.
3. Independent accepted/frozen expectations already owned by the semantic
   contract and conformance package.
4. A literal current colon-form seat payload and the bound inline schema used
   to record both `current_implementation_observed` and
   `formal_contract_conformance` outcomes.
5. An explicit shared-dispatch relation declaration whose initial value is
   `adjacent-not-adapter` and whose evidence is the exact bound source/test pair.

### Outputs

1. `rwo-convergence-report/v1` with separate axes for semantic target, Python,
   Rust, Go, shared dispatch, cross-language witnesses, lifecycle, ontology,
   portability, and external Eve. Each axis uses only `pass`, `fail`, `blocked`,
   `not-run`, or `not-applicable` and carries exact evidence.
2. `rwo-claim-matrix/v1` mapping each observed check to supported and explicitly
   unsupported claims.
3. A deterministic seat-address witness showing that current candidate behavior
   and formal conformance can have different statuses without changing either.
4. An integration-boundary witness proving that no dispatch-to-RWO mapping was
   evaluated when no versioned adapter declaration exists.
5. A validation receipt that preserves the first failure and lists every
   unexecuted downstream check.

### Hard invariants

1. No aggregate conformance boolean or score exists.
2. Missing, skipped, stale, or malformed evidence cannot become `pass`.
3. Expected semantic observations are never generated from the implementation
   under review.
4. Source hashes and lifecycle/status labels are both binding.
5. Runner output is evidence only for its declared claim axis.
6. Rust remains the only semantic compiler/reducer/command owner; the verifier
   cannot recreate its outputs.
7. Go physical evidence cannot promote semantic or external-compatibility
   claims.
8. Shared dispatch remains `adjacent-not-adapter` until a separately owned,
   versioned, lossless mapping is supplied and tested.
9. The colon-form address remains current candidate behavior and formal
   nonconformance; the verifier cannot choose or apply a repair.
10. Network, credentials, live Eve, lifecycle transitions, Git, publication,
    deployment, and canonical mutation are forbidden.

## Internal SWU split

1. `CVG-001 source/status lock` — schema, exact manifest, validator, drift and
   candidate-versus-accepted negatives.
2. `CVG-002 isolated axis runners` — exact Python, Rust, Go, and shared-dispatch
   command descriptors, temp output isolation, toolchain/cwd recording, and
   first-failure propagation.
3. `CVG-003 boundary witnesses` — seat dual-status fixture, independent-oracle
   guard, shared-dispatch `adjacent-not-adapter` witness, and missing-adapter
   negative.
4. `CVG-004 report and claim matrix` — deterministic schema, complete axis
   coverage, unsupported-claim inventory, replay stability, and end-to-end
   validator.

Each SWU has one primary responsibility and can be reviewed independently. The
selected unit closes only when all four recompose.

## Closure and recomposition proof

The unit has named inputs, outputs, one abstraction level, no hidden mapping,
and one responsibility: determine the claim support of an exact current tuple.

```text
exact source/status lock
  + independently bounded runner observations
  + explicit negative boundary witnesses
  + deterministic per-axis claim projection
  = trustworthy current convergence report

trustworthy report
  -> semantic owner can choose a seat-address repair with exact impact
  -> integration owner can design or reject a dispatch-to-RWO adapter
  -> lifecycle owner can adopt only the evidence it selected
  -> reviewers can distinguish local implementation evidence from publication
```

Splitting below this boundary loses the relationship between evidence and claim.
Expanding above it would require semantic, adapter, lifecycle, or external
decisions that this run cannot own.

## Evolution profile

Expected evolution is additional language implementations, contract/profile
versions, adapter candidates, and compatibility campaigns. The smallest useful
extension seam is a versioned axis descriptor plus a new claim-matrix entry.
No plugin system, generalized workflow engine, distributed result store, or
policy DSL is justified by the current local scope.

## Technique pack trace

The full machine-readable trace is in `TECHNIQUE-TRACE.json`.

- Abstraction-level guard: pass; the unit stays at implementation-conformance
  infrastructure.
- Recomposition proof: pass; all four internal parts are necessary and jointly
  sufficient for the bounded report.
- Evolution profile: pass; versioned axes are the only preserved extension.
- Frame-expiry note: recorded below.
- Navigable result: pass; start with CVG-001, then proceed in order.
- Cognitive-load check: triggered; the report uses fixed axes and explicit
  unsupported claims instead of one narrative status.
- Requisite-variety check: triggered; the five-state axis result preserves
  pass, fail, blocked, not-run, and not-applicable distinctions.
- Boundary-object check: triggered; schemas and claim matrices are the review
  boundary across Python, Rust, Go, integration, and lifecycle owners.
- Concept-vs-knowledge check: triggered; current observations are knowledge-
  bound, while a future adapter remains a design concept.
- Premortem: triggered and closed with guardrails below.
- Set-based tournament: skipped; the confirmed Standard budget has one proposal
  track and the candidate split is an internal comparison, not competing teams.

## Premortem

Likely failure: the harness becomes a green dashboard by converting missing
tools, skipped suites, stale source locks, or absent adapters into successful
axes.

Guardrails: no aggregate pass; closed result enum; source/status preflight;
first-failure preservation; an explicit not-run inventory; unsupported-claim
output required even after every runnable axis passes; and negative fixtures
for stale hashes, candidate relabeling, missing tools, masked exits, self-
generated expectations, colon-address drift, and missing adapter declarations.

## Deferred complexity and stable tensions

- Seat-address repair: routed to the semantic-contract owner.
- Dispatch-to-RWO adapter: deferred until source graph, accepted-event, and
  delivery mappings are explicit.
- Live Eve: deferred to a separately authorized compatibility route.
- Unicode portability beyond the host pin: deferred to its own campaign.
- DRT-001 closeout: continues through its existing lifecycle route.
- Ontology promotion and definition acceptance: separate owner actions.
- Git publication: separate ownership inventory and publication action.

No deferred item is required for the selected unit to close. They remain
visible report axes or unsupported claims.

## Frame-expiry note

Re-run Distill if any of these changes: the semantic owner accepts a seat-
address repair; an explicit dispatch-to-RWO adapter contract is accepted; live
Eve becomes an in-scope bound dependency; the Rust/Go ownership split changes;
or the user selects lifecycle adoption instead of implementation convergence.

## Navigation guide

Start with CVG-001. Do not implement runners until the lock can distinguish
accepted, candidate, proposal-only, lifecycle-pending, and adjacent source
postures. Then implement CVG-002 and CVG-003 independently. CVG-004 closes only
when it can reproduce byte-identical reports from identical evidence and retain
all unsupported claims.

The next route is s06 Invoke Design. Design must define the closed schemas,
process boundary, source hygiene, isolation, failure semantics, test matrix,
and exact non-goals. Implementation remains unauthorized until a later Work Pack
is selected and admitted.

## Distill Result

- Target context: next finite local implementation Work Pack for current RWO
  convergence.
- Objective and output artifact: executable evidence boundary; Invoke Design
  package followed by a finite Work Pack.
- Mode and budget: Standard; one track, two rounds, one reconciliation.
- Proposal tracks: one, with labeled parent Proposer and Balancer roles because
  the sole authorized native helper is reserved for s07.
- Recursive rounds: 2/2.
- Verdict: `pass`.
- Current smallest coherent unit: `RWO-CVG-001 executable convergence boundary`.
- Optimization point: smaller fragments lose evidence-to-claim meaning; larger
  units require unauthorized semantic or integration choices.
- Evidence emission: `not-configured`; no accepted event ledger was supplied.
- Telemetry: `not-configured`; recorded as residue, not readiness authority.
- Next route: `invoke design`.
