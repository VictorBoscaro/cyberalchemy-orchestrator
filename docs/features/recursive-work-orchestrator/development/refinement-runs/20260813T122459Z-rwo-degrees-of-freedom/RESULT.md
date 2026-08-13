# Refine Result: Research on System Degrees of Freedom

- Status: `pass`
- Preset: `standard`
- Research decision: local-only during Refine; bounded external comparison proposed for the future
- Plan: `plan/RESEARCH-PLAN.md`

## Final framing

This should be a research program about the **V1 capability envelope and authority transitions**, not
a generic permissions inventory.

Primary question:

> How should CyberAlchemy constrain protected operations and authority transitions across the user,
> authority root, root orchestrator, composite work, delegated agents, tools and effect adapters so
> that V1 supports useful bounded work without implicit inheritance, recursive authority or scope
> amplification—and what evidence must exist before each restriction can be relaxed?

## What the research seeks

The research will determine:

- what “orchestrable” means separately for development target, root configuration, composable
  `Work`, child dispatch lineage and nested scheduler authority;
- which freedoms are allowed, approval-gated, unavailable or outside the V1 model;
- which are attenuably delegable, root-only or forbidden to delegate;
- what is actually implemented/enforced/observed today versus conventional or unknown;
- how grants and global bounds behave through children, tools, adapters, retries, fan-out, resume,
  concurrent execution and separate runs;
- what receipts prove authorization, enforcement, delivery, effect, denial, consumption and
  revocation—and what they do not prove;
- which evidence bundle would justify each later relaxation.

## Smallest coherent research unit

The selected unit is an **Authority Transition Slice (ATS)**: one protected operation where
authority is exercised, derived, transferred, attenuated, issued, revoked or used to change state
or cause an effect. ATS records form causal traces; the research checks qualitative attenuation and
quantitative conservation after each transition and over the complete trace.

Static actor × action × phase matrices remain useful, but only as projections of ATS evidence. This
prevents a row-by-row permission model from missing self-issuance, token lending, confused deputies,
policy two-step escalation, topology smuggling, aggregate budget growth, cross-run laundering,
revocation races or duplicate external effects.

## Candidate V1 thesis to test

The strongest candidate is:

- one non-derived authority root and one root scheduler per confirmed run;
- broad finite/explicitly bounded `Work` composition;
- task-specific attenuated leaf grants with no implicit inheritance;
- root-confirmed subactions may execute without one human prompt per leaf while the frozen envelope
  remains unchanged;
- confined local mutation and bounded subprocesses where confinement is proven;
- network, secrets, tools and external effects only through mediated, evidenced boundaries;
- authority-root creation, capability self-issuance, policy/tool/adapter mutation and automatic
  promotion of dynamic topology unavailable or root-only in V1;
- unknown scope, fence or effect outcome fails closed.

This is a research hypothesis, not an accepted decision. The repository's alternative of bounded
nested orchestrators remains explicit residue.

## Required outputs of the actual research

1. glossary and semantic split of “orchestrable”;
2. closed actor/phase/action/resource universe;
3. current-state enforcement and receipt reconstruction;
4. ATS dataset, causal traces and coverage ledger;
5. current/V1/later matrix with independent availability and delegability axes;
6. utility workflow results;
7. authority-amplification attack results;
8. closed V1 envelope recommendation;
9. restriction-specific relaxation ladders;
10. owner decision packet and preserved residue.

## Boundaries

The research does not design general IAM, implement sandboxing or tokens, promise arbitrary or
unbounded computation, or decide product/RWO/ACI authority by itself. It distinguishes desired V1
behavior from current executability: a capability can be recommended yet unavailable today because
the required enforcement has not been proven.

## Final recommendation

Run the actual research in six phases from `plan/RESEARCH-PLAN.md`. Start with definitions plus
current-state reconstruction. Then request separate permission for one bounded external precedent
pass over object capabilities, workflow/scheduler composition, policy enforcement, sandbox/tool
mediation and external-effect reconciliation. Finish with independent amplification and utility
audits before asking the relevant owner to decide the V1 envelope.

No product decision or implementation was made in this Refine run.
