---
name: mint
description: Mint a NEW domain-specialized repository by composing the domainspec-new-repo scaffolder and casting the cav2 authority spine (authority kinds, definitions tower, constitutions, promotion lifecycle) onto a target domain, so the new repo can author its OWN governed authority. cav2-native, private, intended-not-shipped. Use when starting a new domain/research/project repo that needs a governed authority spine. NOT for editing an existing repo's authority (route to definitions-governance / constitution-governance / decision-gate) and never for a public-attached mint (blocked until the public/private boundary resolves).
---

# Sigil: Mint

<status>
candidate · intended-NOT-shipped · cav2-native (private). **Emit-logic BUILT (2026-07-01):** the core 6
emit-templates + the 13 committed additions + the composing `EMIT-PROCEDURE.md` live at
`cyberAlchemy-v2/development/mint/templates/`. Mint remains **non-executed** — the emit-logic is validated
on the worked example (`examples/`), not a live mint run. Open gates: the L2 signer capability, the
public/private boundary, and generalization beyond one domain (see <gates>).
Design authority: `cyberAlchemy-v2/development/mint/` (SPEC · ARCHITECTURE-BUNDLE · EXECUTION-PACK ·
WORK-PACK · IMPLEMENTATION-LAYERING · HANDOFF).
</status>

<objective>
Cast the cav2 authority spine onto a specific domain, producing a new domain-specialized repo that
knows how to author its OWN authority — inheriting the cav2 META-authority machinery (the MOLD) and
localizing the OBJECT authority (the domain's own kinds / definitions / rules).
</objective>

<logic-type>
Arcana: a signed governance act (compose + authority-casting) with owner-ratification and gates.
</logic-type>

<applicability>
Use when:
- starting a NEW domain/research/project repo from the cav2 framework;
- the new repo must carry a governed authority spine (kinds, definitions, constitutions, promotion lifecycle);
- an owner is available to RATIFY the proposed authority kinds (the D49 owner-gate).

Do NOT use when:
- editing an existing repo's authority — route to the owning governance skill (`definitions-governance` /
  `constitution-governance` / `decision-gate`);
- the mint would emit a PUBLIC-attached repo — BLOCKED by `BLK-CAV2-PUBLIC-PRIVATE-001` until resolved;
- you would inherit cav2's OBJECT kinds as the domain's governing base (circularity — see the guardrail).
</applicability>

<inputs>
| input | meaning |
|---|---|
| `domain` | the target domain/research/project name |
| `target-repo-path` | where the minted repo is created (sibling of domainspec-core) |
| `--source <framework-path>` | the framework half to attach (cav2 + DomainSpec + Arcanum) |
| `--attach submodule\|copy\|symlink` | clone-safe attach mode (default submodule) |
</inputs>

<process>
The 5-stage mint flow (design: ARCHITECTURE-BUNDLE §The 5-stage mint flow). Gate-first — `--mode plan` before `apply`.

**Emit-logic source (built):** `cyberAlchemy-v2/development/mint/templates/EMIT-PROCEDURE.md` composes the
core 6 templates + the 13 committed additions + the **Universal Governance Baseline** (Steps 13–14: the 27
universal cav2 definitions as baseline rules/primitives + the D15 project-space format, seeded PROPOSED with
D11/D31/D40 strip-bindings) — Steps 1–14, per-emit self-checks §7 checks 1–13. Stages 2–3 run that procedure.
The baseline partition is frozen at `development/research/2026-07-01-universal-baseline-partition/findings.md`.

1. **Scaffold (compose).** Call `domainspec-new-repo --source <fw> --attach submodule --mode plan`, surface
   the plan, then `--mode apply` (crosses the scaffolder's own master gate). Output: the partition tree +
   clone-safe attach. **NO edits to `domainspec-new-repo`** — compose only.
2. **Authority-spine seed.** Emit, via the authority-triage front-door (candidate/review-mode), the domain
   spine from the emit-template set:
   - **core:** domain `AUTHORITY-MODEL` (proposed kinds, each with a default-deny row) + `source-spine` +
     `promotion-policy` + `constitution` stub + `DEFINITIONS` skeleton;
   - **committed additions (decision 2026-07-01)** — *Tier 1:* `DEFINITIONS-INDEX` + `DRIFT-AUDIT` (+ `SCHEMAS`)
     stubs [#8]; governance→methods catalogue [#13]. *Tier 2 meta:* narrowest-owner routing [#1];
     invariant→axiom→constitution→validator derivation [#2]; table-level default-deny **CLOSED** declaration
     [#5]; DEFINITION-LOCALIZATION-ROUTE + `definitions/reviews/` staging [#9]; stop/demotion rule (`stop_rule`)
     [#12]. *Tier 2 seed-format (the empty contract, NEVER cav2's rows):* posture-contract [#3]; non-collapse
     rule-slot [#4]; boundary skeleton [#6]; import rung [#7]; `CONSTITUTION-IMPORT-PACK` [#17]. *Cheap:*
     `decisions/README` + D36 schema [#10]; `authority/README` [#18].
   - **Guardrail:** seed the FORMAT, not cav2's ROWS.
3. **Decision-gate (propose → ratify → CLOSE).** Emit a signed `authority/decisions/<date>-mint.md`; the cav2
   owner **RATIFIES** the proposed kinds; emit the **ratify-CLOSE** record so kinds move `PROPOSED`→ratified,
   not left `PROPOSED` [#11]. Actored gate: EXECUTION-PACK §owner-gate.
4. **Crosswalk.** Emit `RELATED-FRAMEWORK-CROSSWALK.md` (per-concept borrow / block / analogy-only / promotion-candidate).
5. **Adopt-back (deferred).** Register the cav2 import surface (L3, not MVP).

**Disclosed non-seeds (Tier 3, decision 2026-07-01 — do NOT emit; record as disclosed decisions):** the
ontology/artifact package (cav2's self-model — seeding re-fuses levels), the disciplines catalog, the
attestation seal (owner: `attestation-capability`), adopt-back.
</process>

<gates>
- **D49 owner-gate:** Mint PROPOSES kinds; the cav2 authority owner RATIFIES. Never unilaterally alter cav2's closed D49 enumeration.
- **Public/private (`BLK-CAV2-PUBLIC-PRIVATE-001`):** a public-attached mint is BLOCKED until resolved.
- **Signer capability (L2):** stage-3's signed record depends on the attestation/signer capability
  (`cyberAlchemy-v2/development/attestation-capability/`, L2-blocked); until then it is an L0-attributional
  placeholder, disclosed.
- **claim ≤ proof:** Mint is intended-not-shipped, one casting organ — never assume the foundry / Saturn / moat is shipped.
- **Non-executed:** the emit-logic (templates + `EMIT-PROCEDURE.md`) is BUILT and validated on the worked example (`examples/`), but no live mint has run — SURVIVED/FALSIFIED are rendered only by the downstream N=3 run. Emit-templates are validated on ONE domain (resonantos); generalization is a named risk, not proven coverage.
</gates>

<inheritance-boundary>
**Inherit the MOLD (how authority is made):** authority-lifecycle `CAV2-D48` + its `stop_rule`; the closure
**rule** `CAV2-D49` applied to the domain's OWN table; non-collapse (D22/D29); claim ≤ proof (D38);
build-from-owned (C17); promotion-policy structure + source-movement + the Authority-Kinds-table **format**;
narrowest-owner routing; invariant→axiom derivation; DEFINITION-LOCALIZATION-ROUTE; the definitions-lifecycle
equipment *as machinery*.
**Localize the CASTING (what this domain holds):** the domain's own kind rows, definitions, constitution
rules, source families, decisions.
**Boundary test:** defines HOW authority is made → inherit; WHAT authority the domain holds → localize.
**Circularity guardrail (machine-map `two-system-5s-recursion-boundary`):** never inherit cav2's OBJECT
kinds/rows as a governing base — the mold becomes a casting of itself. Audit-confirmed 2026-07-01 for the
ontology/artifact package.
</inheritance-boundary>

<quality-bar>
- the minted tree resolves clone-safe (scaffolder Step-7 verify);
- the emitted authority-model parses; every proposed kind carries a default-deny row;
- no minted kind is left `PROPOSED` after stage 3 (ratify-CLOSE ran) [#11];
- the seeded load-bearing-term rule resolves against an emitted `DRIFT-AUDIT` target [#8];
- seed-format additions carry the empty contract, with **zero cav2 rows copied** [guardrail];
- Tier-3 non-seeds are disclosed, not silent;
- claim ≤ proof throughout; no public-attached mint; no edits to `domainspec-new-repo` or cav2 machinery.
</quality-bar>

<anti-patterns>
- inheriting cav2's object kind rows as the domain's governing base (level re-fusion);
- leaving proposed kinds un-ratified (`PROPOSED` forever);
- emitting a seeded constitution rule whose enforcement target isn't emitted (fires into a void);
- copying cav2's populated posture / non-collapse / constitution ROWS instead of the empty format;
- emitting a public-attached mint while `BLK-CAV2-PUBLIC-PRIVATE-001` is open;
- editing `domainspec-new-repo` instead of composing it;
- claiming the foundry / moat is shipped.
</anti-patterns>

<output-contract>
Return:
- minted repo path + attach mode + clone-safe verify result;
- emitted spine files (authority-model, source-spine, promotion-policy, constitution, definitions + additions);
- proposed kinds + ratification status (`PROPOSED` / ratified) + signed decision path;
- crosswalk path;
- disclosed non-seeds (Tier 3);
- open gates (public/private, signer-capability) + next route.
</output-contract>

<origin>
Authored by `sigil-development --new` (2026-07-01) from the `cyberAlchemy-v2/development/mint/` invoke package
(SPEC / ARCHITECTURE-BUNDLE / EXECUTION-PACK / WORK-PACK / IMPLEMENTATION-LAYERING / HANDOFF), which carries
the 2026-07-01 inheritance-audit additions (`development/research/2026-07-01-mint-cav2-inheritance-audit/`
+ `development/decisions/2026-07-01-mint-additions-scope.md`). Precedent (hand-done): resonantos-economy-research.
</origin>
