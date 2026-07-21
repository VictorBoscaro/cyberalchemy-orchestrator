---
name: close-session
description: Close a session and create a session node under sessions/
---

# Close Session Workflow

## Step 0 — Triage

**Create a node if any is true:** repo doc changed/created/deleted, domain code changed, architectural decision made, tests added/modified, contradiction found/resolved.

**Skip if:** no doc/code changes AND purely Q&A with no decisions. Say *"Q&A-only session. No session node created."* and stop.

---

## Step 1 — Write Summary (do this yourself)

Write up to **10 sentences**: what the session set out to do, what was decided (and why), what was done. No sub-headings, no per-file detail. A reader should grasp the arc without access to the conversation. Also draft the **Forward** lines yourself (Step 3). The discriminating test is a judgment — never delegated to Sonnet.

---

## Step 2 — Delegate classification to Sonnet

Spawn an Agent (model: sonnet) with your summary + list of files touched. It returns:

1. **node_type** (first match wins): constitution → premise → conceptual → test → discovery → implementation-plan → audit → spec (fallback).
2. **tags, layer, nature** per `vault/ontology-conventions.md`.
3. **expected_importance** (0–10) + **importance_rationale** (one sentence).
4. **Contradictions** — only if a vault node was validated, contradicted, or questioned. One bullet per edge. Omit section if none.
5. **Files touched** — flat list of paths, no descriptions. Git has the detail.

---

## Step 3 — Assemble the node

File: `sessions/YYYY-MM-DD-HHMM-{short-slug}.md`

```markdown
---
tags: [{tag1}, {tag2}]
node_type: {type}
is_session: true
layer: {layer}
nature: {nature}
status: active
created: YYYY-MM-DD
timestamp: YYYY-MM-DDTHH:MM:SS±HH:MM
expires: {created + 60 days}
decisions_made: true | false
contradictions_found: true | false
specs_updated: [paths or []]
promoted_candidates: [nodes or []]
expected_importance: {0-10}
importance_rationale: "{sentence}"
---

# {Title}

## Summary

{max 10 sentences from Step 1}

## Contradictions

{Omit if none. One bullet per edge: "validates/contradicts/questions {node} — reason."}

## Open questions

{Node-less undecided claim or conjecture — see § Forward registers. Omit if none.}

## Next steps

{Decided action, method known — imperative, priority-ordered. See § Forward registers. Omit if the arc is closed.}

## Recommendation

{The keystone among the items above and how to attack it — see § Forward registers. Omit on routine sessions; never a placeholder.}

## Files touched

{Flat bullet list of paths. No table, no descriptions.}
```

### Forward registers

- Three distinct registers, written by you. **Open questions** are undecided (resolved, never "done"); **Next steps** are decided labor; **Recommendation** ranks across them and asserts nothing new. If a line fits two, apply the discriminating test — can it be done? does it claim a truth? — and move it.
- **Open questions** name an epistemic gap the session opened but did not close — a genuine question or conjecture whose answer would steer future work. It is *resolved*, never *done*: if the method is already known and only labor remains, it is a **Next step**, not an Open question. It is also **node-less only** — a question naming a vault/spec node is a `questions {node}` edge → `## Contradictions`, not Open questions (else the two double-record). Mechanical test: if the target can be written as an existing file path, it is a Contradictions edge; otherwise an Open question. *One topic, three forks:* "Does the enum drift reach beyond the two 2026-07-18 rows?" is an Open question; "audit the appender for enum drift" is a Next step; "questions `ledger-enum-drift-finding` — those rows bypassed the validated appender" is a Contradictions edge.
- **Next steps defer to the backlog.** This repo has no `backlog/` yet (P-BACKLOG) — keep it body-only with `promoted_candidates: []` until one exists.
- **Recommendation obeys the subset rule.** Recommend a direction, never assert the outcome; name the licensing fact (validated node, landed test, resolved contradiction) or self-label a hunch. It references only items in the sections above.
- Omit, don't pad. No open business → omit the empty sections entirely. Absence is the signal.

> **Hard cap:** The body (below frontmatter) must not exceed **200 lines**. If it does, you are writing too much — cut. The three forward sections count inside the 200 and are the lowest-priority — if over cap, trim them first, then omit them.

---

## Step 4 — Review (one Sonnet agent)

Before the node is final, spawn **one Agent (model: sonnet)**, given the assembled node + the list of files touched. It reviews on two axes:

1. **Classification & frontmatter** — node_type, tags, layer, nature, importance, and any edges match `vault/ontology-conventions.md`; frontmatter is well-formed; the body is within the 200-line cap.
2. **Body discipline** — the three forward registers obey the Forward-registers rules (§ above); no narration; body within the 200-line cap.

It returns **PASS** or a list of concrete problems. **If it returns problems, send the node back to the writing agent (the one that wrote it, Steps 1/3) to fix, then re-review.** Only a clean PASS finalizes the node.
