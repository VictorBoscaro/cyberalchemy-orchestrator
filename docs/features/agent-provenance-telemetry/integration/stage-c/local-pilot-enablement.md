# Local-Pilot Enablement Decision

- Scope: `SWU-ACI-APT-VS-001`
- Owner decision date: 2026-07-23
- Current status: `PASS / OPERATIVE_LOCAL_PILOT_ONLY`
- Stage-B execution receipt SHA-256:
  `73f9d568153cffa2d8cdb45f92256802047ab1aa28f32654d09a91e9f4a00ebc`
- Runtime reviewer: PASS / NO OBJECTION, cycle 3/5
- Root-layer reviewer: PASS / NO OBJECTION, cycle 3/5

This independently accepted decision authorizes only an explicitly requested local pilot:

- bind address exactly `127.0.0.1`;
- use an explicit dedicated SQLite database path that is not inferred from the production reader
  or a shared/default runtime database;
- use the configured strict read-only dispatch ledger;
- verify migrations, registered profiles, journal integrity and projection readiness before serving;
- require opaque capabilities bound to the exact principal, action, phase and closed operation
  context for every protected operation; a capability cannot be reused across scopes;
- expose the already reviewed runtime, provenance and health routes only;
- preserve the existing dispatch ledger byte-for-byte.

It does not authorize external-network binding, production deployment, provider execution,
automatic agent launch, audit materialization, ledger writes or cutover. Configuration alone
cannot expand this scope. A failed startup check must fail closed before opening a socket.

The authorization is operative as a governance decision; it is not evidence that a socket is
currently open. The production composition remains hard-disabled, and any local-pilot entrypoint
must refuse to serve unless every condition above is satisfied.

## Independent Reviewer Receipt

- Verdict: `PASS / NO OBJECTION`
- Review cycle: `1/5`
- Reviewer role: independent Stage-C local-pilot enablement reviewer
- Reviewed owner-delta SHA-256:
  `3dc8ddceae017ef93479466ac685f60af934b70b031d2961a06093ecb9668bef`
- Bound Stage-B execution receipt SHA-256:
  `73f9d568153cffa2d8cdb45f92256802047ab1aa28f32654d09a91e9f4a00ebc`
- Bound exact-SWU descriptor SHA-256:
  `fd65af261ec3b9861bf55c28afd57a882adba9296e94e246e71f3ef6623f3640`
- Prior runtime/root review: `PASS / NO OBJECTION`, cycle `3/5`

The reviewer confirms that the operative permission is limited to one explicitly requested,
single-host loopback pilot using a dedicated database and the configured strict read-only ledger.
Startup is fail-closed before socket creation; protected routes retain their exact capability
scope; the dispatch ledger remains byte-identical. Production, non-loopback/external networking,
provider execution, automatic agent launch, audit materialization, legacy/runtime cutover and any
unreviewed route or authority remain blocked.
