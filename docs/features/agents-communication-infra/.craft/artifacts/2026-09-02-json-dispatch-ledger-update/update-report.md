# ACI deterministic JSON dispatch ledger recovery

Date: 2026-09-02

## Recorded facts

- The Stage-E source-integrity repair received independent `KEEP`; its frozen review SHA-256 is
  `4076878260B43E714AD9C79E525DF6705AC9D5A8D8DC1278BF32E4E4FB9BB71C`. This is preflight
  integrity evidence, not launch evidence.
- The later Craft lifecycle opened session `ses_87e29f91b9d29b273730af26b0c9b37e` and closed
  `error`.
- That lifecycle produced zero `host_workflow_turn_bindings`. Its seat was interrupted without a
  terminal mailbox or frozen terminal manifest.
- Partial dispatch files are not execution success.

## Current ledger state

The ledger retains the local-only runtime evidence while keeping
`GAP-ACI-JSON-DISPATCH-HOST-LAUNCH-001` active. The current additions are:

- artifacts `ART-ACI-LOCAL-EXECUTION-RUNTIME-REVIEW`,
  `ART-ACI-JSON-DISPATCH-HOST-GAP-REVIEW`, `ART-ACI-STAGE-E-MANIFEST-REPAIR-REVIEW`, and
  `ART-ACI-CRAFT-JSON-DISPATCH-LIFECYCLE-RESIDUE`;
- decision `DEC-ACI-JSON-DISPATCH-IMPLEMENTATION-ROUTE-001`;
- descriptions `DESC-ACI-ROOT-007`, `DESC-ACI-CONTINUATION-007`, and
  `DESC-ACI-RUNTIME-004`;
- relations `REL-ACI-JSON-DISPATCH-ROUTE-GOVERNS-HOST-GAP`,
  `REL-ACI-LOCAL-RUNTIME-REVIEW-INFORMS-HOST-GAP`,
  `REL-ACI-HOST-GAP-REVIEW-EVIDENCES-HOST-GAP`,
  `REL-ACI-STAGE-E-REPAIR-INFORMS-HOST-GAP`, and
  `REL-ACI-FAILED-CRAFT-LIFECYCLE-EVIDENCES-HOST-GAP`.

No raw blocker was added because the active typed gap and blocked context already represent the
same technical condition.

## Next move and boundary

First repair and independently review one terminal parent-bound single seat. Only after `KEEP`, use
a separate worker/reviewer pair for incremental ready-group handoff and governed feedback, then
independently verify the byte-bound JSON-to-host-bound-seat path end to end.

This update does not claim canonical `aci.execution-graph@2`, `ConfirmRuntimeDispatch@2`,
production host authentication, live provider/tool/credential execution, external effects, or
production readiness. It does not treat the failed lifecycle as a successful dispatch.

Only the feature Craft ledger, its human view, and this update report are in scope. No source,
telemetry, skill, registry, other Craft ledger, commit, or push is part of this repair.
