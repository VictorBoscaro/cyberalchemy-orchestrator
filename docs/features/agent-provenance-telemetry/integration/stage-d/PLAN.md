# Stage D — Brokered Launcher Capability Bootstrap

## Decision and boundary

The next exact unit is `SWU-ACI-APT-LCB-001`. It adds the authority substrate needed by a future
agent launcher, but it does not launch a real provider. Its executable child is a deterministic
fixture that can attempt authorized and adversarial tool calls.

This boundary is required because the current implementation has two unsafe bootstrap shapes for a
real child:

1. `CapabilityManager.issue()` returns the raw bearer token to its caller.
2. `runtime issue-capability` and `runtime activate-local-probe` serialize returned values to
   stdout; activation returns agent, parent and reader tokens together.

The database stores only `sha256:<digest>`, which is correct at rest, and resolution already binds
action and phase. However, a real launcher cannot safely place the returned token in argv,
environment, a prompt, a file or ordinary process output. Stage D replaces that prospective path
with a broker-owned token and an OS-bound child channel.

The existing commands remain compatibility/trusted-operator surfaces during this SWU. They must not
be used by the launcher. Removing or changing them requires a separately reviewed compatibility
decision.

## Authority model

The host creates these identities; no child-authored request may supply or override them:

```text
logical operation
  operation_id = stable across an eligible retry
       |
       +-- physical attempt A
       |     attempt_id = A
       |     launch_id = A
       |     principal_id = agent-launch:A
       |
       +-- physical attempt B (retry)
             attempt_id = B
             launch_id = B
             principal_id = agent-launch:B
```

One launch therefore means one process tree, one attempt and one principal. A retry preserves only
the logical `operation_id`; it creates a new `attempt_id`, `launch_id`, principal and capability set.
The old launch is revoked before the retry becomes claimable. Concurrent active launches for the
same `(operation_id, attempt_generation)` are forbidden by a database uniqueness constraint.

Every brokered capability is bound to the complete closed context:

- repository, Session and Dispatch;
- logical operation, physical attempt and launch;
- principal, action, phase and audience;
- issuance, claim and expiry limits;
- the immutable tool-profile/capability-resolution digest when that profile exists.

The broker derives this context from accepted host state. Child messages contain semantic tool
intent only. Existing forbidden-authority-field rejection remains mandatory.

## Bootstrap and token custody

The capability bearer is generated in the trusted host boundary, registered by digest, and retained
only in the volatile broker secret store. The public result contains capability IDs and expiry
metadata, never bearer bytes.

The launcher creates an OS IPC endpoint before child creation and passes only the inheritable child
endpoint. The endpoint must be:

- non-addressable from unrelated processes;
- bound to the expected child process identity and launch ID;
- closed in the parent immediately after handoff and closed in the child after claim;
- unavailable to grandchildren unless the sandbox policy explicitly permits the broker shim;
- single-claim, with a 30-second maximum claim window.

The child performs a one-shot claim over that channel. A successful claim establishes a
channel-bound broker session; it does not return the ACI bearer. For each tool call, the broker
validates OS peer identity, live launch lease, action, phase, operation and current journal state,
then attaches the raw capability inside the trusted process for the local runtime call.

Raw ACI bearer bytes are forbidden from:

- child argv, environment, stdin and process-visible configuration;
- effective input, prompt, provider request or tool schema;
- SQLite, events, receipts, projections, artifacts and files;
- stdout, stderr, access logs, diagnostics, exceptions and tracebacks.

The broker must use an allowlist serializer for all responses and logs. Recursive “redact keys named
token” is insufficient: tests inject the secret under unrelated keys and inside free text. A
process-wide sensitive-value scrubber must replace exact known secret values before any diagnostic
sink, while normal output schemas never accept such values in the first place.

## Durable and volatile state

Migration `008_launch_bootstrap.sql` will add durable metadata only:

- launch lease identity and immutable binding fields;
- bootstrap-ticket digest, claim deadline and `claimed_at`;
- capability IDs, actions, phases, audiences and expiry metadata;
- process observation reference/identity, state and revocation reason;
- accepted event and command receipt references.

Neither the bootstrap ticket nor an ACI bearer is stored in plaintext. Durable states are:

```text
requested -> claimable -> claimed -> terminal
                    \-> expired
          \----------> revoked
claimed ------------> reconciliation_required
```

`claimed` is not proof that a provider started. For Stage D it proves only that the deterministic
fixture claimed the channel. A process observation becomes authoritative only through a journal
command. Wall-clock and process status are observations; accepted journal order is authoritative.

The volatile broker store is indexed by `launch_id` and capability ID. On restart its content is
gone. Durable `claimable` or `claimed` rows must move to `reconciliation_required`; the runtime must
not regenerate the same bearer or automatically repeat a launch. An authorized reconciliation may
revoke and create a fresh attempt/launch, or record an observed terminal fixture process.

## Expiry, revocation, cancellation and retry

- Capability expiry uses the injected trusted runtime clock and is at most 15 minutes after issue.
- The bootstrap claim expires no later than 30 seconds after it becomes claimable.
- Each broker call re-resolves expiry, revocation, action, phase, audience and full launch context.
- Cancellation first commits an authorized revoke intent. The broker then refuses new calls and the
  launcher terminates the contained process tree. Termination acknowledgement is not terminal state.
- Normal terminal observation revokes every launch capability before the launch is marked terminal.
- Revocation is idempotent by `(launch_id, reason, expected_version)`.
- Retry never resurrects or copies a bearer. It uses a new attempt, launch, principal, bootstrap
  channel and capability set.
- Unknown process/effect state never causes automatic relaunch.

## Logging and evidence

There are three distinct evidence classes:

1. Authoritative journal events and command receipts record accepted launch metadata transitions.
2. Redacted security observations record denial reason codes such as `claim_replay`,
   `peer_identity_mismatch`, `scope_mismatch`, `expired`, `revoked` and `secret_leak_blocked`.
3. Operational logs record lifecycle diagnostics using an allowlist.

Allowed operational fields are timestamp, severity, event code, launch ID, attempt ID, operation ID,
capability ID, action, phase, state, reason code and journal receipt/event references. They exclude
request/response bodies, headers, argv, environment, prompts, bearer/token digests, bootstrap-ticket
digests, exception locals and raw IPC frames.

Security observations are rate-limited for telemetry but each state-changing revoke remains an
authoritative event. Metrics use bounded reason-code labels and never principal names, paths,
content, prompts or secrets.

## Implementation sequence

1. Freeze this descriptor digest and obtain independent security/runtime review plus exact mutation
   authorization.
2. Add the migration with immutability, uniqueness and no-plaintext-secret constraints.
3. Refactor capability creation with a broker-only issuance path returning public metadata; leave
   compatibility CLI behavior outside launcher reach.
4. Implement the volatile secret store, one-shot channel claim and broker mediation.
5. Implement launch request, claim, revoke and reconciliation commands with atomic events/receipts.
6. Add a deterministic fixture child and target-host containment probes. Do not add a provider
   adapter, model credentials or automatic orchestration.
7. Run the acceptance matrix with failure injection, restart tests and an exact secret canary across
   every durable and diagnostic sink.
8. Produce a digest-bound execution receipt and independent post-change review.

## Promotion gate

Passing Stage D establishes only that the fake-child launch/bootstrap boundary is suitable for the
local pilot. A later SWU must separately admit a real adapter and launcher on the target host under
the existing `SandboxLauncher`, verified-opening, process cleanup, credential and provider
conformance gates. Until that receipt exists, real provider execution and automatic launch remain
blocked.
