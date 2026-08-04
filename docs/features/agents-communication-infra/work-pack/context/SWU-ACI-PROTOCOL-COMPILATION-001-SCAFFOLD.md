# Implementation scaffold — SWU-ACI-PROTOCOL-COMPILATION-001

## Function-first targets

| Obligation | Symbol/file | Required change |
|---|---|---|
| PC1-PC9, PC11 | `ProtocolCompiler.compile_candidate` in `protocol_compilation.py` | Strict parse/canonical/schema/digest/cross-reference/semantic validation, exact two-tuple admission and canonical tagged result with exact precedence. |
| PC5 | frozen required-unsupported case | The second exact admitted tuple returns only sorted unsupported IDs and never reaches ArtifactStore. |
| PC7, PC12 | candidate construction | Project logical requirements exactly; introduce no grant/runtime/authority field or integration. |
| PC10 | `RuntimeService.compile_and_store_dispatch_candidate` | Invoke the pure calculation and persist candidate bytes only after `compiled`; map storage conflicts closed. |
| PC1-PC12 | `test_protocol_compilation.py` | Golden, negative, precedence, restart, effect, persistence, traceability and authority-firewall tests. |
| Traceability | traceability JSON/test | Map all twelve IDs to executable selectors. |

## Layer boundaries

- `protocol_compilation.py` imports canonical helpers and runtime errors only; it imports neither
  service nor ArtifactStore.
- `service.py` invokes the pure compiler and orchestrates only the optional ArtifactStore put for a
  `compiled` result, without changing runtime command/event state.
- `artifacts.py` remains unchanged unless an alignment audit proves the existing seam cannot meet
  the accepted contract; such a finding is a stop condition, not implicit scope expansion.

## Ordered implementation path

1. Add failing golden and strict-boundary tests.
2. Implement outer/document parsing and closed schema validation.
3. Implement digest/cross-reference, parameter, obligation and DAG checks.
4. Implement two-tuple frozen admission and exact compiled/unsupported result generation.
5. Add the separate artifact wrapper for the compiled branch only.
6. Add traceability, run focused tests, then the full runtime suite.

## Stop conditions

- Any need to edit outside write scope.
- Any candidate-to-confirmation/runtime wiring.
- Any need to weaken canonical, schema, digest, admission or authority-firewall tests.
- Any hidden filesystem/registry lookup inside the pure compiler.
