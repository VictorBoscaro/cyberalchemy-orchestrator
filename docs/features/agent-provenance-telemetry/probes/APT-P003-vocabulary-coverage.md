# APT-P003 — Vocabulary coverage and residue

## Claim under test

A system-governed tag registry can normalize a useful portion of isolated runtime topic
language without forcing profile fields, expertise tags, Knowledge Taxonomy facets and open-domain
terms into one authority.

## Vocabulary inputs

The run must pin three independent inputs:

1. **Agent-pool profile snapshot:** each entry's exact `field` and distinct tag strings extracted from
   `telemetry/agents/agent-pool.yaml`. These are separate static profile priors.
2. **Claimed canonical vocabulary:** use only if the referenced artifact actually exists and its bytes
   are pinned. At discovery time, `research/pool-tagging/canonical-vocabulary.md` is referenced by the
   pool header but absent from this workspace; absence is recorded, not repaired by inference.
3. **Knowledge Taxonomy snapshot:** exact version/digest of the facet schema and tagging contract.
   Facets classify a record; they are not synonyms for topical expertise.

## Method

1. Collect raw isolated free emissions from APT-P001 and APT-P002 without changing them. Reserve at
   least four additional eligible fixtures as a held-out coverage set not used to construct the seed
   registry.
2. Apply the pinned registry's deterministic exact/alias resolution. Separately report matches to the
   agent-pool usage snapshot; never treat `field` as a tag match.
3. Evaluate KT facets in a separate projection. Never count a facet value as an exact topical match.
4. Report:

   - registry and pool coverage at three levels: micro by occurrence, unique-term and macro per
     seat/fixture;
   - residue rate at the same three levels;
   - `profile_exclusive_overlap`: profile intersections absent from task text and peer emissions,
     reported as description, not proof of copying;
   - collision list: same string with materially different definitions across sources;
   - unavailable-reference count.

5. In a separate randomized three-period crossover diagnostic, the unit is one
   `seat-model × fixture` pair. Run `profile hidden`, `true profile visible` and `placebo profile
   visible` in randomized order in fresh contexts, with three repetitions per condition and no shared
   provider cache. The primary outcome is the fraction of assisted `selected_tag_ids` overlapping the
   true profile; secondary outcomes are free-term/profile overlap and total term count. Estimate the
   within-unit true-minus-hidden and true-minus-placebo differences with paired uncertainty intervals
   as `profile_exposure_effect`. A carryover or order effect makes the diagnostic unresolved; overlap
   alone never establishes leakage.

## Preregistered decision

- Admit agent-pool tags into the system registry only through a versioned import with definitions and
  provenance. Their use as a runtime lookup aid requires held-out macro median exact usage coverage of
  at least 60%; it never gives the pool authority over runtime observations. The exposure diagnostic
  can constrain whether profiles are shown during capture, but is not a vocabulary-coverage gate.
- Always retain open residue; coverage below 60% forbids a closed-enum runtime payload.
- KT may supply orthogonal facet fields only if every adopted field has a pinned definition and no
  collision with topical tags. Otherwise it remains reference-only.
- A missing claimed canonical artifact blocks claims about its size or completeness, but does not
  block measurement against tags actually present in `agent-pool.yaml`.

## Falsifiers and invalid runs

- Free terms are silently coerced to the nearest known tag.
- Profile tags and observed terms are merged before overlap/exposure measurement.
- KT facets are counted as topical matches.
- A vocabulary is described as canonical without available pinned bytes.

## Output

Vocabulary manifests, stratified exact-match tables, profile-exposure results, residue/collision
registers and a reuse disposition:
`usage-aid`, `candidate-topical-vocabulary`, `facet-reference-only` or `unresolved`.
