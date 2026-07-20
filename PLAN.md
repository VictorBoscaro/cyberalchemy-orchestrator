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

**Resolvido (2026-07-20):** a "micro-economia" é o **MOGT**, em
`Arcanum/research/mogt-agentic-conversation/` (público), não um doc separado. Não é
pendência de acesso; é a camada de decisão do orquestrador (ver E4). Correção honesta: o
nome "teoria dos jogos" superestima — é **otimização multi-objetivo** (objetivos
{quality, cost, latency, safety, escalation_risk}, dominância de Pareto, regime
`bargaining_guided` opcional). Estatuto: **design + dry-run, 0% empírico** — herda o
"claim ≤ proof" (todas as claims "insufficient evidence", experimentos "not started").
Valor maior para nós está no **scaffolding de research** ao redor (catálogo/ledger/inventory/
receipt), não no modelo de decisão em si.

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

**A tabela vive em [MAPPING.md](MAPPING.md)** (fonte-única do mapping, protocolo §3): §1 = a
tabela-semente (7 construtos herdados), §2 = os paralelos derivados da skill-base
`domainspec-subagents-strategy` (concat/synthesis, feedback-como-2-cell, sonda-plural,
meta/A6, …). Não duplicar aqui — editar lá.

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

- **P-NOME.** nome e local definitivos do repo (hoje: pasta-irmã local provisória).
- **P-CT.** feedback e robot-talks ainda sem tipo CT — resolver em E2/E3.

*(Resolvido: a "micro-economia" é o MOGT — teoria dos jogos — em
`Arcanum/research/mogt-agentic-conversation/`, não um doc separado do Vladimir. O jogo das
Torres é outro projeto, fora daqui.)*
