---
tags: [agents, pipeline, anti-ruido, frame-refine]
node_type: conceptual
is_session: true
layer: architecture
nature: explanatory, technical
status: active
created: 2026-07-20
timestamp: 2026-07-20T21:19:13-03:00
expires: 2026-09-18
conversation_id: dc4ee8f8-d74d-4ec2-90e4-5a0db21e65f8
decisions_made: true
contradictions_found: true
specs_updated: [vault/hypothesis/orquestracao-anti-ruido.md, MAPPING.md, PLAN.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Introduz frame/refine/espinha-de-citação no coração da hipótese anti-ruído e pega dois erros ALTOS via review tensionada antes de propagarem — mas é design-only, ainda não implementado nem testado."
---

# Frame, refine e espinha de citação no pipeline de research (HYP-ORCH-NOISE)

## Summary

A sessão começou com "que repo é este?" e mapeou o cyberalchemy-orchestrator como semente de
uma máquina-de-conhecimento cujo primeiro alvo executável é um orquestrador de agentes, foco no
`dispatch_type` research. Consolidou os paralelos teoria-das-categorias↔técnicas num arquivo novo
`MAPPING.md` (a tabela-semente herdada do PLAN §4 + paralelos derivados da skill-base
`domainspec-subagents-strategy`: concat/synthesis = coproduto/pushout, feedback = 2-célula,
sonda-plural, meta/A6), e o PLAN §4 passou a apontar pra ele em vez de duplicar. Fez-se limpeza
factual: removeu o "jogo das Torres" (outro projeto) e resolveu que a "micro-economia" é o MOGT —
honestamente otimização multi-objetivo/Pareto, não teoria dos jogos, e design-only 0% empírico.
Dois subagentes de pesquisa (MOGT em ../Arcanum, CANONICAL-KINDS em ../domainspec-core) mapearam
os 4 estágios de um pipeline de research (qual assunto, filtrar papers, registrar papers, salvar
outputs); decidiu-se saída dupla (markdown + observabilidade) e a espinha de citação (chave de
paper, fluxo research→findings, toda claim referenciada). Introduziu-se `frame` (frente do
pipeline = escolha da lente/codomínio C) e `refine` (operador transversal), e decidiu-se que
essas ideias pertencem à hipótese anti-ruído `HYP-ORCH-NOISE`, não ao topo enxuto — editou-se
`vault/hypothesis/orquestracao-anti-ruido.md` com a seção frame/refine/citação, o nó F0 no
mermaid, linhas na tabela de design, OQ-6/7 e um collapse-test. Aplicou-se a própria disciplina
do repo (auto-aplicação A6): registrou-se no ledger um dispatch de review tensionado (n=2, eixo
fit-interno vs solidez-externa). Os revisores discordaram no ponto previsto e acharam dois ALTOs
— factual (o campo `question` é do kind `discovery` e opcional, não do `research`) e estrutural
(o frame carecia de um braço de ruído, exigido pela própria OQ-4) — além de rebaixar `refine`
(esteira fixa, não convergência-zig-zag) e furar a citação fail-closed (viés de
disponibilidade/Goodhart). Todos os consertos foram aplicados, `review.md` persistido, o dispatch
fechado como `resolved`, e o braço de ruído do frame virou a OQ-8; observou-se ainda edição
concorrente do mesmo doc por outra sessão (anotações `costura-feasibility`).

## Contradictions

- contradicts `vault/hypothesis/orquestracao-anti-ruido.md` — a review tensionada achou erro
  factual ALTO: o campo `question` pertence ao kind `discovery` e é opcional, não ao `research`
  como o doc afirmava antes do conserto (corrigido nesta sessão).
- questions `vault/hypothesis/orquestracao-anti-ruido.md` — a review apontou lacuna estrutural
  ALTA: o `frame` carecia de um braço de ruído exigido pela própria OQ-4; registrada como OQ-8,
  ainda não construída.
- validates `vault/hypothesis/orquestracao-anti-ruido.md` — dispatch de review fechado como
  `resolved` após todos os consertos aplicados, elevando a veracidade das adições frame/refine/citação.

## Open questions

- "Construir conhecimento" e "executar coisas" na mesma interface são dois `dispatch_type` da
  mesma máquina, ou dois **modos** dela? Decidido que a interface é única com funções diferentes;
  não decidido se a distinção é de tipo ou de modo — muda a arquitetura.

## Next steps

1. Atacar **OQ-8** — o braço de ruído do frame — reusando a engenharia de
   distribuição-como-ruído da OQ-4 (N frames independentes logados cegos, dispersão como sinal
   de primeira classe); não inventar métrica nova. Em `vault/hypothesis/orquestracao-anti-ruido.md`.

## Recommendation

De todos os itens forward, o keystone é o Next step 1 (OQ-8, o braço de ruído do frame),
reforçado pela aresta `questions` sobre esse mesmo furo. A licença é a review fechada como
`resolved`, que converteu a lacuna estrutural em open-question precisa em vez de design vago — o
caminho está localizado, falta o desenho. Priorizá-lo antes da Open question de arquitetura
(dispatch_type vs modos), que pode esperar até haver um segundo tipo real para tensionar.

## Files touched

- MAPPING.md
- README.md
- PLAN.md
- vault/hypothesis/orquestracao-anti-ruido.md
- docs/essays/orquestrador-anti-ruido/research/frame-refine-review/review.md
- telemetry/agents/subagents-dispatch.yaml
