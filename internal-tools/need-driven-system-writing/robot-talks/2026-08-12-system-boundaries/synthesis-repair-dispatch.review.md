# Independent Review — Synthesis Repair Dispatch

## Verdict

**AMEND**

The repair dispatch is schema-valid, its frozen inputs match, and it captures the five substantive
repairs required by the blocking synthesis review. It must not run yet. Four semantic lifecycle and
authority gaps remain: declared identity separation is not enforced against runtime receipts;
`T-01`–`T-06` are not absolutely frozen; the parent review receipt remains open without an explicit
closeout bridge; and the closeout agent is asked to log a gate presentation before root has
performed the relay.

## Deterministic validation

Command rerun:

```text
python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/robot-talks/2026-08-12-system-boundaries/synthesis-repair-dispatch.json
```

Result:

```text
VALIDATION=pass
DISPATCH=internal-tools\need-driven-system-writing\robot-talks\2026-08-12-system-boundaries\synthesis-repair-dispatch.json
```

All six frozen hashes declared under `source_artifacts` match the current repair contract, parent
dispatch, blocked findings, pre-repair dialogue, and parent `r01`/`r02` receipts. Deterministic
validity does not discharge the semantic gaps below.

## Checks that pass

### Repair scope and exact repairs

**PASS.** The route is limited to the defect identified by
`reports/05-synthesis.review.md`: remove `T-07`; correct the `03.2`, `03.3`, and `04.5` coverage
cells; change the synthesis count and pending range from seven to six; append rather than rewrite
the dialogue history; and do not create a replacement tension or move `04.5` elsewhere
(`synthesis-repair-dispatch.json:282-296`). This accurately captures all five required repairs and
adds no architecture, schema, skill, research, automation, promotion, or code authority.

### Same reviewer and complete re-verification

**PASS.** The review role is bound to the parent reviewer identity
`/root/formalization_automation`, matching the parent `r02` receipt
(`synthesis-repair-dispatch.json:97-103`; parent `r02-independent-review-subagent.json`). Step `r02`
requires independent reconstruction of all 18 eligible formulations and complete re-verification of
`T-01`–`T-06`, their evidence, classification, severity, uncertainty, citations, questions,
coverage, dialogue history, and authority boundary (`synthesis-repair-dispatch.json:362-375`). It
allows the reviewer to append only a dated addendum and receipt, not repair synthesis artifacts.

### Mechanical owner and root boundary

**PASS in structure, subject to the identity and sequencing repairs below.** The closeout/logger is
a third role with no synthesis or evidence-judgment authority, and root is limited to launch, join,
close, timestamp supply, and verbatim relay (`synthesis-repair-dispatch.json:105-112,498-509`). The
promotion guardrails and global stop conditions prevent implementation and require a separate
authorized dispatch for any human answer or follow-up (`synthesis-repair-dispatch.json:680-692`).

### Human disposition authority

**PASS in intent, subject to truthful presentation logging below.** Only the human may disposition
`T-01`–`T-06`; the route does not consume the answer, and every allowed disposition remains pending
until presentation (`synthesis-repair-dispatch.json:512-516,596-604`).

## Required repairs

### 1. Enforce runtime identity separation, not only role metadata

**Problem:** The role entries declare that the repair writer must differ from
`/root/shared_principles` and that the closeout logger must differ from root, writer, and reviewer
(`synthesis-repair-dispatch.json:87-112`). No step expectation or gate compares the actual
`agent_id` in `r01` or `r03` with those exclusions. `g01` checks content, while `g03` checks only
receipt fields and terminal states (`synthesis-repair-dispatch.json:468-495`). An excluded agent
could therefore use the expected `role_id` and satisfy the declared gates.

**Exact repair:**

1. Add an `r01` evidence expectation requiring
   `r01.agent_id != /root/shared_principles`,
   `r01.agent_id != /root/formalization_automation`, and
   `r01.agent_id != root`; require root to reject the spawn before mutation if it fails.
2. Add an `r03` evidence expectation requiring the logger receipt's `agent_id` to differ from root,
   the actual `r01.agent_id`, `/root/shared_principles`, and `/root/formalization_automation`.
3. Amend `g01` to include the repair-writer identity check and `g03` to include all three runtime
   identity relations, not merely matching role IDs.
4. Require the repair and closeout receipts to record the identities compared and the pass/fail
   result under `validation`.

This makes the new repair writer genuinely independent of the original synthesis author rather
than trusting an unenforced prose constraint.

### 2. Freeze `T-01` through `T-06` without an exception

**Problem:** The route claims `T-01`–`T-06` are frozen, but `boundaries.out_of_scope` and
`b02-repair-write-scope` permit a “strictly necessary citation-consistency” edit
(`synthesis-repair-dispatch.json:20-25,552-560`). The repair writer cannot obtain reviewer approval
before the later `r02` step, and the user asked for `T-01`–`T-06` to be frozen. Step `r01` correctly
says a discovered issue should become blocking residue rather than a silent edit
(`synthesis-repair-dispatch.json:289-296`); the broader exception contradicts that rule.

**Exact repair:**

1. Remove the citation-consistency exception from `boundaries.out_of_scope` and
   `b02-repair-write-scope`.
2. State uniformly that every byte of the six tension sections and every coverage mapping unrelated
   to `03.2`, `03.3`, and `04.5` is immutable in this route.
3. Require `r01` to record before/after hashes for each `T-01`–`T-06` section and every unaffected
   coverage row; any mismatch returns `BLOCK` and requires a new dispatch rather than reviewer
   approval inside this route.
4. Require `r02` to verify those section and row hashes against the frozen parent artifact.

### 3. Close or explicitly supersede the parent review lifecycle record

**Problem:** The parent `r01` receipt is terminal, but the parent `r02` receipt has
`join_status: completed` and `close_status: pending`. The repair intent says all delegated lifecycle
records will be closed, yet `r03` verifies only the new repair `r01` and `r02` receipts
(`synthesis-repair-dispatch.json:395-419,452-459`). A terminal new receipt for the same reviewer does
not by itself explain whether or how the parent pending close was resolved.

**Exact repair:**

1. Add both parent receipts as explicit `r03` inputs, not only frozen source metadata.
2. Require the same reviewer’s repair `r02` receipt to state whether it supersedes and closes the
   parent review attempt identified by the parent dispatch ID and receipt path.
3. Require `r03` to record a parent-lifecycle reconciliation: parent `r01` terminal; parent `r02`
   terminally closed by a named runtime close event or explicitly superseded by the same agent's
   terminal repair-review receipt. A stale `pending` state with no later authoritative event blocks.
4. Include that reconciliation in the terminal lifecycle ledger and `r03.validation`; do not rewrite
   the historical parent receipt merely to make it appear terminal.

### 4. Record gate presentation only after the verbatim relay occurs

**Problem:** `r03` currently receives a root-supplied presentation timestamp, writes
`human_gate_logged`, and appends the gate-presentation fact before root receives and relays the
packet (`synthesis-repair-dispatch.json:395-459`). The instruction that root must later relay it
“atomically” is a promise about a future action the logger cannot observe. If relay fails after the
append, `dialogue.md` falsely records a presentation.

**Exact repair:** split the mechanical closeout into a two-phase handshake owned by the same
distinct logger:

1. **Prepare phase:** after a PASS review and terminal repair/review receipts, the logger prepares
   the frozen gate packet and a closeout record that says `presentation: pending`; it does not append
   a presentation timestamp or `human_gate_logged` event.
2. **Relay phase:** root relays the frozen packet verbatim and emits an authoritative presentation
   event containing the actual timestamp and packet hash. Root neither summarizes nor disposes it.
3. **Log phase:** the still-active logger consumes that event, verifies the packet hash, appends the
   actual presentation timestamp and `human disposition: pending` to `dialogue.md`, completes the
   lifecycle ledger and `r03` receipt, and stops without consuming any human answer.
4. If the runtime cannot keep the logger available for the log phase, authorize root only to apply
   a logger-authored, hash-bound mechanical append after relay; root must not author or alter its
   content. Otherwise return `BLOCK` without claiming presentation.

This preserves a distinct mechanical logger while making the durable event describe something that
actually happened.

## Final assessment

The proposed substantive repair is precise and the same independent reviewer is correctly selected
to recheck the complete synthesis. The route also has strong no-implementation and human-authority
guards. The four amendments above are required before execution because current prose constraints
do not prove runtime identity separation, the six surviving tensions are not absolutely frozen,
one parent agent remains unclosed in durable evidence, and the gate log can precede the event it
claims to record.

After these repairs, rerun the deterministic validator and independently verify the amended identity,
freeze, lifecycle-reconciliation, and presentation-order contracts. Until then, do not launch the
repair writer.

## Dispatch Spec Result

- **Dispatch ID:** `robot-talks-2026-08-12-system-boundaries-synthesis-repair-v1`
- **Status:** amend
- **Mode:** mixed
- **Step count:** 3, requiring a two-phase mechanical handoff refinement
- **Patterns:** sequential, validation, handoff
- **Gates:** amend — runtime identity, absolute freeze, parent closeout, and truthful gate logging
- **Handoffs:** repair contract → bounded repair → full same-reviewer verification → mechanical
  packet preparation → verbatim root relay → observed presentation log
- **Subagent strategy:** required; three role-separated owners; authorization approved
- **Subagent lifecycle:** pre-run `none`; repair required before it can prove terminal closeout
- **Observability:** amend — `human_gate_logged` must follow an observed relay event
- **Promotion guardrail:** pass
- **Required repairs:** four, exactly as listed above
- **Next route:** amend this dispatch, revalidate, then independent review before execution

## Repair verification

**Verdict: PASS.** The amended dispatch satisfies all four required repairs and is ready for
execution subject to its own runtime gates.

1. **Runtime identity separation — PASS.** `r01` now requires pre-mutation comparisons against
   `/root/shared_principles`, `/root/formalization_automation`, and root, with spawn rejection on
   failure and the comparisons recorded in receipt validation (`synthesis-repair-dispatch.json:170,
   287-288, 584-585`). `r03` likewise compares its actual logger identity against root, the actual
   `r01.agent_id`, and both named prior agents, records the result, and is enforced by `g03`
   (`synthesis-repair-dispatch.json:224, 453, 595-599`).
2. **Absolute freeze of T-01 through T-06 — PASS.** The citation-consistency exception is removed.
   The dispatch makes every byte of T-01 through T-06 and every unaffected coverage row immutable,
   requires per-section and per-row before/after SHA-256 evidence in `r01`, blocks on mismatch, and
   requires `r02` to verify the same hashes against the frozen parent artifact
   (`synthesis-repair-dispatch.json:294-295, 374, 584-585, 672`).
3. **Parent lifecycle reconciliation — PASS.** Both parent receipts are explicit `r03` inputs
   (`synthesis-repair-dispatch.json:415-422`). The same-reviewer `r02` must cite the authoritative
   close or supersession event (`synthesis-repair-dispatch.json:197, 369-370`), while `r03` must
   reconcile the terminal parent `r01` and the parent `r02`, block on stale pending state, preserve
   the historical receipts, and record the reconciliation in its validation and lifecycle ledger
   (`synthesis-repair-dispatch.json:455-456, 568, 595-599`).
4. **Truthful gate logging — PASS.** `r03` prepares and hashes the packet with presentation pending
   and emits no presentation log (`synthesis-repair-dispatch.json:457-459`). Root then relays it
   verbatim and emits the actual timestamp plus packet hash (`synthesis-repair-dispatch.json:469-510`).
   Only afterward does the same logger verify the event, append the actual timestamp with human
   disposition pending, and complete lifecycle evidence; the fallback permits root to apply only
   logger-authored, hash-bound exact bytes after relay, otherwise the route blocks
   (`synthesis-repair-dispatch.json:515-573, 602-612`).

Deterministic validation returned `VALIDATION=pass` using
`.agents/skills/dispatch-spec/scripts/validate-dispatch.py`.

Frozen-hash verification also passed for all six declared inputs:

- `reports/05-synthesis.review.md` — `CC322DF2BE89C8F169269509FED26A7905AEE63EBFE3831670EBA5121C4DD061`
- `synthesis-dispatch.json` — `2B836B29068FBE263C978722C4676F32185E2D242C555CB8B35E41087B5B8DBC`
- `findings.md` — `B1F9B8290573B78F167A6DDAD66963E68B22EC82974A953A82202B54A8488B11`
- `dialogue.md` — `E10CDCB2FA8DE7239804EEBBFA5D048838072689C9BEA407AC6D1B390A079BAA`
- parent `r01-synthesis-subagent.json` — `7A6AD6DF94D85632379E7ABD6E77F890E53C01BEC3CA01C5153F191655A86DEA`
- parent `r02-independent-review-subagent.json` — `F97A59AAA80C8C1DE30439828244F353B2A3EC399167EBA9342A83137F3CA916`
