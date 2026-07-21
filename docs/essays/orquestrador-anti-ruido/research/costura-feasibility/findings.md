# Feasibility das costuras — viés⊕ruído (Kahneman×CT) e nudge (Thaler×CT)

> **Pergunta:** as duas costuras centrais do paper se tipam formalmente, ou são analogia?
> **Método:** dispatch tensionado `2026-07-20-costura-feasibility` (ledger) — dois pares
> construtor⊥colapsador (um por costura), posições independentes congeladas antes de
> sintetizar; gate `check-tension` passado (both PASS) antes do disparo. Auto-aplicação A6.
> **Estatuto:** concluída, `resolved`. Fonte provisória: `vault/hypothesis/orquestracao-anti-ruido.md`
> (HYP-ORCH-NOISE, candidate/exploratory — esta pesquisa a revisa). Criado 2026-07-20.

## Veredito global

**A tese NÃO quebra.** A **camada de design sobrevive inteira e sem métrica** (ambos os
colapsadores concedem isso explicitamente). A **camada formal/quantitativa precisa de dois
re-tipos** — e os dois aterram na **mesma casa: probabilidade categórica** (categorias de
Markov com estrutura estatística extra), *fora* da óptica nua e da ortogonalidade euclidiana.
Essa co-localização é o resultado estrutural mais forte que o dispatch produziu.

## Costura 1 — Kahneman×CT: `resíduo = viés ⊕ ruído`

**Veredito: `real-sob-condições X`.** Nem analogia (a rota Bregman fecha essa saída), nem
real incondicional (a ortogonalidade euclidiana metric-free é falsa).

**Convergência construtor↔colapsador** (Fritz e Leinster, sem se ver, no mesmo objeto — baixo
ruído): a decomposição é um **teorema real** via divergência de Bregman / geometria dualmente
plana (Pitágoras generalizado de Amari), **sem métrica de Fisher** — só o pareamento primal–dual
de Legendre. Média = único minimizador do Bregman esperado (Banerjee 2005) ⇒ agregação mecânica
= minimizador de ruído provadamente ótimo (a alavanca √N com justificativa, não retórica).

**A condição X, em três peças:**
1. **Adicionar exatamente um potencial de Legendre `F`** (entropia/free-energy generalizada).
   Dele saem `D_F`, coords duais `η=∇F`, o pareamento-como-ortogonalidade, a conexão e-afim.
   O split é **exclusivo** de Bregman (arXiv 2501.18581). *Achado de ouro:* esse `F` **é** a
   "escala comum ancorada / MAP" que a tese já usa — ela paga o imposto sem nomear.
2. **Slot-lock:** aniquilação exata do termo cruzado só com jogo aleatório no **primeiro**
   argumento `D_F(a,s)` (orientação M-projection / reverse-KL). Inverter → gap de Jensen ≠ 0.
3. **Composicionalidade — ABERTA, e é a fronteira real.** Decompôs *um* jogo; se viés⊕ruído
   é functorial ao longo da composição de lentes é não-provado (a composição mistura os dois
   slots de `D_F`). Fritz boundary-2 ≡ Leinster OBS2 (a DPI contrai KL, gira o resíduo para
   fora de ⊥) — os dois nomeiam a mesma fronteira dos dois lados.

**Força:** profundo mas taxado e pontual (teorema exato dado `F` e slot; não-nativo; status
composicional aberto). Não descarrega OBL-E3 — vive no funcional de perda, não na composição
de dispatch.

## Costura 2 — Thaler×CT: `nudge = processo ≠ conteúdo`

**Veredito: `real-sob-condições X`,** X = **re-tipar fora da óptica de juízo único.**

**Adjudicação do fork Myers⊥Jacobs → "vacuoso na óptica, real na fibra de acoplamento"
(endossado).** A 2-célula de Myers (`φ:M→M'`) é *verbatim* o gerador da relação de coend →
dicotomia sem meio: nudge **coerente** = identidade na óptica (vacuoso); **incoerente** = muda
`get/put` = tocou conteúdo. Como `M` é ligado por `∫^M`, não há functor `Optic→C` que devolva
"o resíduo" — "age em M, não em A/B" **não typechecka**. Myers concede exatamente esse buraco
(a fibração-do-resíduo ausente); Jacobs a fornece.

**Os mesmos dentes, relocados:** ambos concordam que processo≠conteúdo *tem* dentes e num
morfismo preserva-conteúdo/move-resíduo. Jacobs **subsume** Myers: os nudges reais (congelar,
independência-então-agregar) agem na **lei conjunta** `D(A^N)`. O independence-nudge
`J ↦ ⊗_i(π_i∗ J)` é **identidade em toda marginal** (conteúdo intacto) e **não-identidade no
conjunto** (mata correlação), detectado pela queda de variância na agregação (o claim √N-sobre-ρ).
Bem-definido nativamente porque **marginalização `D(A^N)→∏D(A)` é não-mônica**.

**Força:** nativamente bem-tipado (não-monicidade é fato de Markov, sem `F` importado), mas
payload positivo mais fino que o Seam 1. **Jacobs > Myers.**

## Meta cross-seam — uma casa só

As duas casas convergem apertado e **substantivamente**: o baricentro `ā=E[a]` (Seam 1) **é** a
agregação; a queda de variância do mean-pushforward (Seam 2) **é** a mesma agregação agindo no
conjunto. O `F` que o Seam 1 importa = a escala ancorada que torna juízos comensuráveis o
bastante para marginalizar/agregar no Seam 2. **Seam 1 dá o teorema de otimalidade da alavanca
(sob `F`); Seam 2 dá a ação bem-tipada dessa alavanca sobre a lei conjunta (nativa).** A
variância-sob-agregação de um é o detector do outro. Não dominam — **compõem**.

## Implicação para a tese-fonte (HYP-ORCH-NOISE) — três re-tipos

1. **`viés ⊕ ruído` / `viés ⊥ ruído` → promover "escala comum ancorada" de heurística a
   PORTADOR FORMAL.** Nomeá-la como o potencial de Legendre `F` / coordenada dualmente plana;
   declarar que a ortogonalidade e o √N são *licenciados por ela*, não por CT sozinha. Sem `F`,
   a forma honesta é `resíduo = viés * ruído` (duas contribuições entrópicas, não pernas
   ortogonais). Responde OQ-2 (rubrica por `dispatch_type` = escolha de `F`) e OQ-4 (as 6
   facetas = coords duais `η=∇F`).
2. **`√N` → revisão de regime.** Fato L2/CLT sob `F=‖·‖²`; fora do CLT a concentração é
   Sanov/large-deviation, **não 1/N**. Enunciar √N como caso gaussiano especial; garantia geral
   = "agregação = m-projeção na família plana, monótona sob independência", expoente condicional.
3. **Nudge processo≠conteúdo → re-tipo (não quebra).** Partir o vocabulário de nudge em duas
   classes tipadas: (a) **nudges de fibra-de-acoplamento** sobre `D(A^N)` para a agregação
   (independência, congelar-antes-do-canal, blinding); (b) **nudges de óptica/lente** só para o
   pipeline per-agente explorer→reviewer (compressor≠juiz). Afia o ajuste 1 (congelar = matar um
   acoplamento de ancoragem antes que se forme) e OQ-3 (persona = prior correlacionado = um
   acoplamento no estágio de julgar → neutralizar = ⊗ marginalizar).

## Guarda de fork

Ambos os seams são **dispersão, não dissenso** (`resolved`, não `dissent_irreconcilable`):
Fritz-b2 ≡ Leinster-OBS2; Jacobs subsume Myers e ambos convergem no morfismo preserva-marginal.
**O fork genuíno a escalar é COMPOSICIONALIDADE** — viés⊕ruído e o re-tipo do nudge são
functoriais ao longo da composição de estágios/dispatch, ou só pontuais por estágio? Isto deve
virar o **4º collapse-test** da tese: *a decomposição sobrevive à composição functorial dos
estágios, ou só pontualmente dentro de cada estágio?* A separação-por-estágio é a resposta de
*design*; a garantia *formal* através da composição é não-provada.

## Auditoria

Ledger `telemetry/agents/subagents-dispatch.yaml` — dispatch `2026-07-20-costura-feasibility`
(4 explorers tensionados: Fritz⊥Leinster, Myers⊥Jacobs; synthesizer Riehl). Gate `check-tension`
por Loregian+Capucci (infraestrutura, não registrada). Fontes técnicas: Banerjee JMLR 2005;
Pfau arXiv 2511.08789; arXiv 2501.18581; Amari (info geometry); Smithe arXiv 2306.17009 /
2109.04461; Riley arXiv 1809.00738; Clarke et al. arXiv 2001.07488; não-monicidade de
marginalização (Fritz-style Markov categories).
