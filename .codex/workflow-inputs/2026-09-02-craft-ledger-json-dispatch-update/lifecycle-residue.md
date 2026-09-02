# Lifecycle residue — 2026-09-02-craft-ledger-json-dispatch-update

- Session: `ses_87e29f91b9d29b273730af26b0c9b37e`
- Close status: `closed`
- Exit reason: `error`
- Seat launched: `craft_ledger_updater_0` (`writer`)
- Seat outcome: deliberately interrupted after it remained running beyond the coordinator's final one-minute completion window; no terminal mailbox return or frozen worker manifest was received.
- Host-binding gap: the seat received the generated `ACI-WORKFLOW-BINDING-V1` prompt, but the host hook did not create a `host_workflow_turn_bindings` row for this dispatch. The launch is therefore not accepted as a parent-bound terminal seat.
- Preserved partial outputs: the scoped Craft ledger, `CRAFT.md`, and `update-report.md` were left intact for independent inspection. Their presence and the updater's checkpoint do not convert the lifecycle outcome to success.
- Close evidence: orchestration event `evt_03d42c9a639768c5ddab0085d7b78983`; YAML close row digest `sha256:4785198b6a42a79ba2857bb4632e9a8698463ed939929be7709a4bf3e3246f91`; orchestration state hash `sha256:324e4a88d52cf25279d37f2a6667e5cd29e7d90094bc4b1637d5beb081f07721`.
- Reroute: Stage B may independently review the preserved path/hash-pinned artifacts, but it must treat Stage A lifecycle completion as failed and must not infer a bound-seat success.

No bridge stdout is persisted here.
