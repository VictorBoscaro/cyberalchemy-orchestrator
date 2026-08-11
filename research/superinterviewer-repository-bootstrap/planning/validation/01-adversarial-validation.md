# Adversarial Validation — `research-plan.md`

## Verdict

**FAIL**

The plan has a sound authority split, protected-question discipline, baseline requirement, formalism gate, and branch-level stopping vocabulary. It nevertheless fails its own admission rule in scheduled work, precommits part of the scaffold it says Horizon A must not decide, lacks a discriminating post-experiment gate, and has no explicit completion condition for the product research program. These are repairable planning defects; they do not require redesigning the whole plan.

## Scope

Checked only for:

- thematic research without a consuming decision;
- dependency or review cycles;
- gates that do not discriminate outcomes;
- missing stopping conditions;
- authority contradictions;
- accidental implementation decisions.

Evidence is quoted from the draft under review. The Prompt-Mestre and `planning/inputs/03-plan-adversary.md` were used as governing checks, not as additional plan authorities.

## Findings

### MAJOR 1 — Scheduled workstreams do not satisfy the plan's own branch-admission contract

**Evidence from the plan**

> “A research branch enters the plan only when it declares: 1. the consuming decision and blocking uncertainty; 2. incompatible alternatives [...] 4. a `result → action` table [...] 5. a falsifier or kill criterion [...] 8. dependencies, bounded effort, and stop condition” (§4, lines 77–87).

The plan then schedules topic-shaped work:

> “Active work: WS0, WS1, and WS2.” (§9, line 322)

> “Active work: WS1–WS3 and WS5–WS7; WS4 designs evaluation.” (§9, line 333)

WS0–WS8 describe concerns and outputs, but do not individually name consuming decisions, incompatible alternatives, result-to-action tables, bounded effort, or branch stop conditions (§7, lines 233–285). The distinction between a workstream and a branch does not cure this: the waves activate workstreams without requiring conforming branch records first.

**Impact**

The product program can begin as thematic research despite §4 explicitly forbidding it. An operator can satisfy the wave by producing maps, schemas, glossaries, and threat models without changing a decision.

**Minimum correction**

Add one sentence to each wave gate: no workstream becomes active until one or more scoped branch records satisfy all nine §4 fields. Label WS0–WS8 as topic containers, not executable branches. The plan need not populate every future branch now.

### MAJOR 2 — No gate adjudicates experiment results against the baseline

**Evidence from the plan**

> “Gate B4 authorizes one bounded prototype only when it names a discriminating uncertainty, simple baseline, expected evidence, risks, kill criterion, and discard/revision path.” (§9, lines 349–350)

> “Gate B6 accepts, restricts, reframes, or abandons each principal claim through a human decision.” (§9, line 359)

B4 is a pre-experiment authorization gate. B6 is a human disposition gate. Between them, no gate requires observed results to be compared with the predeclared baseline and threshold, applies the `result → action` table, or assigns an inconclusive outcome. Wave 3 requires experiments to predeclare these elements, but predeclaration is not adjudication.

**Impact**

The experiment can run and the program can reach B6 without a mechanically checkable statement that the result strengthened, weakened, killed, or left the claim unresolved. Human decision can become a non-discriminating substitute for evidence.

**Minimum correction**

Add a post-experiment gate between B4 and B6 requiring: frozen protocol identity, observed baseline comparison, threshold/guardrail result, application of the predeclared result-action table, typed inconclusive outcome, and explicit claim update. B6 may then approve or reject that evidence-backed disposition.

### MAJOR 3 — Horizon A fixes an exact scaffold before demonstrating the promised consumer test

**Evidence from the plan**

> “Horizon A enables Horizon B but may not decide the product model through directory layout, schemas, providers, or governance machinery.” (§5, lines 125–126)

Yet A1 prescribes an exact tree and file set, including:

> “`product/CHARTER.md` [...] `authority/AUTHORITY-MODEL.md` [...] `authority/DEFINITIONS.md` [...] `manifests/sources.yaml` [...] `manifests/dependencies.yaml` [...] `contracts/execution-link.md`” (§6, lines 145–168).

It asserts:

> “Every file must have an immediate consumer.” (§6, line 171)

but the plan supplies no file-to-consumer-to-decision mapping before accepting the plan authorizes package preparation (§1, lines 21–23; §6 A0–A1). A2 checks consumers only after the artifacts have been prepared, when their presence and taxonomy already shape the review.

**Impact**

The layout, authority vocabulary, YAML manifests, and execution-link artifact become de facto defaults without the evidence required by the plan's own anti-freezing discipline. This is architecture-by-document even though no product code is written.

**Minimum correction**

Make the tree explicitly candidate rather than prescribed. Before creating each file, require a small manifest row: immediate consumer, consuming decision, why an existing artifact cannot serve it, binding status, and removal test. A2 should reject files without an approved row; no empty placeholder is created first.

### MAJOR 4 — The product research program has branch stops but no program completion condition

**Evidence from the plan**

The bootstrap has an explicit completion condition:

> “Bootstrap is complete only when the created repository passes validation, has a creation receipt, is explicitly accepted, and the handoff leaves one canonical editable authority.” (§6, lines 225–229)

The product horizon only defines generic branch stopping (§12, lines 405–417), recurring cycle outputs (§13, lines 451–457), and:

> “Gate B6 accepts, restricts, reframes, or abandons each principal claim through a human decision.” (§9, line 359)

“Principal claim” is not tied to a frozen claim register, and B6 is not declared a completion condition. No rule says when Horizon B, a wave, or the founding-research phase is complete rather than merely ready for another cycle.

**Impact**

The program can continue indefinitely by adding claims or reopening cycles, exactly the “Superinterviewer infinito” failure the Prompt-Mestre warns against at product level. Stopping individual branches does not stop the research program.

**Minimum correction**

At B0, freeze a versioned set of principal claims for the founding phase. Define Horizon B completion as: each frozen claim has a B6 disposition; required result-action tables were applied; no blocking branch remains open; residual questions are explicitly deferred with reopen triggers; and the four Prompt-Mestre closing syntheses are emitted. New claims start a new plan version, not an unbounded extension of the same phase.

### MAJOR 5 — A2 contains an unbounded correct-and-review cycle

**Evidence from the plan**

> “Blocking findings are corrected and the frozen package is reviewed again.” (§6, line 192)

No loop ceiling, non-convergence rule, authority for disputed findings, or exit path is defined. The generic research branch stops do not clearly govern a bootstrap review loop, and A3 cannot occur until an accepted manifest exists.

**Impact**

A persistent disagreement or repeatedly introduced blocker can keep repository creation pending indefinitely. Re-freezing after fixes can also change the target faster than the review converges.

**Minimum correction**

Define a bounded review loop: freeze digest → review → correct only accepted blockers → re-freeze. After a small explicit ceiling, unresolved blockers go to a named human disposition that either changes the package, accepts a documented residual, or stops/reframes the bootstrap. Material changes outside accepted blockers require a fresh review cycle, not silent inclusion.

### MINOR 6 — Plan acceptance and final plan ratification are not distinguished as authority events

**Evidence from the plan**

> “Accepting it authorizes preparation of the founding package” (§1, lines 21–23).

> “A0 — Accept this plan” (§6, line 131).

After package review, immediate work says:

> “obtain explicit acceptance of charter, authority model, decision `0001`, and this research plan.” (§14, lines 467–468)

The text plausibly intends two stages—planning authorization and ratification of a transferred/frozen version—but calls both acceptance of “this plan” without version/digest or supersession semantics.

**Impact**

It is unclear which acceptance makes the plan governing, whether the later event supersedes the first, and which version is installed as canonical. This is an authority ambiguity rather than a product-design flaw.

**Minimum correction**

Name the events separately: `planning authorization` for preparing A1, then `founding-plan ratification` for a specified digest/version after A2. State whether ratification supersedes the planning copy and record the pointer in the transfer manifest.

## Passed checks

- The plan explicitly separates charter, context, plan, findings, decisions, and execution signals (§1).
- Accepted Robot-Talks dispositions are treated as decisions with a revisit posture rather than research results (§2).
- The historical corpus is prohibited from validating its own schema (§7 WS0).
- Protected product questions and automatic-promotion prohibition are explicit (§10).
- Formalization is downstream of observable witnesses and does not block empirical research (§7 WS8; §8).
- Source pins distinguish dirty/untracked state from `HEAD`, and external execution success cannot self-promote to accepted evidence (§11).
- Generic branch stopping, splitting, and thesis-level reframing conditions are substantive (§12).

## Required change set for PASS

1. Make WS0–WS8 non-executable topic containers and require §4-complete branch records before wave activation.
2. Add a post-experiment outcome-adjudication gate before B6.
3. Gate each A1 file on an explicit consumer/decision/removal row; mark the shown tree candidate.
4. Define a bounded completion condition for the founding product-research phase.
5. Bound A2 review convergence and name the non-convergence disposition authority.
6. Distinguish initial planning authorization from final plan ratification by version/digest.

No edit to `research-plan.md` was performed by this validation.

## Revalidation

### Verdict

**PASS**

Revalidation was limited to the six findings above. All six minimum corrections are now present in
`research-plan.md`; no new review scope was opened. The original **FAIL** remains above as the audit
record of the first draft, while this section is the current verdict for the corrected draft.

### Finding-by-finding evidence

#### MAJOR 1 — PASS: workstreams are containers gated by conforming branches

The corrected plan now states:

> “WS0–WS8 are topic containers, not executable branches. A wave may activate a workstream only
> through one or more scoped branch records satisfying all nine admission fields in section 4.”
> (§7, lines 267–269)

Wave 1, Wave 2, and Wave 3 repeat the activation constraint (§9, lines 362–363, 374–375, 387–390).
This closes the path by which thematic work could become scheduled execution without a consuming
decision, alternatives, result-action table, bounded effort, and stop condition.

#### MAJOR 2 — PASS: observed experiment results receive a discriminating adjudication gate

The corrected plan adds:

> “Gate B4a adjudicates observed results before any principal-claim decision. It requires the frozen
> protocol identity, observed comparison with the baseline, threshold and guardrail results,
> application of the predeclared `result → action` table, a typed inconclusive outcome when needed,
> and an explicit proposed claim update.” (§9, lines 397–400)

It also prohibits B6 from substituting preference for missing adjudication (§9, lines 400–401).
This supplies the missing post-experiment evidence gate between prototype authorization and human
claim disposition.

#### MAJOR 3 — PASS: the scaffold is candidate and each file is consumer-gated before creation

The corrected A1 requires `TRANSFER-MANIFEST.md` first and says:

> “Before creating any other candidate file, its row must name the immediate consumer, consuming
> decision, why an existing artifact cannot serve it, binding status, and removal test.” (§6,
> lines 148–151)

It further states:

> “The following tree is a candidate package, not a prescribed scaffold” (§6, line 152)

and prohibits creating a file without an accepted row (§6, lines 151–152). The immediate-consumer
test now precedes artifact creation instead of being deferred to package review.

#### MAJOR 4 — PASS: the founding product-research phase has a bounded completion condition

B0 now freezes a versioned register of principal claims and requires new principal claims to start a
new plan version (§9, lines 355–358). The plan then defines completion:

> “The founding product-research phase completes only when every claim frozen at B0 has a B6
> disposition, all required result-action tables have been applied, no blocking branch remains open,
> residual questions are explicitly deferred with reopen triggers” (§9, lines 412–415).

The same condition requires the four closing syntheses and sends new principal claims to a new
versioned phase (§9, lines 414–416). This bounds the founding phase rather than merely stopping
individual branches.

#### MAJOR 5 — PASS: A2 review convergence is bounded and has a named disposition

The corrected plan specifies:

> “Run at most one initial review and two corrective re-reviews.” (§6, line 200)

Only accepted blockers may be corrected inside that loop; other material changes require a fresh,
explicitly authorized cycle (§6, lines 199–201). If blockers remain, the owner must change the
package, accept a documented residual, or stop/reframe the bootstrap (§6, lines 201–202). This closes
the previously unbounded correct-and-review cycle.

#### MINOR 6 — PASS: planning authorization and ratification are distinct authority events

The corrected authority section distinguishes:

> “Its first acceptance is **planning authorization**” (§1, line 21)

from:

> “a separate **founding-plan ratification** [that] must name the accepted version and digest
> installed in the new repository.” (§1, lines 22–24)

It states that ratification supersedes the planning copy and is recorded in the transfer manifest
(§1, lines 23–25), and A2/§15 repeat the version/digest and supersession requirements (§6,
lines 204–206; §15, lines 536–538). The two authority events are now operationally distinct.

### Revalidation close

- Findings rechecked: 6
- Findings resolved: 6
- Findings surviving: 0
- Current verdict: **PASS**
- `research-plan.md` was not edited by this revalidation.
