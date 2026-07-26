# Post-change review

Reviewed target SHA-256: `6EFCEEC0F48443B4568BFDA5F0DC37B40E9365E143B03B9C6ED37EBA27201796`  
Remediated target SHA-256: `D3892255E8A81CBA422041EA11780049D1BA4282E589155D4A92B055E29E0E92`  
Review verdict: `FIX`  
Remediation status: all four verified findings applied

## Method

Three reviewers independently inspected the edited essay:

- Forrester: reader progression, redundancy, and complete section inventory;
- Nonaka: knowledge lineage, acceptance, history, graph views, projections, and witnesses;
- Liskov: reference integrity, system-view altitude, and ACI/APT correspondence.

The parent synthesized four data-only candidates. Parnas checked their exact quotations, severity, reference support, requested-change coverage, links, section count, and system-view boundaries. All four survived.

## Overall result

The edit materially improved the essay:

- all 38 numbered sections still add distinct information;
- no section should be merged, compressed, moved, or removed;
- the five paths and reading map now orient the reader early;
- graph-family plurality, direct and derived meaning, replayable witnesses, projection non-manufacture, localized drift, terminal evidence, mutation fixtures, and adoption measures are present;
- local references resolve;
- exact schemas, failure codes, mandatory runtime mechanisms, and numerical thresholds remain outside the general narrative.

The reviewed version nevertheless required three conceptual/contract corrections and one copy edit.

## Verified findings and remediation

### P-01 — Minor: duplicated conjunction

The last two section 36 failure cases both ended in `or`.

Remediation: removed the conjunction from the penultimate item.

### P-02 — Major: acceptance boundary absent from the central diagram

The reviewed diagram connected:

> Attributable assertions, decisions, and events  
> durable history

That shape allowed an unaccepted assertion or raw observation to appear as historical truth, conflicting with sections 11–12.

Remediation: the diagram now includes a conceptual review-and-acceptance boundary and distinguishes accepted change from attributable rejection. The prose states that graph views expose facts under a declared acceptance stance. No policy, mechanism, schema, or sufficiency rule was selected.

### P-03 — Major: assignment necessity was decided at system-view altitude

The reviewed version said:

> The assignment bridge is required.

That was a load-bearing necessity verdict despite the essay's proposal-only status.

Remediation: section 35 now frames the explicit assignment bridge as a falsifiable first-slice question. `OD-06 assignment binding` owns the unresolved necessity/sufficiency tension in section 38.

### P-04 — Major: legacy correspondence overstated implementation evidence

The reviewed version said that the runtime records a legacy external-owner reference. ACI and APT specify the ownership and reference variants, but APT's blocked runtime gate does not prove that a runtime or store exists.

Remediation: the paragraph now uses specification language for both variants:

- ACI specifies runtime-managed or legacy-ledger authority ownership;
- APT specifies the corresponding `aci_managed` or `legacy_ledger` reference;
- the paragraph explicitly says these contracts do not prove a runtime exists.

## Redundancy verdict

All numbered sections are `KEEP`.

The recurring five-path vocabulary is functional rather than redundant:

- section 3 states the organizing thesis;
- sections 4–5 explain traversal;
- sections 24–26 explain drift and projections;
- section 35 turns the paths into a candidate vertical slice;
- section 36 turns them into discriminating tests.

Section 21's general evidence ladder remains distinct from section 35's terminal-state/outcome-binding split. Section 29 owns representation shape; section 30 owns derived meaning and witnesses. Sections 37 and 38 remain distinct as broad research questions versus a routed decision inventory.

## Validation after remediation

Parent-side deterministic checks:

- SHA-256: `D3892255E8A81CBA422041EA11780049D1BA4282E589155D4A92B055E29E0E92`;
- exactly 38 numbered sections;
- sequence exactly 1–38;
- all local Markdown targets resolve;
- no `missing-terminal-binding` failure code remains;
- duplicated list conjunction removed;
- `OD-06` is present in the downstream decision inventory.

During subsequent PDF production, the parent corrected the result block from “five” to “six” open
decisions so it agrees with the `OD-01`–`OD-06` inventory. This was a one-word consistency repair;
the PDF was regenerated from the corrected body.

The dispatch used its single confirmed review loop. The four minimal remediations were applied after verification; no claim is made that a second independent agent round reviewed the remediated hash.
