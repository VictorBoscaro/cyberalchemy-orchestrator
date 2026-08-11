---
name: robot-talks
description: Run and preserve a direct multi-agent investigation of cross-layer tensions. Use when a problem spans multiple concerns, independent evidence is needed before action, and the human must validate contradictions before any implementation; not for local bugs or already-specified work.
---

# Robot-Talks: Multi-Agent Investigation Skill

Auditing tool for cross-layer tension discovery. Does NOT implement fixes.

This skill is self-contained. Do not depend on an external constitution or template that is not
present in the repository.

## Invocation Checklist (All must be YES)

- [ ] Problem spans 2+ distinct layers (not a single-file bug or local refactor)
- [ ] A single investigator would trade depth for breadth
- [ ] You need to identify contradictions before acting (audit, not implementation)
- [ ] Cost of misunderstanding exceeds cost of ~90 min investigation

**If any box is empty:**
- Single-file bug → use the repository's available debugging workflow.
- "How does X work?" → inspect the owning artifacts directly.
- Refactor in one module → use the repository's available impact-analysis workflow.
- Well-specified feature → implement directly.

## Phase 1: Setup (~15 min)

**Step 1 — User defines the problem.** The user must provide:

1. **Central question** — what misalignment are we investigating?
2. **Assumptions to challenge** — what we think is true but might be wrong

Do NOT proceed until the user has stated both. Ask if missing.

**Step 2 — Orchestrator proposes strategy.** Based on the user's input:

3. **Agent roles** — each with: concern, central question, explicit exclusions
4. **Strategy check** — state one alternative decomposition considered and why it was rejected. Present both the chosen strategy and the alternative to the user.

Agents do NOT spawn until the user evaluates and approves the approach.

Rules: decompose by **concerns**, not files. No two agents investigate the same question. Evidence overlap is fine.

## Phase 2: Exploration (~15 min per agent, parallel)

Each agent reports independently using this mandatory format:

1. **Key Findings** — 3-5 bullets, each with evidence (file, line number, doc reference)
2. **Gaps or Inconsistencies** — missing, undocumented, or contradictory within scope
3. **Local Tensions** — conflicts within this scope (docs vs code, etc.)
4. **Questions for Synthesis** — what should synthesis focus on?

A finding without evidence is speculation, not data.

## Phase 3: Synthesis (~15 min)

Identify **tensions** (contradictions between layers), not summaries. A tension is:
- Agent A says X, Agent B says NOT-X
- Finding contradicts documented contract
- Frontend assumes Y, backend implements NOT-Y

Each tension needs: what Layer A holds, what Layer B actually does, impact severity, and evidence from specific agent findings.

## Phase 4: Human Gate

No action without human validation. Present tensions, human decides:
- Real + actionable → implementation plan (separate session)
- Real + deferred → backlog item
- Misinterpretation → close with explanation
- Uncertain → targeted follow-up

## Session Preservation

Persist each investigation beside the context that owns its question:

```text
<owning-context>/robot-talks/<YYYY-MM-DD-topic-slug>/
├── dialogue.md
├── findings.md
└── reports/
    └── <NN-role>.md
```

When there is no clear owning context, use
`<repo-root>/robot-talks/<YYYY-MM-DD-topic-slug>/`. Do not use a generic conversations directory.

Create `dialogue.md` immediately after the user approves the strategy and before any agent is
spawned. Give it frontmatter with `node_type: agent-dialogue`, `status`, `date`, and `topic`. Update
it after exploration, synthesis, and the human gate. It preserves the scope, central question,
assumptions challenged, chosen and rejected decompositions, agent prompts, conversation protocol,
cross-agent dialogue when used, synthesis, gate notes, and follow-up links.

Each agent writes one independent report under `reports/` using the mandatory Phase 2 shape.
`findings.md` contains the evidence-backed cross-layer tensions and the human disposition of each
tension. A `ring/` directory for challenges and responses is optional when direct confrontation is
needed. `dispatch.json`, receipts, and governed runtime records are not required.

This preserved session is not a governed dispatch or ledger entry. Robot-Talks may run directly
when the user authorizes it; do not imply that dispatch infrastructure was used. Existing sessions
remain valid at their original paths and are migrated only by an explicit, separate request.

Recommended agent count: 3-5. Heartbeat timeout: 30 min per agent.
