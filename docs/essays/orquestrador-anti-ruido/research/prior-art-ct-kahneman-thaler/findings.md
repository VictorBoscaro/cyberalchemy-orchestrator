# Prior-art — CT × Kahneman × Thaler: a novidade já foi feita?

> **Pergunta:** alguém já ligou formalmente **teoria das categorias** a erro de juízo
> estilo-Kahneman (viés/ruído) e/ou a arquitetura de escolha estilo-Thaler (nudge)?
> **Método:** 3 dispatches tensionados (ledger `2026-07-20-kahneman-thaler-ct-prior-art`
> + `-gapclose`), posições independentes congeladas antes de agregar — a própria
> HYP-ORCH-NOISE aplicada a si mesma (A6). **Estatuto:** concluída, `resolved`. Criado 2026-07-20.

## Veredito

**O centro está vazio — e sobreviveu a busca adversarial.** A tríplice interseção
(CT-como-substrato × decomposição viés⊕ruído × camada de nudge) **não está ocupada**.
Dois agentes independentes com vetores opostos chegaram ao mesmo veredito sem se ver
(baixo ruído → alta confiança), confirmado por um 3º sweep nas bases não-web.

- **CT × nudge/choice-architecture: completamente vazia** — a parte mais forte da novidade.
- **A vizinhança normativa não modela o erro:** *Evidential Decision Theory via Partial
  Markov Categories* (Di Lavore–Román, LICS 2023) é decisão ideal, sem viés nem ruído. O
  movimento "viés = desvio de uma transformação natural" está **não reivindicado**.

## A costura da contribuição (achado mais valioso)

Os **statistical games** do programa do cérebro bayesiano composicional (Smithe,
arXiv:2109.04461; Braithwaite–Hedges–Smithe, MFCS 2023, arXiv:2305.06112) já fazem **três**
das quatro peças: juízo sobre substrato monoidal (lentes bayesianas sobre categorias de
Markov) + juiz como minimizador de um funcional de erro. **O que não fazem:** o erro é
*free energy*, um escalar — nunca refatorado na decomposição ortogonal **viés ⊕ ruído**, e
sem morfismo de nudge sobre o substrato. **Essa é a costura exata do paper.**

## Minas de título a desarmar (citar-e-desarmar)

"Categorização" (agrupar em baldes) ≠ "teoria das categorias". Um revisor pode brandir:

- **Fryer & Jackson**, *A Categorical Model of Cognition and Biased Decision-Making*
  (NBER w9579, 2003; BE-JTE 2008) — https://www.nber.org/papers/w9579
- **Ellis & Masatlioglu**, *Choice with endogenous categorization* (Review of Economic
  Studies, 2022) — mesma família.

## Vizinhos que o paper precisa citar (must-cite)

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
11. Costello & Watts, *Surprisingly rational: probability theory plus noise explains biases* — abordagem **não-categórica** do eixo ruído (contraste).

## Near-misses (CT-de-verdade, mas objeto errado)

- Phillips & Wilson, *Categorial Compositionality* (PLoS CB 2010) — objeto = sistematicidade.
- Ehresmann & Vanbremeersch, *Memory Evolutive Systems* (2007) — objeto = hierarquia/emergência.

## Risco residual (honestidade)

**MathSciNet ficou atrás de paywall institucional** (gateway LibLynx) — única base não
verificada. Mitigação: a base-irmã **zbMATH voltou vazia**, então MathSciNet quase certamente
não difere. Fecha 100% com acesso AMS institucional (query de 2 min). As demais bases
(zbMATH via API aberta, PhilPapers, Google Scholar, índice web) foram alcançadas.

## Auditoria

Ledger: `telemetry/agents/subagents-dispatch.yaml` — dispatches
`2026-07-20-kahneman-thaler-ct-prior-art` (2 explorers tensionados: cético-do-vazio ⊥
cartógrafo-de-vizinhos) e `2026-07-20-kahneman-thaler-ct-prior-art-gapclose` (1 explorer,
bases não-web). Queries por eixo e por base registradas nos retornos dos agentes.
