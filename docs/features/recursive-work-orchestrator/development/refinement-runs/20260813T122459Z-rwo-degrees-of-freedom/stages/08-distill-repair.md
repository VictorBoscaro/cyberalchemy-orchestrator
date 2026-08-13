# Stage 08 — Distill Repair

- Capability: `distill`
- Mode: `validate`
- Verdict: `pass`
- Scenario artifact: `stages/08-scenario-matrix.json`

All three independent reviews were accepted as repairs. The method now treats ATS as a protected
operation record embedded in causal traces, not as an isolated permission row. It separates current
observation, recommended V1 requirements, and later target; separates availability from
delegability; and makes attenuation, conservation, reconfirmation, receipt semantics, and coverage
mechanically inspectable.

The scenario matrix exercises five utility witnesses and twelve attack families over five path
kinds. It preserves the critical distinction between recommended V1 admissibility and current
executability: a workflow may be desirable in V1 yet unavailable today because its fence has not
been proven.

## Repair verdict

- Smallest coherent unit: stable after repair.
- Recomposition: passes through ATS traces → Freedom Slices → closed-axis matrix → V1 envelope.
- Claim ceiling: passes; proposed fences never populate current-observed fields.
- Utility: passes; local mutation is retained conditionally, and effects are adapter-bound.
- Non-amplification: testable through subset checks, conservation accounts, exact root-decision
  receipts, and multi-transition traces.
- Remaining issues: owner decisions and future evidence gaps, not method blockers.

