---
tags: [agents-communication-infra, runtime-v2, migration, architecture-inventory]
node_type: research-initial-definitions
is_session: false
layer: [architecture, application]
nature: [informational, reference]
status: draft
veracity: medium
conviction: high
version: 0.1.0
last_updated: 2026-08-03
---

# Runtime v2 Migration Inventory — Research Initial Definitions

## Context

O repositório `cyberalchemy-orchestrator` desenvolve infraestrutura para manter o trabalho de
agentes ligado aos objetivos, decisões, autoridades e evidências que lhe dão sentido. Hoje esse
trabalho reúne uma lane operacional `legacy-managed`, um piloto local ACI/APT, contratos e
discoveries para uma futura lane `runtime-managed`, além de ferramentas, pesquisas, planos,
telemetria e registros históricos no mesmo repositório.

A evolução para um runtime que compile skills em estruturas executáveis, persista uma autoridade
canônica e coordene agentes sem o agente do chat exige distinguir o que já existe e é confiável do
que é apenas candidato, parcial, duplicado ou ausente. Essa distinção importa para evitar tanto uma
reescrita desnecessária quanto a migração de acoplamentos e ambiguidades para o novo núcleo.

## Purpose

Este documento estabelece o contexto informacional para uma pesquisa governada sobre o estado
arquitetural atual e as opções de migração. Seus resultados informarão o inventário as-built, a
matriz de migração, o desenho do núcleo runtime futuro e a decisão posterior sobre branch,
worktree, reorganização no mesmo repositório ou extração para outro repositório.

## Research Question (Can be refined)

Quais capacidades, componentes, contratos, testes e limites do repositório atual podem ser
reutilizados, adaptados, substituídos ou arquivados para construir incrementalmente um núcleo
`runtime-managed` que compile skills em DAGs confirmáveis e coordene sua execução auditável?

## Confirmed Product Constraints

- O trabalho deve começar distinguindo o que já existe, o que não existe e o que pode ser adaptado.
- Alterações atuais do working tree não podem ser descartadas ou reclassificadas silenciosamente.
- A lane live `legacy-managed` permanece separada da futura lane `runtime-managed` até um cutover
  explicitamente autorizado e comprovado.
- O futuro runtime deve preservar uma autoridade canônica confirmada e impedir ampliações
  semânticas silenciosas durante a execução.
- Skills devem poder contribuir semântica reutilizável para uma estrutura concreta inspecionável
  antes da execução.
- O agente do chat não deve continuar sendo o coordenador implícito das transições depois da
  confirmação runtime.
- Claims de maturidade devem permanecer limitados pela evidência existente; documentação draft não
  prova implementação live.
- A decisão entre branch, worktree, reorganização ou novo repositório deve ser posterior ao
  inventário, não sua premissa.

## Current Evidence Baseline

- O README raiz distingue componentes live de teses e candidatos, incluindo control plane, ledger,
  skills operacionais, hooks e piloto ACI/APT
  ([README](../../../../../README.md)).
- A discovery de protocolos propõe compilar skill, profile, invocation e valores do usuário em um
  `DispatchCandidate`, depois em um `DispatchSpec` canônico confirmado; ela declara que o runtime
  genérico ainda não está implementado
  ([Agents Communication Protocols](../../discovery/agents-communication-protocols/README.md)).
- A ACI SPEC draft já descreve entidades e workflows como `ConfirmedDispatch`, `Run`,
  `AgentInvocationPlan`, `MaterializedAgentInvocation`, `AgentExecutionRequest`, journal, replay e
  reconciliação
  ([Domain](../../specs/domain.md), [Workflows](../../specs/workflows.md)).
- O repositório possui implementação de runtime local, migrations SQLite, artifacts, capabilities,
  projections, provenance, reveal/delivery e testes sob `implementations/server/runtime/` e
  `implementations/tests/runtime/`.
- A implementação candidata `dispatch_workflow.py` materializa launches iniciais, mas a própria
  discovery registra que ela ainda não percorre autonomamente um grafo completo.
- Na inspeção inicial de 2026-08-03, `master` era a única branch local, com 28 arquivos rastreados
  modificados e 49 arquivos não rastreados; esse estado ainda não constitui um snapshot Git
  recuperável por si só.

## Known Gaps

- Não há inventário consolidado que associe cada capacidade declarada à sua implementação, testes,
  consumidores e maturidade observada.
- Não está estabelecido quais módulos atuais formam um núcleo coerente e quais dependem da lane
  legacy, do host Claude, do ledger YAML ou de convenções de sessão.
- Não está demonstrado quanto do compilador skill-to-DAG, scheduler autônomo, Work Bus executável e
  provisionamento real de agentes já existe além de contratos ou slices locais.
- Não há matriz acordada de `reuse`, `adapt`, `rewrite` e `archive` com evidência por componente.
- Não há baseline único dos testes relevantes nem mapa explícito das lacunas de observabilidade e
  recuperação.
- Não está decidido se o núcleo futuro deve permanecer neste repositório, nascer em uma branch com
  worktree separado ou ser extraído posteriormente para outro repositório.
- Não há arquitetura-alvo mínima ratificada nem roadmap de migração com gates de evidência entre
  fases.
