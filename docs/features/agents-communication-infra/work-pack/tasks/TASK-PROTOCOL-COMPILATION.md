# TASK-PROTOCOL-COMPILATION — bounded Protocol Governance compiler

## Objective and boundary

Implement `SWU-ACI-PROTOCOL-COMPILATION-001`: the smallest ACI-PG-001 slice that turns one exact
canonical profile, binding, recipe/DAG and invocation plus the fixed compiler identity into a
non-authoritative `DispatchCandidate` or closed required-unsupported result.

- **Layer:** independent L0 Protocol Governance adjunct.
- **Status:** complete for the bounded SWU; both independent re-reviews PASS.
- **Planning gate:** PASS for this exact SWU only.
- **Coder entry:** completed under a refreshed `domainspec-code-readiness@1` PASS receipt.
- **No promotion:** this task does not enter W6, promote L3/L4 or reuse obsolete `ACI-030`.

## Source contracts

- [`ACI-PG-001`](../../../../decisions/aci-protocol-governance-ownership.md)
- [`protocol-compilation.md`](../../specs/protocol-compilation.md)
- [Aspect test specification](../../specs/TEST-SPEC.md)
- [Feature test specification](../../TEST-SPEC.md)
- [Normative review](../../reviews/2026-08-03-protocol-compilation-spec-review/review.md)
- [Exact descriptor](../descriptors/SWU-ACI-PROTOCOL-COMPILATION-001.json)
- [Context pack](../context/SWU-ACI-PROTOCOL-COMPILATION-001-CONTEXT.md)
- [Implementation scaffold](../context/SWU-ACI-PROTOCOL-COMPILATION-001-SCAFFOLD.md)
- [Readiness receipt](../execution/SWU-ACI-PROTOCOL-COMPILATION-001-code-readiness.json)

## Exact write scope

No implementation or integrity repair may write outside these nine paths:

1. `implementations/server/runtime/protocol_compilation.py`
2. `implementations/server/runtime/service.py`
3. `implementations/tests/runtime/test_protocol_compilation.py`
4. `implementations/tests/runtime/aci-test-traceability.json`
5. `implementations/tests/runtime/test_aci_traceability.py`
6. `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
7. `implementations/server/runtime/local_pilot.py`
8. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
9. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256`

Paths 6–9 only close the existing fail-closed Stage-E integrity chain after paths 1–5 change;
they add no compiler, confirmation or runtime authority. The receipt receives an append-only
revalidation addendum and its companion digest is refreshed; historical evidence is preserved.

`runtime/artifacts.py`, fixtures, specs, routes, migrations, provider/tool adapters, pending sheets,
YAML and legacy dispatch surfaces are read-only dependencies. A required edit there is a stop
condition and must return to planning/decision ownership.

## SWU contract

| Field | Value |
|---|---|
| SWU | `SWU-ACI-PROTOCOL-COMPILATION-001` |
| Dependencies | accepted ACI-PG-001; reviewed v1 contract; exact two-case fixture; refreshed context/index/readiness pins |
| Done criteria | exact compiled and required-unsupported outputs; total closed failures; optional artifact-only persistence; T-ACI-PC1–PC12 and full runtime suite PASS; verifier PASS |
| Acceptance evidence | two independent brownfield audits, task-owned diff/symbol inventory, exact command exits, fixture/result digests, authority-firewall evidence and residual risks |
| Execution owner | one coder after both auditors and refreshed readiness PASS |
| Handoff status | complete for the bounded SWU; no downstream runtime authority promoted |

## Test obligations

The implementation and traceability changes must cover every ID exactly under its accepted source
contract:

| ID | Required proof |
|---|---|
| T-ACI-PC1 | recursively closed strict schemas and total first-error behavior |
| T-ACI-PC2 | literal canonical bytes and qualified digest goldens |
| T-ACI-PC3 | input/compiler digest and lineage invalidation |
| T-ACI-PC4 | explicit scalar parameters; no default, coercion or inference |
| T-ACI-PC5 | total unique obligation mapping and exact unsupported result |
| T-ACI-PC6 | bounded closed acyclic terminal-reachable DAG |
| T-ACI-PC7 | logical capability projection only; no effective grant |
| T-ACI-PC8 | byte identity across fresh processes and stable artifact identity |
| T-ACI-PC9 | pure compiler with zero forbidden dependencies/effects |
| T-ACI-PC10 | compiled-only idempotent ArtifactStore seam and closed conflict |
| T-ACI-PC11 | both exact admitted tuples, all fixture digests and field provenance |
| T-ACI-PC12 | candidate cannot validate or cross as confirmation/runtime authority |

Validation commands are exact:

```text
python -m unittest implementations.tests.runtime.test_protocol_compilation -v
python -m unittest implementations.tests.runtime.test_aci_traceability -v
python -m unittest discover -s implementations/tests/runtime -t .
```

## Execution topology

Brownfield execution is sequential and cannot be collapsed:

1. `alignment-audits`: exactly two independent auditors in parallel — one spec/code alignment and
   one architecture/layering/authority audit.
2. `implementation`: exactly one coder, admitted only after both auditors PASS and after readiness
   pins are reissued.
3. `verification`: exactly one independent verifier receives the pinned contract, complete
   task-owned diff, changed-symbol inventory and exact validation outputs.

Any finding returns to the coder only within the nine-path scope. The final approver is outside all
three working groups. This task does not itself register a dispatch.

## Stop conditions

Stop and return a blocker rather than widening scope if any of these occurs:

- a current hash differs from the readiness/context pin or readiness is not reissued PASS;
- either brownfield audit fails;
- a spec conflict, unrecorded authority choice or third production-admitted tuple is required;
- any edit outside the nine paths is needed;
- a test must be weakened or fixture/spec bytes changed to pass;
- compilation requires clock, randomness, environment, filesystem discovery, registry, network,
  confirmation, journal, bus, scheduler, provider, tool, YAML, legacy dispatch or persistence;
- candidate/result bytes would be used as `DispatchSpec`, confirmation, `ConfirmedDispatch`,
  `Run`, command/event/receipt, route, scheduling or effect authority;
- any production, external-network, provider/tool execution or cutover claim is proposed.

## Synchronization and completion

This task owns only the adjunct status entries in the shared planning artifacts. It cannot change
TASK-080 or infer completion from prose. Mark complete only after the refreshed readiness receipt,
both audit verdicts resolved, the exact nine-path implementation/integrity closure, all three validation commands and the
independent verifier PASS are present. Those conditions are satisfied for this bounded SWU; broader
protocol registries and every downstream runtime authority remain deferred.
