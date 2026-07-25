---
feature: ui-studio
title: UI Studio — control plane + UI-fitness harness
status: draft
created: 2026-07-20
authority: candidate
verification: paired-audit-passed
---

# UI Studio

> **Reading note.** This README is **navigation, context, and evidence** — not a backlog
> nor loose ideas (the `readme-pattern` rule). Every line in the tables is **cited**.
> Paths without a prefix are **relative to the repo root** (`cyberalchemy-orchestrator`);
> paths with `../` point to **sibling repos** (`../ZefraHub`, `../domainspec`,
> `../domainspec-core`, `../Arcanum`).
>
> **Verification status** (column `V`): **✅** = verified first-hand. Rows E-1…E-4
> and E-15…E-19 I read in this session; rows E-5…E-14 (previously second-hand) were **confirmed
> first-hand by the paired review dispatch** `2026-07-20-ui-studio-readme-verify` — auditors
> for **confirmation and falsification** over the identical corpus, see [verification.md](verification.md).
> All 10 resolve; the characterization corrections the audit requested are **already applied
> below**. Claim ≤ proof: no line here is second-hand.

---

## 1. What is this?

**UI Studio** is the feature that brings two halves under one roof: (a) the **control
plane** that organizes, triggers, and observes subagents, and (b) a **UI-fitness harness** —
the surface where a human **scores and comments on each UI element** (per-item score +
category scores + an overall score), to choose, among the variants, which UI survives.
The harness is the **validation route** that the frontend constitution's `Promotion Boundary`
([vault/constitution/frontend-constitution.md](../../../vault/constitution/frontend-constitution.md),
`CONST-FE`) marked as `none-yet`.

## 2. Business Context

This repo is a knowledge machine whose first concrete piece is an **agent orchestrator**
([PLAN.md](../../../plans/governed-agent-work-infrastructure/PLAN.md),
[README.md](../../../README.md)). Phase 1 delivered
a linear multilevel UI + aggregation endpoints over an append-only ledger
([sessions/2026-07-20-1352-linear-multilevel-ui.md](../../../sessions/2026-07-20-1352-linear-multilevel-ui.md)).
The human rated the UI as **too verbose**; the answer is not to erase information, it's
to **make density opt-in** and then **measure** the result — hence the harness. There are
**three prior arts** in sibling repos that already modeled exactly this problem; the goal of
the first cut is to **reuse, not reinvent**.

## 3. Why it matters

Without measurement, "cleaner" is a guess. The harness converts "I found it verbose" into a
**delta measurable by constitution rule**, closes the loop with the repo's decision layer
(MOGT / decision-receipt,
[archived roadmap](../../../plans/governed-agent-work-infrastructure/archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) §5 E4) and resolves the inherited *next
step* of **picking 1 of the 10 variants and deleting the other 9**. It also mitigates the
concrete risk observed in the prior arts (§5): building the autonomous evolutionary engine
**before** the loop closes once — all three deferred it or never triggered it.

## 4. Goal & scope of the first cut

**First cut = only the measurement substrate** (recommended, evidenced 3× in §5):

- **validated append-only** vote (not a mutable blob) — `register-dispatch` discipline;
- **per-element capture**: comment + score 1–5, tied to the element by a stable id;
- **aggregation** by category (`CONST-FE` rules) and **overall** per variant;
- **the human performs the mutation** (decision-receipt). **The autonomous engine is deferred.**

Out of scope in the 1st cut: autonomous Multi-Armed Bandit / Darwin; automatic
variant generation; per-agent cost fleet-telemetry (that's the *other* half — see E-13/E-14).

## 5. Evidence — what we have and where it is

### 5a. Harness prior arts (per-item vote + categories + overall)

| ID | Evidence | Location | V |
|----|-----------|-------------|---|
| E-1 | **Newspaper — atomic vote schema**: `AtomicVote {generation_id, metric_name, score 1–5, comment}`, 9 canonical metrics + `global_fitness`, `internal_score = score−3`, 5 loop handoffs | [../ZefraHub/specs/newspaper/docs/protocol/data-exchange-protocol.md](../../../../ZefraHub/specs/newspaper/docs/protocol/data-exchange-protocol.md) | ✅ |
| E-2 | **Newspaper — 6-agent architecture** (Orchestrator, Platform Architect, Data/Backend, Darwin-Gödel, UI Evolution, Editor-in-Chief) + mermaid diagram of the genetic loop | [../ZefraHub/specs/newspaper/docs/architecture/agent_ecosystem_overview.md](../../../../ZefraHub/specs/newspaper/docs/architecture/agent_ecosystem_overview.md) | ✅ |
| E-3 | **Newspaper — mission**: balance between *maximum density ⊥ minimum fatigue*; immutable rules (ubiquitous hover, instant close, universal tooltip `#tt`+`data-tip`) | [../ZefraHub/specs/newspaper/agents/ui_evolution/manifesto.md](../../../../ZefraHub/specs/newspaper/agents/ui_evolution/manifesto.md) | ✅ |
| E-4 | **Newspaper — vote backend**: `POST /api/vote` (`validate_vote` ~L346, `save_vote` ~L377) persisting to `telemetry_db.json` (**mutable blob — the point we improved on**) | [../ZefraHub/specs/newspaper/evolution/evolution_server.py](../../../../ZefraHub/specs/newspaper/evolution/evolution_server.py) | ✅ |
| E-5 | **ui-prototyping-studio — data model**: `CommentEvent {target{selector,elementLabel,odId}, severity, intent, note, createdBy/At}`, `AnnotationTarget` (bind via `data-od-id`), `MutationBatch`, `RevisionManifestEntry`, `DiffSummaryHonest` (append-only lineage) | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/domain/models.ts` | ✅ |
| E-6 | **ui-prototyping-studio — fitness loop**: `CycleCandidate.score` (finite, winner=max, auto-accept top, append 1 revision), explore/exploit, cycle ceiling | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/run-cycle.ts` | ✅ |
| E-7 | **ui-prototyping-studio — `critique` rubric**: 5 categories (Philosophy consistency, **Visual hierarchy**, Detail execution, **Functionality**, Innovation) 0–10 + 30–80 word evidence paragraph per score (a score without evidence is rejected) + SVG radar + Keep/Fix/Quick-win | `../domainspec-core/arcanum/projects/ui-prototyping-studio/provenance/open-design-reference/skills-references/open-design/skills/critique/SKILL.md` | ✅ |
| E-8 | **ui-prototyping-studio — capture + routes**: `annotateClickScript` overlay + `POST /comment` in the CLI; REST routes (`POST …/comments`, `…/mutation-batches/synthesize\|approve\|apply`, `…/handoff/export`) | `../domainspec-core/arcanum/projects/ui-prototyping-studio/backend/src/cli/studio.ts`, `.../interface/http-routes.ts` | ✅ |
| E-9 | **ui-prototyping-studio — React frontend** (the same feature with a UI): `AnnotationPanel.tsx`, `MutationApprovalPanel.tsx`, `RevisionTimeline.tsx`; error taxonomy `AUTO_APPLY_FORBIDDEN` / `APPROVAL_STALE` in `src/lib/api.ts` | `../domainspec/apps/web/src/components/ui-prototyping-studio/`, `../domainspec/apps/web/src/lib/api.ts` | ✅ |
| E-10 | **Newspaper (mirrored in domainspec)** — same harness (index.html — `<title>` "Genetic Control Center", H1 "Genetic Platform" — + ~19 `gen_*.html` + `evolution_server.py` + `telemetry_db.json` + `generations_manifest.json`) | `../domainspec/implementation/app-frontend/visualizations/newspaper/evolution/` | ✅ |

### 5b. Governance principles (what keeps it from becoming a "metrics wall")

| ID | Evidence | Location | V |
|----|-----------|-------------|---|
| E-11 | **hard-gate vs soft-gradient** (subsection *UX-constraint exploit/explore fitness* **[DEFERRED]**, ~L171–200 — **not** §3, which is Scope): hard gate discards (L180); soft gradient *scores, never discards* (L183); ML2 fitness = heuristic + self-critique + human objective (L190); OQ-5 = soft-score weights (L200). The "honesty rule" I cited **is not a titled clause** — it's the **honest-diff mandate** (`DiffSummaryHonest`, real before/after counts), in §2b/§4/§5. **Reinforces the §6.5 decision**: the studio's own fitness layer is marked [DEFERRED]. | `../Arcanum/.../ui-prototyping-studio/SPEC.md` (byte-identical to the one in `../domainspec-core/...`) | ✅ |
| E-12 | **Action-bearing signal**: every signal routes to *owner + action + evidence* (L394, L243, L414); "avoid empty dashboards" / "not a global score" (L243, L394). Surface names are a **paraphrase**, not verbatim: human "cockpit" (Harness Graph + Calibration Queue, L403), "Fleet Telemetry" (L404) | `../domainspec/PRODUCT-COMPONENTS-IDEA.md` | ✅ |

### 5c. Observing the agents (the other half — fleet telemetry)

| ID | Evidence | Location | V |
|----|-----------|-------------|---|
| E-13 | **agents-telemetry** — `events` SQLite (`ts, session_id, agent_id, event dispatch.start/end, tool, tokens, duration_ms…`) + `log.sh` hook (Pre/PostToolUse) | `../domainspec/internal_tools/agents-telemetry/scripts/schema.sql`, `.../scripts/log.sh` | ✅ |
| E-14 | **"dispatch from the UI" seam** — `openclaw.mjs` spawns agent processes reading seats from `router.yaml`, wired to `server.mjs` | `../domainspec-core/projects/goldenquill/apps/tilth_ui/src/openclaw.mjs` | ✅ |

### 5d. Base in this repo (where the harness plugs in)

| ID | Evidence | Location | V |
|----|-----------|-------------|---|
| E-15 | **Frontend constitution** `CONST-FE` — density⊥fatigue axis; FE-1..FE-8; validation modes (`deterministic`/`review`/`none-yet`); the `Promotion Boundary` that **calls for this harness** | [vault/constitution/frontend-constitution.md](../../../vault/constitution/frontend-constitution.md) | ✅ |
| E-16 | **Current FastAPI + SSE server** — endpoints `/api/snapshot`, `/api/overview`, `/api/repo/{name}`, `/api/dispatch/...`, `/api/stream`; **no `/api/vote` yet** | [implementations/server/main.py](../../../implementations/server/main.py) | ✅ |
| E-17 | **Validated append-only ledger** (discipline to reuse for votes) | [implementations/server/ledger.py](../../../implementations/server/ledger.py), [telemetry/agents/subagents-dispatch.yaml](../../../telemetry/agents/subagents-dispatch.yaml) | ✅ |
| E-18 | **Pending store** wired end-to-end but with no producer (only the `_example` fixture) — the gate watches here | [telemetry/agents/pending/2026-07-19-example-ui-control-plane.json](../../../telemetry/agents/pending/2026-07-19-example-ui-control-plane.json) | ✅ |
| E-19 | **10 UI variants** = the harness's candidate "generations" | [implementations/static/ui/](../../../implementations/static/ui/) (`aurora, blueprint, brutalist, cyberpunk, grimoire, linear, mission-control, radar, swiss, terminal`) | ✅ |

## 6. Design decisions carried over here

1. **The harness IS the `CONST-FE` validation surface.** Direct mapping (E-11 ≡ E-15),
   honoring the constitution's **three** validation modes (read first-hand off each rule's
   `Validation` field): `deterministic` (FE-3/6) → **hard gate** (Playwright, discards on
   fail); `review` (FE-4/7) → **soft gradient** (human 1–5 + comment, never auto-discards);
   `hybrid` (FE-1/2/5/9/10) → **both** (a deterministic sub-check gates *and* a soft-gradient
   human score applies to the same element); `none-yet` (density⊥fatigue axis, FE-8) →
   **human-objective residue**. *(Correction 2026-07-21: an earlier two-bucket map here
   misfiled FE-1 and FE-5 — both `hybrid` per [frontend-constitution.md:123](../../../vault/constitution/frontend-constitution.md#L123),
   [:169](../../../vault/constitution/frontend-constitution.md#L169) — as
   `review`/`deterministic`. The paired verification ([verification.md](verification.md))
   audited only citations E-5…E-14, never this internal CONST-FE cross-reference — a scope
   blind spot, not an auditor miss.)*
2. **Append-only over blob** (E-17 over E-4): a vote is never edited, it's appended and validated.
3. **Three granularities** the human asked for: `overall (shadow) ⊃ category (FE rule) ⊃
   item (comment+score = structure)`. The repo's CT framing: `residue = shadow ⊕ structure` —
   hence comment *and* score on each item.
4. **Action-bearing signal** (E-12): candidate for an **FE-8 amendment** — the overall can't
   be a loose number; it routes to owner + action (which rule, which fix).
5. **Substrate before engine** (E-6/E-11 deferred + newspaper P0): 3× confirmation that
   the autonomous part doesn't come first.
6. **Discreet dual self-explanation** (`CONST-FE` FE-4/FE-9; philosophical root: *form ≡
   content, radical legibility instead of enigma*, E-3): the **same `data-*-id`** that lets an
   element be scored also lets it **explain itself** — the score is the external judgment,
   the explanation is the element's own account. Concretization decided: **explain-mode**
   (discreet toggle) + **quiet marker** always present; in that mode, *dwell* (mouse idle
   ~3s, **configurable**) reveals the element. "Obvious/intuitive" enters as a **scored
   category** in the harness (soft-gradient of friction + a11y checks), not as good
   intentions.

## 7. Routing table — references by build need

| We need… | Canonical reference | ID | Role in our build |
|----------------|---------------------|----|----------------------|
| Vote schema (score+comment+overall) | E-1 (newspaper) ⊕ E-5 (studio `CommentEvent`) | E-1, E-5 | **data model source** — merge: per-element bind (studio) + score 1–5/comment (newspaper) |
| Categories + overall + evidence per score | E-7 (`critique`) | E-7 | shape of the categories; **replace the 9 newspaper metrics with the `CONST-FE` rules** |
| Per-element capture physics (`data-*-id`, overlay) | E-8 (`annotateClickScript`) ⊕ E-3 (`#tt`/`data-tip`) | E-8, E-3 | `#vote` widget, sibling to `#tt`; stable id per element |
| Lossless persistence | E-17 (append-only ledger) **improving on** E-4 | E-17, E-4 | validated `telemetry/fitness/votes.ndjson` |
| Vote/aggregation endpoint | E-16 (current FastAPI) | E-16 | `POST /api/vote`, `GET /api/fitness` on the same server |
| Human gate before mutating | E-9 (`AUTO_APPLY_FORBIDDEN`) ⊕ E-11 (two-gate) | E-9, E-11 | mutation = confirmed decision-receipt |
| Not becoming an inert dashboard | E-12 (action-bearing) | E-12 | rule: every score → owner + action + evidence |
| Variant survival criterion | E-6 (fitness loop) + E-19 (10 variants) | E-6, E-19 | overall per variant picks 1, kills 9 |
| Visual dashboard template | E-7 neighbor `live-dashboard` | E-7 | visual reference (KPI/sparkline) — do not copy the logic |
| Observing the agents (2nd half) | E-13 (SQLite+hook), E-14 (openclaw seam) | E-13, E-14 | fleet telemetry — **later phase** |

## 8. Open questions

- **OQ-1** — Soft-gradient weights (inherited from E-11/OQ-5): how to combine category
  scores from `review` into an overall without inventing false precision? Candidate: mean +
  exposed variance, never a single clean scalar.
- **OQ-2** — Does the per-element bind use `data-od-id` (studio) or an id of our own? Depends
  on verifying E-5 first-hand.
- **OQ-3** — Does the FE-8 amendment (action-bearing) land now or after 1 real cycle?

## 9. Next steps

1. **Done** — first-hand verification via paired dispatch `2026-07-20-ui-studio-readme-verify`; all 10 resolve, corrections applied. See [verification.md](verification.md).
2. Distill the **executable spec** of the 1st cut (`vault/spec/ui-fitness-harness.md`) from
   this evidence.
3. Implement `POST /api/vote` + validated `votes.ndjson` + `#vote` widget.

## 📁 Navigation

- **[README.md](README.md)**: this map — goal, context, cited evidence, and routing.
- *(planned)* **`spec.md`**: the executable spec of the first cut (after §9.1 verification).
- **[verification.md](verification.md)**: paired dispatch return — per-ID verdict (confirmation + falsification) and the corrections applied.
