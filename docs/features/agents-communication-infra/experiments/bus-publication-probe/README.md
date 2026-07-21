# Bus publication probe

This code tests the smallest enforceable version of the question: **can an official subagent
contribution be required to pass through a bus?**

The answer is split deliberately:

1. A subagent receives an MCP server exposing only `bus_publish`.
2. The server derives run, group, seat, attempt and phase from its trusted launch context.
3. A successful call is appended to a JSONL journal before a receipt is returned.
4. The parent accepts the subagent result only when `verify-result.mjs` matches that receipt against
   the journal.

A prompt alone does not enforce publication. The parent-side receipt gate is what prevents an
unpublished final answer from becoming official.

## Run the contract tests

Requirements: Node.js 22 or newer. There are no package dependencies.

```powershell
cd docs/features/agents-communication-infra/experiments/bus-publication-probe
node --test
```

The suite covers:

- accepted publication and durable receipt;
- missing or forged receipt rejected by the parent gate;
- invalid payload;
- identical idempotent retry without a duplicate event;
- idempotency conflict and logical duplicate;
- concurrent retry serialization;
- publication after phase closure;
- an MCP capability surface containing only `bus_publish`, with peer-read denied as an unknown tool.

## Connect one real subagent

1. Copy [`mcp.example.json`](mcp.example.json) into the MCP configuration used to launch the
   subagent, adjusting absolute paths if needed. Each seat must receive its own server entry and
   trusted `BUS_CONTEXT_JSON`.
2. Before launch, create the phase state file named by `BUS_PHASE_STATE_PATH`:

   ```json
   { "closed_phases": [] }
   ```

3. Give the subagent [`prompts/subagent.md`](prompts/subagent.md), plus the actual analysis task.
4. Save its final JSON response as `subagent-result.json`.
5. Apply the parent gate:

   ```powershell
   node src/verify-result.mjs subagent-result.json C:/tmp/agent-bus-probe/journal.jsonl
   ```

The verifier exits `0` only when the returned receipt identifies an accepted event with matching
message ID, payload hash and idempotency key. Missing, invented or altered receipts exit `1`.

For a quick behavioral run in an agent environment that can execute commands, the agent may invoke
the MCP through the included thin client (the client does not write the journal itself):

```powershell
node src/publish-probe.mjs --run-id real-agent-001 --content "the agent's contribution"
```

It prints the exact final JSON shape expected by the parent gate and stores the accepted event under
`.data/<run-id>/journal.jsonl`.

To simulate the collection barrier, replace the phase state content with:

```json
{ "closed_phases": ["collect"] }
```

The already-running MCP server re-reads this file on every publication and must reject a late call
with `phase_closed`.

## What this proves—and what it does not

This probe can prove that the controlled MCP path persists before acknowledging, that retries do not
duplicate a logical contribution, that a sealed phase rejects late publication, and that the parent
can refuse results that lack journal evidence.

It does not yet prove sandbox isolation, cryptographic capabilities, multiple writer safety, SQLite
transactions, reveal delivery, provider portability or the full runtime state machine. JSONL and
environment-bound context are intentionally probe-level mechanisms. If the real-subagent run passes,
the production spec should retain the publication/receipt semantics while replacing these mechanisms
with the journal, policy and capability boundaries described by the feature.
