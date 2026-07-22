---
tags: [orchestration, agents, architecture, ledger, skills]
node_type: discovery
is_session: true
layer: [architecture, application, external]
nature: [explanatory, technical]
status: active
veracity: medium
conviction: medium
version: 0.1.0
created: 2026-07-22
last_updated: 2026-07-22
timestamp: 2026-07-22T13:16:51-03:00
expires: 2026-09-20
decisions_made: true
contradictions_found: false
specs_updated:
  - docs/features/agents-communication-infra/specs/SPEC.md
  - docs/features/agents-communication-infra/specs/architecture.md
  - docs/features/agents-communication-infra/specs/domain.md
  - docs/features/agents-communication-infra/specs/events.md
  - docs/features/agents-communication-infra/specs/glossary.md
  - docs/features/agents-communication-infra/specs/interfaces.md
  - docs/features/agents-communication-infra/specs/mappings.md
  - docs/features/agents-communication-infra/specs/observability.md
  - docs/features/agents-communication-infra/specs/operations.md
  - docs/features/agents-communication-infra/specs/persistence-and-replay.md
  - docs/features/agents-communication-infra/specs/queries.md
  - docs/features/agents-communication-infra/specs/rules.md
  - docs/features/agents-communication-infra/specs/states.md
  - docs/features/agents-communication-infra/specs/workflows.md
promoted_candidates: []
expected_importance: 9
importance_rationale: "Discovery arquitetural amplo, com decisões incorporadas à SPEC, contratos W0 revisados e próximos passos claros; classificação feita com o modelo disponível, pois Sonnet não estava disponível."
---

# Agents Communication Infra — contratos W0 e discovery de protocolos

## Summary

A sessão começou pela revisão do probe e do discovery do barramento de comunicação, incluindo as capacidades que ainda não existem no runtime. A pesquisa em `research/external-tools-verification` foi avaliada, sua premissa de host TypeScript foi corrigida para o host existente em Python/FastAPI e as recomendações de adoção foram registradas. A SPEC de Agents Communication Infra evoluiu para definir validação Pydantic, bytes e digest canônicos controlados pelo runtime, um `AgentAdapter` local e a separação entre ferramentas adotadas, usadas apenas como referência ou adiadas. Três revisores independentes inicialmente pediram correções na SPEC; depois das remediações, a revisão terminou em PASS/PASS/PASS. Como o gate autorizava apenas trabalho documental W0, foram produzidos um ADR, a fixture SQLite com 17 tabelas, vetores canônicos e um plano de 45 testes. Três revisores independentes também conduziram esses contratos por rodadas de correção até PASS/PASS/PASS, sem liberar o runtime. O sistema determinístico de derivação de testes foi localizado em `/tools/test-derivation-engine`, com emissor Python/pytest, mas ainda não possui binding específico para ACI e não gerou código ou testes de runtime. A discussão seguinte estabeleceu diretrizes preliminares para pesquisa, síntese, workers e revisores: relatórios imutáveis, complementos de discussão registrados, escritor único com loop de revisão, autorização por caminhos e feedback mínimo no bus. Para validar essas diretrizes antes de alterar novamente a SPEC ou o runtime, foi criado o discovery `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md` com dez trilhas de pesquisa. Ainda é necessário executar esse discovery, decidir o limite de responsabilidade da feature, promover as decisões aceitas e concluir os contratos W0 restantes antes de implementar o runtime.

## Open questions

- Os protocolos de trabalho e revisão devem pertencer a Agents Communication Infra ou formar uma feature separada que apenas use o barramento?
- Qual é o contrato mínimo de atribuição e revisão que mantém rastreabilidade sem obrigar o agente pai a inventar critérios além da SPEC?
- Como devem funcionar invalidação, retorno direcionado e encerramento quando o limite máximo de ciclos é atingido sem consenso?

## Next steps

- Executar as dez trilhas propostas no discovery de protocolos, começando pelo estado atual, ciência da decisão e pequenos probes executáveis.
- Submeter os resultados e a síntese do discovery a revisões independentes antes de promover qualquer regra.
- Promover as decisões aceitas para a SPEC ou para uma feature separada, conforme a conclusão sobre responsabilidade.
- Criar o binding ACI para o test derivation engine e concluir os contratos W0 que ainda bloqueiam a implementação do runtime.

## Recommendation

Executar primeiro o discovery de protocolos e dois probes pequenos antes de mudar novamente a SPEC. As dúvidas centrais agora são de responsabilidade, contrato mínimo e semântica dos loops; resolvê-las com evidência reduz o risco de acoplar ao barramento uma política de trabalho excessiva ou incompleta.

## Files touched

- `docs/features/agents-communication-infra/CHANGELOG.md`
- `docs/features/agents-communication-infra/EXECUTION-PACK.md`
- `docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md`
- `docs/features/agents-communication-infra/TEST-SPEC.md`
- `docs/features/agents-communication-infra/WORK-PACK.md`
- `docs/features/agents-communication-infra/adrs/ADR-001-persistence-replay-and-canonical-contracts.md`
- `docs/features/agents-communication-infra/adrs/fixtures/canonical-contract-vectors.json`
- `docs/features/agents-communication-infra/adrs/fixtures/slice0-schema.sql`
- `docs/features/agents-communication-infra/adrs/fixtures/SWU-ACI-001-TEST-PLAN.md`
- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `docs/features/agents-communication-infra/discovery/external-tool-adoption/external-tool-adoptions.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-external-tools-spec-review/BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-external-tools-spec-review/FINAL-BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-external-tools-spec-review/REPORT.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-spec-review/BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-spec-review/FINAL-BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-spec-review/POST-REMEDIATION.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-spec-review/REPORT.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/AUTHORITY-REVIEW.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/FINAL-BASELINE.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/REPORT.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/SQL-REVIEW.md`
- `docs/features/agents-communication-infra/reviews/2026-07-21-swu-aci-001-implementation/VECTORS-REVIEW.md`
- `docs/features/agents-communication-infra/specs/SPEC.md`
- `docs/features/agents-communication-infra/specs/architecture.md`
- `docs/features/agents-communication-infra/specs/domain.md`
- `docs/features/agents-communication-infra/specs/events.md`
- `docs/features/agents-communication-infra/specs/glossary.md`
- `docs/features/agents-communication-infra/specs/interfaces.md`
- `docs/features/agents-communication-infra/specs/mappings.md`
- `docs/features/agents-communication-infra/specs/observability.md`
- `docs/features/agents-communication-infra/specs/operations.md`
- `docs/features/agents-communication-infra/specs/persistence-and-replay.md`
- `docs/features/agents-communication-infra/specs/queries.md`
- `docs/features/agents-communication-infra/specs/rules.md`
- `docs/features/agents-communication-infra/specs/states.md`
- `docs/features/agents-communication-infra/specs/workflows.md`
- `docs/features/agents-communication-infra/work-pack/shared/context.md`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md`
- `docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md`
- `docs/features/agents-communication-infra/work-pack/shared/traceability.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-000.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-010.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-020.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-030.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-040.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-050.md`
- `docs/signals/pipeline-signals.jsonl`
- `research/external-tools-verification/findings.md`

## Protocol direction requested by the user

O usuário determinou que relatórios originais nunca sejam substituídos, que complementos produzidos por discussão também sejam registrados, que cada síntese tenha um único escritor com um revisor separado e que esse par possua um loop limitado. Também determinou que workers recebam uma ou mais tarefas coerentes com autorização por caminhos, inclusive para criar arquivos, e que o agente pai referencie a SPEC em vez de inventar resultados esperados ou critérios de conclusão. O feedback de revisão deve registrar no bus apenas o mínimo necessário, enquanto metadados operacionais repetitivos ficam sob responsabilidade do runtime.

## Close-session execution note

A skill local exigia classificadores Sonnet, mas esse modelo não estava disponível entre os subagentes da sessão. Com autorização explícita do usuário, a classificação e a revisão foram executadas por subagentes distintos usando os modelos disponíveis; nenhuma mudança funcional adicional foi incluída neste fechamento.
