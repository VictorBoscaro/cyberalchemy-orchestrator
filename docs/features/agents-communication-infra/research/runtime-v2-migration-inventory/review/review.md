# Review — Runtime v2 migration inventory

Frozen target corpus:

- `research-initial-definitions.md`: `sha256:35c6a90e5d7d6083d6235b6591ba5286c3515243226752dfc906d1bf69461d49`
- `research.md`: `sha256:004dd3ddcebaa1a94498393abfd76a8173f85412e9acf399da5b4fc1e890dfef`
- `findings.md`: `sha256:7fff28019eb7d399138d02dd334e817e57458561257a21ab3eb0944c83988b6a`

## Coverage

| attacker | lens | findings raised | zero-findings defence (if any) |
|---|---|---:|---|
| Ownership/reference-integrity attacker | ownership / reference integrity | 3 candidates | — |
| Mechanics/correctness attacker | mechanics / correctness | 2 candidates | — |
| Fidelity/governance attacker | fidelity / governance | 4 candidates | — |

All three attackers read and attacked all three frozen targets. Thus every target was attacked from
every declared lens. No attacker returned zero findings, so the zero-findings red flag did not fire.
Overlapping candidates about profile/compiler ownership were deduplicated below. Both verifiers
refuted the candidates attacking the legacy compatibility classification because the quoted text is
a migration disposition and the target separately preserves current `legacy-managed` authority;
those candidates do not survive. Candidate claims were checked against the literal target bytes
before inclusion; the attacker and verifier returns are not persisted.

## `research-initial-definitions.md`

No surviving findings. The attacks did not identify a contradictory owner, an executable claim
greater than its evidence, or a governance violation in this target.

**Verdict:** KEEP

## `research.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| R-01 | `research.md` | “Preserve registry resolution, canonicalization/digests, strict opening/close validation, append-only discipline, one-use capabilities, receipts/idempotency” | MAJOR | Replace the blanket `one-use capabilities` claim with `scoped, revocable capabilities`; claim consumption after acceptance only when the governing exact-operation contract explicitly requires it. |
| R-03 | `research.md` | “The 18 failures exposed working-tree drift: the appender/schema moved while fixtures and the Stage-E source manifest remained pinned to earlier bytes. This blocks bridge/hook/local-pilot integration preflight” | MAJOR | Record this as a timestamped historical observation with the exact command, tree state, manifest digests and output; separately report the current reproducible preflight result instead of treating the unfrozen failure as a current workspace property. |

**Verdict:** FIX

## `findings.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| F-01 | `findings.md` | “it does not contain an executable skill-to-DAG pipeline, an autonomous DAG scheduler, or real provider execution” | MAJOR | Narrow the absent capability to integrated `runtime-managed` provider start and effect reconciliation; the live Claude/Codex host already executes real agents in the legacy lane. |
| F-03 | `findings.md` | “Owner (precedent)” and “Stage-A profile mirrors” | MAJOR | Split `Authority owner` from `Implementation precedent`; assign facts/stores to their single governing owners, and identify the profiles as non-authoritative mirrors of digest-bound APT-owned imports rather than as an owner. |
| F-04 | `findings.md` | “Build the skill-to-DAG compiler from the owned protocol discovery and prototype” and “build-from-owned” | MAJOR | Relabel both sources as proposal precedent and block an authority-bearing implementation decision until ownership is settled and the result is ratified and promoted into SPEC. |
| F-05 | `findings.md` | “This is direct evidence that the current working tree is not a stable migration baseline” and “The next synthesis must preserve the test failures and concurrent schema drift as evidence” | MAJOR | Replace the current-state/concurrency conclusion with a reproducible evidence record: timestamp, exact command, tree identity, manifest digests and output; separately state the current preflight result and do not claim concurrency without a witness. |
| F-06 | `findings.md` | “the subsequent precedent, non-vacuity and definitional-soundness skeptics must independently attack that synthesis” | MAJOR | Route the existing-artifact gate as `review`: independent explorer attackers by lens, one writer, skeptic verifiers, and the sole persisted `review.md`. |

**Verdict:** FIX

## Change requests

1. **MAJOR — Separate authority from precedent.** Replace the migration matrix's combined owner/precedent column, bind each authoritative fact or store to one governing owner, and classify Stage-A profile files as non-authoritative mirrors of frozen APT-owned imports.
2. **MAJOR — Keep candidate protocol ownership unsettled.** Treat the protocol discovery and compilation experiment as proposal precedent; block an authority-bearing skill-to-DAG implementation decision until ownership is settled and the result is ratified and promoted into SPEC.
3. **MAJOR — Narrow the provider-execution gap.** Replace the assertion that real provider execution is absent with the supported absence of integrated `runtime-managed` provider start and effect reconciliation.
4. **MAJOR — Correct capability lifetime semantics.** Preserve scoped and revocable capabilities generally; claim consumption after acceptance only when an explicit governing exact-operation contract requires it.
5. **MAJOR — Make drift evidence reproducible.** Attach the historical failing command, tree identity, manifests/digests and output; state the current preflight separately and remove the unsupported concurrency claim.
6. **MAJOR — Correct the next gate.** Replace the proposed research skeptic wave with the canonical existing-artifact `review` topology and its single `review.md` output.
