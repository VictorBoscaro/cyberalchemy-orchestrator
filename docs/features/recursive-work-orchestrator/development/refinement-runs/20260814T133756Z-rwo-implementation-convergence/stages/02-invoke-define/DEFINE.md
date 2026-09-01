# Define — RWO Implementation Convergence

Run ID: `20260814T133756Z-rwo-implementation-convergence`
Invoke mode: `define`
Status: `pass`
Target owner cycle: Recursive Work Orchestrator implementation convergence
Implementation effect: `none`

## Outcome Brief

The current implementation is not missing a semantic kernel or a durable local
prototype. It is missing one evidence-bound convergence boundary that says how
the Python oracle, Rust kernel, Go durable host, shared dispatch workflow,
canonical sources, and lifecycle receipts relate without inheriting each
other's authority. This definition fixes that planning boundary and keeps the
remaining contract, portability, external-integration, and lifecycle gaps
visible.

## Boundary and Next Decision

- Changed: this run now has a convergence definition, linked glossary,
  technique trace, and transport report.
- Unchanged: implementation and tests, accepted semantic sources, canonical
  documentation, definitions, ontology, lifecycle, Git, external Eve, and
  external systems.
- Open questions: which current gap is the smallest coherent next unit and
  whether shared dispatch needs an explicit RWO adapter or must remain separate.
- User decision: none at this stage; the confirmed Refine route owns continued
  analysis but grants no implementation authority.
- Next action: s03 attacks the owner split and evidence taxonomy before s05
  selects a unit.

## 1. Discovery and intent record

Define discovery is satisfied by the existing candidate discovery package
`development/discovery/20260808-rwo-are-inference-boundary/`. Its useful,
still-valid constraint is owner separation: RWO owns structural readiness,
reasoning and provider execution remain outside the kernel, and an accepted
event closes the loop only through its external acceptance owner. The package
is discovery evidence, not current implementation or promotion authority.

No discovery waiver is used. No new interview question was needed: the user
confirmed the exact Refine dispatch, and the strict Context Builder pack closed
all ten definition obligations without a blocker-level choice.

Template selection: reuse the existing RWO Refine `DEFINE.md` structure. It is
eligible because this is a run-local refinement definition, not a new canonical
feature specification. The DomainSpec canonical template would broaden the
artifact family and duplicate already accepted RWO sources.

## 2. Problem

The repository already contains three complementary candidate implementations
and one adjacent shared dispatch compiler:

1. Python independently calculates semantic observations and provides a local
   prototype boundary.
2. Rust owns raw admission, normalized values, compilation, reduction,
   structural defects, immutable command identity, and retry classification.
3. Go durably coordinates physical state around the real Rust child and a
   bounded fake-Eve leaf.
4. The shared dispatch workflow validates governance records and compiles bound
   agent launch plans and workflow envelopes.

These surfaces are individually meaningful, but no current artifact proves
that they are one integrated runtime. Their evidence, semantic authority,
physical authority, lifecycle status, and claim ceilings must be joined by
explicit contracts rather than proximity in one repository.

## 3. Defined convergence boundary

```text
Definitions and accepted semantic contract
       |
       v
Architecture and frozen schemas/vectors
       |
       +--> Python oracle --------------------------+
       |                                            |
       +--> Rust admission/compiler/reducer --------+--> comparable observations
       |                                            |
       +--> Go durable physical host -> fake Eve ---+
       |
       `--> shared dispatch launch compiler -- explicit adapter decision pending

Comparable observations + bounded receipts
       -> evidence projection
       -> lifecycle adoption by a separate owner
       -> never automatic semantic, ontology, release, or production authority
```

Implementation convergence means proving or explicitly rejecting each mapping
between these surfaces under one exact source tuple. It does not mean merging
their code, choosing one language, moving physical state into Rust, moving
semantic scheduling into Go, or treating the shared dispatch compiler as an
RWO adapter without a versioned mapping.

## 4. Owners and forbidden substitutions

| Owner | Current owned responsibility | Forbidden substitution |
| --- | --- | --- |
| Definitions owner | term boundaries | runtime or implementation acceptance |
| Semantic-contract owner | exact tuple, admission, normalization, identities, compile/reduce outcomes, defects, retry boundary | transport, persistence, event acceptance, delivery, execution, or effects |
| Architecture owner | components, interfaces, invariants, evolution seams | changing the exact semantic contract |
| Python implementation | independent reference/oracle and local test doubles | production authority or self-approval of Rust/Go behavior |
| Rust implementation | raw admission and the only semantic compiler/reducer/command owner | physical delivery, provider sessions, lease timing, effect authorization |
| Go implementation | durable physical log, attempts, fences, session correlation, raw terminal evidence, Rust-child hosting | graph interpretation, command fabrication, semantic retry, accepted-event truth |
| Shared dispatch workflow | governance-record validation and bound agent launch-plan compilation | RWO graph compilation, cursor reduction, semantic event acceptance, or command identity |
| External acceptance/journal owner | decides and durably records accepted lifecycle facts | delegating truth or acceptance to RWO delivery receipt |
| Ontology owner | removable proposal-only architecture projection | vocabulary, semantic contract, runtime conformance, or promotion |
| Lifecycle owners | selection, admission, execution receipts, closeout | reconstructing lifecycle completion from aggregate local tests |

## 5. Shared dispatch integration seam

`implementations/server/runtime/dispatch_workflow.py` currently compiles one
validated dispatch record into a bound launch plan. Its tests prove registry
resolution, root/child authority checks, and exact prompt/manifest binding.
No selected evidence shows that it consumes an RWO `WorkGraph`, derives an RWO
cursor, supplies an externally accepted event, or executes an RWO
`CommandIntent`.

Therefore the shared workflow is adjacent integration infrastructure, not a
conforming RWO adapter. Design must choose one of two lawful outcomes:

- keep it separate and document where a future owner would translate between
  governed dispatch facts and admitted RWO values; or
- define a versioned, lossless adapter contract with exact source/target tuples,
  accepted-event ownership, command-delivery ownership, fixtures, and negative
  evidence.

Directly importing its dispatch rows as graphs or treating launch completion as
an accepted event is forbidden hidden glue.

## 6. Evidence axes

| Axis | Current evidence | Maximum current claim |
| --- | --- | --- |
| Semantic target | definitions, accepted contract, schemas, frozen vectors | normative language-neutral target |
| Python | vector/prototype suites and independent calculation | candidate reference behavior |
| Rust | raw-admission, frozen-vector, child-protocol, differential tests | host-pinned candidate semantic implementation |
| Go | gRPC child boundary, append-only store, attempts/fences, fake-Eve and terminal tests | single-host/filesystem candidate physical coordinator |
| Cross-language | Python/Rust witness and real Rust child observed by Go | selected local parity, not universal implementation equivalence |
| Shared dispatch | exact bound launch-plan tests | adjacent governance/launch integration only |
| Lifecycle | candidate campaign report plus unconsumed DRT-001 route | local implementation proof; governed closeout incomplete |
| Ontology | `rwo-architecture@0.3.0` package integrity | proposal-only projection; runtime conformance indeterminate |
| External Eve | in-process selected-shape fake | no external Eve compatibility |

## 7. Drift and residue taxonomy

1. `semantic-contract`: the colon-form `seatv1` address conflicts with the
   frozen identifier grammar. Current behavior is not formal conformance.
2. `implementation-portability`: Rust raw admission depends on observed ICU 74
   and Unicode 15.1.
3. `integration-contract`: no exact shared-dispatch-to-RWO mapping is evidenced.
4. `external-compatibility`: fake Eve does not prove live Eve behavior.
5. `durability-scope`: one process owner and filesystem do not prove multi-host
   coordination or hardware power-loss guarantees.
6. `lifecycle`: aggregate candidate proof is not six Task Session terminal
   receipts; DRT-001 closeout prerequisites remain unapplied.
7. `authority/projection`: ontology, docs, and evidence reports cannot accept
   implementation or promote vocabulary.
8. `repository-state`: current uncommitted/untracked bytes are reviewable local
   state, not publication evidence.

Each later artifact must retain the class, exact source, affected claim, owner,
and route. A later validation pass may close an observation gap but cannot
silently close a semantic or lifecycle decision.

## 8. Required convergence invariants

1. The accepted source tuple is rehashed before every conformance claim.
2. Rust remains the only creator of semantic graph, cursor, outcome, and
   command identity.
3. Python expectations are independently calculated or frozen; they never
   import Rust/Go observations as their oracle.
4. Go persists and coordinates physical facts without decoding graph meaning.
5. Delivery metadata, attempts, leases, fences, provider sessions, and raw
   observations remain outside semantic identity.
6. Shared dispatch facts cross into RWO only through an explicitly owned,
   versioned adapter and an externally accepted event projection.
7. No local success can self-bless frozen expectations or lifecycle state.
8. Negative evidence is required for duplicate, divergent, unknown-version,
   lossy-mapping, stale-fence, ambiguous-delivery, wrong-session, and
   authority-leak cases.
9. Formal residue blocks only the claims it affects; it does not erase valid
   narrower evidence.
10. A final plan remains non-executed until a later owner selects and admits an
    exact SWU.

## 9. Route decision

Selected: current implementation convergence.

Rejected for this run:

- live Eve expansion, because it requires external facts, network behavior,
  credentials, and a separately authorized compatibility route;
- DRT-001 closeout-only, because it is a narrower lifecycle continuation and
  does not resolve the whole implementation convergence question; and
- a language rewrite or unified service, because no evidence shows that code
  consolidation improves semantic fidelity or ownership.

## 10. Definition-scope sanity check

- Mode: `standard`, embedded Invoke Define sanity check.
- Role execution: labeled parent simulation; the one authorized native helper
  is reserved for independent s07 design review.
- Proposer: define a single integrated RWO product runtime across all current
  surfaces.
- Balancer objection (`owner-collapse`): that unit would make evidence,
  lifecycle, launch binding, physical coordination, and semantics appear to
  share one authority.
- Reconciliation: define only the convergence boundary, evidence axes, drift
  taxonomy, and invariants; defer unit selection to s05.
- Closure: the definition has one responsibility—state what must be proven or
  explicitly separated before a new implementation plan can be trusted.
- Recomposition: s05 selects a unit, s06 designs it against these invariants,
  and s09 maps it into a finite Work Pack.
- Verdict: `pass`.

## 11. Claim ceiling

This definition is run-local planning evidence. It does not change the RWO
contract, choose an adapter design, validate current product bytes, synchronize
lifecycle, promote the ontology, authorize implementation, publish Git state,
access Eve, deploy, or establish production readiness.

## Invoke Result

- Mode: `define`
- Phase status: `pass`
- Mode contract: `.agents/skills/invoke/define.md`
- Template selection: existing RWO Refine definition shape; no canonical
  template family or upstream artifact mutation.
- Discovery evidence: existing RWO/ARE/inference boundary discovery; no waiver.
- Interview: zero questions; confirmed route plus strict context closed inputs.
- Glossary: linked in `GLOSSARY-LINKS.md`; no canonical term mutation.
- Implementation layering: explicit gap carried to s09 Invoke Plan.
- Dispatch techniques: recorded in `DISPATCH-TECHNIQUE-TRACE.json`.
- Distill validation: `pass`; boundary definition is coherent, unit selection
  remains s05-owned.
- Unresolved gaps: eight classified residue groups above, none hidden.
- Next route: s03 `interrogation:refine-review`.
