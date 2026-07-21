---
tags: [meta-ontology, sources, import-manifest, domainspec-core, cyberalchemy-v2]
node_type: conceptual
is_session: false
layer: ontology
nature: reference
status: exploratory
version: 0.1.0
last_updated: 2026-07-21
---

# meta-ontology `M` — source leads

> Cross-repo leads to mine when the meta-ontology work is prioritized. Verdict vocabulary borrowed
> from domainspec-v2's `IMPORT-MANIFEST`: **borrow** (import + reformulate), **analogy** (study the
> shape, don't import), **block** (anti-pattern to unify away), **promote-candidate** (import-then-
> promote through a gate). All paths are in the sibling repo `../../../domainspec-core/`. Produced
> by two read-only sweeps (see [SEED.md](SEED.md) for dispatch ids). `Claim ≤ proof`: most of this
> machinery is **candidate / declared**, not enforced — the `State` column says which.

## Sweep A — canonical-kinds / cav2 authority spine

| # | Source (under `domainspec-core/`) | Provides | Stratum | Verdict | State |
|---|---|---|---|---|---|
| A1 | `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` | ~22 carrier-kinds (Tier-1) rolling up to Tier-2 authority-kinds; Kind Contract; `durability` axis; 14 OQs | Documents (ii) | promote-candidate | candidate, "uncited" |
| A2 | `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` | closed Tier-2 authority-kind table, default-deny catch-all, Narrowest-Owner, `invariant→axiom→constitution→gate` chain | Governance (iii) | borrow | review-enforced |
| A3 | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` | **the meta-level**: D48 lifecycle (reflexive parent), D49 closure, D51 canonical-artifact tuple, D40 challenge contract, D23 veracity⊥conviction | Governance (iii) | borrow | declared |
| A4 | `projects/domainspec-v2/definitions/meta-types/meta-types.md` | DS-D1 node meta-types + `.schema.yml` criteria + Challenge/Confirm contracts | Domain (i) | analogy / borrow | **built + enforced** (13 backend) |
| A5 | `implementation/domainspec/vault/ontology-conventions.md` | the **fused** 16-value `node_type` (carrier ⊕ epistemic-role); veracity/conviction/status label design | (ii)⊕(iii) fusion | **block** (counter-example for BL-2) | active (legacy) |
| A6 | `cyberAlchemy-v2/authority/definitions/DEFINITION-TOWERS.md` | altitude/tower scaffolding T-1…T6, promotion queues Q1…Q6 | Governance (iii) | analogy | declared |
| A7 | `cyberAlchemy-v2/authority/promotion-policy.md` (+ domainspec-v2's) | 7-rung promotion ladder + required gates | Governance (iii) | borrow | declared |
| A8 | `authority/decisions/2026-07-13-canonical-kind-one-label.md` | the in-flight **de-fusion** (split `canonical_kind` from `node_type`, role→edges) | (ii)/(iii) split | borrow (aligns BL-2) | decided |

## Sweep B — ledger / event-record machinery

| # | Source (under `domainspec-core/`) | Provides | Stratum | Verdict | State |
|---|---|---|---|---|---|
| B1 | `.claude/skills/register-dispatch/append-dispatch.cjs` | authoritative dispatch/close schema v0.6.0 + validation + append/close discipline | Trace (iv) | borrow (discipline) | **enforced** |
| B2 | `.claude/skills/craft/templates/schemas/ledger-core.schema.yml` | the only true **id+type+payload envelope with a growing family alphabet** (names unbuilt families) | Trace (iv) envelope | **borrow (v-next template)** | declared, no validator |
| B3 | `internal_tools/subagents-dispatch-hooks/hooks/enforce-append-only-dispatch.cjs` | path-canonicalizing append-only deny-hook (fail-open) | Trace (iv) | borrow | enforced |
| B4 | `.claude/skills/dispatch-spec/dispatch.schema.yml` | richest event vocab: `frame\|decision\|ledger\|artifact\|handoff\|trace_event\|receipt`, `subagent_lifecycle`, `receipts[]` | Trace (iv) alphabet | analogy | declared |
| B5 | `telemetry/agents/subagents-dispatch.yaml` | the live trace (enum holds; clean to 2026-07-15) | Trace (iv) | analogy | live |
| B6 | `arcanum/.craft/ledger.yml` (+ `index.json` `trace_events`) | Craft-as-live-authority; a flat `trace_events` string list (not typed) | Trace (iv) | analogy | live |
| B7 | `projects/domainspec-v2/development/**/DECISION-LEDGER.md` + `GAP-LEDGER.md` | bespoke hand-edited decision/gap tables, zero enforcement | (iii) records | **block** (anti-pattern to unify) | unenforced |
| B8 | `projects/domainspec-v2/impl/test-derivation-engine/src/residue/receipt.ts` | `ResidueReceipt` (`format_version:1`) — the "receipt" entry-kind as real code | Trace (iv) receipt | analogy | built |

## The three weaknesses a v-next must fix (from Sweep B synthesis)

1. **Closed 2-kind alphabet welded into one script** (System A can only say `dispatch`/`close`).
   → id+type+payload envelope with an open, schema-declared alphabet (B2 shows how).
2. **Four disjoint identity spaces, no cross-links** (`dispatch_id`, `DEC-*`, `GAP-*`, receipts,
   Craft ids). → one shared namespace + a `relations`-style typed link table = **the provenance
   spine the owner requires** (assertion → generating dispatch/research → trail).
3. **Append-only vs mutable inconsistency + no `supersede`** (only System A is truly append-only;
   Craft edits in place, losing history). → one immutability policy (append + `supersede`) with a
   single validating writer.
