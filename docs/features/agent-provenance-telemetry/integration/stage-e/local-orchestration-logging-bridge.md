# Stage E - Local orchestration logging bridge

- Scope: prospective operator-mediated subagent dispatch logging
- Authorization: owner message `go ahead then, you can fix this issues`
- Authorization evidence:
  `sha256:7bcdc0f29560ce0f3a3e2f13571c1c1759b0f02616986c8715f2eadc3becf17f`
- Runtime boundary: explicit local-pilot database and exact repository dispatch ledger
- Production/provider/materializer cutover: blocked

## Purpose

The bridge closes the immediate observability gap between a confirmed local subagent dispatch and
the existing ACI/APT pilot. It composes two existing authorities without merging them:

1. `append-dispatch.cjs` remains the sole physical writer of the YAML audit opening and close.
2. ACI remains the sole authority for Session identity, the immutable Session-to-Dispatch link,
   and accepted orchestration lifecycle receipts.

The bridge is prospective. It never invents or backfills openings for agents that already ran.
The supported `orchestration_bridge.py` CLI is the admitted mutation entry point. Direct bridge
and runtime service methods are trusted implementation internals, not independent public
authority.

## Opening gate

Before a caller may launch an agent, all of the following must succeed:

1. An unexpired, operation-specific `orchestration.bridge.open` capability binds the principal,
   dispatch, canonical record digest, authorization evidence, nonce, Session name, and origin.
2. The Stage-C local-pilot preflight verifies receipts, the dedicated database, exact ledger,
   profiles, journal integrity, and projection readiness.
3. ACI ensures the current Session for the host-origin digest.
4. The validated appender accepts or idempotently finds the confirmed YAML opening.
5. ACI links the exact opening-row digest to the Session.
6. ACI accepts `orchestration.dispatch_opened@1`, bound to the link event and authorization
   evidence.

Only a returned `status=launch-authorized` receipt licenses the caller to invoke the agent. A
failed or interrupted step does not authorize launch. Retrying the same dispatch converges through
the appender and journal idempotency keys. A successful operation consumes the capability.

## Closing gate

At termination:

1. An unexpired, operation-specific `orchestration.bridge.close` capability binds the principal,
   dispatch, canonical close-record digest, authorization evidence, nonce, and Session.
2. ACI verifies the exact Session-to-Dispatch link and accepted opening before any YAML side
   effect.
3. The validated appender accepts or idempotently finds the YAML close row.
4. The strict resolver verifies that exact close row.
5. ACI accepts `orchestration.dispatch_closed@1` at aggregate version 2 and consumes the
   capability.

The close event records the stamped close time, exit reason, agent counts, feedback prompts, YAML
row digest, row-bytes digest, whole-ledger digest, actor, and authorization evidence. A crash after
the YAML append and before ACI acceptance is recovered by retrying the same close.

The appender serializes writers using
`telemetry/agents/subagents-dispatch.yaml.append.lock`. Its lock record contains a schema, PID,
creation timestamp, and exact ledger path. A present lock always fails closed; use the stale-lock
recovery procedure in the Stage-C operator runbook rather than deleting it blindly.

## Read the infrastructure log

The supported diagnostic verifies the complete journal, each event artifact, dispatch identity,
and exact YAML snapshots before returning the lifecycle:

```powershell
python -m implementations.server.runtime show-orchestration-log `
  --dispatch-id 2026-07-24-orchestration-bridge-review `
  --database C:\absolute\path\pilot.sqlite3 `
  --repo-root C:\absolute\path\repo `
  --ledger C:\absolute\path\repo\telemetry\agents\subagents-dispatch.yaml
```

The result contains the database path, journal verification receipt, Session-to-Dispatch link,
opening and optional close YAML records with digests, and ordered ACI events with offsets, event
IDs, command IDs, artifact references, hashes, and decoded payloads.

## Supported operator invocation

Create the confirmed opening or close as a JSON object. Derive its canonical digest with the
runtime canonicalizer, then issue an expiring capability whose context exactly binds the operation.
Capture the returned token without printing it:

```powershell
$root = (Resolve-Path C:\absolute\path\repo).Path
$db = 'C:\absolute\path\pilot.sqlite3'
$ledger = Join-Path $root 'telemetry\agents\subagents-dispatch.yaml'
$record = Join-Path $root 'confirmed-opening.json'
$recordDigest = python -c "import json,sys; from implementations.server.runtime.canonical import canonical_digest; print(canonical_digest(json.load(open(sys.argv[1], encoding='utf-8'))))" $record
$evidenceRef = 'codex-thread:owner-confirmation'
$evidenceDigest = 'sha256:<64-lowercase-hex>'
$context = @{
  operation='open'
  dispatch_id='confirmed-dispatch-id'
  record_digest=$recordDigest
  authorization_evidence_ref=$evidenceRef
  authorization_evidence_digest=$evidenceDigest
  nonce='unique-operation-nonce'
  session_name='operator-session'
  origin_ref='codex:thread-origin'
} | ConvertTo-Json -Compress
$expires = (Get-Date).ToUniversalTime().AddMinutes(10).ToString('o')
$issued = python -m implementations.server.runtime issue-capability `
  --principal 'operator:owner' --action orchestration.bridge.open --phase bootstrap `
  --context-json $context --expires-at $expires | ConvertFrom-Json
$env:ACI_LOCAL_PILOT_ENABLED = '1'
$env:ACI_ORCHESTRATION_BRIDGE_TOKEN = $issued.token
python -m implementations.server.runtime.orchestration_bridge `
  --project-dir $root --database $db --ledger $ledger open `
  --record $record --session-name operator-session --origin-ref codex:thread-origin
```

For close, use action `orchestration.bridge.close`, phase `finalize`, operation `close`, the close
record's canonical digest, a new nonce, and `session_id` in place of `session_name`/`origin_ref`.
Invoke the bridge `close --record <path> --session-id <id>`. The bridge removes the token from its
environment immediately and consumes the capability only after the exact operation succeeds.

## Integrity boundary

Stage-C preflight pins the Stage-E source manifest and verifies every listed source byte. This is
a fail-closed drift detector, not a cryptographic trust root: the externally reviewable Stage-E
execution receipt records the final verifier, manifest, test, and reviewer evidence digests
without creating a self-hash cycle.

## Current limitations

- Stage F adds mandatory project-local Claude and Codex Agent-tool hooks around this bridge.
  Enforcement still depends on a client loading the trusted project hook layer; system-wide Codex
  enforcement requires administrator-managed requirements.
- The dispatch remains `legacy-managed` during this compatibility stage. The bridge is not the
  TASK-020 audit materializer and does not make SQLite the sole dispatch execution authority.
- Only the live `research`, `code`, `review`, and `experiment` dispatch types are accepted.
- Real provider launch, non-loopback serving, historical import, YAML retirement, and production
  cutover remain blocked.

## First native execution evidence

Dispatch `2026-07-24-orchestration-bridge-review` was the first prospective dogfood run:

| Record | Evidence |
|---|---|
| Session | `ses_1f5d704231d1b706fb96b91987cdaefb` |
| Session start | journal offset `11`, event `evt_766c38e4ea79b62874a653f5ce47939e` |
| Session-to-Dispatch link | offset `12`, event `evt_6fe8fa75499d42534c2737d209079f0e` |
| Orchestration opening | offset `13`, event `evt_ae9c055f9ef5268667312d55ed71f2d9` |
| YAML opening row | `sha256:7d8a274afd469b2be7849d2e4804a6808f46cd9ed407ce005135974b8af5fe3f` |

The two review agents were launched only after these receipts existed and the restarted local pilot
reported a current projection through offset 13.

This first opening used the then-current operator-asserted evidence path. The two review loops
identified the reusable/underbound authority weakness; the supported CLI now requires and consumes
the exact operation-specific capabilities described above. The historical opening remains
append-only. It also predates the appender fix that emits the validated `output_mode`; future rows
retain that field.

## Executable evidence

- `implementations/server/runtime/orchestration_bridge.py`
- `implementations/server/runtime/service.py`
- `implementations/server/runtime/legacy.py`
- `implementations/tests/runtime/test_orchestration_bridge.py`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
