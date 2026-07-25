# Stage G Reference Scout and ingestion execution receipt

Date: 2026-07-24  
Status: `PASS / LOCAL_PILOT_OPERATIONAL / PROVIDER_ADAPTER_DEFERRED`

## Accepted scope

The authoritative local ACI runtime now owns a dispatch-bound, small, single-seat Reference Scout
lifecycle and dispatch input lineage. Scout start, capability issuance, bus publication,
parent verification, bundle commit, delivery, failure/cancellation, restart reads, and Dispatch
close guards use the existing journal, artifact store, capability manager, Session table, and
Dispatch link.

Claude and Codex project hooks record supported tool inputs against exactly one open wrapped
Dispatch. Instrumented repository reads preserve exact bytes and digest; searches, network/MCP
locators, and shell inputs preserve explicitly weaker metadata-only or opaque evidence.

This receipt does not claim a generic external provider launcher, multi-seat tensioned Scout, or
administrator-enforced client hook loading.

## Automated verification

- Integrated Python runtime suite: PASS, 69/69.
- Legacy/compatibility runtime suite: PASS, 31/31.
- TypeScript telemetry contract suite: PASS, 27/27.
- TypeScript typecheck: PASS.
- Total automated tests: PASS, 127/127.
- Runtime bytecode compilation: PASS.
- Claude/Codex hook, policy, and source-manifest JSON parsing: PASS.
- `git diff --check`: PASS.
- Focused Scout and ingestion tests: PASS, 9/9.

The tested failure matrix includes capability/context mismatch, invalid Scout message identity,
unfinished-Scout close denial, explicit failed termination, exact start retry with capability
reissue, divergent ingestion retry, closed-Dispatch ingestion denial, exact file capture, opaque
shell capture, and metadata-only search capture.

## Live local-pilot proof

Migration `008_reference_scout_ingestion.sql` was applied to the existing local pilot. Health
reported `ready=true`, WAL, `synchronous=FULL`, foreign keys enabled, and `quick_check=ok`.

One controlled Codex hook-wire Dispatch exercised the whole path:

```text
dispatch_id: 2026-07-24-auto-codex-agent-1a4ce9bbee43238e
session_id: ses_b002dff9dce400b7d00df406e228d8a2
scout_run_id: sct_b4d046748ebff3cb15fe5492a720ad55
recommendation_id: rec-stage-g-live-1
ingestion_id: ing_741cc632e844f589b5068e4159faa78c

offset 41  orchestration.dispatch_opened@1
offset 42  reference_scout.run_requested@1
offset 43  publication.persisted
offset 44  reference_scout.recommendation_accepted@1
offset 45  reference_scout.bundle_committed@1
offset 46  reference_scout.bundle_delivered@1
offset 47  dispatch.ingestion_recorded@1
offset 48  orchestration.dispatch_closed@1
```

The committed bundle digest is
`sha256:c700d981189f22ee5116e3be8e630756673bba50361512dd1d92b054bfad821c`.
The exact ingested document is
`docs/features/agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md`,
3893 bytes at
`sha256:a9d201d1295eb13ec4ce3ff0c0b178f8301af171863ba3b1ee07719a6cc0672d`.
The verified Dispatch query returned one Scout, one accepted recommendation, and one ingestion.
The compatibility YAML has both opening and close rows; the ACI orchestration aggregate has its
two authoritative lifecycle events.

## Host-loading boundary observed

The controlled hook-wire lifecycle passed, but the current already-running Codex collaboration
environment did not automatically invoke the newly checked-in project hook for an earlier
read-only helper. Project configuration becomes automatic only in a host process that loads it.
Until a fresh client demonstrates a model-originated call, formal review helpers in this session
must be explicitly bracketed by the same mandatory pre/post wrapper. This is an enforcement
boundary, not missing Scout persistence.

## Integrity anchors

```text
6a7613087619dfe6ab7dd0b319a016c2004fa65328b1a745c18c21aaff08cc07  docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
3522cc858e241e53109ccfa018de7f7ec8854906efb7d6bb8c3f80ca8b765d03  implementations/server/runtime/local_pilot.py
e8ca4a42ab115290d9c8f8efbad789780a4f318a3c08ee30f1bf20de71afedc4  implementations/server/runtime/service.py
c66f19e88e118585e1cb7a89f0ee46dd9925a75a3e0072b03da595a3f3e22f6c  implementations/server/runtime/api.py
9b292bca06feb9110faeecf768067d2a1ecb8846512c4316149c8f957d06f021  implementations/server/runtime/host_ingestion_hook.py
a529658440f7d9e8eaabec635959fdb925d4006cfd626590f05dcc37ccc021ab  implementations/server/runtime/migrations/008_reference_scout_ingestion.sql
605b4bd4fcc57430fe4830b559261ba3b914958e42700bcc62411840d9d31ccf  .claude/settings.json
fb763b2c75492f958a9157dfc85ceff387954eabc2a098a1189d72e6ef89084e  .codex/hooks.json
```
