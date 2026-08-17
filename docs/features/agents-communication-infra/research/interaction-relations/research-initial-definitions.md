---
tags: [agents-communication-infra, agent-interaction, typed-graph, workflow-relations, interaction-semantics]
node_type: research-initial-definitions
is_session: false
layer: [architecture, domain, application]
nature: [informational, reference]
status: draft
veracity: medium
conviction: high
version: 0.3.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Relations — Research Initial Definitions

## Context

O repositório `cyberalchemy-orchestrator` desenvolve infraestrutura para manter o trabalho de
múltiplos agentes ligado aos objetivos, decisões, suposições, ações e evidências que lhe dão
sentido. A feature `agents-communication-infra` concentra os contratos candidatos e as capacidades
parciais pelas quais estruturas confirmadas, protocolos reutilizáveis, mensagens, resultados e
transições de execução podem permanecer relacionados sem depender implicitamente do agente do chat.

Os workflows atuais expressam relações entre partes do trabalho por meio de grafos, `connections`,
recipes, regras descritas em documentos e coordenação do parent. O produto deve continuar sendo
baseado em grafos, mas suas arestas precisam carregar relações tipadas cujos tipos expressem
diferenças semânticas reais. Ainda não há uma caracterização estável da menor base de tipos capaz de
representar os padrões de interação necessários sem transformar topologia, política, autoridade e
efeito de runtime em rótulos de aresta indistintos.

## Purpose

Este documento estabelece o contexto informacional para uma pesquisa governada que informará uma
discovery posterior sobre relações tipadas em grafos de trabalho multiagente. A compreensão
resultante deverá permitir avaliar qual base reutilizável, se alguma, é suficiente para construir os
padrões de interação relevantes, quais diferenças precisam permanecer distintas e quais limites uma
decisão arquitetural posterior deverá preservar.

Ele não seleciona antecipadamente os tipos de relação, não presume que padrões nomeados sejam
primitivos, não define schema, serviço ou máquina de estados e não autoriza alteração do runtime. A
pesquisa poderá concluir que existem famílias incompatíveis de relações ou que certos padrões só são
representáveis como subgrafos compostos, e não como um único tipo de aresta.

## Research Question (Can be refined)

Qual é, se existir, a menor base extensível de relações tipadas capaz de reconstruir em grafos os
padrões de interação multiagente observados e relevantes — incluindo `sequential`, review,
`zig-zag`, feedback e robot-talks — sem perder diferenças de dependência, fluxo de evidência,
autoridade, coordenação, término, falha ou efeito executável? O que as soluções contemporâneas
externas de comunicação de agentes e sistemas já demonstram sobre essa base e sobre seus limites?

## Confirmed Product Constraints

- Por direção do usuário nesta abertura, a pesquisa deve preceder a discovery e permanecer sob
  `docs/features/agents-communication-infra/research/interaction-relations/` enquanto não houver
  evidência para um owner de feature independente.
- O objetivo de produto confirmado é permitir que diferentes maneiras de relacionar trabalho
  multiagente possam ser configuradas como grafos com relações tipadas. Cada tipo aceito precisa
  corresponder a uma diferença semântica demonstrável; nomes diferentes não justificam tipos
  diferentes por si só.
- O grafo é a estrutura de composição confirmada. A pesquisa deve determinar os tipos de relação e
  suas distinções, sem reabrir a decisão de representar o trabalho como grafo.
- Padrões nomeados como `zig-zag`, feedback e robot-talks devem poder emergir como tipos primitivos,
  subgrafos compostos ou famílias separadas conforme a evidência; o nome atual não decide sua
  classificação.
- A decisão posterior deve considerar soluções contemporâneas externas e seus contratos
  executáveis, não apenas precedentes internos. Alegações de estado atual precisam ser verificadas
  em fontes primárias vigentes no momento da pesquisa.
- "Todos os tipos possíveis" é uma direção de expressividade, não uma alegação demonstrável sobre
  um domínio aberto. A base precisa cobrir o corpus declarado, explicitar seus limites e admitir
  extensão sem apagar as diferenças semânticas já preservadas.
- ACI Protocol Governance possui `SkillExecutionProfile`, `SkillProtocolBinding`, recipe/DAG e a
  compilação determinística somente até um `DispatchCandidate` não autoritativo
  ([ACI-PG-001](../../../../decisions/aci-protocol-governance-ownership.md) e
  [Protocol Compilation](../../specs/protocol-compilation.md)).
- Resolução efetiva de capabilities e `DispatchSpec` final permanecem com a confirmação ACI;
  confirmação humana, `ConfirmedDispatch` e `Run` não são efeitos de uma recipe ou de um candidato
  compilado ([Protocol Compilation](../../specs/protocol-compilation.md#ownership-and-authority-boundary)).
- Scheduling, attempts, effects, recovery e replay permanecem sob o runtime/kernel; capabilities,
  providers, tools, permissions e sandbox permanecem sob Agent Tools e Delegated Supervision;
  routing e entrega de mensagens permanecem sob os contratos do Work Bus. A pesquisa não pode
  transferir esses owners por escolha terminológica
  ([Agents Communication Protocols](../../discovery/agents-communication-protocols/README.md#1-business-context)).
- O DAG acíclico e os quatro `edge_kind` do contrato V1 são limites do primeiro slice implementado,
  não uma decisão de suficiência para a linguagem futura
  ([Protocol Compilation](../../specs/protocol-compilation.md#dag-validity)).

## Current Evidence Baseline

- O schema atual reconhece `sequential`, `zig-zag` e `feedback`, mas a própria
  arquitetura da feature afirma que essas `connections` ainda não constituem um runtime de
  comunicação entre agentes e que a sessão continua exercendo integração implicitamente
  ([ACI README](../../README.md#3-estado-atual-e-estado-alvo)).
- O slice implementado de `ProtocolRecipe` V1 admite somente um pacote built-in congelado, com dois
  casos read-only, e produz deterministicamente um `DispatchCandidate` não autoritativo. Ele não
  oferece registry, admissão arbitrária de recipes nem runtime de protocolos, e a interface não
  agenda nem executa o grafo
  ([Protocol Compilation](../../specs/protocol-compilation.md#contract-status-and-objective)).
- O `ProtocolRecipe` V1 admite um DAG finito, acíclico e fechado, com arestas `depends_on`,
  `review_of`, `feeds` e `gates`. Esse contrato não representa ciclos
  ([Protocol Compilation](../../specs/protocol-compilation.md#protocolrecipe) e
  [DAG validity](../../specs/protocol-compilation.md#dag-validity)).
- O adaptador operacional da lane `legacy-managed` aceita workflows sem conexões e workflows com
  conexões `sequential`; para cada aresta `sequential` declarada, exige um handoff receipt já
  materializado. Outras semânticas são bloqueadas explicitamente, e os testes preservam a rejeição
  de `feedback` e `zig-zag`
  ([`compile_bound_launch_plan`](../../../../../implementations/server/runtime/dispatch_workflow.py#L246)
  e [`test_feedback_zigzag_reverse_and_unknown_edge_semantics_fail_explicitly`](../../../../../implementations/tests/runtime/test_runtime_type_bootstrap_abuse.py#L207)).
- O serviço de host workflow da lane `legacy-managed` possui mecanismos para vincular turnos
  posteriores ao mesmo seat, exigir um template de follow-up declarado, verificar terminalidade do
  turno anterior e registrar outputs aceitos. Esses mecanismos não constituem, por si, um
  interpretador geral de relações
  ([`bind_host_workflow_turn`](../../../../../implementations/server/runtime/service.py#L5522) e
  [`complete_host_workflow_turn`](../../../../../implementations/server/runtime/service.py#L5850)).
- O dispatch `knowledge-formation` usa `zig-zag` junto de um scheduler textual separado que define
  writer, três skeptics, revisão, reconfirmação, convergência e contador compartilhado. Assim, o
  rótulo da conexão sozinho não contém o protocolo observado
  ([knowledge-formation dispatch](../../../../../research/knowledge-formation/dispatch.yaml) e
  [ledger](../../../../../research/knowledge-formation/LEDGER.md)).
- Review, research, experiment e robot-talks fornecem outros padrões locais em que ordem,
  independência, confronto, confirmação, síntese e autoridade não são redutíveis ao simples fato de
  dois grupos estarem conectados. Esses padrões constituem evidência de produto a ser distinguida
  das superfícies que atualmente os declaram ou executam
  ([review](../../../../../.agents/skills/review/SKILL.md),
  [research](../../../../../.agents/skills/research/SKILL.md),
  [experiment](../../../../../.agents/skills/experiment/SKILL.md) e
  [robot-talks](../../../../../.agents/skills/robot-talks/SKILL.md)).
- A arquitetura candidata da feature mantém `feedback` e `zig-zag` fora dos primeiros slices e
  registra como aberta a semântica de `feedback`
  ([ACI README](../../README.md#fase-2--robustez-e-topologias)).

## Known Gaps

- Não está estabelecido quais tipos de relação são necessários para reconstruir os padrões locais
  nem quais nomes atuais designam apenas topologias ou protocolos compostos.
- Não está estabelecido quais diferenças pertencem à semântica da aresta e quais pertencem a
  composição do grafo, política, coordenação, autoridade ou execução.
- Não está estabelecido quais entidades uma relação tipada conecta: agentes, seats, papéis, grupos,
  turnos, estados, artefatos, resultados ou outra unidade ainda não identificada.
- Não há evidência de que uma base candidata seja mínima: nenhum tipo possui ainda um testemunho de
  necessidade mostrando o que deixa de ser representável quando ele é removido.
- Não há evidência de suficiência: `sequential`, review, `zig-zag`, feedback e robot-talks ainda não
  foram reconstruídos sobre uma mesma base candidata com suas diferenças preservadas.
- Não está estabelecido quais relações são composáveis, quais tipos restringem sua composição nem
  quais propriedades precisam sobreviver à composição.
- Não está estabelecido como representar iteração, convergência e revisão limitada sem confundir
  relação tipada, subgrafo de protocolo, ciclo de runtime e política de término.
- Não há mapping demonstrado entre os padrões de workflow, `ProtocolRecipe`, as `connections`
  legadas, a autoridade confirmada, o Work Bus e os bindings/follow-ups executados pelo runtime.
- Não há levantamento verificável das soluções contemporâneas externas, de suas primitivas, de suas
  garantias executáveis, de sua maturidade ou das lacunas que deixam para este produto.
- Não está estabelecido como estender a base para relações não presentes no corpus sem transformar
  cada novo padrão em lógica especial nem enfraquecer os tipos existentes.
- Não está estabelecido se existe uma base única ou famílias incompatíveis, nem em qual boundary
  elas poderiam existir sem transferir responsabilidades de Protocol Governance, confirmação ACI,
  Agent Tools, Delegated Supervision, runtime ou Work Bus.

## Connections

| Document | Type | Description |
|---|---|---|
| [ACI-PG-001](../../../../decisions/aci-protocol-governance-ownership.md) | `depends-on` | Fixa a autoridade de Protocol Governance e o limite não autoritativo de `DispatchCandidate`. |
| [Agents Communication Protocols](../../discovery/agents-communication-protocols/README.md) | `depends-on` | Preserva o owner de protocol governance e a fronteira entre candidato, confirmação e execução. |
| [Protocol Compilation](../../specs/protocol-compilation.md) | `depends-on` | Fornece o contrato V1 já implementado e seus limites deliberados. |
| [ACI README](../../README.md) | `contextualizes` | Registra o estado-alvo da feature, os tipos de conexão precedentes e as topologias ainda diferidas. |
| [Knowledge Formation dispatch](../../../../../research/knowledge-formation/dispatch.yaml) | `contextualizes` | Fornece uma ocorrência concreta em que o rótulo `zig-zag` depende de protocolo adicional. |
