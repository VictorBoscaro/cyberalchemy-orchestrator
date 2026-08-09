# Paired-views report: ResonantOS meetings

## Artifacts

- Vocabulary and concept graph: [`ontology-view.md`](ontology-view.md)
- Context, shape, and stakes: [`system-view.md`](system-view.md)
- Verdict status and candidate contracts: [`engineer-view.md`](engineer-view.md)
- Research boundary: [`research-plan.md`](research-plan.md)

## Triad result

- Overall: **pass with evidence flag**.
- Structural invariants: **pass**.
- Content maturity: **candidate** — real meeting inventory, participant interviews, and community
  validation remain undone.

## Invariant validation

1. **One home per term: pass.** All 18 `term:*` handles are defined only in
   `ontology-view.md`. The other views reference them without redefining them.
2. **Name once, decide once: pass.** Nine `stance:*` handles are named in `system-view.md`; D1–D9
   provide exactly one owning row each in `engineer-view.md`.
3. **No verdict upstream: pass.** `ontology-view.md` records meanings and conflicts;
   `system-view.md` names tensions without settling them.
4. **Authority on every verdict: pass.** Every decision row cites an official source, the research
   plan, or explicitly states that no running gate exists.

## Decision inventory summary

- OPEN: D1 family names; D2 secondary emphases; D3 openness boundaries; D4 proportional memory;
  D5 conditional pre-read; D6 series/occurrence split; D7 leaders-forum authority; D8
  attendance/contribution treatment.
- CRITICAL: D9 ratification owner. Without an authorized owner, the model can be tested but cannot
  honestly be presented as community policy.
- RESOLVED: none. This is intentional; the research has not yet produced community evidence or a
  ratified decision.

## Open naming conflicts

- `work` versus `community life` may imply a false opposition.
- `meeting` and `forum` need a tested event/venue distinction.
- `open`, `public`, and `transparent` are overloaded.
- `community leaders meeting` hides its authority posture.
- `documentation` and `recording` are often collapsed.
- `attendance` and `contribution` must remain distinct.

## Diagram decision

No diagram was added. At this stage, the axes table in `ontology-view.md` explains the important
relationship: family, format, access, participation, authority, preparation, memory, and cadence
are separate questions. An `x-ray` should be considered only if participant testing shows that this
table does not make the model understandable.

## Recommended next step

Execute the bounded evidence phase in `research-plan.md`:

1. inventory 10–15 real meetings or formats;
2. hold 5–8 short conversations across organizer, contributor, occasional, and newcomer
   perspectives;
3. classify the cases and preserve failures and ambiguity;
4. revise the three views from findings; and
5. route D9 before calling the result community policy.
