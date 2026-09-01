# Recursive Work Orchestrator Definitions

Status: lifecycle-neutral candidate definition content. Canonical placement is
proved only by an external exact owner-acceptance and post-creation validation
receipt.

These are the proposed normative term definitions for the RWO core. They define
semantic boundaries, not an implementation, runtime, service, authority grant,
or ontology promotion. Exact operation and value rules remain governed by
`RWO-SEMANTIC-CONTRACT/1.0.0`.

---

<a id="def-rwo-001"></a>

## Recursive Work Orchestrator

- **ID:** DEF-RWO-001
- **Status:** candidate
- **Scientific/formal voice:** The Recursive Work Orchestrator is a
  deterministic structural system `RWO = (C, R)` where compiler `C` maps one
  admitted `ExplicitComposition` to a closed `CompileOutcome`, and reducer `R`
  maps one compatible tuple `(WorkGraph, OrchestrationCursor,
  AcceptedEventView)` to one closed `ReduceOutcome` containing at most one
  immutable `CommandIntent`. Equal admitted inputs under one exact registered
  contract tuple produce byte-identical semantic observations.
- **Plain-language voice:** RWO turns a declared work arrangement into a graph,
  then answers what structural command—if any—follows from one accepted event.
- **Domain-context voice:** In cyberalchemy-orchestrator, RWO is the reusable
  thin kernel beneath future services and adapters. It does not execute work,
  decide whether an event is true, or authorize effects.
- **Boundary:** RWO is not a domain workflow owner, journal, transport, retry
  scheduler, reasoning policy, or execution service.
- **Related:** DEF-RWO-002, DEF-RWO-003, DEF-RWO-004, DEF-RWO-005,
  DEF-RWO-006, DEF-RWO-009, DEF-RWO-010.

---

<a id="def-rwo-002"></a>

## Explicit Composition

- **ID:** DEF-RWO-002
- **Status:** candidate
- **Scientific/formal voice:** An Explicit Composition is an admitted,
  versioned structural source value that declares one composition identity,
  addressed nodes, and event-triggered edges with exact event and command
  schema references. It is an input to compilation and is not a valid
  `WorkGraph` until compilation succeeds.
- **Plain-language voice:** It is the work arrangement a caller asks RWO to
  validate and compile.
- **Domain-context voice:** It is the adapter-neutral input through which
  cyberalchemy-orchestrator can later express sequence, fan-out, fan-in, gates,
  sidecars, or bounded repetition without placing those policies in a transport.
- **Boundary:** An Explicit Composition is not an execution plan, accepted
  graph, runtime trace, or permission to invoke work.
- **Related:** DEF-RWO-001, DEF-RWO-003, DEF-RWO-009.

---

<a id="def-rwo-003"></a>

## Work Graph

- **ID:** DEF-RWO-003
- **Status:** candidate
- **Scientific/formal voice:** A Work Graph is the normalized, closed structural
  value produced only by successful RWO compilation. Its nodes and edges have
  total schema-owned ordering, valid endpoints, exact event and command
  contracts, and a derived typed graph identity.
- **Plain-language voice:** It is the validated graph RWO is allowed to reduce.
- **Domain-context voice:** The RWO Work Graph is narrower than the repository's
  general Workflow Graph (`DEF-SWI-001`): it contains deterministic structural
  routing semantics, not agent authority, confirmation, prompts, or an entire
  permitted execution space.
- **Boundary:** A Work Graph is not a mutable scheduler state, a Dispatch, a Run,
  or a graph accepted merely because it has the right JSON shape.
- **Related:** DEF-RWO-002, DEF-RWO-004, DEF-RWO-005, DEF-RWO-009,
  DEF-SWI-001.

---

<a id="def-rwo-004"></a>

## Accepted Event View

- **ID:** DEF-RWO-004
- **Status:** candidate
- **Scientific/formal voice:** An Accepted Event View is the closed semantic
  merge of `AcceptedEventIdentity` and `AcceptedEventPayload` supplied to the
  reducer after an external owner has accepted the event. Its semantic identity
  excludes delivery, attempt, clock, trace, broker, and adapter metadata.
- **Plain-language voice:** It is the exact event RWO is told to consider,
  already accepted by somebody else.
- **Domain-context voice:** A cyberalchemy-orchestrator journal or adapter may
  project accepted history into this value, but RWO does not decide whether the
  source event deserved acceptance.
- **Boundary:** Receipt or delivery of an event is not acceptance, and RWO
  reduction does not make it accepted.
- **Related:** DEF-RWO-001, DEF-RWO-005, DEF-RWO-010.

---

<a id="def-rwo-005"></a>

## Orchestration Cursor

- **ID:** DEF-RWO-005
- **Status:** candidate
- **Scientific/formal voice:** An Orchestration Cursor is a normalized derived
  value bound to one graph identity and stream. It records accepted-event
  identity-to-payload-digest entries, satisfied edge identities, and emitted
  command-identity-to-payload-digest entries under one reducer semantics version.
- **Plain-language voice:** It is RWO's rebuildable bookmark for structural
  progress.
- **Domain-context voice:** The cursor may be persisted by an external adapter so
  cyberalchemy-orchestrator can resume reduction, but accepted history remains
  owned elsewhere.
- **Boundary:** A cursor is not an authoritative journal, domain state, work
  result, confirmation state, or external-effect record.
- **Related:** DEF-RWO-003, DEF-RWO-004, DEF-RWO-006, DEF-RWO-010.

---

<a id="def-rwo-006"></a>

## Command Intent

- **ID:** DEF-RWO-006
- **Status:** candidate
- **Scientific/formal voice:** A Command Intent is an immutable structural
  request derived by the reducer from one graph identity, edge identity,
  accepted-event identity, command type, target node, and schema-valid payload.
  Its semantic identity and payload digest exclude delivery attempts and
  transport metadata.
- **Plain-language voice:** It says which declared work should be asked to run
  next and with what payload.
- **Domain-context voice:** A future cyberalchemy-orchestrator delivery service
  may send the same intent through different adapters without changing its RWO
  identity.
- **Boundary:** A Command Intent is not delivery, acceptance, execution,
  authorization, completion, or proof of an external effect.
- **Related:** DEF-RWO-001, DEF-RWO-005, DEF-RWO-010, DEF-RWO-011.

---

<a id="def-rwo-007"></a>

## Structural Defect

- **ID:** DEF-RWO-007
- **Status:** candidate
- **Scientific/formal voice:** A Structural Defect is a closed failure value with
  phase, typed structural path, code, and typed detail digest. A defect set has
  one total order defined by phase rank, path comparator, code, and detail
  digest; equal duplicate defects are a conformance failure.
- **Plain-language voice:** It is a stable, comparable explanation of why RWO
  rejected an input or transition.
- **Domain-context voice:** RWO implementations in cyberalchemy-orchestrator must
  return the same ordered defects rather than language-specific exception text.
- **Boundary:** A Structural Defect is not a domain failure, delivery outcome,
  retry decision, or log message.
- **Related:** DEF-RWO-009, DEF-RWO-010.

---

<a id="def-rwo-008"></a>

## Semantic Digest

- **ID:** DEF-RWO-008
- **Status:** candidate
- **Scientific/formal voice:** A Semantic Digest is the lowercase SHA-256 digest
  of the accepted length-framed preimage containing the RWO domain tag, exact
  contract and profile versions, schema and value-type identities, and canonical
  payload bytes. It is domain-separated from the digest of bare payload bytes.
- **Plain-language voice:** It is a fingerprint that includes what kind of RWO
  value the bytes mean, not just the bytes themselves.
- **Domain-context voice:** The same canonical JSON payload used as two different
  RWO types cannot silently receive the same semantic identity.
- **Boundary:** A Semantic Digest is not authority, provenance by itself,
  transport identity, or proof that a value is true.
- **Related:** DEF-RWO-003, DEF-RWO-004, DEF-RWO-005, DEF-RWO-006,
  DEF-RWO-007.

---

<a id="def-rwo-009"></a>

## Compile Outcome

- **ID:** DEF-RWO-009
- **Status:** candidate
- **Scientific/formal voice:** A Compile Outcome is the closed result of RWO
  compilation: either `Compiled`, containing the normalized Work Graph,
  canonical bytes, and graph identity, or `Rejected`, containing deterministically
  ordered Structural Defects and no graph.
- **Plain-language voice:** Compilation either returns one complete valid graph or
  an exact rejection—never a half-valid graph.
- **Domain-context voice:** Callers in cyberalchemy-orchestrator must branch on
  this closed result before any work can be structurally reduced.
- **Boundary:** Successful compilation does not authorize execution or prove that
  referenced work exists.
- **Related:** DEF-RWO-002, DEF-RWO-003, DEF-RWO-007.

---

<a id="def-rwo-010"></a>

## Reduce Outcome

- **ID:** DEF-RWO-010
- **Status:** candidate
- **Scientific/formal voice:** A Reduce Outcome is one of `Applied`, `Duplicate`,
  `DivergentDuplicate`, or `Rejected`. `Applied` contains a normalized next
  cursor and zero or one command intent. Every other outcome preserves the
  byte-identical original cursor and emits no command.
- **Plain-language voice:** It records exactly what RWO decided after considering
  one accepted event.
- **Domain-context voice:** The result gives cyberalchemy-orchestrator stable
  routing and replay material without claiming that a command was delivered or
  executed.
- **Boundary:** A Reduce Outcome is not a journal record, domain verdict, retry
  schedule, or effect result.
- **Related:** DEF-RWO-004, DEF-RWO-005, DEF-RWO-006, DEF-RWO-007.

---

<a id="def-rwo-011"></a>

## Retry Situation

- **ID:** DEF-RWO-011
- **Status:** candidate
- **Scientific/formal voice:** A Retry Situation is an explicit classification
  presented to separately owned service or adapter policy for mapping to one of
  `DoNotRetry`, `RetrySame`, `ReconcileThenDecide`, `DeadLetter`, or `Escalate`.
  RWO constrains semantic identity preservation but does not schedule an attempt.
- **Plain-language voice:** It describes what kind of recovery question exists;
  another owner decides and schedules the operational treatment.
- **Domain-context voice:** For cyberalchemy-orchestrator, retry attempts may
  change delivery metadata but `RetrySame` must retain the complete immutable
  Command Intent and its semantic identities.
- **Boundary:** A Retry Situation is not permission to retry. Structural
  repetition is explicit new graph work, not a delivery retry.
- **Related:** DEF-RWO-006, DEF-RWO-010.

## Definition-set claim ceiling

These definitions become canonical only after exact owner acceptance, canonical
target creation, index synchronization, and post-creation validation. Even then,
they establish vocabulary only. They do not establish implementation,
conformance execution, ontology promotion, publication, deployment, or runtime
readiness.
