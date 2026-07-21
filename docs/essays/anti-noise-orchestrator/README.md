# Essay — The Orchestrator as a Noise-Reduction Machine

> **Status:** high-level draft, **unreviewed**, local. `Claim ≤ proof`. This README
> raises the paper (thesis, refs, contribution) to *later* go into detail. Derives from
> `vault/hypothesis/anti-noise-orchestration.md` (`HYP-ORCH-NOISE`). Created 2026-07-20.

## Thesis (one sentence)

An agent orchestrator is, formally, a **judgment-error-reduction machine**;
the reference frameworks **compose** — they do not compete — on the repo's native lever
`residue = bias ⊕ noise`.

## The levels (open scope decision)

| Level | Role | Status in the paper |
|---|---|---|
| **Category theory** | *in what* — type substrate | **central pillar** |
| **Kahneman / *Noise*** | *why* — error model (bias ⊕ noise) | **central pillar** |
| **Thaler / *Nudge*** | *how* — process choice architecture | **central pillar** (decision 2026-07-20: primary for now) |

> **Decision (2026-07-20, revised).** All **three** enter as primary arguments. There was
> consideration of downgrading Thaler to a corollary (two pillars of homogeneous standing, more
> focus), **but** the prior-art sweep showed that **CT × nudge is the emptiest cell of all** —
> the most indisputable territory of novelty. Dropping Thaler would give that up. Therefore Thaler
> is primary and **requires its own feasibility research** (nudge = morphism over the lens/the
> process, never over the content of the judgment — does this actually type, or is it an analogy?).

## New contribution (the seam)

Refactor the **scalar** error functional of compositional *statistical games*
(Smithe; Braithwaite–Hedges–Smithe) into the **orthogonal bias ⊕ noise** decomposition from
*Noise*, over a substrate of **Markov categories** (Fritz) — and (if Thaler enters) add a
**Nudge morphism** that acts on the *process* (the lens/the type), never on the content.
No one has united these frameworks: **proven by an auditable sweep across 5 databases** (see
`research/prior-art-ct-kahneman-thaler/`).

## Anchor argument — `bias ⊥ noise`

Bias calls for **tension/opposition**; noise calls for **independence/aggregation** —
contradictory tools, resolved by **stage separation** (tension in *generating*, independence in
*evaluating*). The very production process of this paper is an instance of this (self-application,
PLAN.md §1 A6).

## References (high level, grouped)

- **Foundations of error:** Kahneman, Sibony & Sunstein, *Noise* (2021); Thaler & Sunstein,
  *Nudge* (2008).
- **Categorical substrate:** Fritz, *Markov categories* (Adv. Math. 2020); Ghani–Hedges–
  Winschel–Zahn, *Compositional Game Theory* (LICS 2018); Di Lavore–Román, *Evidential
  Decision Theory via Partial Markov Categories* (LICS 2023).
- **The seam / nearest neighbor:** Smithe, *Compositional Bayesian Brain* (2022);
  Braithwaite–Hedges–Smithe (MFCS 2023); Capucci et al., *Categorical Cybernetics* (2021).
- **Cite-and-defuse (title mines — "categorization" ≠ "categories"):** Fryer–Jackson
  (2003/08); Ellis–Masatlioglu (2022).
- **Non-categorical approach to the noise axis (contrast):** Costello & Watts, *Surprisingly
  rational: probability theory plus noise*.
- **The repo's own substrate:** `HYP-ORCH-NOISE`, `MAPPING.md`, anti-bias discipline
  (`check-tension`, P5/P14).

## Structure (outline, to be detailed later)

1. Judgment has two orthogonal errors (bias ⊕ noise) — and the orchestrator incurs them all the time.
2. CT as type substrate — why error needs categorical ground.
3. The seam: decomposing the statistical games functional into bias ⊕ noise.
4. `bias ⊥ noise` → stage separation (tension vs. independence).
5. (minor) Nudge as process architecture.
6. Self-application (A6) + collapse-tests.

## Research (`research/`)

Container of investigations, one folder per question:

- **`prior-art-ct-kahneman-thaler/`** — has the novelty already been done? Verdict: **empty
  center** (auditable, 5 databases). ✅ completed.
