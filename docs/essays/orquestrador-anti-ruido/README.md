# Ensaio — O Orquestrador como Máquina de Redução de Ruído

> **Estatuto:** rascunho alto-nível, **não-revisado**, local. `Claim ≤ proof`. Este README
> levanta o paper (tese, refs, contribuição) para *depois* entrar no detalhe. Deriva de
> `vault/hypothesis/orquestracao-anti-ruido.md` (`HYP-ORCH-NOISE`). Criado 2026-07-20.

## Tese (uma frase)

Um orquestrador de agentes é, formalmente, uma **máquina de redução de erro de juízo**;
os referenciais **compõem** — não competem — sobre a alavanca nativa do repo
`resíduo = viés ⊕ ruído`.

## Os níveis (decisão de escopo em aberto)

| Nível | Papel | Estatuto no paper |
|---|---|---|
| **Teoria das categorias** | *em quê* — substrato de tipo | **pilar central** |
| **Kahneman / *Noise*** | *por quê* — modelo de erro (viés ⊕ ruído) | **pilar central** |
| **Thaler / *Nudge*** | *como* — arquitetura de escolha do processo | **pilar central** (decisão 2026-07-20: primário por ora) |

> **Decisão (2026-07-20, revisada).** Os **três** entram como argumentos primários. Chegou-se
> a considerar rebaixar Thaler a corolário (dois pilares de registro homogêneo, mais foco),
> **mas** a varredura de prior-art mostrou que **CT × nudge é a célula mais vazia de todas** —
> o território de novidade mais indiscutível. Largar Thaler abriria mão disso. Portanto Thaler
> é primário e **exige pesquisa própria de feasibility** (nudge = morfismo sobre a lente/o
> processo, nunca sobre o conteúdo do juízo — isso se tipa, ou é analogia?).

## Contribuição nova (a costura)

Refatorar o funcional de erro **escalar** dos *statistical games* composicionais
(Smithe; Braithwaite–Hedges–Smithe) na decomposição **ortogonal viés ⊕ ruído** do *Noise*,
sobre substrato de **categorias de Markov** (Fritz) — e (se Thaler entrar) adicionar um
**morfismo Nudge** que age sobre o *processo* (a lente/o tipo), nunca sobre o conteúdo.
Ninguém uniu esses referenciais: **provado por varredura auditável em 5 bases** (ver
`research/prior-art-ct-kahneman-thaler/`).

## Argumento-âncora — `viés ⊥ ruído`

Viés pede **tensão/oposição**; ruído pede **independência/agregação** — ferramentas
contraditórias, resolvidas por **separação de estágio** (tensão no *gerar*, independência no
*avaliar*). O próprio processo de produção deste paper é uma instância disso (auto-aplicação,
PLAN.md §1 A6).

## Referências (alto nível, agrupadas)

- **Fundamentos do erro:** Kahneman, Sibony & Sunstein, *Noise* (2021); Thaler & Sunstein,
  *Nudge* (2008).
- **Substrato categórico:** Fritz, *Markov categories* (Adv. Math. 2020); Ghani–Hedges–
  Winschel–Zahn, *Compositional Game Theory* (LICS 2018); Di Lavore–Román, *Evidential
  Decision Theory via Partial Markov Categories* (LICS 2023).
- **A costura / vizinho mais próximo:** Smithe, *Compositional Bayesian Brain* (2022);
  Braithwaite–Hedges–Smithe (MFCS 2023); Capucci et al., *Categorical Cybernetics* (2021).
- **Citar-e-desarmar (minas de título — "categorização" ≠ "categorias"):** Fryer–Jackson
  (2003/08); Ellis–Masatlioglu (2022).
- **Abordagem não-categórica do eixo ruído (contraste):** Costello & Watts, *Surprisingly
  rational: probability theory plus noise*.
- **Substrato do próprio repo:** `HYP-ORCH-NOISE`, `MAPPING.md`, disciplina anti-viés
  (`check-tension`, P5/P14).

## Estrutura (esboço, a detalhar depois)

1. O juízo tem dois erros ortogonais (viés ⊕ ruído) — e o orquestrador os toma o tempo todo.
2. CT como substrato de tipo — por que o erro precisa de um chão categórico.
3. A costura: decompor o funcional dos statistical games em viés ⊕ ruído.
4. `viés ⊥ ruído` → separação de estágio (tensão vs independência).
5. (minor) Nudge como arquitetura do processo.
6. Auto-aplicação (A6) + collapse-tests.

## Pesquisas (`research/`)

Container de investigações, uma pasta por pergunta:

- **`prior-art-ct-kahneman-thaler/`** — a novidade já foi feita? Veredito: **centro vazio**
  (auditável, 5 bases). ✅ concluída.
