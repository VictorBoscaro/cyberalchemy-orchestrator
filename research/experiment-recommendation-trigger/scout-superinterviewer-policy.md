# Superinterviewer scout — interaction policy for recommending a test

## Scope and disposition

This is a bounded, read-only extraction from `C:/Users/victo/superinterviewer`. No external literature or independent empirical corpus was examined. The repository contains a proposed product and research foundation, so the result below is a **candidate interaction policy**, not a validated trigger or product authority.

The strongest supported conclusion is negative: **“several research runs and no observed construction” is not, by itself, enough to recommend an experiment**. The corpus supports a suggestion only when a live decision-relevant distinction can be named, an observable result could change a live alternative or next step, and a reversible candidate can produce that result at acceptable burden and risk. Lack of construction may instead reflect deliberate exploration, missing authorization, a world-owned signal that should be retrieved rather than tested, a direct-answer preference, a named reason to wait, or a legitimate decision not to act.

## Authority separation

### Ratified repository authority

The governing repository policy requires claims no stronger than evidence, preserves counterevidence and typed residue, and forbids silently promoting inferred intention, assent, reduced uncertainty, a proposed next step, or execution completion into user intention, consent, benefit, authorized action, or accepted evidence (`C:/Users/victo/superinterviewer/AGENTS.md:3-18`). Consequently, the system may **offer** a test but cannot infer that the person wants experimentation, treat uptake as broad consent, launch the test, or count completion as validation without separate authority and evidence.

### Proposed product and research policy

The product charter is explicitly proposed and unratified. It says the person retains authority to correct, refuse, restore a frame, and decide what follows; direct answer, deferral, branching, and stopping are legitimate outcomes (`product/CHARTER.md:3-24`). Its learning condition requires independent episodes, attributable decision-relevant change, preserved agency, superiority to simpler baselines, and acceptable burden and risk (`product/CHARTER.md:30-32`).

The research plan proposes testing asking, informing, suggesting, reframing, waiting, and advancing rather than assuming their taxonomy or policy is settled (`research/research-plan.md:290-305`). It also requires comparison against direct answers and simpler baselines and permits stopping or reframing when those baselines win (`research/research-plan.md:474-505`). These are research obligations, not evidence that the candidate policy works.

### Internal synthesis

The internal synthesis proposes the source-of-signal rule: ask when the person likely owns the signal; retrieve or test when the world owns it; suggest when a reversible candidate could unlock learning; reframe when representation is the bottleneck. Waiting, silence, direct answer, referral, branching, and stopping remain first-class alternatives (`research/foundation-game-framing/research.md:21-27`). The proposed turn grammar is `prior state → missing distinction → intervention → signal → contestable delta → next step or typed residue`, but it is an observation candidate, not a settled ontology (`research/foundation-game-framing/research.md:5-13`).

### Open residue

No independent corpus, literature review, or controlled comparison has validated the product framing (`research/foundation-game-framing/research-initial-definitions.md:26-41`). The relative weighting of decision relevance, discriminating power, reversibility, burden, privacy, induction risk, and cost is unknown and may vary by person, domain, and risk (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104`). Also unresolved are what observable evidence separates autonomous revision from compliance, when waiting/direct answer/stopping count as success, what constitutes permission to recommend, and who validates an appropriate next step (`research/foundation-game-framing/lanes/03-agency-governance.md:137-152`).

## Candidate constraints for a test suggestion

### Minimum eligibility

A test suggestion is eligible only if all of the following are present:

1. **Live consequence:** at least one plausible result could change a live alternative, next action, safeguard, or stop decision (`docs/game/THINKING-THE-GAME.md:28-32`). “More knowledge” without a named consequence is insufficient.
2. **Named missing distinction:** the proposed test distinguishes something that blocks a choice, understanding, action, test, or legitimate deferral. If that distinction cannot be named prospectively, the system should ask or preserve uncertainty rather than retrospectively invent the test's purpose (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:56-66`; `research/foundation-game-framing/lanes/01-auditable-transition.md:42-50`).
3. **World-owned observable:** the decisive signal is in evidence, comparison, calculation, observation, or the result of action—not merely in the person's unelicited preference or authorization (`docs/game/QUESTION-LANDSCAPE.md:5-19`). If the person owns the signal, ask; if an existing source owns it, retrieve before experimenting.
4. **Recoverable probe:** the candidate is small and reversible, and its assumptions and disconfirming result can be exposed. The local landscape explicitly prefers reversible, low-cost probes when expected value is similar (`docs/game/QUESTION-LANDSCAPE.md:21-29`).
5. **Contestable offer:** identify that it is a proposal, whose proposal it is, what assumptions it makes, what permission it requires, what result would change, and how the person can decline or amend it. Suggestion introduces a candidate commitment and carries anchoring, compliance, and disguised-decision risks (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:69-80`).
6. **Proportionate burden:** among eligible moves, a test should beat asking, retrieving, reframing, waiting, or directly answering on a local ordinal comparison: greater decision relevance, discrimination, answerability, and reversibility; lower cognitive load, time, privacy exposure, induction risk, cost, and irreversibility (`docs/game/THINKING-THE-GAME.md:28-32`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104`).

### Autonomy and authorization boundary

Declared intention, system inference, proposed revision, confirmed revision, operational commitment, and system intervention intent must remain distinct; confirming one does not authorize recommending, executing, remembering, or sharing another (`authority/AUTHORITY-MODEL.md:19-21`). Therefore:

- the ledger may support a system inference such as “research appears to have reached a decision boundary,” but the prompt must expose that inference and invite correction;
- a recommendation should not claim that experimentation is the user's objective merely because research accumulated or construction did not occur;
- accepting the recommendation authorizes neither execution nor persistence unless separately scoped;
- a refusal, correction, request for a direct answer, or silence is a valid counter-move, not failure (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:78-80`).

### Integration after the move

If a suggestion is offered, the interaction should preserve: what changed, what did not, who accepted or contested it, and what remains unresolved. A result may end in a next step or typed residue; execution is not required (`research/foundation-game-framing/lanes/01-auditable-transition.md:93-105`). An observed run proves neither causation nor benefit: acceptance may arise from fatigue, deference, persuasion, or a desire to finish (`research/foundation-game-framing/lanes/01-auditable-transition.md:62-70`).

## Implication for a ledger-based trigger

The ledger should be treated as a **candidate detector**, not a decision maker. A safe recommendation needs evidence for at least these distinctions:

| Needed signal | Likely owner | What the system may infer | What still needs confirmation or observation |
|---|---|---|---|
| A live choice or blocked next possibility | person, sometimes joint | repeated research may indicate a boundary | whether any choice is actually live and whether action is desired |
| A discriminating uncertainty | person and/or world | unresolved, conflicting, or repeatedly revisited findings may nominate one | which result would materially change the person's decision |
| Existing evidence versus absent evidence | world/corpus | whether the ledger links a source or only a gap | whether retrieval is sufficient before a new test |
| Permission and hard constraints | person/authority | none from silence or prior assent | whether suggestions are welcome and what must not be sacrificed |
| Reversibility, cost, and risk | world plus person | provisional estimate | acceptability and domain-specific competence/safety boundary |
| Experiment outcome | world | observed result only | interpretation, acceptance, and authorization of the next action |

Thus the correct interaction is usually a **conditional offer**, for example: “The research appears to leave X as the distinction blocking Y. A small reversible test Z could distinguish A from B. If that is not the decision you are making—or you prefer a direct answer, more evidence, waiting, or stopping—we should not run it.” This wording is an inference from the candidate policy, not a ratified script.

## Decision table

| Observed condition | Preferred move | Why | Abstain/suppress condition | Citation |
|---|---|---|---|---|
| The person owns the missing preference, experience, constraint, interpretation, or authorization | **Ask** one decision-changing question | The system cannot recover a user-owned signal from external evidence or ledger history | No plausible answer changes a live alternative, safeguard, next move, or stop decision; question is high-burden, invasive, concealed-purpose, or difficult to refuse | `docs/game/QUESTION-LANDSCAPE.md:7-19,21-31`; `docs/game/THINKING-THE-GAME.md:19-32` |
| The missing signal exists in a source, calculation, comparison, or observation | **Retrieve / inform** | World-owned evidence should not be displaced by further introspection | Retrieval cannot discriminate the alternatives, source authority would be laundered into truth, or information overload exceeds local value | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:69-76,96-104` |
| A live decision-relevant distinction requires a new observable, and a small recoverable action can produce it | **Suggest a bounded test** | A reversible candidate can unlock learning without claiming the action or interpretation is established | No named decision-changing result; existing evidence is sufficient; candidate is irreversible, costly, unsafe, outside competence, difficult to refuse, or lacks permission; “no construction” is the only trigger | `docs/game/QUESTION-LANDSCAPE.md:5-19,21-29`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:73-101` |
| The current representation hides or collapses the decisive distinction | **Offer a contestable reframe** | Changing the representation may reveal alternatives that another question or test would miss | The old frame, trade-offs, excluded alternatives, and route back cannot be exposed; reframe risks goal substitution or capture | `docs/game/THINKING-THE-GAME.md:19-32`; `research/foundation-game-framing/lanes/03-agency-governance.md:52-66` |
| The user asks for an answer and a concise answer is sufficient to enable the choice | **Answer directly** | Inquiry or experimentation adds burden without discriminating value | A direct answer would conceal material uncertainty, exceed competence, or authorize a consequential action the user has not chosen | `product/CHARTER.md:5-15`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:116-126` |
| More inquiry has lower expected value than a named future event, evidence source, or permission | **Wait / deliberately defer** | Non-action preserves option value and avoids manufacturing urgency | There is an immediate safety or time-critical duty requiring referral or qualified help | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:106-114`; `research/foundation-game-framing/lanes/03-agency-governance.md:99-104` |
| The person can state an authorized, proportionate next step and its decisive reasons or remaining uncertainty | **Advance** | The selected next possibility is no longer blocked; another intervention has lower marginal value | The apparent commitment is only inferred, induced, or accepted under pressure; risks or authority remain unresolved | `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:106-114`; `authority/AUTHORITY-MODEL.md:15-21` |
| Two consecutive moves fail to change alternatives, constraints, authorization, or next step | **Change mode or stop** | Continuing produces burden without observed decision value | The person explicitly chooses open exploration and its burden/risk remains acceptable | `docs/game/QUESTION-LANDSCAPE.md:21-31`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:96-104` |
| Ambiguity is productive, authority is missing, risks dominate, no witness exists, or a simpler baseline wins | **Preserve residue, refer, branch, or stop** | Closure and action are not automatic successes; safety, refusal, and unresolved conflict are legitimate outcomes | Do not use residue as an unfalsifiable dumping ground: name an owner/reopen trigger where one exists | `docs/game/THINKING-THE-GAME.md:42-48`; `research/foundation-game-framing/lanes/01-auditable-transition.md:72-80` |

## Strongest overturning fact

The table should be overturned, not merely tuned, if preregistered comparisons on independent bounded episodes show that its source/eligibility/agency routing cannot be coded reliably **or** that a simpler user-selected mode (especially concise direct answer or ordinary competent conversation) yields equal or better decision quality, correction/refusal, and later reversibility with materially lower burden. The corpus itself names those results as collapse conditions (`docs/game/THINKING-THE-GAME.md:46-48`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:116-129`).
