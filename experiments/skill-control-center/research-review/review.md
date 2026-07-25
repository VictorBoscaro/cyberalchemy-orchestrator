# Research review — skill and dispatch control center

## Verdict

`FIX` for both reviewed artifacts. The central direction survives: a task-led control workspace
with contextual topology is appropriate. Discovery may start only from the corrected research
contract, not from the original wording.

## Coverage

| attacker | lens | targets | surviving findings |
|---|---|---|---:|
| evidence attacker | claim fidelity, source authority, model ownership | `research.md`, `findings.md` | 3 |
| operability attacker | executable journeys, contracts, gates and fixtures | `research.md`, `findings.md` | 8 |

The parent rechecked every finding against the frozen local targets. The APG Tree View and COGA
Design Guide classifications were also checked against their official W3C pages.

## Findings

### `research/findings.md`

1. **MAJOR — relation evidence is over-collapsed.** Quote: “Current graph data is `declared`.”
   The fixture contains 15 `explicit_path` edges and 247 `named_reference` edges. A textual name
   occurrence does not establish a declared call or dependency. **Fix:** expose `explicit-path`
   and `extracted-mention` separately and prohibit “calls/depends on” language for weak mentions.

2. **MAJOR — skill topology is extrapolated to dispatch lineage.** Quotes: “After selecting a skill
   or dispatch” and “This preserves the relational witness established by the repository graph.”
   The witness contains skill nodes only. **Fix:** keep three read models distinct: skill relation
   graph, dispatch parent lineage, and intra-dispatch group/connection graph.

3. **MAJOR — selection transition is contradictory.** `research.md` says “Não mudar de visualização
   automaticamente”; `findings.md` says the focal graph becomes primary after selection.
   **Fix:** define explicit `select`, `open detail`, `open topology`, `back`, and deep-link states;
   selection alone must not change view.

4. **MAJOR — evidence and usage are not computable.** The requirement to show observed counts,
   windows, coverage and freshness lacks an observation envelope, identity, deduplication,
   retry semantics, denominator and freshness algebra. **Fix:** freeze those semantics before API
   or UI implementation.

5. **MAJOR — path behavior is underspecified.** “Which path connects A to B?” does not define edge
   set, direction, tie-break, cycles, maximum depth, multiple paths or truncation. **Fix:** define a
   deterministic path-query contract with empty, error and partial states.

6. **MAJOR — configuration is described but not executable.** The draft/authority boundary lacks an
   action-by-authority matrix and transition model. **Fix:** define local preference, draft,
   validate, approval, conflict, failure, retry and accepted-receipt transitions.

7. **MAJOR — UX thresholds are not reproducible.** Completion percentages and action counts omit
   participant population, sample, fixtures, task wording, timing rules and comparison decision
   rule. **Fix:** freeze a benchmark protocol before testing.

8. **MAJOR — scale fixtures are conflated.** The 70-node/262-edge topology fixture and the proposed
   ~700-dispatch catalog exercise different costs. **Fix:** benchmark two independent fixtures and
   report browser, hardware, cache, network and cold/warm conditions.

9. **MAJOR — accessibility gate uses a nonexistent WCAG severity.** Quote: “zero critical
   accessibility failure”. WCAG conformance is expressed by A/AA/AAA success criteria, not a
   “critical WCAG” category. **Fix:** enumerate applicable WCAG 2.2 AA criteria and add manual
   keyboard, focus, screen-reader/live-region, zoom/reflow and non-canvas checks.

10. **MAJOR — three variants can pass as cosmetic reskins.** “Distinct art direction” has no
    observable originality test. **Fix:** require differences in layout hierarchy, navigation
    model, density/rhythm and topology treatment while holding semantics and tasks constant; use a
    fixed viewport/theme/state matrix and blind screenshot review.

### `research/research.md`

11. **MINOR — W3C guidance is mislabeled as normative.** The claim table classifies APG Tree View
    and the COGA Design Guide as `normative`. They are W3C guidance/practice; WCAG supplies the
    conformance requirements used here. **Fix:** classify both as
    `accessibility-guidance/practice` and reserve `normative` for WCAG and governing local
    authority.

## Required change order

1. Correct evidence labels and separate the three graph/lineage models.
2. Freeze interaction, path, observation and configuration state contracts.
3. Replace the benchmark, performance, accessibility and originality gates with reproducible
   protocols.
4. Correct source classifications.

## Close

- `exit_reason`: `resolved`
- attackers: 2
- planning/capability/tension helpers: completed
- parent verification: completed
- final verdict: `FIX`
- next gate: parent verifies corrected research, then approves discovery dispatch
