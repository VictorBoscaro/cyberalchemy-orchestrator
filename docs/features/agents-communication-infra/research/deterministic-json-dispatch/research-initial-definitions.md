# Deterministic JSON Dispatch — Research Initial Definitions

## Context

The Agents Communication Infrastructure governs how agent work remains connected to the objectives, decisions, authority, actions, and evidence that give it meaning. A dispatch is not complete merely because a graph can be compiled or simulated: the governed intent must cross the host boundary without losing identity, authority, ordering, or accountability.

The accepted local runtime establishes a bounded deterministic path from manifested JSON inputs through compilation, exact local acceptance, durable scheduling, a scripted local adapter, and terminal evidence. The unresolved problem is the boundary beyond that local proof: whether and how the same governed JSON can authorize a real host launch and remain attributable and observable through completion. Resolving that boundary matters because claims of deterministic dispatch would otherwise exceed the capability actually evidenced.

## Purpose

This document establishes the informational boundary for determining what remains unknown before the project can claim that governed JSON results in a deterministic dispatch actually launched and accompanied by the host. Its answers will inform later authority, host-integration, runtime, and evidence decisions while preserving the distinction between the already accepted local capability and any broader live or production capability.

## Research Questions (Can be refined)

### Required program question

**RQ-0.** What remains unresolved, and what evidence would support each material claim, between the accepted local JSON-to-terminal path and a governed JSON dispatch that the host actually launches and accompanies deterministically?

### Authority and governed representation

**RQ-A1.** Which artifact or relation constitutes execution authority at every boundary from governed JSON through host launch?

**RQ-A2.** Which principals or systems are authoritative to issue, verify, consume, or revoke each execution decision at those boundaries?

**RQ-A3.** What canonical representation applies to the JSON, compiled ExecutionGraph, confirmation or acceptance evidence, assignments, and host launch request?

**RQ-A4.** What version relationships govern the JSON, compiled ExecutionGraph, confirmation or acceptance evidence, assignments, and host launch request?

**RQ-A5.** What digest bindings connect the JSON, compiled ExecutionGraph, confirmation or acceptance evidence, assignments, and host launch request?

**RQ-A6.** Which unresolved semantic and compatibility differences separate the currently proven proposed ExecutionGraph and local acceptance from canonical `aci.execution-graph@2` and `ConfirmRuntimeDispatch@2`?

### Host launch boundary

**RQ-H1.** Which existing host entry points can receive an accepted graph and cause an actual governed seat or worker launch?

**RQ-H2.** What information does the host require to bind a launched seat to its graph node, agent identity, role, inputs, authority, and parent dispatch?

**RQ-H3.** What authoritative event distinguishes a requested launch from an acknowledged, started, running, reconnected, or terminal host execution?

**RQ-H4.** Which duplicate-launch behaviors are currently defined at the host boundary, and which remain undefined?

**RQ-H5.** Which orphan behaviors are currently defined at the host boundary, and which remain undefined?

**RQ-H6.** Which retry behaviors are currently defined at the host boundary, and which remain undefined?

**RQ-H7.** Which restart behaviors are currently defined at the host boundary, and which remain undefined?

**RQ-H8.** Which cancellation behaviors are currently defined at the host boundary, and which remain undefined?

**RQ-H9.** Which partial-failure behaviors are currently defined at the host boundary, and which remain undefined?

### Determinism and live execution

**RQ-D1.** Which aspects of dispatch are required to be deterministic when execution crosses into a host, provider, tool, credential, or other effectful boundary?

**RQ-D2.** Which sources of nondeterminism exist in the current host and adapter boundary, and where can their outcomes remain governed without being falsely described as deterministic computation?

**RQ-D3.** What subagent execution capability is supported by independently checkable current evidence?

**RQ-D4.** What provider execution capability is supported by independently checkable current evidence?

**RQ-D5.** What tool execution capability is supported by independently checkable current evidence?

**RQ-D6.** What credential-dependent execution capability is supported by independently checkable current evidence?

### State, evidence, and accountability

**RQ-E1.** Which durable records bind a host launch and its subsequent events to the accepted graph digest, node, assignment, attempt, result, and receipt?

**RQ-E2.** Which runtime and host fields have enforcing consumers, which are merely recorded, and which currently have no demonstrated consumer?

**RQ-E3.** What evidence distinguishes successful terminal execution from a local simulation, an acknowledged launch, an orphaned dispatch, an incomplete observation, or a forged report?

**RQ-E4.** Which integrity properties survive process restart, and what are their known boundaries?

**RQ-E5.** Which integrity properties survive host reconnection, and what are their known boundaries?

**RQ-E6.** Which replay properties survive process restart, and what are their known boundaries?

**RQ-E7.** Which replay properties survive host reconnection, and what are their known boundaries?

**RQ-E8.** Which ordering properties survive process restart, and what are their known boundaries?

**RQ-E9.** Which ordering properties survive host reconnection, and what are their known boundaries?

**RQ-E10.** Which provenance properties survive process restart, and what are their known boundaries?

**RQ-E11.** Which provenance properties survive host reconnection, and what are their known boundaries?

### Capability boundary

**RQ-C1.** Which portions of the full JSON-to-host-dispatch claim are supported by documentary assertion, executable observation, independent recomputation, or formal proof?

**RQ-C2.** What contrary evidence, unresolved failure modes, or missing authority would prevent a claim that deterministic JSON dispatch is functioning end to end?

**RQ-C3.** What is the narrowest capability statement supported by the accumulated evidence once the host boundary is accounted for?

## Confirmed Product Constraints

- Governed JSON is the source from which dispatch execution must originate.
- The dispatch path must preserve deterministic, explicitly governed interpretation rather than relying on unstated host behavior.
- No live, provider, tool, credential, external-effect, or production capability may be claimed without direct evidence supporting that exact scope.
- The accepted local runtime proof remains a capability boundary; it must not be relabeled as canonical-v2, `ConfirmRuntimeDispatch@2`, human confirmation, production host authentication, or live execution.
- Subsequent work is delegated through subagents only; the coordinating agent does not perform the research or implementation itself.
- Every worker is paired with one reviewer.
- Work may continue across the necessary bounded dispatches without repeated user confirmation.
- Claims must remain no stronger than their addressable evidence.

## Current Evidence Baseline

The accepted source for this baseline is [`IMPL-ACI-EXECUTION-RUNTIME-001/review.md`](../../development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md), whose independently recomputed SHA-256 is `8B5F152CD04AE9BBE44BC868802241432C779ACAE5FA3C01E0828937EB8F9DFF`.

That review records a final `KEEP` for one bounded local path:

`9 manifested JSON inputs -> pure DraftGraph compilation -> proposed ExecutionGraph candidate -> exact local acceptance -> SQLite admission/state machine -> ScriptedLocalAdapter -> terminal receipts/snapshot`

The review records executable observations and independent attacks supporting that bounded claim: `95/95` tests passed; the fixture loader verified `9/9` exact named inputs; a modified accepted principal was rejected before database creation; a post-admission graph mutation was rejected with zero adapter calls; and the sequential handoff bootstrap remained `19/19`.

The same accepted review explicitly excludes canonical `aci.execution-graph@2` promotion, `ConfirmRuntimeDispatch@2`, human confirmation, production host authentication, live subagent/provider/tool/credential adapters, external effects, concurrency, feedback cycles, and production readiness. Therefore the baseline demonstrates deterministic local execution through a scripted adapter, not a real host-launched dispatch.

## Known Gaps

- The authoritative chain from governed JSON to a real host launch is not yet established by the accepted evidence. Covered by RQ-A1–RQ-A6.
- The host entry point, required launch bindings, acknowledged state transitions, and failure semantics are not established by the accepted evidence. Covered by RQ-H1–RQ-H9.
- The intended meaning and achievable boundary of determinism across effectful host, provider, tool, and credential execution remain unresolved. Covered by RQ-D1–RQ-D6.
- The durable relationship between host events and graph, node, assignment, attempt, result, and receipt evidence is not established by the accepted evidence. Covered by RQ-E1–RQ-E11.
- The evidence strength and narrow defensible capability statement for the end-to-end host path remain unresolved. Covered by RQ-C1–RQ-C3.
- Canonical `aci.execution-graph@2`, `ConfirmRuntimeDispatch@2`, human confirmation, production authentication, and live adapters remain explicitly outside the accepted local proof; their exact relevance and authority boundaries for the desired dispatch capability are unresolved. Covered by RQ-A3–RQ-A6, RQ-D3–RQ-D6, and RQ-C3.
