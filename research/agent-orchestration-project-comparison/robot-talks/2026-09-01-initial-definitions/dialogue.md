---
node_type: agent-dialogue
status: complete
date: 2026-09-01
topic: Initial definitions for comparative research on agent orchestration projects
---

# Robot-Talks: initial definitions for comparative research

## Scope

This session prepares the informational context for later comparative research. It does not perform
the deep comparison, select features, design a research method, or authorize implementation.

The later research concerns these public repositories:

- `builderz-labs/mission-control`
- `boundflow/boundflow`
- `open-multi-agent/open-multi-agent`
- `OrlojHQ/orloj`
- `temporal-community/temporal-agent-harness`
- `LF-Decentralized-Trust-labs/gitmesh`
- `Chorus-AIDLC/Chorus`
- `chankov/agent-fleet`

## Central question

What do these eight projects provide that could strengthen Cyberalchemy; what do they cover that
Cyberalchemy is not proposing; what does Cyberalchemy provide that they do not; and which concepts,
patterns, or license-compatible implementations may be reusable?

The wording is explicitly refinable. This session must not treat it as a final research design.

## Assumptions challenged

1. The eight projects are comparable enough to produce useful learning.
2. Cyberalchemy should remain governance/evidence-first and repository-local.
3. A capability claimed in a README is not proven without supporting implementation evidence.
4. A capability absent from Cyberalchemy may be a deliberate boundary rather than a gap.
5. Reuse includes concepts and patterns; code reuse additionally requires compatible licensing and
   implementation fit.

## Chosen decomposition

The investigation is decomposed by concern rather than by repository:

1. **Cyberalchemy reality auditor** — establishes the proven current baseline: built, proposed,
   open, or contested.
2. **Comparative-framing critic** — tests whether the question, boundaries, and assumptions support
   an honest later comparison.
3. **Decision-context editor** — identifies the later decision this research must inform and keeps
   context, purpose, constraints, evidence, and unknowns distinct.

## Rejected decomposition

Splitting the eight external repositories among agents was rejected for this session. It would begin
the deep research before its informational definitions exist and would fragment the framing by
project instead of establishing a shared comparison context. That decomposition may be reconsidered
only in the later research design.

## Agent prompts

### 01 — Cyberalchemy reality auditor

Inspect only the smallest authoritative local evidence needed to distinguish what Cyberalchemy has
built, what it proposes, and what remains open or contested. Answer: *What proven baseline must the
later comparison respect?* Exclude external-repository research, feature recommendations, research
methods, and implementation planning. Write `reports/01-cyberalchemy-reality-auditor.md` using the
Robot-Talks Phase 2 report shape.

### 02 — Comparative-framing critic

Use the confirmed question, assumptions, and the already-established summaries of the eight
candidates to test the comparison boundary. Answer: *Which boundaries and unknowns must be explicit
before a fair comparison can begin?* Exclude new deep inspection of the candidates, solution
selection, research methods, success criteria, and implementation advice. Write
`reports/02-comparative-framing-critic.md` using the Robot-Talks Phase 2 report shape.

### 03 — Decision-context editor

Inspect the local objective and decision context needed to state what later discovery, design, or
decision the comparative research will inform. Answer: *What context, purpose, confirmed
constraints, current evidence, and known gaps belong in the initial-definitions document?* Exclude
research topology, sources, workstreams, hypotheses, candidate vocabulary, recommendations, and
implementation. Write `reports/03-decision-context-editor.md` using the Robot-Talks Phase 2 report
shape.

## Conversation protocol

- Agents report independently; they do not coordinate during exploration.
- Every finding cites a local file and line, a repository document, or the confirmed session input.
- Unsupported statements are marked as assumptions or gaps, never facts.
- Reports use: Key Findings; Gaps or Inconsistencies; Local Tensions; Questions for Synthesis.
- The parent synthesizes tensions after all reports exist.
- No implementation or deep external-repository research occurs before the human gate.

## Exploration

Three independent reports were completed:

- `reports/01-cyberalchemy-reality-auditor.md`
- `reports/02-comparative-framing-critic.md`
- `reports/03-decision-context-editor.md`

The exploration established a layered Cyberalchemy baseline, exposed ambiguities in the comparison
boundary, and identified missing downstream decision and licensing context.

## Prior candidate basis

The eight repositories were selected in a preliminary GitHub sweep before this session. That sweep
used repository pages and README descriptions to establish relevance, not implementation proof:

- [`builderz-labs/mission-control`](https://github.com/builderz-labs/mission-control) — self-hosted
  agent control plane with dispatch, reviews, gates, approvals, and audit surfaces.
- [`boundflow/boundflow`](https://github.com/boundflow/boundflow) — durable agent/workflow control
  plane with policies, approvals, audit receipts, and observability.
- [`open-multi-agent/open-multi-agent`](https://github.com/open-multi-agent/open-multi-agent) —
  dynamic multi-agent DAG orchestration with approval and replay claims.
- [`OrlojHQ/orloj`](https://github.com/OrlojHQ/orloj) — declarative multi-agent runtime with policies,
  approvals, handoffs, and operational visibility.
- [`temporal-community/temporal-agent-harness`](https://github.com/temporal-community/temporal-agent-harness)
  — durable agent workflows with recorded turns, tool calls, approvals, and handoffs.
- [`LF-Decentralized-Trust-labs/gitmesh`](https://github.com/LF-Decentralized-Trust-labs/gitmesh) —
  policy-governed orchestration for repository work.
- [`Chorus-AIDLC/Chorus`](https://github.com/Chorus-AIDLC/Chorus) — agent harness for task lifecycle,
  subagent orchestration, permissions, and human verification.
- [`chankov/agent-fleet`](https://github.com/chankov/agent-fleet) — coding-agent dispatcher with
  verification contracts, resumable fleets, and an operator dashboard.

These summaries are prior orientation only. The later research must not treat them as proof that
the described capabilities are implemented or complete.

## Synthesis

Seven framing tensions were synthesized in `findings.md`:

1. comparison-object state asymmetry;
2. unsettled status of repository-local and governance-first boundaries;
3. missing downstream decision and owner;
4. mismatch between evidence standard and preliminary candidate basis;
5. code-reuse intent without a receiving repository license;
6. host-bounded and contested enforcement beneath the “mandatory” label; and
7. tension between comparative learning and first-principles target derivation.

The one-line result is that the research is warranted, but its definitions must preserve evidence
states and prevent precedent, README claims, or current deployment choices from becoming design
authority.

## Human gate

On 2026-09-01, the user accepted all seven recommended dispositions in `findings.md` and instructed
the parent to create the initial-definitions document. The resulting informational context is
`../../research-initial-definitions.md`.

This gate authorizes that document only. It does not authorize deep external-repository research,
feature adoption, code reuse, or implementation.
