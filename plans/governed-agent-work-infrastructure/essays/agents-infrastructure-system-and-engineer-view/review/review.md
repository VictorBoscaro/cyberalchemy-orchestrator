---
tags: [review, agents, infrastructure, emission, zig-zag, adversarial]
node_type: review
is_session: false
status: complete
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
authority: proposal-only
reviews: plans/governed-agent-work-infrastructure/essays/agents-infrastructure-system-and-engineer-view/essay.md
reviewed_version: 0.1.0
review_kind: independent-adversarial-zigzag
exchanges: 3
verdict: FIX
---

# Review — Agent Work Infrastructure system-and-engineer view v0.1.0

One independent adversarial reviewer, three zig-zag exchanges with the author. Read-only
throughout; the reviewer edited nothing. Scope was the essay plus `plans/` and the two bound skill
contracts — current implementation was explicitly out of scope, since the essay is a target state.

**Verdict: FIX.** The essay's spine survives. Its central contract does not.

## 1. Outcome in one paragraph

Round 1 returned twenty findings, five of them BLOCKER. Round 2 established that five of those
findings share a single cause — the `address` field of the emission contract — and returned a
structural verdict that the three-axis emission model is the wrong decomposition, with a concrete
replacement. Round 3 attacked that replacement at the author's request, conceded one independence
claim, chose the fork it had previously only named, and concluded that the replacement costs the
essay two of its three externally-authorised verdicts. Fifteen of the original findings survive the
re-cut unchanged; six new holes are opened by it.

## 2. The structural verdict

`address : sealed | directed(<node>)` is not an axis of the same kind as `payload` and `return`. It
is `Maybe<NodeId>` — a boolean fused to an identifier — doing three jobs at once: whether a
recipient exists, who and how many, and whether the barrier applies. Five independent findings
trace to that fusion.

The fused field also encodes a falsehood. A sealed emission is not unaddressed: its recipient is
the aggregator, under a delivery condition. "No edge in the work graph" was always a fiction, and
it was that fiction that made `return = reply` unconstructible and left `PLAN-DRIFT` unable to
check the one class of emission the design exists to protect.

The replacement, after round 3's repair moved `release` off the emission and onto the recipient:

```text
emission:
  recipients : set of (node, release)      release ∈ { immediate, on-barrier(<group>) }
  payload    : judgment | content | empty
  return     : none | ack | reply
  binding    : (prompt_template@version, response_format@version)
```

Per-recipient release makes vacuity unconstructible and lets one emission carry different release
conditions to different recipients — the granularity `stance:sealed-read-authority` needs.

The essay's §2.4 argument survives intact: it argued for **axes over an enumeration of types**, and
this is still that. Only the count changed, because `address` was two things.

## 3. Resolutions reached in the exchange

| Question | Resolution |
|---|---|
| Question-dependent fan-out width | **Permitted.** What is forbidden is width decided by the compiler, which is FM-1 by definition. A width-determining scoping step is confirmed first; the extended graph is confirmed before the fan-out fires. D2's "two confirmations, one digest" generalises to one confirmation per width-determining boundary, and the digest becomes a chain with lineage. Confirming a width *bound* and letting the compiler pick inside it was considered and rejected: the human confirms a range, the record shows a topology nobody confirmed. |
| Are the judges' inputs recorded? | **The frozen target is an emission** — one emission, N recipients, `payload = content`. The alternative loses provenance permanently: replay covers what was said and never what was seen, "on what basis" has no referent, common-input identity is unrepresentable, and no aggregate's validity is checkable. This branch costs storage; the other costs the thesis. |
| Does first-class `group` create a second topology? | **Yes, and the fix is to delete the third source.** The group carries no membership list; members of `g` are exactly the emissions carrying a recipient with `release = on-barrier(g)`. The group owns identity, completion rule, and shared scale, nothing else. New invariant: the completion rule's arity equals the confirmed member count (`GROUP-ARITY`) — which also closes the round-1 hole "a sealed emission that never arrives." |
| Is the aggregator deterministic? | **Not as stated.** The essay modelled the aggregator as a node with a prompt binding — an LLM — and asserted its determinism flatly. The repair is to make it a fabric-owned function outside the WorkGraph. The honest claim is then "the aggregate is a total function of the sealed set and the function version," checkable by recomputation, not "it is deterministic." New code `AGG-IRREPRODUCIBLE` makes FM-3 detectable for the first time rather than merely named. |
| Does the aggregator repair keep D5 resolved? | **No. D5 splits and mostly reverts.** See §4. |

## 4. The authority finding

D5 was the essay's strongest row: RESOLVED on owner direction, session 2026-07-27 — *the fabric
transports and never authors*. The aggregator repair gives the fabric three new powers: computing a
function whose choice encodes a position on dissent, persisting a durable derived fact, and being
named as a principal in the record.

The reviewer's test is this repository's own. `CANDIDATE-INVARIANTS.md` K1: *"automation cannot
acquire more authority than was delegated to its definition or run."* Amending D5's prohibition
list inside the document that benefits from the amendment — "may not rank" becoming "may not rank
by its own judgment" — is exactly the move K1 forbids.

Resolution: D5 stays RESOLVED in its narrow form (may not rewrite, summarise, reinterpret, or
choose a recipient), because nothing proposed touches those and that is what the owner ruled. The
ranking prohibition and the three new powers move to a new row, **OPEN, no gate, pending fresh
owner direction.**

Combined with finding 12 (D3's citation supports D9's proposition, not D3's), the accounting
becomes: **one verdict in the essay is covered by external authority — D9.** The essay claimed
three.

## 5. Delta against the re-cut

**Moot — dissolved (5):** sealed × reply impossible · `PLAN-DRIFT` blind to sealed channels ·
group membership unbound to seal · multicast inexpressible · a reply has no axes of its own.

**Survive unchanged (15):** D5's verdict stated in Part I §2.5 (now worse — D5 splits and §2.5
states the wrong half) · the classifier is in the architecture and governed nowhere · D2's verdict
stated in Part I §3 "Given" · §4's caption reintroduces "emission kinds" · the dangling "four
combinations named in Part I" · D7's weaker constraint stated in Part I · the proposal accounting
counts three non-decisions as proposals · D3's citation supports D9 · RESOLVED means decided *and
enforced* · the result block says D2 has no mechanism when it has two ·
`stance:sealed-read-authority` is missing and D6 is CRITICAL for the wrong proposition · D4 meets
the CRITICAL bar · FM-6 contradicts §2.1's promised decoupling · FM-7 cites "Single-writer", which
is named nowhere · the companion essay's `stance:projection-vs-authority` is answered here under a
different slug.

**Survive modified (4):** "each rule follows from exactly one axis" is false under any cut — claim
instead that every rule derives from stated fields *of the emission* · barrier deadlock, which
`GROUP-ARITY` does not detect · confirm-to-confirm drift, sharpened by the confirmation chain ·
**angle collapse, wholly untouched.**

**New — opened by the re-cut (6):** digest lineage across a confirmation chain, without which a
late confirmation launders earlier drift · `GROUP-ARITY` plus a hard prohibition on membership
lists · event volume roughly doubles and rendered input text enters the record while the digest
excludes it, an asymmetry that must be stated rather than inferred · read-authority becomes
per-recipient-edge, a strictly harder question than the emission-level one · D5 splits and
externally-authorised rows drop from three to one · the aggregator leaves the WorkGraph, so a human
confirms a function reference — the first schema-shaped confirmation in the design, which §2.3's
own table calls rubber-stamping.

## 6. What survived attack

- The §5 ↔ §7 bijection is exact: nine stances, nine rows, no orphan and no duplicate, checked
  pair by pair. The one self-check in the essay that is fully earned.
- The citation to `PLAN.md` §3.1 and §3.3 is accurate on both halves.
- "Services, not phases" survives its strongest counter. The fabric is present during every step
  and constitutes none of them, and the per-TYPE / per-INSTANCE lifetime split is structural rather
  than a naming preference.
- The axes-over-types argument survives the re-cut.
- No proposed failure mode was a non-failure, and none was a strict duplicate.
- The fourth "visibility" axis asked about in §12 is correctly rejected — but the essay's stated
  reason is wrong. Visibility is not determined by address plus barrier; that §9 must enumerate the
  non-readers in prose is the proof. It is a read-authority policy evaluated against the reader's
  principal, which is why it belongs to `stance:sealed-read-authority` and not to the emission.

## 7. The two deepest findings

**The headline failure was constructible inside the essay's own contract.** Nothing forbade a
directed judgment from belonging to an aggregation group. Such a judgment is peer-visible before
aggregation, `EMIT-SCALE` passes because the format matches, `BARRIER-EARLY` never fires because
nothing was sealed, and the aggregate is contaminated with no code raised. The failure family could
not see the failure that motivated it. The re-cut dissolves this.

**Angle collapse is untouched and remains the mode the design cannot see.** Nothing checks that two
nominally opposed angles are actually opposed. Two attackers with correlated angles produce an
aggregate that is perfectly sealed, perfectly recorded, and confidently wrong. The barrier defends
against contamination and does nothing against correlation-by-construction — which is the
correlated bias named as the founding failure in `PLAN.md` §1. Every guarantee in the essay holds
and the answer is still wrong.

## 8. Open Questions

- Does the re-cut hold against a second independent reviewer, or only against its own author? It
  was attacked in exchange 3 by the reviewer who proposed it — better than nothing, worse than
  independence.
- What detects angle collapse? Nothing in this design does, and nothing in the reviewed essay
  claimed to.
- Does the confirmation chain make question-dependent width affordable in practice, or does
  confirmation fatigue defeat it before the topology does?
- Who supplies fresh owner direction for the fabric's new powers, and does that row's absence block
  the rest of the design or only the aggregation half?
