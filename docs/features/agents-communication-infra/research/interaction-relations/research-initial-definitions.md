---
tags: [agents-communication-infra, agent-interaction, workflow-relations, interaction-semantics]
node_type: research-initial-definitions
is_session: false
layer: [architecture, domain, application]
nature: [informational, reference]
status: draft
veracity: medium
conviction: high
version: 0.2.0
last_updated: 2026-08-15
---

# Interaction Relations — Research Initial Definitions

## Context

O repositório `cyberalchemy-orchestrator` desenvolve infraestrutura para manter o trabalho de
múltiplos agentes ligado aos objetivos, decisões, suposições, ações e evidências que lhe dão
sentido. A feature `agents-communication-infra` concentra os contratos candidatos e as capacidades
parciais pelas quais estruturas confirmadas, protocolos reutilizáveis, mensagens, resultados e
transições de execução podem permanecer relacionados sem depender implicitamente do agente do chat.

Os workflows atuais expressam relações entre partes do trabalho por meio de `connections`, recipes,
regras descritas em documentos e coordenação do parent. Ainda não há uma caracterização estável do
que permanece semanticamente igual ou diferente entre essas relações. Isso dificulta saber se novos
modos de interação podem compartilhar estruturas reutilizáveis ou se exigem famílias distintas,
e aumenta o risco de misturar relação de domínio, coordenação, autoridade, política e efeito de
runtime sob um mesmo rótulo.

## Purpose

Este documento estabelece o contexto informacional para uma pesquisa governada que informará uma
discovery posterior sobre relações de interação em workflows multiagente. A compreensão resultante
deverá permitir avaliar se alguma abstração reutilizável é justificada, qual problema ela resolve e
quais distinções e limites uma decisão arquitetural posterior precisaria preservar.

Ele não seleciona elementos primitivos, não presume uma composição formal, não define um serviço,
schema ou máquina de estados e não autoriza alteração do runtime. A pesquisa poderá concluir que não
existe uma base única, que existem famílias incompatíveis ou que a abstração útil está em outro nível
que não relações entre agentes concretos.

## Research Question (Can be refined)

Considerando as `connections` legadas, o grafo limitado de `ProtocolRecipe` V1, os
bindings/follow-ups da lane `legacy-managed` e as relações previstas nos contratos do Work Bus, o
que, se algo, permanece invariável entre essas superfícies e o que isso implica sobre a pertinência
de estruturas reutilizáveis? Nesta pesquisa, uma diferença será semanticamente consequente quando
alterar dependência entre trabalhos, fluxo de evidência, autoridade, coordenação ou efeito
executável.

## Confirmed Product Constraints

- Por direção do usuário nesta abertura, a pesquisa deve preceder a discovery e permanecer sob
  `docs/features/agents-communication-infra/research/interaction-relations/` enquanto não houver
  evidência para um owner de feature independente.
- O objetivo de produto confirmado é permitir que diferentes maneiras de relacionar trabalho
  multiagente possam ser configuradas. Isso não determina se compartilharão implementação,
  representação ou mecanismo de execução.
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
- A arquitetura candidata da feature mantém `feedback` e `zig-zag` fora dos primeiros slices e
  registra como aberta a semântica de `feedback`
  ([ACI README](../../README.md#fase-2--robustez-e-topologias)).

## Known Gaps

- Não está estabelecido quais diferenças entre as relações observadas pertencem à semântica do
  trabalho e quais pertencem à coordenação, autoridade, política ou execução.
- Não está estabelecido se os nomes atuais designam classes estáveis ou agrupam comportamentos
  diferentes por precedente histórico.
- Não está estabelecido quais entidades são relacionadas: agentes, seats, papéis, grupos, turnos,
  estados, artefatos, resultados ou outra unidade ainda não identificada.
- Não há evidência de uma decomposição mínima, suficiente ou estável das interações observadas.
- Não está estabelecido se as relações relevantes são composáveis, quais tipos restringem sua
  composição nem quais propriedades formais, se alguma, são preservadas.
- Não está estabelecido como representar relações iterativas ou de revisão limitada sem confundir
  protocolo, ciclo de runtime e política de término.
- Não há mapping demonstrado entre `ProtocolRecipe`, as `connections` legadas, a autoridade
  confirmada e os bindings/follow-ups executados pelo runtime.
- Não está estabelecido quais partes do protocolo `knowledge-formation` são reutilizáveis e quais
  pertencem somente àquele dispatch.
- Não está estabelecido se existe uma estrutura comum entre as relações observadas nem em qual
  boundary ela poderia existir sem transferir responsabilidades de Protocol Governance, confirmação
  ACI, Agent Tools, Delegated Supervision, runtime ou Work Bus.

## Connections

| Document | Type | Description |
|---|---|---|
| [ACI-PG-001](../../../../decisions/aci-protocol-governance-ownership.md) | `depends-on` | Fixa a autoridade de Protocol Governance e o limite não autoritativo de `DispatchCandidate`. |
| [Agents Communication Protocols](../../discovery/agents-communication-protocols/README.md) | `depends-on` | Preserva o owner de protocol governance e a fronteira entre candidato, confirmação e execução. |
| [Protocol Compilation](../../specs/protocol-compilation.md) | `depends-on` | Fornece o contrato V1 já implementado e seus limites deliberados. |
| [ACI README](../../README.md) | `contextualizes` | Registra o estado-alvo da feature, os tipos de conexão precedentes e as topologias ainda diferidas. |
| [Knowledge Formation dispatch](../../../../../research/knowledge-formation/dispatch.yaml) | `contextualizes` | Fornece uma ocorrência concreta em que o rótulo `zig-zag` depende de protocolo adicional. |
