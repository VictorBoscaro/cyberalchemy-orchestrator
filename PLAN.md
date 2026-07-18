# PLAN — Máquina de Conhecimento / Orquestrador de Agentes (semente)

> **Nome do repo:** provisório (`cyberalchemy-orchestrator`). Renomear.
> **Status:** PLANO / brainstorm. Não-revisado. Local, sem push. Claim ≤ proof.
> Este é o **objeto enxuto** — só o plano. O vault cresce em cima dele depois.
> Origem: sessão 2026-07-18 com Victor, após recon de 5 sondas.

---

## 0. O que este objeto é (e não é)

**É:** o plano mínimo para começar a construir um vault que modela **conhecimento**
(o que é, propriedades, relações, efeitos, quem age sobre ele) e, como primeira peça
concreta, um **orquestrador de agentes**.

**Não é:** o vault. Não é código. Não é uma afirmação de que algo já funciona. Nada
aqui está tipado em Lean ainda; onde eu digo "é uma categoria / é Yoneda", leia
**candidato a tipar**, não resultado.

---

## 1. Problema

Modelar conhecimento com estrutura suficiente para **produzir sistemas** — inclusive
a si mesmo, usando a si mesmo. A primeira fatia executável dessa ambição é um
orquestrador de agentes que investiga, sintetiza e critica conhecimento.

**Tese (registrada, não inflada).** O próprio trabalho é uma *instância* do framework
epistemológico que ele estuda. Isso **já está nomeado** no repo-mãe (BACKLOG A6,
"framework as its own instance") — não é claim novo, é a auto-aplicação apontada para
o processo de produção de conhecimento. Honestidade: uma instância *declarada* não é
prova de que o processo obedeça o framework; é uma descrição candidata, falsificável.

---

## 2. Mapa — material bruto que JÁ existe (o 1º trabalho é consolidar, não criar)

| Fonte | O que fornece | Onde | Acesso |
|---|---|---|---|
| robot-talks | investigação paralela por *concern* + confronto no eixo de tensão | `.claude/skills/robot-talks/` (Arcanum + lean-formalization) | local/público |
| subagents-strategy | router: trigger, human-gate, invariantes (tensão, claim≤proof) | `Arcanum` skills + `ARCANUM-SUBAGENT-STRATEGY.md` | local |
| DISPATCH-COMPOSITION-MODEL | ontologia de dispatch em 4 níveis, **edges tipados**, retry-bounded | `Arcanum/TO-VLAD/DISPATCH-COMPOSITION-MODEL.md` | público |
| MOGT | camada de decisão multi-objetivo {qualidade,custo,latência,segurança,escalação}; "decision receipt"; regime Nash-bargaining | `Arcanum/research/mogt-agentic-conversation/` | público — **experimentos não-iniciados** |
| trilha CT | monoidal categories / multicategories como framing formal | `Arcanum/research/monoidal-categories-multicategories/` | público |
| Orquestração por Pulso | ciclos Descida/Execução/Subida, buses efêmeros, função-custo (entropia/tokens/latência/fidelidade) | `business-philosopher/assuntos/orquestracao-multi-agente/` | local |
| Economia de atenção | tokens como moeda; carregar por redução-de-incerteza-por-token | `business-philosopher/assuntos/agents-optimization/` | local |
| domainspec-language | a "linguagem do sistema", já CT-orientada (objetos/morfismos, presheaf/Lan, FDM) | `domainspec-core/.../domainspec-language/` | local |
| protocolo de definições | fonte-única-de-verdade + estrutura por-termo + drift-audit | `Arcanum/definitions/DEFINITIONS.md` | público |
| âncoras Lean CT | resíduo, Yoneda-como-tradução, comma-connected (zig-zag) | `domainspec-lean-formalization/lean-formalization/` | local |

**Pendência crítica de acesso:** o doc de micro-economia que o Victor atribui ao
**Vladimir** NÃO foi encontrado em nada público (a org só tem Arcanum/mars/visualization;
domainspec-core é privado). Vlad aparece como *destinatário* dos memos `TO-VLAD*`, não
como autor de uma tese micro-econômica. **Não assumir que existe** — Victor aponta ou dá
acesso ao domainspec-core privado. Até lá, MOGT (game theory) é o análogo mais próximo.

---

## 3. Protocolo de definições (adotado de `Arcanum/definitions/DEFINITIONS.md`)

Regra flagged pelo Victor como necessária. Adotamos, com um campo a mais.

- **Fonte única de verdade.** Um termo é definido normativamente em UM lugar; downstream
  só explica/aplica/referencia, nunca redefine.
- **Estrutura por-termo:** Status · Termo+Aliases · Voz Científica/Formal · Interpretação
  Operacional · Voz Coloquial · Contexto de Domínio · **Fronteira** (o que fica de fora) ·
  Consumidores (paths) · Relacionadas.
- **IDs namespaced** (ex.: `DEF-ORCH-*` para este repo vs `DS-*`/`DEF-ARC-*` herdados).
- **Drift-audit:** um arquivo que rastreia divergência entre a definição normativa e os usos.
- **CAMPO NOVO — Tipo categórico:** cada definição carrega seu **mapping CT + âncora**
  (ver §4). Uma definição sem tipo categórico é candidata, não fechada.

---

## 4. Disciplina de mapping categórico (a espinha do vault)

**Regra.** Todo construto da linguagem-de-agentes → seu tipo em teoria das categorias +
âncora num arquivo real (regra herdada do CLAUDE.md do repo-mãe). Sonda e zig-zag são
apenas os dois primeiros exemplos.

**Tabela-semente (candidata, a ser tipada):**

| Construto | Tipo CT candidato | Âncora | Tipo do paralelo |
|---|---|---|---|
| sonda/probe (recon) | elemento generalizado / functor-of-points (Yoneda) | `YonedaAsTranslation.y`, `Probe.lean` | candidato forte |
| probe (experiment) | falsificação Popperiana | `experiment/SKILL.md` | rima nominal (≠ Yoneda) |
| zig-zag | identidades triangulares / `EqvGen` ida-e-volta | `P1Positive.CommaConnected`, `probe_zigzag_nf.lean` | candidato forte |
| sequential | composição `∘` | `connections` | estrutural |
| dispatch | diagrama tipado `J → Cat` | schema v0.6.0 | candidato |
| feedback / robot-talks | ? (2-célula / (co)limite de perspectivas) | — | aberto |
| residue de uma síntese | `FunctorialResidueStructure` / unit de Lan não-iso | `FunctorialResidueStructure.lean` | estrutural |

**Regra-do-verbo (a partir da direção do Victor).** Um verbo (implements/validates/
refines/…) é uma **ação sobre um objeto que deveria preservar a simetria do objeto sob
certas premissas**. Correção honesta do repo-mãe: um morfismo *qualquer* NÃO preserva
simetria — só isos/automorfismos preservam, e **a perda de simetria É o resíduo**
(memória `symmetry-invertible-lever-is-enrichment`). Logo o tipo de um verbo é:

> **verbo = morfismo + a condição sob a qual ele é simetria-preservante.**
> As "premissas" do Victor = exatamente essa condição. Fora dela, o verbo gera resíduo —
> e isso torna o resíduo **mensurável por verbo**, que é o que dá valor à disciplina.

**Claim-forte (rebaixado a candidato, com collapse-test).** Se `groups`=objetos e
`connections` tipadas compõem associativamente, a linguagem-de-agentes **é** uma
categoria (não *parece*), e o resíduo de uma orquestração é o mesmo objeto que o repo-mãe
estuda — fechando o laço A6. **Colapsa a decoração** se (a) zig-zag/feedback não compõem
associativamente (é só DAG anotado), ou (b) o resíduo-de-síntese não for o mesmo objeto
que `FunctorialResidueStructure` (e não só count-shaped). Tipar (a) ou (b) é a **primeira
obrigação real** — ver E3.

---

## 5. Plano por etapas (cada uma carrega seu collapse-test)

- **E0 — este PLAN.** Feito. Collapse: se não sobreviver à revisão de consistência, refaz.
- **E1 — vault mínimo + vocabulário de movimentos.** README + este plano + a tabela §4
  como doc inicial, ancorada em `DISPATCH-COMPOSITION-MODEL.md`. *Collapse:* se a tabela
  não fechar um mapping por construto, é glossário, não linguagem.
- **E2 — primeiras definições no protocolo §3.** ~5 termos (sonda, zig-zag, verbo,
  resíduo, dispatch) escritos com os 9 campos + tipo categórico. *Collapse:* se duas
  definições precisarem se redefinir mutuamente, a fronteira está errada.
- **E3 — testar o claim-forte (§4).** Tipar (a) leis de categoria OU (b) resíduo=mesmo-objeto.
  *Collapse-test já embutido:* se só der pra "provar" reexibindo a diamond, é decoração.
  Esta é a fatia que decide se o repo é matemática ou metáfora.
- **E4 — camada de decisão (MOGT) como "física" do orquestrador.** Adotar o "decision
  receipt" e os objetivos multi-critério. *Bloqueado* por: (i) o doc do Vladimir (acesso),
  (ii) MOGT ter zero experimento rodado — herda o mesmo "sem evidência ainda".

---

## Pendências / perguntas abertas

- **P-ACESSO.** doc micro-econômico do Vladimir: não-encontrado no público. Apontar/liberar
  `domainspec-core` privado, ou confirmar que é MOGT, ou que ainda não foi escrito.
- **P-NOME.** nome e local definitivos do repo (hoje: pasta-irmã local provisória).
- **P-ESCOPO.** o jogo das Torres (IDEAS.md I1) é projeto à parte ou interface sobre esta
  mesma máquina?
- **P-CT.** feedback e robot-talks ainda sem tipo CT — resolver em E2/E3.
