---
tags: [orchestration, agents, dispatch, architecture, ledger]
node_type: discovery
is_session: true
layer: [architecture, domain, application]
nature: [explanatory, technical]
status: active
created: 2026-07-26
timestamp: 2026-07-26T02:44:30-03:00
expires: 2026-09-24
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "A sessão corrigiu uma recomendação estratégica com evidência executável, confirmou o recorte atual do BUS e definiu o consumidor real de worker B como próxima capacidade de maior alavanca, embora a execução provider end-to-end no serviço ativo permaneça não provada."
---

# BUS smoke and worker B direction

## Summary

A sessão começou examinando as sessões fechadas mais recentes e identificando os principais fios de arquitetura e workflow. O usuário pediu a próxima capacidade de maior alavanca e autorizou um fan-out governado pelo repositório. Três scouts compararam ACI-005, um harness host→BUS e um verifier de SWU; a síntese inicial escolheu o verifier e gerou artefatos de pesquisa e decisão. Perguntas posteriores expuseram que SWUs não são universais e que a restrição determinística de `write_scope` hoje é declarada e validada, mas não imposta por sandbox; por isso a recomendação do verifier genérico foi rebaixada. A conversa voltou ao BUS: o recorte atual implementa publish→verify→sealed close→reveal→authorized materialized peer input, mas ainda não executa um worker ou provider real. A suíte focada do BUS passou 7/7 e um smoke direto em banco temporário entregou uma mensagem de `seat-a` ao effective input do target, criando um execution request `accepted` com effect `pending` e `provider_start_count` zero. O piloto local está `ready` em `127.0.0.1:8766` e a UI em `127.0.0.1:8765`, mas o processo iniciou antes do código atual de reveal e não há rotas HTTP para close/reveal/plan/materialize; portanto o caminho novo não foi provado dentro do serviço ativo. No fechamento do dispatch governado, hashes de source-integrity foram sincronizados e apareceu drift de schema `0.6.1`→`0.6.2` em fixture, hook e cópias de skill. A direção decidida é retomar o BUS com um consumidor real de worker B; autoria de SWU, sandbox de escrita e verifier ficam como requisitos de suporte ainda não ratificados.

## Open questions

- Qual é a menor rota autorizada que consome `MaterializedAgentInvocation`/`ExecutionRequest` e inicia o worker B sem expandir prematuramente para todo o pipeline de providers?
- Como o `write_scope` do worker deve ser imposto deterministicamente: proxy de ferramentas, sandbox do sistema operacional ou workspace isolado?
- O piloto ativo em `8766` deve ser reiniciado ou substituído por uma instância isolada, e quais rotas precisam ser expostas antes do primeiro dogfood ao vivo?
- Qual artefato é a autoridade única da versão do schema de dispatch para eliminar o drift entre `0.6.1` e `0.6.2`?

## Next steps

1. Subir uma instância isolada do piloto a partir do código atual, após preflight, e registrar a revisão/digest realmente carregada.
2. Implementar e dogfoodar o menor consumidor host-worker que transforme o peer input materializado em execução real do worker B, mantendo explícito que effect/provider ainda não foi reivindicado.
3. Exercitar casos negativos de alteração de byte, seat e scope, além de early reveal e entrega duplicada.
4. Consolidar a autoridade da versão do schema e reparar fixtures, hooks e cópias de skill obsoletas como manutenção separada.
5. Pré-registrar um experimento de barreira determinística de escrita depois que existir o primeiro caminho real de code worker para restringir.

## Recommendation

Priorizar a instância do piloto com o código atual e o consumo real pelo worker B antes de construir um verifier genérico de SWU. A licença para esse passo é concreta: os sete testes do BUS passaram e o smoke produziu o input efetivo correto; o limite observado também é concreto, pois a execução parou em request aceito, effect pendente e zero inicializações de provider.

## Files touched

- .codex/delegation-receipts/repository-leverage-priority-20260725-v1.json
- plans/governed-agent-work-infrastructure/workstreams/repository-leverage-priority-delegated-execution-envelope.json
- research/repository-leverage-priority/research-initial-definitions.md
- research/repository-leverage-priority/proposal-v1.json
- research/repository-leverage-priority/dispatch-open.json
- research/repository-leverage-priority/workflow/seat-0-turn-0.json
- research/repository-leverage-priority/workflow/seat-1-turn-0.json
- research/repository-leverage-priority/workflow/seat-2-turn-0.json
- research/repository-leverage-priority/research.md
- research/repository-leverage-priority/findings.md
- docs/decisions/repository-leverage-priority.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- implementations/server/runtime/local_pilot.py
- telemetry/agents/subagents-dispatch.yaml
- sessions/2026-07-26-0244-bus-smoke-and-worker-b-direction.md

## User direction

- Manter o trabalho ancorado na implementação concreta do BUS; o verifier de SWU não substitui essa linha.
- Injetar no worker um SWU mínimo e imutável e bloquear deterministicamente qualquer escrita fora do escopo declarado.
- O sistema deve preencher o YAML e os campos de identidade a partir de fatos autoritativos; a pessoa revisa a intenção e o escopo, não realiza bookkeeping de baixo nível.
