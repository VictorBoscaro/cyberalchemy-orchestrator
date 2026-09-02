# ExecutionGraph v2 implementation layering

## Objective served

Turn the owner-selected single authority into an accepted, independently reviewed contract before
any runtime path can consume it. Success means the runtime never invents an unconfirmed executable
value and CONF v1 evidence remains truthful during migration.

## L0 — Accepted specification

**Question answered:** Do we have one normative, closed definition of the graph, its semantics,
views, confirmation boundary and v1 relationship?

Deliverables:

- new `specs/execution-graph-authority-v2.md`;
- aligned domain/interface/operation/mapping references without rewriting CONF v1;
- accepted closed JSON shapes for graph, views, trusted observation, confirmation command and
  accepted authority envelope;
- canonical bytes/digest rules, semantic cross-field rules and material-change matrix;
- explicit statement that graph bytes are the sole logical authority while observation and runtime
  state are external.

Gate: independent spec review returns PASS with no authority ambiguity. No production code entry
before this gate.

## L1 — Golden conformance package

**Question answered:** Can the normative contract be reproduced and falsified deterministically?

Deliverables:

- real `review → correct → verify` graph with non-placeholder content/provider/model/tool refs;
- topology/basic/full golden projection outputs;
- v2 observation, command, accepted-envelope and receipt vectors;
- semantic validator vectors for uniqueness, references, graph topology, budgets, predicates,
  commands, schemas and content digests;
- negative mutations for every authority-bearing field, hidden defaults, ref drift, self-digest,
  observation mismatch, replay and concurrent divergent confirmation.

Gate: canonical fixture reproduction + independent fixture/spec review PASS.

## L2 — Compiler and confirmation preview

**Question answered:** Can the product turn a short user intent into the complete graph and show one
of three trustworthy views?

Deliverables:

- compiler contract and implementation that resolves effective providers/models/tools before
  presentation;
- validation that rejects missing or implicit executable choices;
- deterministic projector implementation;
- chat confirmation flow that records selected view evidence while binding the full graph digest;
- recompile/reconfirm behavior on every graph-byte mutation.

Gate: tests prove three views/one digest, no model-generated projection, no resolver substitution
after confirmation and no execution call.

## L3 — ConfirmRuntimeDispatch@2 acceptance

**Question answered:** Can the runtime atomically accept v2 authority without confusing it with v1?

Deliverables:

- new v2 decoder/batch builder/service operation;
- versioned persistence for graph, observation and accepted authority digest lineage;
- reuse of trust, canonicalization, replay/conflict and single-writer mechanics where semantics are
  identical;
- explicit v1 coexistence and no digest aliasing;
- internal projection/materialization of runtime IDs only after accepted confirmation.

Gate: atomicity/failpoint/replay/concurrency tests PASS; CONF v1 regression remains green; no
provider/tool/external effect occurs.

## L4 — Execution integration

**Question answered:** Can OPEN and later execution consume only accepted v2 authority?

Deliverables:

- scheduler/input-binding consumption of v2 graph;
- policy enforcement at tool/network/filesystem/effect boundaries;
- attempt/result/receipt linkage to the accepted graph digest;
- fail-closed capability/content drift and explicit resumption rules.

Gate: separate code-entry decision after L3 evidence. This refinement grants none.

## Layer risks

- Skipping L0 lets implementation choices silently become product authority.
- Skipping L1 makes digest/projection claims non-reproducible.
- Combining L2 and L3 makes compiler UX bugs indistinguishable from confirmation transaction bugs.
- Combining L3 and L4 crosses the external-effect boundary before authority acceptance is proven.
