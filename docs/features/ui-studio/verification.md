---
feature: ui-studio
title: Citation verification — UI Studio README
status: complete
created: 2026-07-20
dispatch: 2026-07-20-ui-studio-readme-verify
verification: first-hand, paired (confirm + falsify)
---

# Citation verification — UI Studio README

> Return of the **paired** review dispatch `2026-07-20-ui-studio-readme-verify`
> (see [telemetry/agents/subagents-dispatch.yaml](../../../telemetry/agents/subagents-dispatch.yaml)).
> Two independent auditors read **first-hand** the same corpus of citations E-5…E-14 from
> [README.md](README.md), with **opposite dispositions** (anti-bias axis: *confirmation* vs
> *falsification*), so the correlated bias would cancel. The corrections were applied to the README.

## Consolidated result

**All 10 citations (E-5…E-14) RESOLVE first-hand. No FAIL.** The two dispositions
converged — they pointed to exactly the same characterization corrections, which is the sign
that the pair worked (an optimistic bias alone would not have caught the inflation of E-11; a
falsifier alone might have overstated a label nuance as FAIL).

| ID | Confirmer | Falsifier | Consolidated | Correction applied to README |
|----|-------------|--------------|-------------|------------------------------|
| E-5 | RESOLVES (models.ts L33-49,71-129) | RESOLVES | ✅ | — |
| E-6 | RESOLVES (run-cycle.ts L87-204) | RESOLVES | ✅ | — |
| E-7 | RESOLVES | RESOLVES | ✅ | exact categories: "Visual hierarchy", "Functionality"; evidence 30–80 words per note |
| E-8 | RESOLVES (studio.ts L267/281; http-routes L231-357) | RESOLVES | ✅ | — |
| E-9 | RESOLVES (api.ts L59-60) | RESOLVES | ✅ | — |
| E-10 | RESOLVES | RESOLVES | ✅ | "Genetic Control Center" = `<title>`; H1 = "Genetic Platform"; ~19 `gen_*.html` |
| E-11 | RESOLVES **with caveat** | **PARTIAL** (inflated) | ✅ **corrected** | material is in the *UX-constraint fitness* subsection **[DEFERRED]** ~L171-200, **not** in §3 (Scope); "honesty rule" = honest-diff mandate (`DiffSummaryHonest`), not a titled clause; the two `SPEC.md` are byte-identical |
| E-12 | RESOLVES (L394/243/414) | RESOLVES | ✅ | surface names are paraphrase ("cockpit", "Fleet Telemetry"), not verbatim |
| E-13 | RESOLVES (schema.sql L6-27; log.sh L3,41-93) | RESOLVES | ✅ | — |
| E-14 | RESOLVES (openclaw.mjs L78,143; server.mjs L8,262-268) | RESOLVES | ✅ | bare path, composite characterization correct |

## The one inflated citation — E-11

Both auditors caught it: the README attributed the hard-gate/soft-gradient + "honesty
rule" pair to **§3** of `SPEC.md`. In fact:

- **§3 is the Scope section** ("L0→L2"). The fitness material (hard gate discards L180;
  soft gradient scores-never-discards L183; ML2 fitness L190; OQ-5 L200) lives in a
  **later subsection marked `[DEFERRED]`** (~L171-200).
- **The "honesty rule" does not exist as a titled clause.** The concept is the **honest-diff
  mandate**: diff counts are derived from the real before/after, never from the declared
  `changeType` (`DiffSummaryHonest`, in §2b/§4/§5).

**Useful side effect:** that the fitness layer is literally `[DEFERRED]` in the
studio is **first-hand confirmation** of the README's §6.5 decision (substrate before engine) —
it adds to the newspaper (P0) and to the open OQ-5 to give the 3× that supports "the autonomous
doesn't pay first."

## Label nuances (non-blocking, applied for precision)

- **E-7:** category #2 is "Visual hierarchy" (not "Hierarchy"), #4 is "Functionality" (not "Function").
- **E-10:** "Genetic Control Center" is the `<title>`/description name; the H1 on the page reads "Genetic Platform".
- **E-12:** "Harness Cockpit"/"Agent Fleet Telemetry" are paraphrases of "human cockpit" and "Fleet Telemetry".
- **E-11:** the two cited `SPEC.md` paths are the same file (byte-identical) — dedup in the citation.
