---
tags: [agents, architecture, mathematics, category-theory, lean, research]
node_type: research
status: synthesized
version: 0.2.0
last_updated: 2026-07-24
related_plan: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
stream_id: R1
dispatch_id: 2026-07-24-agent-language-formalization-design
target_document: docs/architecture/agent-language-system-view.md
---

# Research: Agent-Language Mathematical Formalization

## Research boundary

This artifact preserves the three independent design returns commissioned for the mathematical and
Lean appendix. It belongs to R1 of the
[Agent Work Language Research](../../plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md); it is not
an independent plan or a new formalization project.

The dispatch was read-only. The Lean corpus was inspected textually, not built. Consequently the
strongest admissible status is `proof-present-in-bound-source`; no result is called
`machine-checked-currently`, build-current, `sorry`-free-current, or axiom-audited-current.

## Shared status discipline

The seats agreed that the appendix must distinguish:

- definition, premise, candidate axiom, invariant, proposition, countermodel, and proof obligation;
- `open`, `statement-present`, `proof-present-in-bound-source`, and later verified proof states;
- direct, adapted, analogy-only, conflicting, insufficient, and no-correspondence mappings; and
- semantic structure, accepted runtime fact, derived projection, executable authority, and
  external physical effect.

A mathematical proof establishes a proposition relative to definitions and premises. It does not
establish product correspondence, runtime premise truth, promotion, or execution authority.

## Independent return A — categorical and local-to-global seat

This seat recommended starting below category level:

1. Use provisional many-sorted carriers rather than a universal `Object`.
2. Represent direct relations as proof-relevant typed edges.
3. Add partial composition only through an explicit admissibility witness.
4. Call a translation a functor only after totality and preservation laws are justified.
5. Represent effective context as indexed materialization; lineage supplies no canonical
   reindexing map.
6. Treat accepted event history and deterministic folds separately from rebuildable projections.
7. Model recursive work as a finite ranked graph compiled into bounded leaf assignments.
8. Define bootstrap as finite checking relative to declared roots, not self-justification.

Its candidate notation was:

| Notation | Proposed meaning |
|---|---|
| \(O,\kappa:O\to K\) | addressable objects and provisional kinds |
| \(E_r(x,y)\) | proof-relevant direct edge of relation kind \(r\) |
| \(\operatorname{Adm}(f,g;h)\) | witness that two edges admit a result of kind \(h\) |
| \(\Sigma_i,T_{ij}\) | bounded contracts and declared translations |
| \(\Gamma,X_\gamma,\rho_u\) | context index, effective context, and authorized reindexing |
| \(H,\operatorname{fold}\) | accepted history and deterministic reducer |
| \(\pi_v:H\to V_v\) | versioned, rebuildable projection |
| \(A(x)\) | scoped authority record |
| \(W=(V,E,\operatorname{rank},B)\) | finite recursive work graph |
| \(\operatorname{Compat}(\Sigma_i,\Sigma_j)\) | proof-relevant compatibility witness |
| \(B_0\) | explicit finite bootstrap boundary |
| \(\operatorname{Res}(F,P)\) | failure locus relative to intended preservation |

The seat proposed proof obligations for admitted partial composition, deterministic replay,
explicit context materialization, shallow execution compilation, local-to-global validation, and
finite bootstrap. It identified existing Lean propositions on permission-policy composition,
acyclicity, and failure of instance-level faithfulness as bounded precedents, not product proofs.

Its most important negative finding was that DomainSpec's typed relation fragment does not already
supply a category: the heterogeneous relation kinds do not share a uniform identity or composition
law.

## Independent return B — Lean mechanization seat

This seat proposed a countermodel-first Lean roadmap centered on proof-relevant records:

1. correspondence boundary and claim-status vocabulary;
2. identity, versions, and provisional kinds;
3. relation signatures, direct facts, witnessed derivation paths, and cycle policies;
4. authority claims and execution fences;
5. accepted events, pure replay, and projections;
6. finite work graphs and bounded leaf compilation;
7. dispatch/attempt/reveal boundaries; and
8. counterexamples and an Open Questions registry.

Its candidate declarations included `ObjId`, `Version`, `Kind`, `RelationSig`, `DirectEdge`,
`DerivationPath`, `CyclePolicy`, `AuthorityClaim`, `LayeredPolicy`, `AcceptedEvent`, `History`,
`WorkGraph`, `LeafAssignment`, `RevealEvidence`, and `CorrespondenceRecord`.

The proposed first proposition set was:

- identity is independent of mutable description and placement;
- a derived relation retains its direct-edge path and composition-rule version;
- acyclicity is graph-level, not node-local;
- layered permission composition is a meet only under the exact selected policy algebra;
- a projection cannot mint execution authority;
- replay is deterministic and effect-free under fixed premises;
- lineage does not imply authority or context inheritance; and
- a reveal is bound to an explicit source manifest and attempt.

The seat recommended excluding category theory from the first executable dependency cone except
where a named obligation requires it. It also warned that the inspected empty permission policy is
algebraically `allow`; a product boundary adopting that algebra would need a separate fail-closed
validation rule.

## Independent return C — infrastructure correspondence seat

This seat organized the model around responsibility boundaries already present in ACI:

```text
semantic structure
≠ accepted runtime fact
≠ derived projection
≠ executable authority
≠ external physical effect
```

It recommended a responsibility ledger as an entry gate. Every formal construct must name its
exact source, owning infrastructure responsibility, applicability, authority boundary,
correspondence status, and non-claim. A construct without a responsible owner should not enter the
core merely because it is mathematically attractive.

This seat sharpened the following correspondences:

- stable identity is distinct from mutable naming, description, classification, and placement;
- direct relation facts are distinct from witnessed derived paths;
- provenance is a typed origin/transformation chain, not proof or authority;
- accepted event streams and pure reducers reconstruct state without performing effects;
- authority is an indexed accepted record, not graph reachability;
- `ExecutionAuthorityFence` corresponds to an operational boundary, but a mathematical inhabitant
  cannot prove physical sandbox or process enforcement;
- projections are rebuildable views and cannot authorize mutation;
- confirmed recursive work can compile to bounded leaf plans without nested orchestrator
  authority.

It also recommended keeping all results in this existing research node and embedding the formal
result in Section 16 of the system view.

## Convergence

All three seats independently converged on these design constraints:

1. No universal category of all system objects and relations is currently justified.
2. A many-sorted, proof-relevant typed multigraph is the safer base.
3. Direct edges and derived paths are different constructs.
4. Composition is partial, relation-specific, versioned, and witness-bearing.
5. Authority is not ordinary graph reachability and does not flow through lineage.
6. Physical effects and enforcement remain outside the pure semantic model.
7. Accepted history, pure replay, and derived projections are distinct responsibilities.
8. Recursive work structure can be deep while runtime orchestrator authority stays shallow.
9. Countermodels should precede ambitious categorical enrichment.
10. Lean formalizes only a selected pure subset and must carry a correspondence ledger.
11. The current Lean corpus supplies bounded precedents, not verified product authority.
12. One Plan, one formalization research node, and one appendix are sufficient.

## Product-linked countermodels

| ID | Countermodel | Refuted collapse |
|---|---|---|
| CM-01 | Two artifacts change paths but retain their IDs | placement defines identity |
| CM-02 | A child has lineage but no accepted delegation or context manifest | lineage grants authority or context |
| CM-03 | A stale dashboard says `ready` while no accepted fact does | projection is authoritative fact |
| CM-04 | A structurally valid Dispatch candidate lacks confirmation | schema validity grants execution authority |
| CM-05 | All nodes pass unary lint while their edges form a cycle | local checks prove graph acyclicity |
| CM-06 | A faithful schema translation induces non-faithful instance behavior | schema preservation guarantees materialization fidelity |
| CM-07 | Empty layered policy evaluates to `allow` | elegant algebra is operationally fail-closed |
| CM-08 | An unranked feedback cycle delegates orchestration capability | recursive work automatically compiles to bounded execution |

## Lean source observations

The seats identified these exact bounded precedents:

- `../domainspec-lean-formalization/lean-engineer/cav2-governance/GovernsAcyclicity.lean`
  contains a proof that node-local data cannot characterize graph acyclicity.
- `../domainspec-lean-formalization/lean-engineer/AgentPermissionKernelAlgebra.lean`
  contains policy-composition results and exposes the empty-policy `allow` caveat.
- `../domainspec-lean-formalization/lean-formalization/LanFaithfulRefutation.lean` and its bicyclic
  support contain a counterexample to lifting schema-side faithfulness to all instances.

These observations remain `proof-present-in-bound-source`. Reuse is conditional on semantic match,
selected build target, dependency-cone review, `sorry` scan, and axiom audit.

## Post-synthesis owner critique and Lean-kernel precedent

After the independent returns were synthesized, the owner challenged whether the proposed
`kernel-of-kernels` was implicitly using the actual Lean theorem-prover kernel as its model. A
bounded follow-up checked the current program artifacts, the separate local `permguard` research,
and the official Lean reference.

The current program did not use Lean's logical kernel as an explicit architectural reference.
The valid precedent is narrower: Lean elaborates an expressive surface into a smaller core language,
then a small trusted kernel checks declarations before accepting them into the environment. Proof
terms may also be rechecked by independent implementations. This motivates an `analogy-only`
pipeline from rich contracts to normalized obligations and explicit witnesses checked relative to
a finite trust base.

The precedent does not supply product semantics for scope, provenance, authority, precedence,
violation response, temporal obligations, or effects. Lean's kernel checks well-typedness relative
to its environment and admitted axioms; it does not establish that arbitrary axioms are mutually
consistent or that a theorem corresponds to a product requirement. The local `permguard` artifact
is a policy decision program verified in Lean, not the Lean prover's own kernel.

The owner critique also exposed that `kernel-of-kernels` was carrying at least five separable
responsibilities:

- a meta-contract \(M\) for well-formed kernel and invariant declarations;
- a global invariant set \(G\);
- bounded domain kernels \(K_i\); and
- compatibility/composition witnesses \(C_{ij}\); and
- a small conformance checker \(Q\), all relative to admitted bootstrap \(B_0\).

The correction is to ask whether
\(B_0;\Gamma\vdash_Q\operatorname{WellFormed}_M(K_i)\) and whether a scoped \(C_{ij}\) passes the
declared compatibility and preservation judgments for \(G\), not to claim \(M\vdash K_i\).
Well-formed metadata, mathematical preservation, joint satisfiability, accepted governance status,
and execution authority remain different judgments. Authority does not repair logical
incompatibility, and precedence is applicable only under an explicit scoped composition policy.

Primary sources:

- [Lean elaboration, compilation, and kernel checking](https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/)
- [Validating Lean proofs and independent rechecking](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
- [Lean axioms and their audit boundary](https://lean-lang.org/doc/reference/latest/Axioms/)

## Residue and non-claims

- The primitive carrier taxonomy is not selected.
- No general composition table or associativity law is accepted.
- No operational adapter is established as a functor.
- No projection is claimed fresh, complete, or authoritative.
- No proof models the physical writer boundary, process tree, credentials, provider behavior,
  sandbox, or filesystem enforcement.
- No provenance chain proves correctness.
- No formal result establishes that a person understood or accepted a proposal.
- No termination theorem is claimed for arbitrary agent behavior.
- No thermodynamic, signal/noise, Yoneda, reflection-tower, or universal-residue vocabulary belongs
  in the core without an exact infrastructure responsibility.

## Open Questions

| ID | Question | Status | History |
|---|---|---|---|
| ALF-OQ-001 | What are the minimal primitive carriers, and can any common `Object` abstraction avoid collapse? | open | Opened 2026-07-24; many-sorted start recommended. |
| ALF-OQ-002 | Which relation kinds admit composition, partial composition, or no composition? | open | Opened 2026-07-24; universal composition rejected. |
| ALF-OQ-003 | Which derived closures may affect validation or decisions, under what witness/version contract? | open | Opened 2026-07-24. |
| ALF-OQ-004 | What lifecycle combination of event streams, transition systems, intervals, or temporal logic is sufficient? | open | Opened 2026-07-24. |
| ALF-OQ-005 | What is the minimal authority record, and what remains exclusively runtime-enforced? | open | Opened 2026-07-24. |
| ALF-OQ-006 | What compiler invariant proves no invoked orchestrator can invoke another orchestrator? | open | Opened 2026-07-24. |
| ALF-OQ-007 | Will the product adopt intersection-of-authority policy composition, and how will empty policy fail closed? | open | Opened 2026-07-24 from Lean precedent. |
| ALF-OQ-008 | What finite bootstrap validates compatibility without a metakernel regress? | open | Opened 2026-07-24. |
| ALF-OQ-009 | What evidence is sufficient to claim mathematical-to-product correspondence? | open | Opened 2026-07-24; ledger proposed, adequacy unresolved. |
| ALF-OQ-010 | Which Lean results remain explanatory, generate validators, or become governed evidence? | open | Opened 2026-07-24. |
| ALF-OQ-011 | What is the canonical identity, ownership, reopening, and projection contract for Open Questions? | open | Opened 2026-07-24. |
| ALF-OQ-012 | How do research nodes remain visibly connected to one Plan without folder proliferation? | resolved | Resolved 2026-07-24: Plan registry, bidirectional metadata, existing node reused. |
| ALF-OQ-013 | Are the meta-contract, conformance checker, global invariant set, composition protocol, and bootstrap distinct artifacts or views over one mechanism? | open | Opened by owner critique 2026-07-24. |
| ALF-OQ-014 | What proof obligation distinguishes well-formed invariant metadata from actual preservation under transitions? | open | Opened by owner critique 2026-07-24. |
| ALF-OQ-015 | Which parts of the Lean kernel/TCB pattern correspond to the product acceptance boundary, and which remain analogy-only? | open | Bounded precedent recorded 2026-07-24. |
