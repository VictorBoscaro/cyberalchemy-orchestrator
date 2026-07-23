# Visual QA / Art-Direction Review — 10 Dispatch-Viewer Variants

Rendered headless (Chrome via puppeteer-core), served over `http://localhost:8099`, viewport 1400x900.
Two shots per variant, judged by eye:

- `<variant>-rich.png` = richest dispatch `2026-07-22-agents-protocol-readme-update-review` (5 groups / 6 agents / 4 edges)
- `<variant>-small.png` = small dispatch `2026-07-20-agent-name-selection-arch` (1 group / 2 agents / 0 edges)

Shots in `.review/shots/`. Scores are 1-5 (5 = ship as-is, 1 = rework). This is an assessment pass; no variant HTML was modified.

---

## Shared rubric (what a fixer should aim at)

Applied to BOTH the context header and the graph, per variant.

**1. Clean** — uncluttered, whitespace used on purpose.
- [ ] No accidental overlaps, no text bleeding through, no clipped/truncated labels.
- [ ] No crossing/tangled edges; edge routing is deliberate.
- [ ] Nodes are not cramped or colliding.

**2. Easy to understand / intuitive** — the eye lands in the right order (goal -> type -> structure).
- [ ] Group clustering is obvious at a glance.
- [ ] Edge direction reads immediately (arrowheads visible, flow follows a spine).
- [ ] Reviewer/skeptic/auditor nodes are visually distinct.
- [ ] The click affordance (agent node is clickable) is evident.

**3. Direct** — primary info front-and-center, secondary info quiet/opt-in.
- [ ] Goal + type + agent count + the graph dominate.
- [ ] Long context is collapsed behind an opt-in toggle (it is, everywhere).

**4. Informative** — high-level context is legible and useful.
- [ ] Labels aren't truncated to uselessness (agent names readable).
- [ ] Stat row communicates scale (agents / groups / links / reviewers / outcome).
- [ ] Header status reflects the *current* selection (no stale "standby" text).

**5. Balanced** — header is a compact band; the graph owns most of the space and fills it.
- [ ] Header is a band, not half the stage.
- [ ] Graph is centered and fills its area (not sunk to the bottom, not sparse islands).
- [ ] Multi-agent groups don't fling one member across the stage.

---

## Cross-variant problems (fix once, benefits many)

1. **Empty-state placeholder bleeds through behind the graph — ALL 10 variants.**
   CSS `#stage-empty{ ... display:flex }` outranks the `[hidden]` attribute (UA `[hidden]{display:none}` loses on specificity), so the placeholder sentence *"Escolha um dispatch a esquerda para ver o grafo dos agentes."* never actually hides. It sits at z-index behind the nodes and shows through every gap. Most damaging on dark/empty-center variants (glass, orbital, mission, mono — full sentence dead-center); barely visible where opaque boxes cover it (sketch, brutalist). Fix: hide `#stage-empty` with `display:none` (e.g. `#stage-empty[hidden]{display:none}`) instead of relying on the attribute.
2. **Under-filled stage / graph sunk low.** The 2-agent *small* case is sparse in almost every variant (unavoidable to a degree), but the *rich* case also under-fills in mono, sketch (graph sits in the lower ~40%), and swiss. Vertical centering / scaling to the stage would help.
3. **Agent-name truncation.** orbital clips every name ("Meyer, Ber...", "Parnas, Da..."); brutalist single-agent groups show only the ROLE and drop the name entirely.
4. **Weak directed/typed edges in stacked layouts.** editorial shows only a dotted vertical spine (no per-connection arrows); mono draws arrows only in the top label-rail and leaves the agent row unconnected. Edge *type* (zig-zag / feedback) is tooltip-only everywhere — acceptable, but nothing signals it statically.
5. **Stale header status.** orbital ("STANDBY · AGUARDANDO SELEÇÃO DE DISPATCH") and mission ("STANDBY · NENHUM DISPATCH EM FOCO · selecione um alvo") keep their idle status bar after a dispatch is selected.
6. **Lopsided multi-agent placement.** swiss flings the 2nd attacker to the far right; editorial pushes all agents far right of the group spine.

---

## Per-variant

### terminal — graph 4 / header 5  (STRONG)
`terminal-rich.png`, `terminal-small.png`
- Clean horizontal spine, code-bracket boxes, crisp green arrows with clear direction; reviewer nodes in amber read at a glance; names visible; nothing overlaps.
- Header is exemplary: prompt line + `AGENTS=6 GRP=5 LINKS=4 REV=3 LOOPS=1/1 EXIT=resolved` — compact, direct, fully informative.
- Punch list:
  - Empty-state bleed shows as fragments between boxes ("...rtch...", "o g...") — shared fix #1.
  - Small case is sparse (single centered box); acceptable but could scale up.

### sketch — graph 4 / header 4.5  (STRONG)
`sketch-rich.png`, `sketch-small.png`
- Best reviewer distinction of the set: reviewer groups get dashed borders + peach fill on the skeptic/auditor agents; hand-drawn spine with clear arrows between all 5 groups; names readable; opaque boxes mask the bleed bug.
- Header clean: type + RESOLVED pills, goal, stat pills.
- Punch list:
  - Graph sits in the lower ~40%; large empty grid band between header and the graph row — lift/center it vertically.
  - Bleed bug technically present (shared fix #1) though visually masked.

### blueprint — graph 4 / header 4.5  (STRONG)
`blueprint-rich.png`, `blueprint-small.png`
- Engineering-drawing columns; dimensioned group boxes, orthogonal boundary-to-boundary edges, corner ticks; horizontal spine reads as a clean pipeline; reviewer boxes in gold. Well balanced.
- Header (title-block) is clean and informative: type badge, goal, id subtitle, stat cells, outcome.
- Punch list:
  - Empty-state bleed shows as stray fragments ("atch", "graph") between the group boxes in rich, and the full sentence behind the single box in small — shared fix #1.
  - 2-agent group (attackers) box is taller and dips slightly below the single-agent boxes' centerline — mild asymmetry.
  - Small case: lots of empty space around one centered box.

### swiss — graph 3 / header 5  (MID)
`swiss-rich.png`, `swiss-small.png`
- Header is the cleanest, most "direct" of all: red rule, big numerals, tidy stat grid, outcome inline. 5/5.
- Graph: vertical group rows with a left arrow-spine (solid + one dashed feedback segment) — direction reads well.
- Punch list:
  - Lopsided: the 2-agent attackers group puts one box centered and the other at the far RIGHT edge, leaving an isolated box and dead space; single-agent rows leave the entire right half empty. Cluster agents next to their group, don't span full width.
  - Empty-state bleed behind the verifiers row — shared fix #1.
  - Small case uses only the lower band; huge empty top.

### brutalist — graph 3.5 / header 4.5  (MID)
`brutalist-rich.png`, `brutalist-small.png`
- Loud neo-brutalist; header cyan block with big stat boxes is punchy, legible, direct; hard black arrows between groups read clearly.
- Punch list:
  - **Single-agent group boxes show only the ROLE chip (WRITER / SKEPTIC / AUDITOR) and clip the agent name**; the 2-agent attackers group DOES show names — inconsistent, names lost. Increase box height or reflow so name always shows.
  - Large empty yellow band between header and graph; the spine sits low — center it vertically.
  - Header is a fairly tall band (big boxes) — on the edge of eating too much stage.

### glass — graph 3 / header 4.5  (MID)
`glass-rich.png`, `glass-small.png`
- The prettiest: glass panels, gradient stage, elegant curved edges with arrowheads and a dashed feedback edge; header chips are clean and informative.
- Punch list:
  - **Worst-hit by the bleed bug**: the full placeholder sentence sits legibly in the dark center of the graph — shared fix #1 (highest priority here).
  - Organic/scattered node placement (synthesizer top-left, verifiers right, attackers mid-left, coverage/final_approval bottom) — flow direction has to be hunted; large empty bottom-right quadrant; risk of edge crossings in denser graphs.
  - Small case sparse with bleed text behind the single box.

### editorial — graph 3 / header 5  (MID)
`editorial-rich.png`, `editorial-small.png`
- Beautiful magazine header (5/5): small-caps type, serif goal headline, id subtitle, dot-separated stat line, outcome top-right.
- Punch list:
  - Big horizontal gap: group labels + dotted spine hug the far LEFT while agent boxes float center-right — reads disconnected and lopsided.
  - Directed/typed edges essentially absent: only a dotted vertical spine, no per-connection arrows, so the 4 links aren't visible as flow — shared fix #4.
  - Empty-state bleed behind the verifiers row — shared fix #1.

### mono — graph 2.5 / header 4.5  (MID)
`mono-rich.png`, `mono-small.png`
- Minimal grayscale; header is very clean/direct; group-label rail across the top with thin connecting arrows is a nice touch.
- Punch list:
  - **Disconnect**: group-label rail is pinned to the very top while agent boxes float in the vertical middle with no connecting lines — a group and its agents are linked only by column alignment, reads disjointed. Move agents under their labels or draw connectors.
  - Very sparse; the graph doesn't fill the stage.
  - Empty-state bleed behind the agent row — shared fix #1.

### mission — graph 2.5 / header 3.5  (NEEDS MOST WORK)
`mission-rich.png`, `mission-small.png`
- "Mission control" theme; header chips (AG/GRP/LIG/REV/LOOP) + RESOLVED badge are compact and informative.
- Punch list:
  - **Stale status bar**: "STANDBY · NENHUM DISPATCH EM FOCO · selecione um alvo" persists after selection — shared fix #5.
  - Scattered radial placement around a decorative radar ring; the flow is a loop the eye must trace; group clustering unclear.
  - Empty-state bleed dead-center through the graph — shared fix #1.
  - Curved edges pass near/under the center text; role labels tiny.

### orbital — graph 2 / header 3.5  (NEEDS MOST WORK)
`orbital-rich.png`, `orbital-small.png`
- Concentric-orbit theme; header has stat boxes + type badge + goal, reasonably clean.
- Punch list:
  - **Hardest graph to read**: agents/groups scattered on rings, multiple curved edges converge on synthesizer at the bottom creating a tangle/crossings; no obvious entry point or direction.
  - **Every agent name truncated** ("Meyer, Ber...", "Wirth, Nikl...", "Parnas, Da...") — shared fix #3.
  - Decorative concentric rings add clutter with no meaning; for the 2-agent small case the giant ring is empty and wasteful.
  - **Stale status bar** "STANDBY · AGUARDANDO SELEÇÃO DE DISPATCH" after selection — shared fix #5.
  - Empty-state bleed dead-center — shared fix #1.

---

## Overall ranking

**Strong (leave mostly alone — fix the shared bleed bug + minor):**
1. terminal — clean spine, best-balanced, exemplary header.
2. sketch — clearest reviewer coding, clean arrows; just lift the graph.
3. blueprint — tidy engineering columns, orthogonal edges.

**Mid (good headers, graph layout/edges need work):**
4. swiss — 5/5 header; de-lopside the multi-agent placement.
5. brutalist — fix single-agent name clipping; center the graph.
6. glass — gorgeous; kill the center bleed text; tighten scattered layout.
7. editorial — 5/5 header; close the label->agent gap and add real directed edges.
8. mono — connect the top label-rail to the floating agent row; fill the stage.

**Needs most work (rework the graph):**
9. mission — stale status + scattered radial + center bleed.
10. orbital — tangled radial, truncated names, stale status, decorative-ring clutter.
