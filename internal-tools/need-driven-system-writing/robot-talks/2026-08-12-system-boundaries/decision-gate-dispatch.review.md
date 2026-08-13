# Decision-gate dispatch review

## Verdict

**AMEND**

The route is structurally valid and its authority design satisfies the requested Decision Gate
constraints, but it cannot currently pass its own frozen-input gate. One exact repair is required
before any analyst is launched.

## Blocking finding

### 1. The completed dialogue hash is stale

`source_artifacts.completed_dialogue.sha256` is
`D37C26EFE3243806E63F538D9F29E855F04C1869F5810C950E217B3BE5120684`
(`decision-gate-dispatch.json:49-52`), while the current `dialogue.md` SHA-256 is
`601ED38425EE0335F616FCBB795CDA818169036A09AC57FD2729E61B8A3CC825`.

This is not an optional provenance discrepancy. Step `d01` requires every frozen input hash to
match and returns `BLOCK` on mismatch (`decision-gate-dispatch.json:230`); `g01` likewise requires
all artifact hashes to match (`decision-gate-dispatch.json:456-460`); and the dispatch-wide stop
condition forbids analysis while any frozen source hash differs (`decision-gate-dispatch.json:616`).

The live dialogue contains the completed, append-only `Human-gate relay and lifecycle closeout`
section, including the still-pending six dispositions and the no-consequential-work boundary. The
dispatch was written after that file, so the pinned value does not identify the declared completed
input.

**Exact repair:** verify that the current append-only dialogue is the intended completed source,
then replace only `source_artifacts.completed_dialogue.sha256` with
`601ED38425EE0335F616FCBB795CDA818169036A09AC57FD2729E61B8A3CC825`.
Re-run the deterministic validator and all four frozen-source hash comparisons. If `dialogue.md`
changes again before execution, freeze the new intended bytes instead; do not bypass the mismatch
gate.

## Requested contract checks

- **Analyst recommends but never decides — PASS.** `d01` labels recommendations as advice, forbids
  preselection, and stops before presentation. Human selection is the sole authority under `g05`.
- **All six tensions represented — PASS.** `d01` must address `T-01` through `T-06` individually;
  its receipt records six classifications, and `d02` independently reconstructs all six from the
  frozen findings.
- **Evidence-grounded classification — PASS.** Classification is relative to a named next
  consequential stage, must preserve uncertainty, and may use only the verified findings and final
  review. `d02` separately checks blocker/deferrable/assumption calibration.
- **Concrete blocker options and Explain path — PASS.** Every blocker requires at least two viable
  real options, benefit, cost or risk, when-to-choose guidance, reversibility, downstream impact,
  related decisions, one non-binding recommendation, and a separate non-committal
  `Explain / more context` path. The explanation loop repeats the same options through `d02`,
  `d03`, and `d04` before another verbatim relay.
- **Independent review and repair loops — PASS.** The reviewer must be one stable identity distinct
  from analyst, presenter, recorder, and root. Recommendation, packet, and record failures reroute
  only to their owning role and return to the same reviewer; the reviewer never edits repairs.
- **Mechanical frozen presentation — PASS.** `d03` may only condense PASS-reviewed content, assigns
  stable IDs, records presentation as pending, and hashes the packet. `d04` verifies byte fidelity
  and freezes the exact approved hash before relay.
- **Recorder waits for an actual choice — PASS.** `d05` requires both an authoritative relay event
  and an exact `human_answer` event. Silence, ambiguity, questions, uncertainty, and Explain requests
  resolve nothing; partial answers preserve gate status `BLOCK`.
- **No implementation and root orchestration-only — PASS.** Root is limited to launch, join, close,
  verbatim relay, and authoritative event emission. `g08`, promotion guardrails, boundaries, and
  stop conditions prohibit architecture, planning, research, schema or skill mutation,
  implementation, automation, promotion, and code.
- **Lifecycle and observability terminality — PASS.** Every iteration has versioned receipt and
  artifact evidence; all attempted agents require terminal join and close or reviewed handoff,
  with residue and reroute on non-happy paths. `g07` blocks pending successful paths, and events are
  grouped by dispatch, iteration, role, identity, question, hashes, gate state, and lifecycle.

## Validation evidence

- Deterministic validator:
  `.agents/skills/dispatch-spec/scripts/validate-dispatch.py decision-gate-dispatch.json` —
  `VALIDATION=pass`.
- Frozen hashes: `findings.md` **PASS**,
  `reports/05-synthesis.review.md` **PASS**, `human-gate-packet.md` **PASS**,
  `dialogue.md` **MISMATCH**.
- Latest authorization: represented as `source_artifacts.authorization_context`; it preserves
  agent execution, root orchestration-only, subagent-authored dispatches, and independent final
  review.

## Dispatch Spec Result

- **Dispatch ID:** `robot-talks-2026-08-12-system-boundaries-decision-gate-v1`
- **Status:** amend
- **Mode:** mixed
- **Step count:** 6
- **Patterns:** decision, validation, handoff
- **Gates:** amend — frozen dialogue mismatch; all requested authority and execution gates pass
- **Subagent strategy:** required; four role-separated owners; authorization recorded as approved
- **Subagent lifecycle:** pre-run `none`; terminality contract is feasible
- **Observability:** pass
- **Promotion guardrail:** pass
- **Required repairs:** one, exactly as stated above
- **Next route:** amend the frozen dialogue hash, revalidate, then independently re-review before
  execution

## Repair verification

**PASS**

The sole required repair is complete. `source_artifacts.completed_dialogue.sha256` now equals
`601ED38425EE0335F616FCBB795CDA818169036A09AC57FD2729E61B8A3CC825`, exactly matching the current
SHA-256 of `dialogue.md`. The stale `D37C…0684` value is no longer used.

Deterministic validation also returned `VALIDATION=pass` using
`.agents/skills/dispatch-spec/scripts/validate-dispatch.py`.

The repaired dispatch therefore clears the prior frozen-input blocker and is ready for execution
subject to its runtime gates. No additional repair is required by this review.
