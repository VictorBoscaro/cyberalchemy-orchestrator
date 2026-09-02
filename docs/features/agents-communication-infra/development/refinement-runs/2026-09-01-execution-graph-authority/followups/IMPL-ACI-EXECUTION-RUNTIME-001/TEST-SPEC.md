# Test spec — IMPL-ACI-EXECUTION-RUNTIME-001

## Positive oracle

Load the persisted local-execution manifest and verify the paths and SHA-256 digests of all nine
compiler input documents, issuer evidence/trust artifacts, canonical acceptance bytes and expected
candidate digests without rewriting their semantics. `compile_candidate` must freeze but not
execute them. A separately supplied canonical local acceptance whose exact digest is allowlisted by
the configured local trust must bind the graph and compilation authority before
`execute_accepted_graph` may admit or launch the in-memory scripted adapter.
Review output must become correction input; review and correction outputs must become verification
inputs. The run succeeds only on verification verdict `pass`.

## Required attacks

1. Re-submit byte-identical inputs after success: return the identical snapshot and launch nothing.
2. Re-submit the same `(dispatch_id, revision)` with a changed material graph: conflict and preserve
   all prior bytes.
3. Omit, tamper or use an untrusted acceptance: reject before database creation.
4. Reject one correction validation and then accept it: persist attempts 1/2 in order and succeed.
5. Fail the review worker: exhaust its node, fail fast and skip downstream nodes.
6. Return verification `flag`: take the declared `stop_graph` branch.
7. Return verification `block`: take the declared `fail_graph` branch.
8. Pause after one node and request cancellation: preserve the completed node and cancel remaining
   nodes without another adapter launch.
9. Migrate/reopen: migration 016 applies once and all five local tables remain readable.
10. Legacy bootstrap: all 19 handoff/type tests pass, including missing/tampered/cross-route receipt
    rejection and exact ordered sequential sources.
11. Change durable graph, authority, assignment, result or receipt bytes beneath their stored
    digests: fail closed before another adapter launch or apparently valid snapshot.
12. Use a valid `any_predecessor_succeeded` graph whose array order exposes a hidden barrier:
    launch on the first active route event and deterministically skip unfinished work after terminal
    completion.
13. Request `allow_running_nodes_to_stop`: reject before writes because this local executor does not
    implement it.
14. Disable a required audit class or supply a missing/incompatible receipt schema member: reject
    before writes; validate every accepted receipt body against the pinned schema.
15. Change only `accepted_by` while copying valid issuer metadata: reject before database creation.
16. Remove a manifest artifact or drift an input/acceptance digest: reject before compilation or
    admission; the positive E2E must equal the manifest's graph/authority/acceptance digests.

## Evidence ceiling

These tests prove a deterministic local fake adapter and persistence path. They do not prove
external validator execution, cryptographic acceptance signatures, human confirmation `@2`, production host authentication, a canonical promoted EG v2 contract,
provider/tool execution, host subagent launch, concurrency, feedback cycles, live cancellation or
production safety.
