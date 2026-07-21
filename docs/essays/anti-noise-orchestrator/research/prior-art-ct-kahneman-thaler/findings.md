# Prior-art — CT × Kahneman × Thaler: has the novelty already been done?

> **Question:** has anyone formally linked **category theory** to Kahneman-style
> judgment error (bias/noise) and/or Thaler-style choice architecture (nudge)?
> **Method:** 3 tensioned dispatches (ledger `2026-07-20-kahneman-thaler-ct-prior-art`
> + `-gapclose`), independent positions frozen before aggregating — HYP-ORCH-NOISE itself
> applied to itself (A6). **Status:** completed, `resolved`. Created 2026-07-20.

## Verdict

**The center is empty — and it survived adversarial search.** The triple intersection
(CT-as-substrate × bias⊕noise decomposition × nudge layer) **is not occupied**.
Two independent agents with opposed vectors reached the same verdict without seeing
each other (low noise → high confidence), confirmed by a 3rd sweep across non-web databases.

- **CT × nudge/choice-architecture: completely empty** — the strongest part of the novelty.
- **The normative neighborhood does not model error:** *Evidential Decision Theory via Partial
  Markov Categories* (Di Lavore–Román, LICS 2023) is ideal decision-making, with no bias or noise. The
  move "bias = deviation from a natural transformation" is **unclaimed**.

## The seam of the contribution (most valuable finding)

The **statistical games** of the compositional Bayesian brain program (Smithe,
arXiv:2109.04461; Braithwaite–Hedges–Smithe, MFCS 2023, arXiv:2305.06112) already do **three**
of the four pieces: judgment over a monoidal substrate (Bayesian lenses over Markov
categories) + judge as minimizer of an error functional. **What they don't do:** the error is
*free energy*, a scalar — never refactored into the orthogonal **bias ⊕ noise** decomposition, and
no nudge morphism over the substrate. **That is the exact seam of the paper.**

## Title-mines to disarm (cite-and-disarm)

"Categorization" (grouping into buckets) ≠ "category theory". A reviewer might brandish:

- **Fryer & Jackson**, *A Categorical Model of Cognition and Biased Decision-Making*
  (NBER w9579, 2003; BE-JTE 2008) — https://www.nber.org/papers/w9579
- **Ellis & Masatlioglu**, *Choice with endogenous categorization* (Review of Economic
  Studies, 2022) — same family.

## Neighbors the paper needs to cite (must-cite)

1. Kahneman, Sibony & Sunstein, *Noise* (2021)
2. Thaler & Sunstein, *Nudge* (2008)
3. Ghani–Hedges–Winschel–Zahn, *Compositional Game Theory* (LICS 2018) — arXiv:1603.04641
4. Bolt–Hedges–Zahn, *Bayesian open games* (Compositionality 2023) — arXiv:1910.03656
5. Fritz, *A synthetic approach to Markov kernels…* (Adv. Math. 2020) — arXiv:1908.07021
6. Di Lavore–Román, *Evidential Decision Theory via Partial Markov Categories* (LICS 2023) — arXiv:2301.12989
7. Smithe, *Mathematical Foundations for a Compositional Account of the Bayesian Brain* (2022) — arXiv:2212.12538
8. Braithwaite–Hedges–Smithe, *The Compositional Structure of Bayesian Inference* (MFCS 2023) — arXiv:2305.06112
9. Capucci–Gavranović–Hedges–Rischel, *Towards Foundations of Categorical Cybernetics* (ACT 2021) — arXiv:2105.06332
10. *Choice Structures in Games* (GEB 2023) — arXiv:2304.11575
11. Costello & Watts, *Surprisingly rational: probability theory plus noise explains biases* — **non-categorical** approach to the noise axis (contrast).

## Near-misses (real CT, but wrong object)

- Phillips & Wilson, *Categorial Compositionality* (PLoS CB 2010) — object = systematicity.
- Ehresmann & Vanbremeersch, *Memory Evolutive Systems* (2007) — object = hierarchy/emergence.

## Residual risk (honesty)

**MathSciNet stayed behind an institutional paywall** (LibLynx gateway) — the only
unverified database. Mitigation: the sibling database **zbMATH came back empty**, so MathSciNet
almost certainly doesn't differ. Closes 100% with institutional AMS access (2-min query). The other
databases (zbMATH via open API, PhilPapers, Google Scholar, web index) were reached.

## Audit

Ledger: `telemetry/agents/subagents-dispatch.yaml` — dispatches
`2026-07-20-kahneman-thaler-ct-prior-art` (2 tensioned explorers: skeptic-of-the-void ⊥
neighbor-cartographer) and `2026-07-20-kahneman-thaler-ct-prior-art-gapclose` (1 explorer,
non-web databases). Queries per axis and per database recorded in the agents' returns.
