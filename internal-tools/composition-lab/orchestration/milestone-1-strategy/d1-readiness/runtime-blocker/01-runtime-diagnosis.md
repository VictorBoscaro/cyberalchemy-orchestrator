---
artifact_kind: runtime-blocker-diagnosis
status: diagnosed-no-change
date: 2026-08-13
dispatch_id: 2026-08-13-repository-lens-inventory-extraction
scope: compile_bound_launch_plan and governed host-workflow binding path
---

# D1a runtime diagnosis: connected topology

## Verdict

`opening-record.json` is a valid ledger opening but is deliberately not a compilable legacy-managed
workflow. The exact blocking branch is
[`dispatch_workflow.py:120-126`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L120):
after canonical opening validation and route resolution, any truthy `connections` value raises
`GateBlockedError` before the output directory or any manifest is created.

This is a safety fence, not an accidental schema disagreement. The appender accepts typed
connections, while the compiler can produce only independent turn-zero launches with empty input
slots. Removing the fence would misrepresent the D1a graph as executed while launching its writer,
auditor, and approver without governed upstream inputs or readiness.

The smallest **syntactic** change would be to delete or narrow the truthiness check. That change is
unsafe and does not support sequential semantics. The smallest **semantically honest** change is a
staged, sequential-only compatibility path that (1) launches only ready roots, (2) records an
accepted producer output, (3) materializes an exact downstream manifest from that output, and (4)
then issues the existing bound turn-zero launch for the downstream group. It must reject
`zig-zag`/`feedback` until their lifecycle is separately defined. This is more than a one-line
compiler edit because the current terminal binding contract records no accepted output.

D1a would remain blocked by such a sequential-only increment: its exact record includes a
`feedback` edge as well as two `sequential` edges
([`opening-record.json:88-91`](../record/opening-record.json#L88)). Supporting sequential alone is a
useful first runtime slice, not sufficient readiness for this dispatch.

## Exact failure path

1. `compile_bound_launch_plan` first invokes the canonical appender's validate-only path
   ([`dispatch_workflow.py:61-91`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L61),
   [`dispatch_workflow.py:102-103`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L102)).
   D1a passes it.
2. The registry resolves `research` as `live`, routable, `legacy-managed`, using
   `host/inherited@1` ([`dispatch-type-registry.v1.json:5-13`](../../../../../../implementations/contracts/dispatch-type-registry.v1.json#L5)).
3. The compiler checks ledger schema and dispatch type, then reads `connections`
   ([`dispatch_workflow.py:109-120`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L109)).
4. Because D1a's array is non-empty, lines 121-126 raise before `_relative_output`, manifest
   generation, or `_write_canonical` can run.
5. The focused regression test explicitly requires that behavior and proves the output directory
   remains absent ([`test_dispatch_workflow.py:127-163`](../../../../../../implementations/tests/runtime/test_dispatch_workflow.py#L127)).

The failure therefore occurs in the compiler, after record validity and route validity, and before
binding materialization. It is not caused by D1a's hashes, group names, model names, schema version,
or research capability registration.

## Intended contracts and the divergence

### Ledger/dispatch contract

The canonical appender declares `connections` as optional typed edges and admits exactly
`sequential`, `zig-zag`, and `feedback`
([`append-dispatch.cjs:17-32`](../../../../../../.claude/skills/register-dispatch/append-dispatch.cjs#L17),
[`append-dispatch.cjs:139-173`](../../../../../../.claude/skills/register-dispatch/append-dispatch.cjs#L139)).
It validates endpoints and the `loop_cap` restriction
([`append-dispatch.cjs:443-458`](../../../../../../.claude/skills/register-dispatch/append-dispatch.cjs#L443)).
For `code`, it goes further: canonical group sequences are required to have exact sequential edges
([`append-dispatch.cjs:460-494`](../../../../../../.claude/skills/register-dispatch/append-dispatch.cjs#L460)).
Thus the persisted schema treats connections as meaningful dispatch structure, not unknown data.

The research capability says group function comes from agent roles and workflow position from
`connections`; its canonical shape uses sequential, zig-zag, and conditional feedback
([`.claude/skills/research/SKILL.md:46-58`](../../../../../../.claude/skills/research/SKILL.md#L46),
[`SKILL.md:80-96`](../../../../../../.claude/skills/research/SKILL.md#L80)). It assigns dependency
scheduling, retries, and effective inputs to the host/runtime
([`SKILL.md:121-125`](../../../../../../.claude/skills/research/SKILL.md#L121)). D1a depends on exactly
that promise: extractor returns precede the sole writer, then audit, then approval
([`d1-dispatch-sheet.md:120-130`](../record/d1-dispatch-sheet.md#L120)).

### Current compiler contract

For connectionless records, the compiler:

- iterates every group and every seat;
- assigns every seat `turn_ordinal: 0`;
- emits `slots: []`;
- creates a digest-bound workflow manifest and an `ACI-WORKFLOW-BINDING-V1` envelope containing the
  exact confirmed prompt; and
- returns all launches in one flat plan.

These behaviors are at
[`dispatch_workflow.py:127-204`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L127)
and are asserted by
[`test_dispatch_workflow.py:85-111`](../../../../../../implementations/tests/runtime/test_dispatch_workflow.py#L85).
There is no ready-set calculation, topological ordering, downstream launch state, result capture, or
edge-to-slot compilation.

### Existing lower-level runtime capabilities

The host and runtime already provide useful pieces, but not a graph scheduler:

- The host hook distinguishes spawn (`turn_ordinal == 0`) from follow-up (`turn_ordinal > 0`) and
  refuses unbound follow-ups
  ([`host_dispatch_hook.py:423-477`](../../../../../../implementations/server/runtime/host_dispatch_hook.py#L423),
  [`host_dispatch_hook.py:510-513`](../../../../../../implementations/server/runtime/host_dispatch_hook.py#L510)).
- A follow-up is a later turn of the **same group/seat**, requires the immediately prior turn to be
  terminal, targets that bound agent, and uses a prompt template already bound by the confirmed seat
  prompt ([`service.py:5511-5558`](../../../../../../implementations/server/runtime/service.py#L5511)).
  It is not a cross-group sequential edge.
- `WorkflowInputManifest` can validate repository sources and `binding-output` sources by exact path,
  digest, byte size, producer binding, same-dispatch identity, and terminal producer state
  ([`service.py:5286-5425`](../../../../../../implementations/server/runtime/service.py#L5286)).
- Focused tests prove both later-turn binding and terminal-producer-gated `binding-output`
  ([`test_host_workflow_binding.py:348-381`](../../../../../../implementations/tests/runtime/test_host_workflow_binding.py#L348),
  [`test_host_workflow_binding.py:383-430`](../../../../../../implementations/tests/runtime/test_host_workflow_binding.py#L383)).

The missing seam is between a terminal producer and a schedulable downstream group. A bare
connection contains only `from`, `to`, `type`, and optional `loop_cap`; it carries no result path,
schema, cardinality, byte ceiling, acceptance rule, or mapping from producer seats to downstream
slots. D1a likewise has no such machine-readable declarations. Its prompts say that extractors
return reports and that the writer receives governed handoffs, but prompts are not a materialization
contract ([`opening-record.json:23-57`](../record/opening-record.json#L23)).

The repository's workflow-graph discovery reaches the same bounded conclusion: terminal binding
state plus matching file bytes does not prove that those bytes were the producer's accepted output
([`workflow-graph.md:43-72`](../../../../../../docs/discovery/workflow-graph/workflow-graph.md#L43)). It
classifies `binding-output` as a compatibility seam and requires a total mapping from terminal
binding, accepted-output receipt, immutable artifact identity, and logical operation to an accepted
output reference ([`workflow-graph.md:343-378`](../../../../../../docs/discovery/workflow-graph/workflow-graph.md#L343)).
That document is discovery evidence, not current runtime authority.

## Capability matrix

| Surface | Supported now | Not supported |
|---|---|---|
| Canonical appender | Validates and persists typed connection declarations | Execution, readiness, delivery |
| Registry | Resolves `research` to live `legacy-managed` capability | `runtime-managed` route (focused test explicitly rejects it at [`test_dispatch_workflow.py:206-212`](../../../../../../implementations/tests/runtime/test_dispatch_workflow.py#L206)) |
| Launch compiler | Exact bound prompts/manifests for independent turn-zero seats | Any non-empty topology, dynamic slots, downstream waves |
| Host hook | Enforces binding marker, turn kind, exact envelope, prompt, manifest | Deciding which group is ready |
| Runtime binding | Validates frozen manifests and terminal producer references | Capturing/accepting the producer's output; traversing connections |
| Research contract | Defines semantic topology and handoff expectations | Implements neither scheduler nor transport |

## Risks of apparent fixes

1. **Delete the guard.** All seven D1a seats would appear in one launch plan at turn zero with empty
   slots. The writer could run before extractors, the audit before files exist, and the approver
   before audit. This is connection erasure disguised as support.
2. **Topologically sort but still emit all launches.** Ordering a JSON array does not make host tool
   invocations wait, nor does it bind outputs to inputs. The parent remains an unrecorded scheduler
   and relay.
3. **Use `followup_task` for downstream groups.** The runtime binds follow-ups to the same group,
   seat, prior turn, and agent target. Reusing it cross-group would violate its authorization and
   prompt-template invariants.
4. **Generate static downstream manifests during initial compilation.** A valid `binding-output`
   needs a producer binding ID plus a path, digest, and byte size that do not exist before the
   producer finishes. Inventing them would fail integrity checks or manufacture provenance.
5. **Treat terminal state as output acceptance.** `resolved`, `error`, and `cancelled` are all
   terminal enough for today's compatibility source check; none proves an official successful
   output. The workflow-graph discovery calls this exact proof gap out.
6. **Ignore attempt identity while adding waves.** The compiler currently creates
   `attempt-{group_id}-{seat_index}-0`, omitting `dispatch_id`
   ([`dispatch_workflow.py:144-160`](../../../../../../implementations/server/runtime/dispatch_workflow.py#L144)),
   while the database makes `attempt_id` globally unique
   ([`009_host_workflow_binding.sql:1-10`](../../../../../../implementations/server/runtime/migrations/009_host_workflow_binding.sql#L1)).
   Enabling more staged launches without dispatch-scoped identity preserves a known cross-dispatch
   collision hazard.
7. **Claim D1a is ready after sequential support.** The writer-to-auditor edge is `feedback` with
   `loop_cap: 2`; the exact record still requires feedback lifecycle and re-entry semantics.

## Smallest safe sequential increment

The narrowest change worth calling sequential support is a compatibility-only, fail-closed slice:

1. **Admission:** accept only acyclic `sequential` edges; reject self-edges, cycles,
   `zig-zag`, and `feedback`. Preserve canonical appender validation. Do not silently drop an
   unsupported edge.
2. **Compilation:** compile bound launch envelopes only for root groups. Preserve the existing
   envelope schema, exact prompt digest, manifest digest, route resolution, and host hook. Use
   dispatch-scoped attempt IDs before issuing new bindings.
3. **Output acceptance:** extend terminal completion with an explicit immutable output receipt
   (artifact/path, digest, size, schema, producer binding, successful standing). Do not infer output
   from a file appearing in the working folder or from terminal state alone.
4. **Readiness/materialization:** after every required predecessor has a successful accepted-output
   receipt, create the downstream `WorkflowInputManifest` with ordered `binding-output` sources and
   issue that group's existing turn-zero spawn envelope. A downstream group remains absent from the
   ready plan until this succeeds.
5. **Evidence:** persist an edge/release decision tying the declared connection, producer receipt,
   downstream manifest digest, and downstream binding. ACI bindings continue to validate exact
   prompts and bytes; the compatibility scheduler does not bypass the host hook.
6. **Tests:** retain the current connectionless behavior; prove root-only launch, blocked downstream
   before producer acceptance, exact downstream byte delivery after acceptance, wrong producer,
   wrong digest, failure/cancellation, cycle, unsupported edge, retry/idempotency, and no-write on
   rejection.

Steps 3-5 are the irreducible new seam. Existing manifest validation can be reused, but no current
contract supplies the accepted output or release decision. If the project does not want to add that
seam to the legacy adapter, the honest alternative is to keep the guard and implement sequential
scheduling only in the future canonical workflow runtime.

For D1a specifically, a later decision must additionally define `feedback`: what result triggers a
correction, who receives it, how a new writer/auditor turn is bound, what `loop_cap` counts, and what
accepted output supersedes or preserves the prior version. Nothing in this diagnosis authorizes
flattening that edge.

## Reproduction and evidence commands

Repository state used:

```text
git rev-parse HEAD
6f9d7d860a3e3dd3c6e702fbb1117a3741b22930

Get-FileHash -Algorithm SHA256 <opening-record.json>
CE18E35A7ECECF057CE2FE7E20488784171A1F17912F8B484C6E548302863875
```

Non-mutating D1a probe (the nominated output path was absent before and after):

```text
output_exists_before=False
opening_validation=PASS
compile=GateBlockedError: legacy-managed workflow compilation does not materialize connection handoffs; refuse connected topology until governed downstream input materialization is available
output_exists_after=False
```

The probe loaded the exact JSON, called `validate_opening_record`, then
`compile_bound_launch_plan(... capability_ref='research' ...)`, caught `GateBlockedError`, and checked
the output path on both sides. No append, bridge open, binding, or launch occurred.

Focused executable evidence:

```text
python -m unittest implementations.tests.runtime.test_dispatch_workflow -v
Ran 6 tests in 0.488s — OK

python -m unittest \
  implementations.tests.runtime.test_host_workflow_binding.HostWorkflowBindingTests.test_followup_requires_terminal_bound_agent_and_frozen_template \
  implementations.tests.runtime.test_host_workflow_binding.HostWorkflowBindingTests.test_binding_output_requires_terminal_producer_and_exact_bytes -v
Ran 2 tests in 0.893s — OK
```

These tests establish the current guard and the lower-level primitives only. They do not establish a
connection scheduler, accepted-output publication, or D1a executability.

## Decision for D1a

Keep `status: prepared-not-opened`. Do not confirm, append, compile, open, or launch the current
record. A sequential-only runtime increment would reduce one capability gap but would not discharge
D1a's feedback edge. The next legitimate readiness artifact must either cite implemented and tested
sequential **and feedback** materialization or present a newly strategy-owned exact record whose
semantics no longer require feedback; either path requires fresh validation and human confirmation.
