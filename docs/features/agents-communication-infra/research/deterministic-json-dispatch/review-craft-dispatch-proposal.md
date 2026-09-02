# Review — Craft dispatch proposal for deterministic JSON ledger state

- Reviewer: `/root/craft_dispatch_proposal_reviewer`
- Worker: `/root/craft_dispatch_proposal_worker`
- Review date: 2026-09-02
- Verdict: **FIX**
- `recheck_required`: `true`
- Frozen proposal SHA-256: `8A25DFEBD6CC8CF284ED97844B8081A7707DFF78C44970508892CF6370025A26`
- Frozen update opening SHA-256: `206341660D8B41E752322D4E23F98A1C9FA71D79BE22865D5521287B88F084E0`
- Provisional validator opening SHA-256: `866B2070718E0936D05D81D82C3F2EB46B7E26F8DA6BDBA6607628FE62B9C591`
- Proposal manifest SHA-256: `152851BEF7951BA18C19C3AB38F02911A06239681D9FFD524F773FC329AE37E1`

## Coverage

| lens | targets | result |
|---|---|---|
| ownership / reference integrity | workspace resolution, target ledger/view, proposed row IDs and links | Owning scoped ledger is correct and every proposed ID is currently absent, but four stale source-ledger references are omitted from the update contract. |
| determinism / operability | both openings, proposal manifest, pre/post-A staging | Both openings validate, but the source contract and pre-update target bytes used by A are not pinned; B also reads an unpinned proposal. |
| governance / claim ceiling | accepted hashes, fallback decision, canonical review boundary, open gaps | Local KEEP and host BLOCK are separated correctly; task-session is only an authorized next route; no canonical review or JSON-to-host success is claimed. |
| lifecycle / effects | routes, topology, confirmation order, filesystem and telemetry residue | The two single-seat Craft dispatches avoid the observed sequential compile cycle and give the updater exactly one independent validator. B remains provisional. No compile/open/append/launch/close evidence exists. |

This is not a zero-findings review. Every proposal artifact was read in full and both opening validators were independently rerun.

## Verified evidence

- Four Craft ledgers exist. `docs/features/agents-communication-infra/.craft/ledger.yml` uniquely owns `CTX-ACI-ROOT`, `CTX-ACI-RUNTIME-BASELINE`, `CTX-ACI-RESUMABLE-FEEDBACK`, and `DEF-ACI-DETERMINISTIC-DISPATCH-001`; the selected owner is correct.
- The five cited evidence hashes reproduce exactly: runtime review `8B5F...9DFF`, research definitions `5603...0B61`, definitions review `20FC...ECC`, confirmed opening `C4A4...702C`, and lifecycle BLOCK review `9173...F9B`.
- The current ledger/view hashes remained `4CD03CC9376CE607710C5E1F52D04B7A72AA627BA4445E0B765C408E8C51A492` and `E15F4FD0357A8EB10B966C45270D3A27B6C18E91316584565411D5E9FF928B1C` from the pre-freeze snapshot through review. The proposal worker did not mutate them.
- Both JSON openings parse, pass `validate_opening_record`, and return `valid dispatch record (schema v0.7.0)` under appender `--validate-only`.
- Resolver output reproduces the embedded Craft route digest `sha256:d3181166e9564a6dd3445cb9568fd16121cdbab79c21e8b304e5e532bde657ca`. The separately documented canonical review route digest is `sha256:34013d06ac00aaf69c8b2553eb7456930e9dce730e62da8deb71186bdcb7ec66`.
- `Lampson, Butler` has `role_fit: [writer, auditor]`; `Parnas, David` has `role_fit: [auditor, skeptic]`.
- Both dispatch IDs and all proposed row IDs are absent from the target ledger and append-only telemetry. The workflow folder contains only the proposal, manifest, frozen A opening, and provisional B opening.
- `anti_bias_mode` is `disabled`; each opening has one agent, no connections, explicit model/budget/prompt/effects/path, and no forbidden overlay fields.
- The accepted runtime review proves only the local scripted path and explicitly excludes canonical v2, `ConfirmRuntimeDispatch@2`, host-live/provider/tool/credential execution, feedback cycles, external effects, and production readiness. The proposal preserves that ceiling.

## Findings

### F1 — the confirmed A task can consume mutable task and target bytes

- Severity: **MAJOR**
- Evidence from `opening-craft-update.json`:

  > `Apply only the row-by-row changes frozen in PROPOSAL.md`

  The opening neither names the proposal's `8A25...5A26` digest nor pins the current ledger/view digests. The separate proposal manifest is not an input consumed or checked by the seat. Thus `PROPOSAL.md`, `ledger.yml`, or `CRAFT.md` could change after confirmation while the opening and generated binding remain unchanged.
- Related evidence from `PROPOSAL.md`:

  > `Required precondition: after A closes, create an exact runtime-owned aci-workflow-input-manifest/v1 pinning A's terminal update-report.md, ledger.yml, and CRAFT.md bytes and digests`

  B also audits the row contract in `PROPOSAL.md`, but that proposal is omitted from its required manifest and its digest is absent from the provisional prompt.
- Required fix: add the exact proposal SHA-256 and the accepted pre-update ledger/view SHA-256 values to A's frozen contract and require byte checks before mutation. Require B's post-A manifest to include the exact proposal bytes/digest in addition to A's report, ledger, and view, or otherwise bind and verify the same digest in B. Regenerate all affected hashes and the proposal manifest.

### F2 — the row contract knowingly preserves stale ledger claims

- Severity: **MAJOR**
- Evidence from `PROPOSAL.md`:

  > `Preserve status: active, severity: block, its canonical-v2/confirmation/production exclusions, and its existing links.`

  One existing link is labelled `Local fake execution repair pending same-reviewer recheck`; preserving that label contradicts the accepted final KEEP.
- Additional omitted stale source rows in `.craft/ledger.yml`:

  > `next_move: Preserve identity/role implementation Recheck KEEP ... while downstream runtime review proceeds.`

  > `impact: Commit f981397 and its forward-only repair cannot be promoted until independent implementation recheck passes. Runtime integration remains blocked.`

  > `reason: ... while implementation recheck and runtime ingestion remain unproven.`

  Runtime review is complete, and the identity implementation recheck already returned KEEP. The contract updates only root/runtime/continuation contexts and leaves these contradictory current-state fields behind.
- Required fix: add exact changes for `CTX-ACI-PROTOCOL-COMPILATION.next_move`, `DEC-ACI-AGENT-IDENTITY-ROLE-001.impact`, and `REL-ACI-IDENTITY-ROLE-DECISION-INFORMS-GAP.reason`; change the stale canonical-gap link label while preserving its target. Refresh the corresponding `indexes.next_moves` entry. Preserve all still-open runtime-ingestion, canonical-v2, confirmation, host-live, and production gaps.

## Verdict

**FIX.** The lifecycle shape is sound: A performs the bounded Craft update, B is an independently confirmed Craft validation after A and is exactly the updater's one reviewer, and neither is falsely labelled as canonical `review`. The remaining defects are load-bearing input-determinism and ledger-consistency gaps. No source/ledger mutation, compile, open, append, launch, close, commit, or push was performed by this reviewer.

Return the repaired frozen corpus to this same reviewer.

## Recheck 1 — repaired frozen corpus

- Recheck date: 2026-09-02
- Prior review SHA-256: `2D0D36726D07BD0D794CF47CA01440FC5C380BEEA88DD102BDF51891B4296B70`
- Repaired proposal SHA-256: `C21CAF952A74D1CE3C2A9050028DF7760C644C64ECB652A31E6614B24CEC0518`
- Repaired update opening SHA-256: `40D95BB399D7C51B977139A9EEA610FB2D70C1038C59873FE84A39C1592E32D0`
- Repaired provisional validator opening SHA-256: `A23A220C2FD5AF3AF7C5611A44D46555BD7C40F1887698EE51D54A4782A31CE3`
- Repaired manifest SHA-256: `C5400C8F99DBE4BCB57BCF3BD766A92E209F2229A946112A4EE5C6DF71BB3C12`
- Recheck verdict: **KEEP**
- `recheck_required`: `false`

### Finding resolution

- **F1 resolved.** A's binding prompt now requires exact pre-mutation matches for the repaired proposal (`C21C...0518`), ledger (`4CD0...A492`), and view (`E15F...28B1`) and requires `BLOCK` with zero target edits on mismatch. B remains explicitly provisional and cannot be frozen until its runtime-owned input manifest covers the exact proposal, A's terminal report, and post-A ledger/view bytes and digests. The proposal manifest repeats these preimages; every internal file hash matches the actual bytes.
- **F2 resolved.** The row contract now explicitly updates `CTX-ACI-PROTOCOL-COMPILATION.next_move`, `DEC-ACI-AGENT-IDENTITY-ROLE-001.impact`, `REL-ACI-IDENTITY-ROLE-DECISION-INFORMS-GAP.reason`, the stale canonical-gap link label, and the corresponding `indexes.next_moves` entry while preserving every open authority/execution gap.

### Reproduced checks

- Both repaired openings parse, pass `validate_opening_record`, and pass the appender's `--validate-only` check under schema `0.7.0`.
- Resolver digests and agent pool role fits are unchanged and valid.
- Every candidate dispatch/row ID remains absent from the target ledger and telemetry.
- The target ledger and view still match their frozen preimages. No update or validation output folder exists.
- The proposal folder contains exactly `PROPOSAL.md`, `proposal-manifest.json`, frozen A, and provisional B. It contains no launch plan, binding, runtime input manifest, receipt, or close record.
- A and B remain distinct single-seat Craft dispatches with no connection edge. B is exactly A's one independent validator, not a canonical `review` claim, and it can only be confirmed after A's terminal bytes exist.
- The task-session decision records only authorization to use that bounded route. The host sequential/feedback gap remains active, and the next move is implementation plus independent checking and a real JSON-to-host witness—not schema work or a success claim.

### Final verdict

**KEEP.** The repaired proposal is ready to present only Dispatch A's exact frozen sheet for confirmation. Dispatch B is not pre-confirmed or executable yet; it must be materialized against A's actual terminal outputs and separately confirmed. No compile, open, append, launch, close, ledger/view/source mutation, commit, or push was performed by this reviewer.
