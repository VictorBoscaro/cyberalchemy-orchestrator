---
artifact_kind: bounded-owner-map-advice
track: external-composition-precedents
unit: engineered-systems-owner-map
status: ready-for-bounded-collection
date: 2026-08-13
authority: procedural-only
---

# Advisor — engineered systems owner-map

## Boundary and purpose

This artifact specifies one bounded, read-only external collection task. It is not a governed
`research` dispatch, does not produce a canonical candidate matrix or verdict, and does not answer
the Composition Lab's general question. Its only output is an evidence-preserving owner-map for an
engineered domain.

## Operational question

Which owned accounts in software architecture, systems/component design, workflow or dataflow,
and end-user composition define a composition operation through interfaces, contracts, closure,
or substitution; what conditions and observable obligations make that operation valid; and how
does each account distinguish composition from integration, configuration, orchestration, mere
connection, or aggregation?

The collector must report what each source itself licenses. Shared vocabulary across sources is
not evidence of a shared mechanism.

## Permitted corpus

Use exactly **5–7 anchors**, all primary or official and accessible through effective web use.
The bounded corpus must cover these slots:

1. at least one primary work by the named originator of an explicit software modularity or
   information-hiding account;
2. at least one official component-model, module-system, or architecture specification;
3. at least one primary paper or official specification for workflow, process, or dataflow
   composition;
4. at least one primary paper or official specification for end-user composition, mashups, visual
   composition, or an equivalent user-facing composition mechanism;
5. at least one primary or official source whose purpose or content exposes a boundary, invalid
   composition, incompatibility, failure mode, or limit.

One anchor may satisfy more than one slot, but the final set must contain evidence from at least
three of the four substantive surfaces above. Permitted source classes are original peer-reviewed
papers, original scholarly books or chapters by the account's owner, standards, specifications,
institutional publications, and official technical documentation that defines normative behavior.
Reviews and handbooks may be used only to navigate toward anchors and must not appear as evidentiary
anchors.

## Inclusion and exclusion

Include an account only when the anchor supplies all of the following:

- an identifiable owner or issuing authority;
- an explicit operation, construction, or rule by which parts are combined;
- an interface, contract, type, protocol, port, connector, or equivalent boundary condition;
- at least one observable validity obligation, invariant, closure property, substitution rule, or
  failure condition;
- enough source text to distinguish the operation from at least one neighboring phenomenon.

Exclude:

- dictionaries, encyclopedic summaries, unsourced explainers, vendor thought pieces, blogs, and
  marketing material;
- surveys or handbooks used as final evidence;
- sources that use “composition” only metaphorically or as an unexplained label;
- accounts supported only by an implementation example without a stated rule or obligation;
- sources whose stable bibliographic identity, official status, or relevant passage cannot be
  verified;
- any source selected because it resembles the repository's current vocabulary or design.

## Required record for every admitted account

Record each account separately, preserving source boundaries. Every entry must contain:

- **owner and citation:** exact owner/authority, title, date/version, stable URL or identifier, and
  access date;
- **interface:** the boundary or contact surface through which parts participate;
- **contracts:** explicit guarantees, assumptions, protocols, types, obligations, or compatibility
  rules;
- **conditions:** prerequisites for the composition operation to be defined or valid;
- **operation:** what is done to the parts, stated in the source's own technical terms;
- **preservation:** identities, properties, invariants, behavior, or substitutability the source
  claims are retained, including “not specified” when absent;
- **emergence:** behavior or capability attributed to the composed result but not to an isolated
  part, only when the source supports that attribution; otherwise “not claimed”;
- **failures:** invalid combinations, broken obligations, interference, mismatch, non-closure, or
  other stated failure/boundary cases;
- **neighbor distinction:** the evidenced difference from integration, configuration,
  orchestration, connection, aggregation, or another nearby operation;
- **limits:** scope conditions and matters the account does not explain;
- **transfer risk:** what would have to be true to use this distinction for skills, interfaces,
  artifacts, knowledge, work, agents, or lenses, and why that transfer may fail;
- **evidence:** a pinpoint quotation or faithful paraphrase tied to a precise page, section, clause,
  or documentation heading.

Do not fill absent fields by inference. Mark them `not specified by source` and preserve the gap.

## Isolation rules

- Do not inspect or cite the internal-composition corpus, its findings, Inventory cards, repository
  implementation, or `domainspec-v2`.
- Do not inspect or cite the sibling formal/structural owner-map or borrow its vocabulary,
  candidates, sources, inclusion decisions, or findings.
- Do not compare domains, propose a unified account, define composition generally, rank theories,
  or recommend architecture, runtime, governance, interface, or product changes.
- Do not emit canonical precedent/non-vacuity/soundness verdicts, GO/KILL decisions, a candidate
  matrix, `research.md`, or `findings.md`.
- Treat `interface`, `contract`, `closure`, and `substitution` as search surfaces, not predetermined
  necessary or sufficient conditions of composition.

## Verifiable researcher instructions

1. Before collecting, create a source/search log listing every query, candidate URL, inclusion or
   exclusion decision, decision reason, and final anchor count.
2. Confirm effective web access by opening and reading every admitted anchor. If web access is not
   effective, stop with `BLOCK`; do not substitute memory.
3. Keep the final evidence corpus to exactly 5–7 anchors and satisfy every corpus slot and the
   three-surface minimum.
4. For each anchor, verify owner/authority, stable identity, primary/official status, and the
   pinpoint supporting each required field.
5. Separate source claims from collector inference. Label any minimal inference explicitly and do
   not use it to satisfy an admission criterion.
6. Include at least one admitted boundary/failure source and at least one concrete failure or
   invalidity case in the map.
7. Write only `owner-map.md` in this run folder. Do not edit this advice, other research artifacts,
   the repository source tree, or governance/telemetry files.
8. End `owner-map.md` with a checklist reporting corpus count, surface coverage, required-field
   completeness, unresolved gaps, and files written.

## Review criteria

The later bounded review may PASS only if all are true:

- the only research output is `owner-map.md` in the authorized folder;
- the source/search log is complete and reproducible;
- there are exactly 5–7 admitted primary/official anchors;
- all required corpus slots are met and at least three substantive surfaces are represented;
- every account passes every admission condition;
- every required field is present, evidenced or explicitly marked absent, with pinpoint support;
- at least one source and one mapped case expose a boundary or failure;
- neighboring phenomena are distinguished using source evidence rather than assertion;
- source claims, collector inferences, and transfer risks are visibly separated;
- no forbidden internal corpus, sibling formal work, cross-domain synthesis, general definition,
  canonical verdict, or design recommendation appears;
- citations and stable identifiers resolve to the claimed source and ownership.

Review must return **BLOCK** if any condition above fails, if web use was ineffective or
unverifiable, if the corpus exceeds or falls below the bound, if a required field is silently
invented, or if source boundaries are collapsed. BLOCK also applies when contamination prevents
the engineered map from being independently evaluated. The reviewer may request a bounded repair;
it may not repair evidence, add sources, or synthesize findings itself.

