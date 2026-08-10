# Cyberalchemy Orchestrator Craft Ledger

Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is the source of truth; this page is a linked navigation surface.

## Quick links

- Current next move: [review the baseline and select a bounded child context](#next-move).
- Active blockers: none.
- Blocking or open decisions: none.
- Active gaps: [GAP-WRITE-SIDE-CUTOVER-001](#gap-gap-write-side-cutover-001) and [GAP-ORCH-CATEGORY-PROOF-001](#gap-gap-orch-category-proof-001).
- Source artifacts: [AGENTS.md](AGENTS.md), [README.md](README.md), [OBLIGATIONS.md](OBLIGATIONS.md), and [BACKLOG.md](BACKLOG.md).

## Contexts

### <a id="context-ctx-cyberalchemy-orchestrator-root"></a>CTX-CYBERALCHEMY-ORCHESTRATOR-ROOT — Cyberalchemy Orchestrator

- Stage: `define`
- Gate: `flag`
- Purpose: keep agent work connected to the objectives, decisions, assumptions, actions, and evidence that make it reliable.
- Current state: the read-side control plane and governed dispatch substrate have working surfaces; write-side cutover and broader formal claims remain incomplete.

#### <a id="next-move"></a>Next move

Review this initial Craft baseline, then select one active gap or explicit workstream as the next child context.

## Definitions

### <a id="definition-def-governed-agent-work-001"></a>DEF-GOVERNED-AGENT-WORK-001 — Governed agent work

Candidate local definition: agent work whose objective, authorization, assumptions, actions, and supporting evidence remain explicitly connected and reviewable across decomposition and handoff.

## Blockers and decisions

- Active blockers: none.
- Blocking decisions: none.
- Other open decisions: none.

## Gaps

### <a id="gap-gap-write-side-cutover-001"></a>GAP-WRITE-SIDE-CUTOVER-001

- Severity: `flag`
- Treatment: `plan`
- Owner lane: `operations`
- Summary: the confirm-gated write path is built, but production cutover, sole-writer proof, generic provider launch, and related materialization remain incomplete.
- Evidence: [README.md](README.md).

### <a id="gap-gap-orch-category-proof-001"></a>GAP-ORCH-CATEGORY-PROOF-001

- Severity: `flag`
- Treatment: `defer`
- Owner lane: `research`
- Summary: `OBL-E3` remains open; the orchestration language has not been proven to form the claimed category, and the claim may narrow to its sequential fragment.
- Evidence: [OBLIGATIONS.md](OBLIGATIONS.md).

## Pending by node

### Cyberalchemy Orchestrator (`.craft/ledger.yml`)

- Readiness: `flag`
- Active blockers: none.
- Blocking decisions: none.
- Other open decisions: none.
- Active gaps: `GAP-WRITE-SIDE-CUTOVER-001`, `GAP-ORCH-CATEGORY-PROOF-001`.
- Pending artifacts or routes: none recorded.
- Recomposition residue: none.
- Next move: Review this initial Craft baseline, then select one active gap or explicit workstream as the next child context.

## Boundary check

This root ledger does not import or mutate the ledgers under `Arcanum/`, `Arcanum/spells/goal/`, or `tools/test-derivation-engine/`. It also does not activate parked candidates from `BACKLOG.md`.
