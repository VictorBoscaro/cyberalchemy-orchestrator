# Test and precedent scout: connected workflow compilation

Date: 2026-08-13  
Route: read-only repository and local-history scout  
Question: is there an implemented or tested path from a dispatch record with `connections` to a genuinely staged, binding-safe launch plan with dynamic downstream manifests?

## Finding

**No current precedent shows a connected topology being materially compiled into staged launches.** The repository has three different layers that must not be conflated:

1. a **built and tested isolated-seat compiler/binding path**;
2. a **built and tested manual manifest-consumption path**, including a legacy path-based `binding-output` mechanism now disallowed by the newer specification;
3. a **proposed but unimplemented connected-workflow materializer and launch gate**.

Historical `launch-plan.json` files do exist beside opening records containing `connections`, but their manifests all have empty `slots`, and the compiler version that created them iterated over groups without reading `connections`. They are evidence that all seats were envelope-compiled, not that topology or downstream dataflow was compiled.

## Built

| Capability | Evidence | Boundary |
|---|---|---|
| Deterministic bound launch-plan generation for independent seats | `implementations/server/runtime/dispatch_workflow.py:94-109` resolves the route; `:127-204` emits one manifest/envelope/launch per agent and writes `launch-plan.json`. | Every generated manifest has `slots: []` (`:151-164`). No scheduler or dependency materialization occurs. |
| First-line ACI binding envelope | Constants at `implementations/server/runtime/dispatch_workflow.py:24-27`; encoded envelope and message emission at `:165-193`. | Binds identity, prompt and manifest digest; does not make a downstream seat ready. |
| Manifest integrity and slot validation at binding time | `implementations/server/runtime/service.py:5286-5425` validates exact manifest fields, target identity, ordered unique slots, source cardinality, bytes and source kinds; `:5559-5576` verifies file digest and prepares artifacts before binding. | This consumes an already-authored manifest. It does not derive it from `connections`. |
| Host hook admission for a compiled bound seat | `implementations/tests/runtime/test_host_dispatch_hook.py:163-220` compiles one reviewer and feeds the exact `spawn_arguments` to the hook, then closes the bound turn. | Single group/seat; no connection or stage handoff. |
| Legacy/manual upstream output as a manifest source | `implementations/tests/runtime/test_host_workflow_binding.py:383-443` manually creates a `binding-output` slot, proves the producer must first be terminal, then binds the consumer and rejects digest drift. | The source is a caller-authored repository path (`:389-405`). The ratified replacement says caller paths cannot establish producer attribution (`docs/features/agents-communication-infra/specs/domain.md:203-228`; `operations.md:777-806`). This is partial precedent, not the accepted target design. |
| Fail-closed connected-topology fence | `implementations/server/runtime/dispatch_workflow.py:120-126` rejects any non-empty `connections` before the output directory is created. | Deliberate blocker, not missing validation by accident. |

No dedicated connected-handoff feature flag was found. `ACI_LOCAL_PILOT_ENABLED` gates the local runtime generally (`implementations/server/runtime/local_pilot.py:152`; `implementations/server/runtime/cli.py:106`), and the host-hook policy has its own enablement, but neither selectively enables connected compilation or downstream materialization.

## Tested

| Test/evidence | What it proves | What it does not prove |
|---|---|---|
| `implementations/tests/runtime/test_dispatch_workflow.py:85-111` | Exact envelope, prompt, target, digest and empty initial manifest are produced. | Dynamic slots, stage order, handoff or consumer readiness. |
| `implementations/tests/runtime/test_dispatch_workflow.py:127-163` | Any connected record raises `GateBlockedError`, and the output directory is not written. | There is no positive connected compilation case. |
| `implementations/tests/runtime/test_host_workflow_binding.py:383-443` | A manually supplied downstream manifest can be gated on producer terminality and exact bytes. | Compiler-derived mappings, host-observed terminal-response evidence, automatic handoff, replay-safe launch intent or accepted new attribution semantics. |
| `implementations/tests/runtime/test_host_dispatch_hook.py:163-220` | One compiled bound launch opens and closes under one parent. | Multi-stage topology. |
| Commit `65e5dce` (2026-08-10) | Added the connected-topology rejection and its no-write test. Commit message reports seven targeted tests passing. | It explicitly says downstream materialization remains unavailable; this is negative safety evidence. |

### Expected but absent executable coverage

The architecture bundle lists TOH-001 through TOH-008, including atomic response persistence, deduplication, rejection of terminal-state-only/path-based sources, restart safety, incomplete-slot denial and exactly-one downstream launch (`docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/ARCHITECTURE.md:97-107`). No matching `TOH-*` executable tests exist under `implementations/tests/runtime`.

There is also a traceability mismatch worth preserving: `docs/features/agents-communication-infra/specs/rules.md:398-415` now names ACI-R20 as the host terminal-output rule, while `docs/features/agents-communication-infra/TEST-SPEC.md:39,201` still maps T-ACI-R20 to the older causal-start-prerequisite case. The new rule therefore lacks a clean named test mapping.

## Proposed

The accepted design is unusually concrete, but remains explicitly non-executable:

- `docs/features/agents-communication-infra/specs/SPEC.md:127` classifies host terminal-output handoff as **specified for 1 producer -> 1 required slot; not implemented**.
- `docs/features/agents-communication-infra/specs/operations.md:777-878` defines terminal response commit, downstream manifest materialization, launch authorization and the rule that topology alone is not a data dependency.
- `docs/features/agents-communication-infra/specs/rules.md:398-415` requires producer-bound evidence, an active mapping, visibility authorization, exactly one manifest entry, a verified binding and atomic launch intent.
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/ARCHITECTURE.md:13-53` specifies the end-to-end L0 path; `:84-94` defers fan-in to L2 and recommends capture/verification dark launch before enabling one sequential topology.
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/IMPLEMENTATION-LAYERING-SEED.md:1-7` puts one sequential handoff in L1 and keeps the compiler fence until that layer is proven.
- `.codex/skills/subagents-dispatch-lifecycle/SKILL.md:37-40` permits replacing an empty manifest only through an exact governed compiler extension plus reconfirmation. This is an operational instruction for a future extension, not such an extension.

No implementation TODO marker or hidden feature flag was found for these operations. The work is carried as specification, design bundle, layering seed, expected acceptance cases and an explicit compiler fence.

## Historical connected-plan precedents

Four checked-in examples pair a non-empty `connections` record with a `launch-plan.json`:

| Dispatch | Connections | Launches | Slot counts |
|---|---:|---:|---|
| `.codex/workflow-inputs/2026-08-08-resonantos-minimal-meeting-ontology/` | 2 | 7 | all 0 |
| `.codex/workflow-inputs/2026-08-10-craft-root-ledger-review/` | 4 | 6 | all 0 |
| `.codex/workflow-inputs/2026-08-10-dispatch-defects-backlog-review/` | 3 | 5 | all 0 |
| `.codex/workflow-inputs/2026-08-10-review-next-path-reconciliation/` | 3 | 5 | all 0 |

Each opening and plan is a one-line canonical JSON artifact; inspect line 1 in the corresponding `opening.json`, `launch-plan.json` and `*-turn-0.json` files. Commit `16d8a24` (2026-08-10 11:39 -0300) added the Craft example. The later commit `65e5dce` (14:26 -0300) introduced the fence after recognizing that the existing compiler did not materialize connection handoffs.

The pre-fence compiler at commit `f309972` loops over `groups`, emits `slots: []`, and never references `connections`. Therefore these plans are correctly classified as **historically compiled envelopes for all declared seats**, not **compiled multi-stage workflows**. Any actual ordering around them was parent/host orchestration outside the launch plan and is not evidence that compilation owned the topology.

## Readiness consequence

The smallest honest runtime blocker is not “teach `dispatch_workflow` to accept `connections`.” It is to implement and test the accepted L0 evidence chain:

`host-observed terminal bytes -> producer receipt -> confirmed source-to-slot mapping -> canonical downstream manifest -> verified binding/prerequisite heads -> one launch intent`.

Relaxing the fence before that chain exists would recreate the historical false precedent: a plan that names connected groups while compiling every seat as independently ready. The current evidence supports beginning from the L0 terminal-output handoff design, not from the old path-based manifest test and not from the checked-in empty-slot launch plans.

## Classification summary

- **Built:** isolated bound-seat compilation; binding-envelope integrity; manifest validation; manual manifest consumption; fail-closed topology fence.
- **Tested:** isolated compile/hook flow; manual legacy `binding-output`; connected topology rejection before writes.
- **Proposed:** host-observed terminal-response evidence, governed source-to-slot mapping, automatic downstream materialization, connection-aware scheduling, atomic downstream launch authorization, restart-safe L1 sequential handoff, later fan-in/feedback/zig-zag semantics.

