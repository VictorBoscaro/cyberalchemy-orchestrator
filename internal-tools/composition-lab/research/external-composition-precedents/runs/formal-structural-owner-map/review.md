# Review — formal and structural owner map

## Verdict

**PASS / KEEP**

The artifact satisfies the advisor contract. The six substantive owner sources are primary author texts or primary research papers, every entry contains the eight required fields, and the claims remain local to their owning formalism. One non-blocking citation-label defect survives.

## Coverage

| target | lens | result |
|---|---|---|
| `advisor.md` | contract fidelity | All completion criteria and blockers checked. |
| `findings.md` | source primarity and ownership | Six substantive sources checked directly; the supplementary Abadi–Lamport publication note is official provenance, not a separate tradition. |
| `findings.md` | citation and claim fidelity | Definitions, operations, hypotheses, preservation claims, and failure boundaries checked against the cited texts. |
| `findings.md` | schema completeness | All six entries contain all eight required fields plus visibly separated Evidence, Paraphrase, and Inference. |
| `findings.md` | scope discipline | No internal-repository evidence, cross-domain synthesis, universal theory, or winning-formalism recommendation appears. |

## Source checks

| source | direct check |
|---|---|
| [Leinster, *Basic Category Theory*](https://arxiv.org/pdf/1612.09375) | Definition 1.1.1 and Remark 1.1.2(b) support typed morphism composition, identities, associativity, and the unique composite induced by a typed chain. |
| [Fong, “Decorated Cospans”](https://arxiv.org/pdf/1502.00872) | Proposition 3.2 supports the category and pushout composition of decorated cospans; the later results support the qualified hypergraph/functor claims. |
| [Spivak, “The operad of wiring diagrams”](https://arxiv.org/html/1305.0297) | The operad definition supports multivariable composition, identities, and associativity; the typed construction and §3.1 support the type and invariant boundaries stated. |
| [Plotkin, “A Structural Approach to Operational Semantics”](https://homepages.inf.ed.ac.uk/gdp/publications/sos_jlap.pdf) | Definition 11 supports stuckness; the language rules and Facts 13/15 support the bounded operational and preservation claims. |
| [Turi–Plotkin, “Towards a Mathematical Operational Semantics”](https://homepages.inf.ed.ac.uk/gdp/publications/Math_Op_Sem.pdf) | §§7.1–7.3 support distributive laws, bialgebra compatibility, compositional universal semantics, and preservation of behavioral distinctions; the safe-tree-rule boundary is explicit. |
| [Abadi–Lamport, “Composing Specifications”](https://lamport.azurewebsites.net/pubs/abadi-composing.pdf) | The paper explicitly states the three-part composition principle, its circularity, the need for side conditions, and composition via intersection/conjunction with qualification. |

## Findings

### MINOR — Fong result 3.5 is mislabeled

- **File:** `findings.md`
- **Evidence:** “`(Proposition 3.2; Theorem 3.5; Theorem 4.1)`”
- **Issue:** In Fong’s paper, result 3.5 is labeled **Corollary 3.5**, not Theorem 3.5. The surrounding substantive claim remains supported, so this is a reference-precision defect only.
- **Proposed fix:** Replace `Theorem 3.5` with `Corollary 3.5`.

No CRITICAL or MAJOR finding survived verification.

## Contract checks

- Sources: 6 substantive primary sources; 1 official supplementary note associated with an existing owner. This remains within the 5–7-source bound under either reasonable count.
- Traditions: 6; required minimum is 4.
- Required fields: 8/8 in every entry.
- Evidence / Paraphrase / Inference: explicitly separated in every entry.
- Failure/non-example and transfer risk: present in every entry.
- Universalization, internal evidence, cross-domain synthesis, and winner selection: absent.
- Required artifacts: `findings.md` and independent `review.md` present.

**Final disposition: PASS / KEEP.**
