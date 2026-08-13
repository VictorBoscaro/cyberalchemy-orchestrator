# Findings — Work overview composition

## Synthesis

The reports support one editorial sequence:

```text
one person's intended outcome
→ why direct agent use becomes difficult at scale
→ the user-visible working loop, in ordinary language
→ a second pass naming the local concepts already encountered
→ a backward-looking synthesis into larger explanatory compositions
→ continuity from execution history to reusable knowledge
→ scope, present status, and tests of value
```

The larger groups should be presented as useful projections over related responsibilities, not as
natural kinds or deployment boundaries. Each must state the relation that holds its parts together,
the capability that emerges from the group, and the limit of the chosen boundary.

## Cross-layer tensions

### T1 — Product subject versus architectural generality

- **Product layer:** the latest explicit editorial decision makes the subject one person extending
  their capacity through AI agents while retaining comprehension and control.
- **Current overview:** the opening replaces that subject with a generic model for arbitrary
  compositions of people, machines, tools, and services.
- **Impact:** major. The mechanisms remain relevant, but the document no longer explains the
  product the intended reader is being asked to understand.
- **Evidence:** `sessions/2026-08-12-1757-work-overview-editorial-drift.md:21-32`;
  `work-and-knowledge-system-overview.md:22-31,71-74`.
- **Proposed disposition:** real + actionable. Restore the person-and-agents objective at the
  opening; move architectural generality to scope as an unvalidated design ambition.

### T2 — Local clarity versus unexplained wholes

- **Local layer:** the overview introduces objective, parts, dispatch, participant, role,
  authority, attempt, events, result, evidence, provenance, review, and scope.
- **Composition layer:** it groups variants of these nouns three times, but does not explain why
  each subset belongs together or what the whole makes possible.
- **Impact:** major. The reader can understand individual terms without acquiring a usable model of
  the system.
- **Evidence:** `work-and-knowledge-system-overview.md:28-36,76-78,160-164,203-218`.
- **Proposed disposition:** real + actionable. Use a first pass in ordinary language and a second
  pass that names the relations, then synthesize three explanatory compositions:
  1. **bounded work:** objective, proposed parts, approved description, roles, authority, and limits;
  2. **accountable execution:** approved description, attempt, events, decisions, result, evidence,
     and observation;
  3. **continuity of knowledge:** produced information, provenance, evidence, review, scoped
     acceptance, and use by later work.

### T3 — User simplicity versus premature system vocabulary

- **Experience layer:** the system is meant to absorb operational coordination and let the person
  state an intention, follow what matters, and intervene selectively.
- **Narrative layer:** formal vocabulary and representation requirements appear before a compact
  account of that user experience.
- **Impact:** major. The reader must model the machinery before knowing what practical relationship
  it creates.
- **Evidence:** `work-and-knowledge-system-overview.md:22-36,60-78,82-108`;
  `sessions/2026-08-12-1757-work-overview-editorial-drift.md:29-32`.
- **Proposed disposition:** real + actionable. Complete the user-visible loop without internal names;
  introduce names only on the deliberate return over that loop.

### T4 — Proposal status versus present-tense behavior

- **Status layer:** the complete flow is proposal-only; only registration, refusal of invalid
  launches, append-only history, and some local linking currently run.
- **Narrative layer:** some scenario passages say the system records, returns, and presents results
  in ways that can sound implemented.
- **Impact:** major for credibility with a practical reader.
- **Evidence:** `work-and-knowledge-system-overview.md:17-18,101-108,227-238`.
- **Proposed disposition:** real + actionable. Mark present, proposed, and open status where each
  material capability first appears, then summarize at the end.

### T5 — Nested orchestration rule contradicts the companion design

- **Overview layer:** an orchestrator may invoke another orchestrator within dispatch authority and
  a depth limit.
- **Agent-language layer:** only the root orchestrator may decompose; an invoked orchestrator may
  not invoke another.
- **Impact:** major architectural contradiction, but unnecessary to resolve for this reader-facing
  overview.
- **Evidence:** `work-and-knowledge-system-overview.md:154-158`;
  `agent-language-system-view/essay.md:211-230`;
  `sessions/2026-08-12-1716-work-knowledge-overview-language.md:29-44`.
- **Proposed disposition:** real + actionable editorially, unresolved architecturally. Remove the
  disputed nesting rule from the overview and state only that further decomposition must remain
  within approved authority; preserve the architecture decision as open elsewhere.

### T6 — Three purpose frames are related but not yet reconciled

- **Predecessor:** model knowledge and build an anti-bias/noise agent orchestrator as the first
  executable slice.
- **Active Plan:** decision hygiene for multi-agent judgment.
- **Latest product framing:** extend one person's working capacity through agents while preserving
  comprehension and control.
- **Impact:** moderate. Treating them as identical would overstate alignment; presenting all three
  would overload the external overview.
- **Evidence:** `archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md:30-48`;
  `PLAN.md:66-88`; `sessions/2026-08-12-1757-work-overview-editorial-drift.md:27-32`.
- **Proposed disposition:** real + actionable for the overview. Use the latest explicit product
  objective as the controlling frame; retain decision quality and knowledge continuity as reasons
  and capabilities, not competing openings. Leave Plan reconciliation outside this edit.

## Human gate

The user validated all proposed dispositions on 2026-08-12 and authorized the overview rewrite.
The unresolved nested-orchestration choice remains outside this edit; the overview will stop
asserting either disputed rule.
