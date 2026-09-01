# POLICY-002 Integrated DomainSpec Review

**Date:** 2026-09-01  
**Verdict:** **PASS for planning only (author recheck)**; independent follow-up and POLICY-002 code entry remain separately gated  
**Behavioral contract:** coherent, including integrated L0-L2 capability ownership and explicit POLICY-003 deferral  
**Repair history:** the first **BLOCK** is preserved at `sha256:da74c3243ad804e388cc818e4918d9377d0ef00a1ed3efce4d6ec84e4d19d1a0`; the immediately preceding review at `sha256:4b010ddff3c2378f99fd0c0afcf0aceea18723a500ad5adab92c0694279641e0` was subsequently blocked by independent review because TEST-SPEC G5 made a stale repository-state claim

## Objective and claim boundary

This review asks whether the current POLICY-002 DomainSpec contracts are mutually consistent enough to authorize a separately readied, test-only fake-denial workpack. It checks the denial receipt, canonical digests, closed twelve-label corpus, failpoints, replay/conflict, file-backed reopen, zero external/production authority and deferral of POLICY-003.

This is static specification evidence only. It does not inspect or claim a POLICY-001 or POLICY-002 implementation, executable tests, provider behavior, host enforcement, product-selected grants or code-entry readiness. Lean-bridge files and claims are excluded entirely. The governing-source changes covered by the review history are two ownership-reference repairs, the removal of G5's stale POLICY-001 implementation-state claim and the resulting SC-019 hash refreshes.

## Reviewed source set

| Contract | SHA-256 |
|---|---|
| `specs/domain.md` | `978e5c018e8aaa97d277cbd403594c0dca511aa395cb603a0496cb567ba91f9c` |
| `specs/SPEC.md` | `319130e802af1d85aec2373517b3f9d72f79f6a68a221154c6691c47e2620c60` |
| `specs/TEST-SPEC.md` | `bfd080bc0ec4860d7c5b9f3f028b8bbd0560786e9e61a83ce51168b0d21b985d` |
| `specs/rules.md` | `eeac22fe4dc0edc3a31a2f9cbf94aea7d976cda1e61e1ce793fe66e0fc758225` |
| `specs/interfaces.md` | `c5e055ef443a3f3a1391b49e20b1f74b0bc7e5c523ca54295bf496037e70f028` |
| `specs/architecture.md` | `6991ebb1b470733b8044a9f081ba5284ce87f127671e12db0b9a2e205c381832` |
| `specs/glossary.md` | `f8c561b7d69a0eaf4dbd404d6d7ec01d9ddfaa67adf45a264e97d89e98de3efb` |
| `specs/capabilities/execution-policy-authority.md` | `8b8fa86efbd49ed74dd49da9cd05e33ed183e5194d4c3c27f2d0a08d8f7f241a` |
| `plan/TECH-POLICY-D0.md` | `522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` |

## Contract-by-contract result

| Contract | Result | Evidence and boundary |
|---|---|---|
| `domain.md` | **PASS** | Defines the closed `aci.execution-policy-fake-denial-receipt@1` fields, exact reason order, dual identity axes, one-row creation boundary and canonical denial/receipt vectors. Independent SHA-256 reproduction matched both declared digests. |
| `SPEC.md` | **PASS** | Registers the receipt, harness and ACI-R23 and states POLICY-002 as specified but separately gated, with no product values, callable action, provider, production fence or host enforcement. |
| `TEST-SPEC.md` | **PASS** | T-ACI-POL2-1 through T-ACI-POL2-8 cover the required behavior, the connection row routes the complete L0-L2 test surface to the current capability, and G5 now names separately reviewed POLICY-001 evidence as a prerequisite without asserting repository implementation state. |
| `rules.md` | **PASS** | ACI-R23 defines the L2 behavior, and the connection row now correctly identifies the capability's L0/L1/L2 ownership without extending it to POLICY-003. |
| `interfaces.md` | **PASS** | The test-only harness accepts only the temporary database path, denial key, persisted lineage identity, one closed label and optional failpoint; it exposes no executable callable or production export. |
| `architecture.md` | **PASS** | All six views preserve the package-level denial, one additional test table, no attempted-action arrow and the L3 firewall. SC-015, SC-018 and SC-019 pin the reviewed TECH, capability and TEST-SPEC hashes exactly. |
| `glossary.md` | **PASS** | Registers the receipt, harness, rule and the distinctions among selector, package-level denial and production-authority firewall without promoting the fixture to authority. |
| `execution-policy-authority.md` | **PASS** | Explicitly owns POLICY-000/L0, POLICY-001/L1 and POLICY-002/L2 and routes the fake-denial invariants, harness and T-ACI-POL2-1 through T-ACI-POL2-8. |
| `TECH-POLICY-D0.md` | **PASS** | Allocates L2 to fake deny-all with zero external action and keeps target-host enforcement in POLICY-003. The DomainSpec's non-executable selectors are a compatible refinement of its attempted-category language. |

## Invariant audit

| Required invariant | Result | Evidence |
|---|---|---|
| Closed durable receipt | **PASS** | One schema, ten required fields, exact `decision=denied` and exact ordered reasons are frozen in `domain.md`; no label is persisted. |
| Denial and receipt digests | **PASS** | Independent hashing of the literal UTF-8 canonical lines reproduced `bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399` and `5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11`. |
| Closed action-attempt corpus | **PASS** | T-ACI-POL2-3 contains exactly 12 non-empty, unique labels. Rules, interface, capability and architecture treat them only as routing selectors. |
| Atomic failpoints | **PASS** | `policy_denial.after_begin`, `policy_denial.after_receipt` and `policy_denial.before_commit` require zero rows after reopen; `policy_denial.after_commit` is only a lost response after transaction exit. |
| Replay and conflict | **PASS** | Same denial key or lineage identity with the same `denial_digest` converges on the first receipt; drift under either axis is a permanent no-write conflict. |
| File-backed reopen | **PASS** | Fresh handles must reproduce exact receipt bytes, receipt digest, denial digest and source-lineage binding; in-memory SQLite is explicitly insufficient. |
| Zero external and production authority | **PASS** | Only temporary SQLite I/O and one additional test-only receipt table are admitted. External-call spies and all production authority/runtime/effect rows remain zero. |
| POLICY-003 deferral | **PASS** | Product grants, real provider admission, production fence, sandbox launch, cutover evidence and target-host enforcement remain excluded. |
| Integrated ownership routing | **PASS** | TEST-SPEC, rules, architecture and the capability now agree that the current capability owns bounded POLICY-000/L0, POLICY-001/L1 and test-only POLICY-002/L2; POLICY-003 remains outside. |
| Implementation-state claim boundary | **PASS** | TEST-SPEC no longer infers whether POLICY-001 is implemented; it requires separately reviewed and digest-pinned harness, persistence and file-backed reopen evidence before POLICY-002 code entry. |

## Resolved BLOCK and repair history

### G-POL2-01 — stale capability ownership in `TEST-SPEC.md` — resolved

Prior contradictory text at line 461:

> Owns the bounded L0-L1 capability, parser/lineage harness boundaries, invariants and authority firewall checked by T-ACI-POL0-1 through T-ACI-POL1-8. POLICY-002 derives separately from TECH-POLICY-D0 and the domain receipt until a later capability amendment is independently reviewed.

Applied replacement:

> Owns the bounded L0-L2 capability, parser, lineage-harness and fake-denial-harness boundaries, invariants and authority firewall checked by T-ACI-POL0-1 through T-ACI-POL2-8.

### G-POL2-02 — stale capability ownership in `rules.md` — resolved

Prior contradictory text at line 765:

> Bounded L0/L1 contract surface, synthetic-lineage invariants and authority firewall; it does not yet own this L2 amendment.

Applied replacement:

> Bounded L0/L1/L2 contract surface, synthetic-lineage and fake-denial invariants, and authority firewall.

### G-POL2-03 — stale POLICY-001 implementation-state claim in `TEST-SPEC.md` G5 — resolved

The subsequent independent review blocked the preceding PASS because the G5 heading and body said POLICY-001 executable lineage evidence was not implemented. That claim was stronger than this amendment could prove.

Applied replacement:

> This amendment does not create or review POLICY-001 executable evidence. POLICY-002 code entry requires the POLICY-001 harness, persistence and file-backed reopen evidence to be separately reviewed and digest-pinned. POLICY-002/L2 implementation and POLICY-003/L3 target-host enforcement remain separate work.

These reference-integrity repairs did not change POLICY-002 behavior. SC-019 now pins the current TEST-SPEC digest `sha256:bfd080bc0ec4860d7c5b9f3f028b8bbd0560786e9e61a83ce51168b0d21b985d`. The author rerun found no remaining stale ownership or implementation-state assertion and reproduced both canonical denial digests and all twelve unique labels. This statement is not an independent approval of the repaired review.

## Workpack condition

The author recheck finds the integrated DomainSpec coherent for bounded workpack planning. Independent follow-up of this repaired revision remains pending; this document must not be used as self-approval for code entry. Code entry remains gated by all of the following:

1. An independent reviewer accepts this repaired DomainSpec review against the exact source hashes above.
2. Bounded POLICY-001 harness, persistence and file-backed reopen evidence is separately reviewed and digest-pinned as the executable prerequisite; this review does not promote or substitute for that evidence.
3. A separate POLICY-002 descriptor and readiness receipt freeze only the test-only harness, one additional temporary table, exact fixture/oracle inputs and T-ACI-POL2-1 through T-ACI-POL2-8.
4. The descriptor/readiness inputs pin the independently accepted review and its exact repaired source hashes.

Even after those conditions pass, the authorization ceiling is code entry for the bounded POLICY-002 test lane only. It does not authorize POLICY-003, production migrations or exports, runtime/journal/API wiring, real actions, providers, product policy values, cutover or deployment.
