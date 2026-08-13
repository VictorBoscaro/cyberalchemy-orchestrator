# Context Pack: RWO Degrees of Freedom

Status: runnable local evidence baseline  
Mode: standard, strict, runtime handoff  
Coverage: 10/10 obligations  
Selected sources: 8

## Obligations

| ID | Obligation | Status | Evidence |
|---|---|---|---|
| O1 | Distinguish recursive composition from recursive authority | covered | `DESIGN.md:19-36,372-387` |
| O2 | Bound the “anything” claim | covered | `DESIGN.md:455-465` |
| O3 | Identify existing open questions | covered | `DESIGN.md:484-497` |
| O4 | Preserve the documented architectural contradiction | covered | `findings.md:77-90` |
| O5 | Identify unresolved tool/capability inheritance | covered | `research-initial-definitions.md:91-100,193-202` |
| O6 | Separate intended capability model from current enforcement | covered | ACI `README.md:746-783`; `pair-03-authority.md` |
| O7 | Establish current executable route limits | covered | `dispatch-type-registry.v1.json`; `capabilities.py` |
| O8 | Find precedent for deliberately narrow V1 surfaces | covered | `skill-control-center-phase-1-scope.md:8-47` |
| O9 | Preserve lineage versus authority distinction | covered | `meta-orchestration/findings.md:3-13,56-61` |
| O10 | Keep result proposal-only and owner-routed | covered | `DESIGN.md:23-26`; Refine seed write scope |

## Selected evidence

- `docs/features/recursive-work-orchestrator/DESIGN.md:19-36,54-89,372-387,440-465,484-497`
  — candidate root-only design, kernel non-goals, fail-closed invariants, claim ceiling, open residue.
- `research/agent-invocation-and-collaboration-topology/research-initial-definitions.md:91-100,193-202`
  — task-specific tools, no nested orchestrator authority, unresolved enforcement and classification.
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md:77-90`
  — explicit unresolved contradiction between root-only and bounded nesting.
- `docs/features/agents-communication-infra/README.md:746-783`
  — intended capability, isolation, policy, mediation, approval and receipt boundary.
- `implementations/as-built/pairs/pair-03-authority.md`
  — current runtime cannot yet prove the authorizer or enforce declared filesystem/tool/network fences.
- `implementations/server/runtime/capabilities.py:17-31,60-148`
  — action/phase/context-bound opaque tokens, expiration, revocation, and client authority-field rejection.
- `implementations/contracts/dispatch-type-registry.v1.json:1-74`
  — current route types, `legacy-managed` authority mode, and inherited host tool profile.
- `docs/decisions/skill-control-center-phase-1-scope.md:8-47`
  — accepted precedent for a useful read-only/draft-only first phase without simulated authority.

## Evidence boundary

The local corpus is sufficient to frame the research, but not to decide the final V1 envelope. RWO
is proposal-only; ACI's stronger isolation model is partly intended state; the as-built audit is the
claim ceiling for current enforcement. The recent nested-orchestration contradiction remains open.

## Excluded candidates

- Broad repository-wide orchestration search — excluded because the selected sources cover every
  initial obligation.
- External IAM, workflow-engine, and capability-system literature — excluded from this Refine run;
  it belongs to the future bounded research after its comparison questions are frozen.
- Product/runtime implementation files outside the capability and route boundary — excluded until
  the research design names a specific enforcement claim to inspect.

## Handoff rule

Downstream stages may use these selectors and expand only to close a named obligation. Absence of a
fence is `unknown` unless code/tests/as-built evidence establishes it; proposal text is never
implementation proof.

