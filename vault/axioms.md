---
tags: [vault, anti-bias, anti-noise, orchestration, epistemology]
node_type: axiom
is_session: false
session_ref: null
layer: ontology, domain
nature: reference
status: draft
veracity: high
conviction: high
version: 0.2.0
last_updated: 2026-07-20
---

# Axioms — the commitments taken as given

> **Status:** `draft`, unreviewed. These are **assumed**, not discharged. Per
> [[ontology-conventions]], an `axiom` is challenged with *"revisiting it breaks everything
> built on it"* — not with *"show me evidence"* (that is a `premise`). Promoting a claim here
> **removes it from test on purpose**: the research program downstream stops asking *whether*
> and starts asking *what is the best way*. Each axiom states **exactly what it does and does
> not** axiomatize, so nothing evidence-revisable is smuggled in as settled.
>
> `Claim ≤ proof` is not violated by an axiom: the certainty is declared as **assumed**, and
> every claim *made within* the method stays falsifiable. What is fixed is the frame, not the
> findings.
>
> **Revised 2026-07-20** after tensioned review (`2026-07-20-review-claim-graph-axioms`): AX-1
> was re-cut so the *axiom* is a value **commitment** (not an evidence-graded claim), and the
> untested **agent-transfer** was demoted to the named premise **P-AGENT-TRANSFER**; the
> existential-efficacy assumption behind "best way" was made explicit.

---

## AX-1 — Debiasing is worth pursuing *(a value commitment)*

**Assumed as a commitment, not an empirical prediction.** Reducing correlated **bias** and
**noise** in judgment is a goal worth building the orchestrator around. This is challenged by
*"is this goal worth pursuing?"* — not by *"show me it works."* It is held **regardless of proven
achievability**; that is what makes it an axiom rather than a premise.

- **What this axiomatizes:** the *value/goal*, grounded in decision science (Kahneman on
  bias/noise) as an established worth for judgment.
- **What this does NOT axiomatize — two things kept open, not smuggled:**
  1. **Agent-transfer** — that the human-established value carries over to *agents specifically*.
     This is untested and lives below as **P-AGENT-TRANSFER** (a `premise`, not part of the
     axiom).
  2. **Efficacy** — that any given countermeasure actually cancels correlated bias rather than
     relabels it. Agents on a shared base model produce correlated errors, capping what
     independence buys. This is the optimization handed to [[anti-noise-orchestration]].
- `conviction: high` (the whole orchestrator is built around the commitment). Veracity is **not
  the operative dimension for a commitment**; the evidence-graded part is P-AGENT-TRANSFER below.

### P-AGENT-TRANSFER — *(premise, not axiom)* the value transfers to agents

`node_type: premise` · `veracity: low` · `conviction: high`. **Working bet:** agent judgment
inherits enough of the human bias/noise structure that debiasing *agents* is worthwhile in the
same way it is for humans. **Falsifier:** if agents' correlated bias on a shared base model is
effectively irreducible — no countermeasure measurably beats the single-agent baseline — the
transfer fails and AX-1's *agent applicability* collapses (the commitment to the goal survives;
its relevance to this project would not).

## AX-2 — The scientific process is the operating method

**Assumed true.** The repo runs on the `claim ≤ proof` loop: **state a falsifiable claim → probe
it → keep what survives → enrich the model from what breaks.** This method is the substrate, not
a hypothesis under test.

- **What this axiomatizes:** the *method* — falsifiability, collapse-tests, veracity never larger
  than the evidence. This is the T0 root the other three faces (decision-science, categorical,
  engineering) are instances of.
- **What this does NOT axiomatize:** any *particular* claim expressed in the method. The loop is
  fixed; the contents run through it and remain refutable. The method being assumed is what lets
  a collapse-test *mean* something.
- `veracity: high` (a well-established principle in the field) · `conviction: high`.

## AX-3 — Framework as its own instance *(recording the existing axiom)*

Already stated in [`PLAN.md §1`](../PLAN.md) (BACKLOG A6): the work of building this repo is
itself an instance of the epistemological framework it studies, recorded in the same ledger it
operates. Listed here so the axiom layer is a single source. Honest caveat carried from PLAN: a
*declared* instance is not proof the process obeys the framework — the self-application is an
axiom of stance, and its reflexive claims (e.g. self-similarity/fractality) remain to be earned,
not assumed.

---

## Consequence — validation → optimization

Fixing AX-1/AX-2 **re-poses** the downstream program. Questions of the form *"is debiasing/the
scientific method worth it?"* are closed by decree; questions of the form *"what is the **best**
architecture of dispatch, tension, freeze, aggregation, and claim-typing to serve them?"* are the
open work. Two efficacy conditions survive as **collapse conditions, not assumptions**:

- **∀-method** (per-method): "best way" does **not** assume any *particular* method succeeds.
- **∃-method** (existential): "best way" **does** presuppose that *at least one* countermeasure
  measurably beats the single-agent baseline. If **no** method clears baseline, there is no
  "best" — only equal failures — the optimization is empty, and AX-1's agent applicability
  (P-AGENT-TRANSFER) collapses. Stated here so the existential assumption is explicit and
  falsifiable, not silent.

> **Reconciliation flagged (not yet done).** [`README.md`](../README.md) currently frames the
> founding claim as a falsifiable founding hypothesis rather than settled fact. AX-1 promotes its
> **value half** to a commitment/axiom while keeping **agent-transfer** (P-AGENT-TRANSFER) and
> **efficacy** as premises. README and AX-1 must be **reconciled** — with neither presupposed as
> the side that yields — before either moves up a level.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[anti-noise-orchestration]] | `grounds` | AX-1 hands it the "best way" optimization; the efficacy question AX-1 refuses to axiomatize lives here as the open thesis. |
| [`PLAN.md`](../PLAN.md) | `derives-from` | §1 already names A6 as axiom; AX-3 records it in the axiom layer. |
| [[claim-graph]] | `grounds` | AX-2 (scientific method) is the root the claim-graph mechanizes: veracity propagation + `contradicts` as the enrichment engine. |
| [`README.md`](../README.md) | `contradicts` | ⚠️ README frames debiasing-value as hypothesis; AX-1 promotes it to a commitment/axiom. Reconcile (neither side presupposed) before either moves up a level. |
| [[ontology-conventions]] | `depends-on` | Uses its `axiom` vs `premise` distinction and confidence dimensions. |
