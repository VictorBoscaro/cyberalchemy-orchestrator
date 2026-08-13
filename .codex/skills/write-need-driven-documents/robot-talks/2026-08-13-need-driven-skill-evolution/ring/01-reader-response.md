# Cross-challenge 01 — Reader movement response

## 1. Conservative package routing versus mandatory repository routing

**Position: partial disagreement.** The engineering report is right that behavior differs by
environment, but I do not accept that this is inherently an unresolved contract. The package says
to use the skill “explicitly and sparingly”
(`.codex/skills/write-need-driven-documents/SKILL.md:2-3`) and disables implicit invocation
(`.codex/skills/write-need-driven-documents/agents/openai.yaml:4-7`). The repository then makes one
artifact-based route explicit and mandatory (`AGENTS.md:13-18`). Those rules can compose cleanly:
the package does not trigger itself opportunistically, while the repository deliberately routes a
narrow class of work to it.

**Attempted refutation.** If the two authorities truly conflicted, the repository would either
require an excluded artifact or bypass the skill's scope. It does neither: its positive route and
exclusions substantially repeat the package boundary (`AGENTS.md:15-18`; `.codex/skills/write-need-driven-documents/SKILL.md:2-3`).
Environment-dependent invocation is expected when a repository supplies local routing policy; it
does not by itself imply stale metadata.

**Impact on my recommendations.** I withdraw any implication that the skill package needs broader
implicit routing in order to solve the Part II failure. Invocation and writing quality are separate
questions here.

**Minimum surviving change.** Make an explicit decision that `allow_implicit_invocation: false` is
intentional and retain `AGENTS.md` as the repository-local router. Change metadata only if the
desired product behavior is automatic use outside this repository; no evidence currently
establishes that objective.

## 2. High freedom versus reliable openings

**Position: agreement.** The engineering report independently confirms my central finding: the
skill has the right abstraction level but lacks a discriminating operation at the opening and
ending surfaces. “Begin with something the reader can recognize” permits both a perceptible
situation and a generic universal claim (`.codex/skills/write-need-driven-documents/SKILL.md:22-25`).

**Attempted refutation.** The strongest defense of the current text is that the opening sentence,
the instruction to delay names, and the final-read correspondence jointly give a capable writer
enough judgment (`.codex/skills/write-need-driven-documents/SKILL.md:22-25,94-100`). The existing
essay does produce a strong causal movement from emerging distinctions to reduced global visibility
and then to system need
(`plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md:43-48,74-88`).
But that success does not show the rule is discriminating: the same contract also accepts the
essay's highly general first claim
(`plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md:21-24`), while
the investigation was created specifically because the supplied Part II opening exposed this
failure surface
(`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:24-28,53-55`).
Writer skill, not the instruction, may explain the successful passages.

**Impact on my recommendations.** I retain the opening and transition tests, but narrow them to
failure detection. The skill should not prescribe anecdotes, questions, concrete scenes, or any
single rhetorical form.

**Minimum surviving change.** Add an interchangeability test for openings and one reader-state test
for passage transitions: if the opening could begin many unrelated essays, or if a passage can move
without changing what the reader can next understand or ask, revise the movement.

## 3. Coverage versus growth: rebalance examples before enlarging the skill

**Position: agreement, with a limit.** The engineering report correctly observes that three of four
negative examples spend substantial space on the relation-versus-collection family
(`.codex/skills/write-need-driven-documents/SKILL.md:59-85`). The missing behaviors should not simply
be appended as a new style manual.

**Attempted refutation.** The examples are not fully redundant. A catalogue of actions, co-present
domain objects, and premature terminology fail differently: one hides causality, one asserts
composition, and one transfers decoding work
(`.codex/skills/write-need-driven-documents/SKILL.md:61-85`). Removing all but one would weaken
the skill's defining relational insight. The fourth example also protects against layout being used
as explanation (`.codex/skills/write-need-driven-documents/SKILL.md:87-92`), which is a distinct and
useful failure.

**Impact on my recommendations.** I no longer recommend adding separate examples for opening,
ending, voice, and revision. Tests are more compact and less likely to create stylistic templates.
Voice should remain attached to movement, not receive its own example.

**Minimum surviving change.** Compress or merge the catalogue and co-presence examples while
preserving both failure distinctions. Spend the recovered space on compact tests for generic
openings, artificial paragraph progression, sequence-aware autonomy, summary endings, and diagnosis
before restructuring. The net skill should remain near its present size.

## 4. Package purity versus preserved investigation evidence

**Position: agreement on the boundary, disagreement on timing.** Process records are not runtime
instructions. The platform contract explicitly excludes documentation about creation and testing
from a skill package (`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:123-133`). The
Robot-Talks record is explicitly a development and review workflow
(`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:69-85`).
Package purity therefore matters. But moving an active dialogue during the dialogue would invalidate
its registered paths and weaken the evidence chain it is meant to preserve.

**Attempted refutation.** One could argue that only `SKILL.md` and directly referenced resources are
loaded, so nested evidence has no runtime cost. That answers context consumption, not package
semantics: the package directory still contains files that do not directly support skill execution,
contrary to the cited platform rule. Conversely, package purity does not justify deleting evidence;
the repository explicitly values independent checks and preservation of what results support
(`AGENTS.md:22-28`).

**Impact on my recommendations.** This does not change the behavioral edits I proposed, but it adds
a lifecycle constraint: evidence relocation must not be mixed into an active review step or treated
as prose improvement.

**Minimum surviving change.** Preserve the complete Robot-Talks record in place until the dialogue
closes; then relocate the whole record atomically to a repository-owned review/evidence location
outside the distributable skill directory, preserving a stable reference from the governing record.
Do not summarize the process into `SKILL.md` and do not delete the raw evidence.

## 5. Independent review versus blind forward-testing

**Position: full agreement.** The current reviewers inspect the skill with the suspected weaknesses
named in advance (`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:49-67`).
They can validate findings and editorial choices, but they cannot show that the revised instructions
change unaided writing behavior. The platform's forward-test standard requires fresh agents, raw
artifacts, realistic task framing, and no leaked intended fix
(`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:386-416`).

**Attempted refutation.** The planned zig-zag uses frozen versions and fresh reviewers
(`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:69-85`),
which protects causal traceability and may reveal regressions. But reviewers
remain evaluation-aware. Even if one reviewer drafts sample prose, knowledge of the diagnoses would
make that a targeted demonstration rather than a blind transfer test. Mechanical validation is
narrower still: it checks frontmatter, required fields, and naming only
(`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:362-370`).

**Impact on my recommendations.** Claims should be split. The review chain may support “the revised
contract addresses the identified failure modes”; only forward-tests can support “the skill reliably
produces better essays.” My earlier behavioral recommendations remain provisional until that second
claim is tested.

**Minimum surviving change.** After the final reviewed edit, run at least two blind forward-tests:
the raw Part II task and one unrelated conceptual essay that must stand alone while belonging to a
sequence. Give agents the skill and source artifacts, not these reports. Judge whether the opening is
non-interchangeable, each transition changes reader state, the document stands alone without recap,
and the ending changes the reader's understanding of the opening situation.

## 6. Material restructuring as a coherent part of scope

**Position: agreement.** The engineering report questions whether revision should receive explicit
diagnosis or leave the scope. The description already routes material restructuring
(`.codex/skills/write-need-driven-documents/SKILL.md:2-3`), so omitting all revision behavior would
leave the declared scope unsupported.

**Attempted refutation.** Removing restructuring from the description would make the package more
internally uniform and avoid procedural growth. But the existing final read already commands
revision of a failing passage (`.codex/skills/write-need-driven-documents/SKILL.md:94-100`); revision
is therefore not foreign to the body.
The real gap is that a route-level failure may be misdiagnosed as a local passage failure.

**Impact on my recommendations.** I retain diagnosis before rewriting, but reject a separate revision
framework or subsection unless forward-testing shows one sentence is insufficient.

**Minimum surviving change.** Add one conditional instruction: when restructuring an existing draft,
recover its current reader movement and locate the first break before moving or rewriting passages.
