# Stage D Acceptance Matrix

Every row is required. “No mutation” means no launch row, capability row, event, head, effect intent
or command receipt is added unless the row explicitly requires a redacted security observation.
Tests use a unique secret canary and scan the database bytes, WAL/SHM, repository test outputs,
captured stdout/stderr, HTTP logs, exception text and fixture-child process metadata.

| ID | Probe | Required result |
|---|---|---|
| T-LCB-IDENTITY-01 | Request one launch with accepted host-derived Session, Dispatch, operation and attempt context. | Exactly one launch, principal and closed context are committed; public output contains IDs/expiry only. |
| T-LCB-IDENTITY-02 | Child supplies or conflicts with launch, principal, attempt, Session, Dispatch, action or phase. | Reject the complete request; no authority is reinterpreted from child input. |
| T-LCB-IDENTITY-03 | Request a second active launch for the same attempt generation. | Uniqueness/CAS conflict; no second capability set or process effect. |
| T-LCB-HANDOFF-01 | Expected fixture child claims the inherited channel once before deadline. | Claim commits once and creates a channel-bound broker session; no bearer is returned. |
| T-LCB-HANDOFF-02 | Claim the same channel/ticket twice. | Second claim denied as `claim_replay`; no second session. |
| T-LCB-HANDOFF-03 | Copy claim bytes to another process or another channel. | Denied as peer/channel mismatch; expected launch may be revoked by policy. |
| T-LCB-HANDOFF-04 | Claim after 30-second deadline. | Denied as expired; launch becomes expired/revoked and no tool call is accepted. |
| T-LCB-LEAK-01 | Inspect child argv, environment, stdin, prompt/effective-input fixture and inherited handles. | No raw ACI bearer; only the intended IPC endpoint is inherited. |
| T-LCB-LEAK-02 | Force success, validation, authorization, timeout and unexpected-exception paths with a secret canary. | Canary absent from stdout, stderr, HTTP/access logs, tracebacks and returned errors. |
| T-LCB-LEAK-03 | Scan SQLite main/WAL/SHM, journal payloads, receipts, projections, artifacts and generated test files. | No raw bearer or bootstrap ticket bytes; only approved IDs and non-secret metadata persist. |
| T-LCB-LEAK-04 | Place the canary under unrelated keys and inside free-text exception messages. | Sink scrubber blocks/replaces exact secret values; key-name-only redaction cannot pass. |
| T-LCB-SCOPE-01 | Use a live broker session for its exact allowed action/phase/operation. | Broker revalidates full context and the local runtime accepts the intent once. |
| T-LCB-SCOPE-02 | Replay against another launch, attempt, operation, Session, Dispatch, action, phase or audience. | Authorization denied before local runtime mutation; redacted reason code recorded. |
| T-LCB-SCOPE-03 | Attempt peer-read, general event read, artifact read or undeclared tool access. | Default deny; the launch receives only its frozen allowlisted tools. |
| T-LCB-EXPIRY-01 | Advance injected trusted clock to exactly expiry and beyond. | Calls fail closed at `now >= expires_at`; no grace period or wall-clock fallback. |
| T-LCB-EXPIRY-02 | Request TTL above 900 seconds or expiry earlier than claim. | Invalid request rejected before persistence or issuance. |
| T-LCB-REVOKE-01 | Revoke before claim, after claim and during an in-flight tool call. | New calls fail immediately; in-flight result cannot create an acceptance after revoke-version conflict. |
| T-LCB-REVOKE-02 | Repeat identical revoke and issue a conflicting revoke reason/version. | Identical retry returns stable receipt; conflict fails without a second transition. |
| T-LCB-REVOKE-03 | Observe normal fixture terminal or authorized cancel. | All launch capabilities are revoked before terminal launch state; contained process tree is cleaned up. |
| T-LCB-RETRY-01 | Retry an eligible failed logical operation. | Same operation ID, new attempt/launch/principal/channel/capabilities; old bearer remains revoked. |
| T-LCB-RETRY-02 | Present any prior-attempt channel frame after retry starts. | Denied against the old launch; cannot affect the new attempt. |
| T-LCB-CRASH-01 | Crash before/after launch request commit, volatile-secret deposit, claim, tool call, revoke and terminal observation. | Restart converges without duplicate accepted transition, capability resurrection or automatic relaunch. |
| T-LCB-CRASH-02 | Restart with durable `claimable` or `claimed` state and an empty volatile store. | State becomes `reconciliation_required`; operator-authorized reconcile is required. |
| T-LCB-CRASH-03 | Reconcile unknown child process status. | No completion or relaunch is invented; observation and decision remain separate facts. |
| T-LCB-LOG-01 | Exercise all accepted and denied paths. | Journal/receipt/security/operational evidence classes remain distinct and contain only their allowlisted fields. |
| T-LCB-LOG-02 | Flood invalid claims and scope mismatches. | Telemetry is bounded/rate-limited; authoritative revocation is not dropped or coalesced. |
| T-LCB-CONTAINMENT-01 | Fixture child spawns a descendant and attempts handle duplication. | Undeclared inheritance/escape is denied; termination cleans the complete contained process tree. |
| T-LCB-CONTAINMENT-02 | Run target-host negative filesystem, network, process and credential probes. | All policy-denied access fails closed with redacted evidence. |
| T-LCB-LEDGER-01 | Hash `telemetry/agents/subagents-dispatch.yaml` before and after the full suite. | Bytes and digest are identical; Stage D performs no dispatch-ledger write. |
| T-LCB-GATE-01 | Configure a real adapter/provider, model credential or non-loopback endpoint. | Startup/launch rejects before process or socket effect; provider gate remains blocked. |
| T-LCB-GATE-02 | Invoke launcher through current `issue-capability` or `activate-local-probe` raw-token output. | Launcher rejects this bootstrap source; compatibility surfaces are not launcher authority. |
| T-LCB-GATE-03 | Omit descriptor review, mutation receipt, target-host containment evidence or Stage-B/C receipt verification. | Fail closed before migration, capability issuance, process creation or socket change. |

## Exit evidence

The Stage-D execution receipt must bind:

- descriptor, plan and acceptance-matrix SHA-256 digests;
- every changed implementation/migration/test path and digest;
- the exact target host and containment probe version;
- test commands, counts and results;
- pre/post dispatch-ledger digest;
- database/journal integrity results;
- secret-canary sink-scan results;
- crash-point matrix results;
- explicit statements that no real provider ran, no external credential was loaded, no automatic
  launch was enabled and no production/non-loopback authority was granted.

An independent security reviewer and runtime reviewer must reproduce the critical leak, scope,
crash and ledger probes. Their PASS permits only fake-child local-pilot use. Real-provider launch
still requires a separate admission and enablement receipt.
