# APT Stage B Execution Receipt

Date: 2026-07-23  
Status: `PASS / IMPLEMENTED_AND_VERIFIED / PRODUCTION_SERVE_DISABLED`

## Accepted scope

The minimal APT/ACI vertical slice now persists and queries:

- immutable Session history with current-origin head and explicit rollover CAS;
- `StartNewSession` as `apt.start-new-session@1`, atomically emitting event types
  `apt.session_started` / `apt.session_context_rebound` under schema refs
  `apt.session-started@1` / `apt.session-context-rebound@1` while rebinding the origin head;
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
`/api/provenance/*` routes plus the gated `GET /api/health` route frozen in
`SWU-ACI-APT-VS-001`.

Authoritative appends and artifact finalization commit before projection work.
A projector failure preserves the durable receipt and reports
`projection_status=pending`; the HTTP research endpoint maps that state to 202.

## Verification

- `python -m unittest discover -s implementations/tests/runtime -p "test_*.py" -q`
  — PASS, 27/27. This includes the real uvicorn subprocess
  POST → stop → restart → GET round trip and exact legacy-ledger byte identity.
- `python -m unittest discover -s tests -p "test_*.py" -q`
  from `implementations/agent-runtime` — PASS, 31/31.
- `npm.cmd test` from `tools/agent-provenance-telemetry` — PASS, 27/27.
- `npm.cmd run typecheck` — PASS.
- `python -m compileall -q implementations/server/runtime implementations/tests/runtime`
  — PASS.
- `git diff --check` — PASS.
- Independent Stage B reviewer cycle 4/5 — `PASS / NO OBJECTION`;
  subsequent runtime-review findings were remediated and the complete runtime
  matrix was rerun.

## Production serve status

The routes are implemented and were exercised through a separate test-only
enabled composition. The production reader still mounts runtime, provenance and
health routers with `enabled=lambda: False`. No production/local-pilot serve
enablement, provider execution, cutover or external mutation is claimed by this
receipt.

## SHA-256 evidence

```text
c72bb8bd5662f753effa3cd3e0d30a76e09d21a68a836beb8fbfa33e86e3e9b1  implementations/server/runtime/provenance.py
f8f902f54ea84c69e894d843a4705e35657c11fb68dfd3a33a06ab89b12b057a  implementations/server/runtime/api.py
164f3c1242e5dca07a585fa4f011d68865c1b5922acf3451f20f2ac112270bed  implementations/server/runtime/service.py
e1bac214144cc56a8234e581886dd93d82b9318ccd08bb73a0a813d58d1d2a0e  implementations/server/runtime/projections.py
61a4ae62818abc333d613df610e6612744f30043c12002ae0c26ca22fbc17c5f  implementations/server/runtime/journal.py
d15d4b8d3e562f575c299f40828da81633b37254e42d10cd1238553fde7261fc  implementations/server/runtime/database.py
f75e049f36811bb4659308bb00757a6dc6a34f8cb20aedc6a9421ea7b3ed415d  implementations/server/runtime/artifacts.py
879d23196f9d551cff35d38bb743bf55284dc4ed899135d3b718de6add4014fb  implementations/server/runtime/migrations/004_apt_projection.sql
a778139595531394039e092655b847df706b49f2535820bdfbc7e1c0d05f8308  implementations/server/runtime/migrations/005_apt_granular_projection.sql
334857e279c6d6c6bee16418fd7dd2336efc86e6794319dc339286d13c8c2ebd  implementations/server/runtime/migrations/006_apt_projector_state.sql
04ad172910200723a8bcb156d8477be2cefbf7531965c2d00e442cb9ee9203f9  implementations/server/runtime/migrations/007_session_origin_heads.sql
1c2aec4c325c7dc2cfc2970aa89b89825d5eab0edf38fa470ffbb09c4bd066b1  implementations/server/main.py
bfe5a7178a69a4501199844021265ece62405bc24039cc5f049aec14f4bc7d4b  implementations/server/config.py
2b33bbbe565103a07f579974ef1909b15d22e2787b55c74c826f8d28d5fb7ba0  implementations/server/runtime/cli.py
67db324b27b413321684e8d7cd9b3ca900ec855ebd9c709f3ce651524a71b497  implementations/config.example.json
c88455ef7eb7b392df216e16db44bdd567786b07f5b12fe15fca6fbd5377ea8b  implementations/tests/runtime/test_stage_b.py
e9e208f438cb3812559a5727abc518eeff20290d3ba9ab6489fb571690bbd439  implementations/tests/runtime/test_apt_stage_b.py
82fe3d29fe2d39402a856799e3bb56a3afb3a4e5b7461ea7aa91b5e6ba6424d8  implementations/tests/runtime/test_apt_projector.py
634635a656693d3ae5c61ce870e8460cd6f78dc99595b8bd6d5d3bd64fd4dc70  implementations/tests/runtime/apt_subprocess_app.py
fd65af261ec3b9861bf55c28afd57a882adba9296e94e246e71f3ef6623f3640  docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-APT-VS-001.json
839a3352f4c56910f227cdd243152d8a8b5afe7a4a1e8571ad69f2744a77e21e  docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-APT-VS-001-stage-b-execution-receipt.json
33316d5629587bc9c7cae399eb6dc2624e9fc6124e2d8d523eb2f1bac769cb47  docs/features/agent-provenance-telemetry/integration/stage-a/SWU-ACI-APT-VS-001.md
```
