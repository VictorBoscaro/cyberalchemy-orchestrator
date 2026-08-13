---
node_type: agent-dialogue
status: awaiting-human-gate
date: 2026-08-13
topic: Evolving write-need-driven-documents through independent investigation, reviewed findings, and zig-zag validation
---

# Robot-Talks: need-driven writing skill evolution

## Scope

Evaluate and strengthen `.codex/skills/write-need-driven-documents/SKILL.md` without turning it
into a general style manual. Preserve its central responsibility: conducting an intelligent reader
from available understanding to a new understanding, judgment, or decision.

## Central question

Does the skill reliably produce clear, subtle, progressive essays - especially autonomous
documents that gain meaning when read in sequence - or does it only describe good writing
principles?

## Assumptions challenged

- Good principles are sufficient to change writing behavior.
- The current opening guidance is specific enough.
- Simplicity and clarity preserve voice without additional guidance.
- The final-read procedure can detect artificial progression.
- A document can stand alone and belong to a sequence without an explicit composition rule.

## Chosen decomposition

Two independent investigators examine different concerns before direct confrontation:

1. reader movement, openings, progression, sequence, endings, voice, and revision behavior;
2. skill routing, scope, degrees of freedom, failure modes, packaging, and validation.

After their reports, each receives the other's report and must challenge claims rather than merge
summaries. The parent synthesizes only evidence-backed tensions into `findings.md`. A fresh reviewer
then verifies and may correct those findings before any editor consumes them.

## Rejected decomposition

A writer and illustrator-style split, or four parallel reviewers, was rejected. It would divide the
artifact by output surface rather than concern, and it would let later reviewers inspect different
or unfrozen versions. The selected sequence preserves independence and causal traceability.

## Agent prompts and skills

### Investigator 01 - reader movement

Primary skill: `write-need-driven-documents`.

Inspect the current skill as a behavioral contract for reader-facing conceptual essays. Test its
guidance against the supplied Part II opening problem and the existing short essay. Focus on what a
writer can actually do, not on compiling a generic style guide. Write
`reports/01-reader-movement.md` using the Robot-Talks report shape. Do not edit the target skill or
read the other investigator's report before submitting your own.

### Investigator 02 - skill engineering

Primary skills: `create-skill` and `skill-creator`.

Inspect the current skill as an invocable skill package. Evaluate routing, coherent scope,
instruction density, degrees of freedom, typical errors, progressive disclosure, metadata,
validation, and forward-testing. Write `reports/02-skill-engineering.md` using the Robot-Talks
report shape. Do not edit the target skill or read the other investigator's report before
submitting your own.

## Planned downstream sequence

1. Cross-challenge between the two investigators under `ring/`.
2. Parent synthesis into `findings.md`.
3. Fresh findings reviewer verifies and corrects `findings.md` when evidence requires it.
4. Editor consumes only the reviewed findings and updates the skill package.
5. The same editor alternates with three fresh reviewers:
   reader movement, routing/scope, then skill packaging/validation.
6. Human gate classifies residual findings as actionable, deferred, misinterpretation, or uncertain.

## Conversation protocol

- Independent reports precede all cross-agent exposure.
- Claims require file and line evidence.
- Cross-challenges must name agreement, disagreement, attempted refutation, and surviving change.
- Reviewers do not edit the target; only the designated editor does.
- Every editor revision precedes the next reviewer, producing one frozen version per review.

## Exploration update

Both investigators completed independent reports before exposure to the other. Their cross-challenge
converged on five bounded behavioral changes: opening specificity, reader-state transitions,
transformation-based closure, conditional sequential autonomy, and structural diagnosis before
revising. They also converged on rebalancing existing examples instead of growing a general style
manual. Separate tensions remain around package evidence location and the distinction between review
and blind behavioral validation.

## Synthesis update

The parent synthesized eight candidate findings in `findings.md`. F1-F5 bound the proposed edit; F6
records a likely no-change routing decision; F7 defers evidence relocation until the dialogue closes;
F8 limits the claims available without blind forward-testing. A fresh findings reviewer must verify
and may correct the artifact before editing begins.

## Findings review update

A fresh reviewer checked the full evidence chain and revised `findings.md` to status `reviewed`.
The reviewer combined the three movement boundaries under F1, kept sequential autonomy conditional,
regraded restructuring to moderate, rejected a standalone voice expansion, converted example
rebalancing into an edit constraint, preserved routing, deferred evidence location to the human gate,
and limited behavioral claims without blind forward-tests.

## Editing and zig-zag update

The designated editor consumed only reviewed findings and updated both runtime mirrors. The first
reviewer returned `REVISE`: the transition test wrongly required novelty rather than deepening, and
the sequence rule wrongly privileged a new question over other forms of movement. The editor
accepted both findings and corrected them. The routing reviewer then returned `ACCEPT`, and the
editor recorded the no-change consumption. The package reviewer accepted the runtime contract but
returned `REVISE` on the unresolved distribution boundary; the editor correctly classified that
finding as `HUMAN_GATE` and changed no runtime or evidence file.

Final runtime digests:

- `SKILL.md`: `59B70A04856F8D2695C0980FA3270ECAD6348A661FD1B8CEABEEBD81B0ECE166`
- `agents/openai.yaml`: `6CDCFCFC89F0EF021C9FC933265BB0206CD8D89592B46DA9094ACACF2573D4DC`

Both `.codex` and `.agents` runtime mirrors pass `quick_validate.py`, are byte-identical by file,
and pass `git diff --check`.

## Human gate pending

1. **F7 / package boundary:** define the distributable skill as the two runtime files
   (`SKILL.md` and `agents/openai.yaml`), or separately authorize an atomic migration of this
   Robot-Talks record to a different owning context. No migration is currently authorized.
2. **F8 / behavioral claim:** run blind forward-tests before claiming that the revision reliably
   improves essay output, or defer them and retain the narrower claim that the reviewed contract
   addresses the identified failure modes.
