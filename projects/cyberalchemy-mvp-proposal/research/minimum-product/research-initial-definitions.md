---
tags: [cyberalchemy-mvp-proposal, research, product-minimum, features]
artifact_kind: research-initial-definitions
layer: project
version: 0.4.0
created_at: 2026-08-15T14:03:57-03:00
updated_at: 2026-08-15T14:50:34-03:00
---

# Minimum Product — Initial Research Definitions

## Context

CyberAlchemy MVP Proposal busca definir um produto integrado no qual um Orchestrator permanece no
chat, compreende a intenção do usuário e governa trabalho realizado fora de sua janela de contexto.
Uma infraestrutura determinística deve conectar decisões, estado do projeto, delegação, execução e
evidências sem transformar o chat em executor direto.

O projeto já nomeia diversas capacidades necessárias, mas ainda não estabeleceu quais delas formam
uma experiência mínima coerente de produto. Essa distinção importa porque uma lista de componentes
de infraestrutura não demonstra, por si só, um resultado utilizável de ponta a ponta.

## Purpose

Este documento estabelece o contexto inicial para uma pesquisa que informará a definição das
features do produto mínimo e, depois, a priorização do que deve ser integrado, adaptado ou criado.
Ele preserva o ponto de partida sem decidir a arquitetura, o plano de implementação ou a composição
do Dispatch de pesquisa.

## Research Question (Can be refined)

Qual é o menor conjunto coerente de features que permite ao CyberAlchemy acompanhar um usuário desde
a criação de um repositório autossuficiente e a formação de suas primeiras specs até trabalho
governado, observável, revisado, implementado e ligado ao objetivo maior — considerando as
capacidades que já existem nos repositórios?

## Confirmed Product Constraints

- O Orchestrator é o agente principal do chat e não executa diretamente pesquisa, alteração de
  arquivos ou trabalho especializado.
- O Orchestrator pode invocar Dispatches e outras capacidades autorizadas.
- Workers especializados existem somente dentro de Dispatches.
- Scouts realizam investigações pequenas e delimitadas e são nós terminais.
- O Superinterviewer pode ser usado diretamente ou invocado por pessoas e agentes, inclusive pelo
  Orchestrator, e pode invocar Scouts.
- Craft é o sistema canônico de estado do projeto e deve preservar decisões, tarefas, perguntas,
  assumptions, contradições, evidências e próximos movimentos.
- O produto deve contemplar Inventory e mecanismos de ledger. A divisão de responsabilidades e
  autoridade entre eles ainda precisa ser verificada.
- A jornada inicial começa antes de existir uma spec aceita: o produto deve ajudar o usuário a criar
  e refinar essa spec.
- O produto deve permitir criar um repositório que já nasça com schemas para alguns artefatos e com
  um conjunto inicial de tipos canônicos.
- O repositório criado deve ser autossuficiente e poder ser extraído do repositório de origem. Skills,
  serviços e outros recursos importados precisam permanecer dependências explícitas e provenanceadas;
  o mecanismo para isso ainda não está definido.
- Inicialmente podem ser usados os tipos canônicos existentes neste ecossistema, mas o modelo deve
  admitir que o projeto crie seus próprios tipos.
- O produto mínimo precisa contemplar Dispatch, revisão e implementação de especificações, além da
  governança de decisões e etapas mantida pelo estado do projeto.
- Grupos de subagentes precisam ser invocáveis com trabalho observável, rastreável e explicitamente
  ligado ao objetivo maior.
- `Research` é um modo de trabalho multiagente realizado por meio de Dispatch. Seu nome de produto
  pode mudar sem alterar essa posição arquitetural.
- A janela de contexto do Orchestrator deve ser preservada com apenas informação relevante e
  recuperável.
- O estado real dos serviços existentes deve ser verificado nos repositórios antes de qualquer
  capacidade ser tratada como pronta ou integrada.

## Current Evidence Baseline

- O [README do projeto](../../README.md) registra as fronteiras atuais entre Orchestrator,
  Coordination Runtime, Superinterviewer, Scouts, Dispatches, workers, Craft e a superfície de
  skills.
- A [sessão de fundação](../../../../sessions/2026-08-14-1756-cyberalchemy-mvp-proposal.md) registra
  que o review governado não chegou a abrir um Dispatch: sua topologia requeria `zig-zag`, enquanto
  o compilador observado aceitava apenas conexões `sequential`.
- Como observação preliminar, o repositório contém artefatos nomeados para Dispatch, review,
  implementação de specs, Craft, inventory, observabilidade de skills e estratégias de subagentes.
  A presença desses artefatos não demonstra, sem inspeção adicional, integração operacional ou
  prontidão de produto.
- Ainda não existe neste projeto uma definição aceita da jornada mínima completa, do catálogo de
  features ou dos critérios que distinguem produto mínimo de infraestrutura habilitadora.

## Known Gaps

- Não está definido qual resultado concreto o usuário obtém na primeira jornada completa, desde a
  criação do repositório até o primeiro ciclo de trabalho encerrado.
- Não está definido quais arquivos recebem schemas no bootstrap nem quais tipos canônicos são
  indispensáveis para o primeiro ciclo.
- Não está definido como um projeto cria, valida, promove e torna portáveis seus próprios tipos.
- Não está definido o contrato operacional de autossuficiência, importação e extração de um projeto.
- Não está definido o contrato de identidade e ligação entre Craft Ledger, Inventory, journal do
  runtime e Dispatch Audit Ledger.
- Não está claro quais capacidades são features visíveis, serviços internos ou mecanismos de
  governança compartilhados.
- Não se sabe quais partes de Dispatch, review, implementação de specs, Craft/inventory e
  observabilidade estão implementadas, apenas especificadas ou atualmente incompatíveis entre si.
- Não está definido como uma intenção vira spec, como essa spec é validada e selecionada para
  implementação, nem como a mudança resultante é revisada e reconciliada com decisões e evidências
  anteriores.
- Não está definido quando o Orchestrator usa Superinterviewer, Scout, uma skill direta ou um
  Dispatch.
- Não está definido qual projeção mínima do estado retorna ao chat nem como detalhes são recuperados
  sem contaminar o contexto principal.
- Não está claro se reviewers constituem uma feature própria ou um papel reutilizável dentro de
  diferentes Dispatches.
- Não está definido quais modos de Dispatch pertencem ao produto mínimo nem quais nomes devem ser
  apresentados ao usuário para `research`, review, implementação e outras composições.
- Não está definido quais métricas de skills e Dispatches são necessárias para operar o produto
  mínimo, em oposição a uma camada posterior de melhoria.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [CyberAlchemy MVP Proposal](../../README.md) | `derives-from` | Fornece as decisões e fronteiras já confirmadas para o produto. |
| [Sessão de fundação](../../../../sessions/2026-08-14-1756-cyberalchemy-mvp-proposal.md) | `contextualizes` | Preserva a origem conversacional das decisões e o blocker observado no fluxo de review. |
