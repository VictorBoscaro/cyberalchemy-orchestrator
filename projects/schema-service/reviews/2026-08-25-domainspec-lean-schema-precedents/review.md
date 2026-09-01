# Review — DomainSpec Lean schema precedents

## Coverage

The frozen corpus is the 11-path/hash manifest at
`.codex/workflow-inputs/2026-08-25-domainspec-lean-schema-precedents-review/targets.json`.
All 11 hashes matched before review, and every target was read in full under both declared attack
lenses. No target was modified and no repair was applied during this dispatch.

This review ran in **degraded orchestration mode**. The workflow compiler could not express the
canonical sequential/zig-zag handoffs because the required handoff receipts were unavailable, so
the two attackers and the verifier ran independently over the full frozen corpus. The parent then
performed the missing literal reconciliation. This preserves independent attack coverage, but it
reduces confidence in process provenance compared with the canonical review graph.

| attacker/check | lens | target coverage | findings raised | zero-findings defence |
| --- | --- | --- | --- | --- |
| Booch | fidelity / governance | 11/11 | 5 candidates | n/a |
| Liskov | ownership / reference integrity | 11/11 | 4 candidates | n/a |
| Dijkstra | independent literal verification | 11/11 | 3 documentary contradictions; no load-bearing conclusion refuted | n/a |
| Parent reconciliation | cross-check against frozen targets and governing verdict contract | 11/11 | 7 findings survived | n/a |

The following candidates were dropped after literal reconciliation: H1 was not presented as proof
of sufficiency because `findings.md` explicitly retains it as a baseline with collapse-tests; the
`KILL` verdicts do not permanently prohibit multilevel mechanisms; the corpus does not prohibit
`type`, `objective`, or `tags` individually; and the minimal diagram does not finally select the
meta-validation carrier because its report still targets an exact but unresolved tuple. A proposed
requirement to embed agent identity and the sibling repository commit in every report was also
dropped because no governing requirement for it was established.

## `research-initial-definitions.md`

No surviving finding. It keeps `skill-first`, separates confirmed constraints from evidence and
gaps, and leaves serialization, the universal envelope, relation semantics, and closure open.

**Verdict:** KEEP

## `research.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R1 | `projects/schema-service/research/domainspec-lean-schema-precedents/research.md` | Line 10 says, “The following three returns are preserved verbatim from the independent explorer seats.” Line 21 instead begins “O repositÃ³rio sustenta com forÃ§a...”, while the corresponding report begins “O repositório sustenta com força...”. None of the three standalone reports occurs exactly in the aggregate. | MAJOR | Regenerate `research.md` by encoding-safe UTF-8 concatenation of the three report bodies, verify exact equality, and then refresh the frozen hash. |

**Verdict:** FIX

## `findings.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R2 | `projects/schema-service/research/domainspec-lean-schema-precedents/findings.md` | Lines 34–35 use the verdict “**GO condicionado**”, including “ainda não como implementação local completa”. The governed matrix admits only `GO` for witnessed-and-sound candidates or typed `KILL`; a future condition cannot be encoded as a third verdict. | MAJOR | Split each row into the witnessed claim, which may receive `GO`, and any stronger unwitnessed local claim, which receives typed `KILL — no-witness`; retain reopening conditions outside the verdict cell. |
| R3 | `projects/schema-service/research/domainspec-lean-schema-precedents/findings.md` | Lines 21–25 state absolutely, “Ele não implementa o `MetaSchema`, a `SchemaDefinitionRevision`, o `ManifestRevision` ou a torre reflexiva”, while lines 106–109 later delimit the repository and literature checks. | MINOR | Replace the absolute wording with “não foi encontrada, na busca/corpus delimitado, uma implementação correspondente”. |

**Verdict:** FIX

## `reports/01-schema-metaschema.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R4 | `projects/schema-service/research/domainspec-lean-schema-precedents/reports/01-schema-metaschema.md` | Line 312 says, “Falta tipar qual representação da `SchemaDefinitionRevision` é validada pelo MetaSchema; o `Type` semântico, a revisão, o effective schema e seus bytes não são o mesmo objeto.” Line 334 nevertheless fixes the witness as “validates bytes of SkillSchemaDefinitionRevision@0”. | MAJOR | Replace `bytes` with an explicit unresolved meta-validation-target candidate set or tuple; select bytes only after a discriminating fixture and criterion. |

**Verdict:** FIX

## `reports/02-artifact-representation.md`

No surviving finding. It preserves the evidence boundary, distinguishes capability, package,
installation, invocation, tool, and receipt, and does not promote the sibling precedents to a
universal Schema Service lifecycle.

**Verdict:** KEEP

## `reports/03-literature-multilevel-metamodeling.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R5 | `projects/schema-service/research/domainspec-lean-schema-precedents/reports/03-literature-multilevel-metamodeling.md` | Lines 277–283 use “**GO / build-from-owned condicionado a witness**”, another conditioned `GO`, plus `DEFER` and “não estabelecido” as verdict-like outcomes. These do not satisfy the governed terminal `GO`/typed-`KILL` contract. | MAJOR | Rewrite the conclusion as explicit candidate rows: `GO` only for witnessed-and-sound structural precedents and typed `KILL — no-witness` for stronger local-necessity claims; keep future reopening notes outside the verdict. |

**Verdict:** FIX

## `robot-talks/.../dialogue.md`

No surviving finding. The dialogue is in the correct nested research folder, preserves the human
gate, links correctly to the revised research context, and records dispositions without silently
changing the Schema Service contract.

**Verdict:** KEEP

## `robot-talks/.../findings.md`

No surviving finding. It keeps relative roles together with governed kinds, denies transitivity,
and preserves `skill-first`.

**Verdict:** KEEP

## `robot-talks/.../reports/01-formal-soundness.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R6 | `projects/schema-service/research/domainspec-lean-schema-precedents/robot-talks/2026-08-25-relational-metaschema-research-design/reports/01-formal-soundness.md` | Line 7 points to “`projects/schema-service/robot-talks/2026-08-25-relational-metaschema-research-design/dialogue.md`”, which is not the persisted location. | MINOR | Point to the actual nested research path, preferably with a relative link. |

**Verdict:** KEEP

## `robot-talks/.../reports/02-operational-architecture.md`

No surviving finding. It explicitly preserves the unresolved artifact/manifest/representation
carrier question and separates validation, publication, and enforcement.

**Verdict:** KEEP

## `robot-talks/.../reports/03-evidence-framing.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
| --- | --- | --- | --- | --- |
| R7 | `projects/schema-service/research/domainspec-lean-schema-precedents/robot-talks/2026-08-25-relational-metaschema-research-design/reports/03-evidence-framing.md` | Line 11 cites `research-initial-definitions.md:18-21` for wording no longer present there; line 25 cites `:54-58` for the prior `type`/`objective_ref`/`tags` passage; line 34 cites `dialogue.md:59-69` for a relation list no longer present at those lines. | MINOR | Mark these as pre-revision citations and preserve/hash the revisions actually read, or update the pointers against the final targets without changing the arguments. |

**Verdict:** KEEP

## Change requests

1. **MAJOR — R1:** restore byte/text fidelity of the supposedly verbatim `research.md` aggregate.
2. **MAJOR — R2:** replace `GO condicionado` in `findings.md` with governed, claim-split `GO` or typed `KILL` outcomes.
3. **MAJOR — R4:** reopen the exact carrier of meta-validation instead of prematurely selecting bytes.
4. **MAJOR — R5:** normalize the literature report's conclusion to the governed research verdict contract.
5. **MINOR — R3:** bound the executive negative claim about the sibling repository to the searched corpus.
6. **MINOR — R6:** repair the stale Robot-Talks dialogue path.
7. **MINOR — R7:** repair or revision-bind the stale pre-synthesis line references.

## Dispatch record

- output mode: persisted
- agents spawned: 4 planned/executed seats (2 attackers, 1 verifier, 1 dedicated final approver)
- exit reason: resolved — dedicated final approver returned `APPROVE`
