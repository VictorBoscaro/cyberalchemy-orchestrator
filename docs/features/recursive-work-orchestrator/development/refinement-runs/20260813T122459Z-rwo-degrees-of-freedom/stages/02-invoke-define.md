# Stage 02 — Invoke Define

- Capability: `invoke`
- Mode: `define`
- Verdict: `pass`
- Target artifact owner: Refine run; later research owner remains undecided

## Defined problem

The system lacks a decision-ready account of its degrees of freedom. Existing material already
constrains recursive authority, capability scope, and first-version mutability, but it does not join
them into one model that says who can do what, to which resource, in which phase, under which bound,
with which enforcement and proof.

## Defined terms

| Term | Meaning in this research |
|---|---|
| Expressivity | Structures and workflows the language can represent. |
| Authority | Legitimate power to approve or deny a class of action. |
| Capability | A concrete, bounded grant to one principal for one action/resource/phase. |
| Enforcement | Mechanism that prevents actions outside the grant. |
| Evidence | Durable proof of authorization, use, denial, revocation, and resulting effect. |
| Composition | Reuse or nesting of work definitions inside one root execution plan. |
| Orchestration authority | Power to expand/schedule work and issue commands under an authority root. |
| Authority root | Non-derived source from which execution grants become legitimate. |
| Scope amplification | Gaining tools, context, budget, effects, topology, or delegation rights not explicitly granted. |

## Research object

The unit of analysis is a **protected action envelope**:

```text
(actor, action, resource, phase, bounds, authority owner,
 capability, enforcement point, receipt, failure posture)
```

The research compares those envelopes across current state, recommended V1, and later target.

## Claim ceiling

- Current enforcement claims require code, tests, or as-built evidence.
- RWO and future ACI material may define candidate obligations but cannot prove operation.
- “Everything with permission” is rejected as a premise; permissions cannot create support for
  unbounded computation, absent adapters, unavailable capabilities, or self-originating authority.
- The result may recommend a V1 envelope but cannot accept it on behalf of product/RWO/ACI owners.

## Decision enabled

The final research should let the owner accept, revise, or reject a closed V1 capability envelope
and know exactly which restrictions are product choices, security boundaries, implementation gaps,
or intentionally deferred freedoms.

