# APT Stage B Execution Receipt

Date: 2026-07-23  
Status: `PASS / IMPLEMENTED_AND_VERIFIED / PRODUCTION_SERVE_DISABLED`

## Accepted scope

The minimal APT/ACI vertical slice now persists and queries:

- immutable Session history with current-origin head and explicit rollover CAS;
- `StartNewSession` as `apt.start-new-session@1`, atomically emitting the successor
  `apt.session_started@1` and `apt.session_context_rebound@1` while rebinding the origin head;
- Session-to-Dispatch links bound to the immutable legacy-ledger snapshot;
- Research captures, questions, protected final answers, references, problems,
  inferred claims and mathematical/logical formalizations;
- official reference-probe lineage bound to verified ACI event, command receipt,
  publication receipt, profile registration and complete accepted prefix;
- independent granular projections with durable watermark, lag rejection,
  catch-up and deterministic rebuild.

The implemented storage increment is the ordered migration set
`005_apt_granular_projection.sql`, `006_apt_projector_state.sql` and
`007_session_origin_heads.sql`. The intent-only HTTP surface is exactly the eight
`/api/provenance/*` routes frozen in `SWU-ACI-APT-VS-001`.

Authoritative appends and artifact finalization commit before projection work.
A projector failure preserves the durable receipt and reports
`projection_status=pending`; the HTTP research endpoint maps that state to 202.

## Verification

- `python -m unittest discover -s implementations/tests/runtime -p "test_*.py" -q`
  — PASS, 26/26. This includes the real uvicorn subprocess
  POST → stop → restart → GET round trip and exact legacy-ledger byte identity.
- `python -m unittest discover -s tests -p "test_*.py" -q`
  from `implementations/agent-runtime` — PASS, 31/31.
- `npm.cmd test` from `tools/agent-provenance-telemetry` — PASS, 27/27.
- `npm.cmd run typecheck` — PASS.
- `python -m compileall -q implementations/server/runtime implementations/tests/runtime`
  — PASS.
- `git diff --check` — PASS.
- Independent Stage B reviewer cycle 4/5 — `PASS / NO OBJECTION`;
  focused APT/projector rerun 7/7 PASS.

## Production serve status

The routes are implemented and were exercised through a separate test-only
enabled composition. The production reader still mounts both runtime and
provenance routers with `enabled=lambda: False`. No production/local-pilot serve
enablement, provider execution, cutover or external mutation is claimed by this
receipt.

## SHA-256 evidence

```text
9c10aca8488e7b1a682a2b72ba8bcb55995e425a330a41a47b8bea0df53b9479  implementations/server/runtime/provenance.py
e91af2efb4d9665ecc6450adf439958c85ef78ddb8c592faeb48178181dc7e8b  implementations/server/runtime/api.py
791af479cc36ee26facc71d6d383e322bb733b7ed57a8834ff89237adf1c843a  implementations/server/runtime/service.py
82afc6b8a41347ccfb1d60466181a98acb762147489b4f26579fb96851b17706  implementations/server/runtime/projections.py
d15d4b8d3e562f575c299f40828da81633b37254e42d10cd1238553fde7261fc  implementations/server/runtime/database.py
f75e049f36811bb4659308bb00757a6dc6a34f8cb20aedc6a9421ea7b3ed415d  implementations/server/runtime/artifacts.py
879d23196f9d551cff35d38bb743bf55284dc4ed899135d3b718de6add4014fb  implementations/server/runtime/migrations/004_apt_projection.sql
a778139595531394039e092655b847df706b49f2535820bdfbc7e1c0d05f8308  implementations/server/runtime/migrations/005_apt_granular_projection.sql
334857e279c6d6c6bee16418fd7dd2336efc86e6794319dc339286d13c8c2ebd  implementations/server/runtime/migrations/006_apt_projector_state.sql
04ad172910200723a8bcb156d8477be2cefbf7531965c2d00e442cb9ee9203f9  implementations/server/runtime/migrations/007_session_origin_heads.sql
2ee2b870e6c1c8c380a55e06e541379c9c48823a5cfbc80485a3636cfc9538b9  implementations/server/main.py
bfe5a7178a69a4501199844021265ece62405bc24039cc5f049aec14f4bc7d4b  implementations/server/config.py
2b33bbbe565103a07f579974ef1909b15d22e2787b55c74c826f8d28d5fb7ba0  implementations/server/runtime/cli.py
67db324b27b413321684e8d7cd9b3ca900ec855ebd9c709f3ce651524a71b497  implementations/config.example.json
72c6b19ef9749bc66f226fc2dceeb28e0d07a1b46ad3838a73a8fe48f7b231cb  implementations/tests/runtime/test_apt_stage_b.py
ae68db08a324cb0dad7f497c4591b824f6c32b06b4ff15ae7ebc20d1bb344993  implementations/tests/runtime/test_apt_projector.py
634635a656693d3ae5c61ce870e8460cd6f78dc99595b8bd6d5d3bd64fd4dc70  implementations/tests/runtime/apt_subprocess_app.py
```
