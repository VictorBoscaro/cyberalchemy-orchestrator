---
tags: [orchestration, agents, agent-telemetry, provenance, sessions, reference-scout, observation-probe, lenses, agent-pool, taxonomy, replay, receipts, sqlite]
node_type: test
is_session: true
layer: [architecture, domain, application]
nature: [explanatory, technical]
status: active
created: 2026-07-23
timestamp: 2026-07-23T17:24:44-03:00
expires: 2026-09-21
decisions_made: true
contradictions_found: false
specs_updated: [docs/features/agent-provenance-telemetry/specs/SPEC.md, docs/features/agent-provenance-telemetry/specs/architecture.md, docs/features/agent-provenance-telemetry/specs/glossary.md, docs/features/agent-provenance-telemetry/specs/experimental-runtime-l0.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "Valida um núcleo durável que separa Scout e Sonda, fixa lineage de Session e Dispatch e executa uma lente real com receipts, hash-chain e replay, embora ainda sem cutover de produção."
---

# Session, Reference Scout and Observation Probe Runtime E0

## Summary

A sessão começou auditando o que estava realmente implementado e ativo, separando código executável de processos em execução. Foi decidido que Session não é Conversation, que journal e receipts são a autoridade experimental e que tabelas semânticas são projeções reconstruíveis. A hierarquia ficou explícita como Session → Dispatch → ScoutRun, admitindo também ScoutRun direto na Session, e o Reference Scout passou a designar somente a ferramenta que produz recomendações de referências. Probe/Sonda foi separada do Scout como ferramenta observacional que aplica uma lente versionada e produz observações normalizadas, sem promovê-las automaticamente a fatos. O runtime SQLite E0 ganhou `ObservationProbeTool`, dois novos conjuntos de projeções e quatro comandos, preservando `probe_id` e eventos `probe.*` apenas como wire legado do Scout. Uma primeira lente coarse foi criada e executada sobre o `agent-pool.yaml`, mostrando que `field` é a dimensão coarse, tags são afinidades finas e os facets da Knowledge Taxonomy classificam registros, não cientistas. Uma execução aceitou um digest incompleto, foi preservada como evidência negativa e levou ao endurecimento do gate SHA-256; a execução v2 foi entregue com digest e receipt válidos. A telemetria durável contém 31 eventos encadeados, dois ScoutRuns, dois ProbeRuns e suas recomendações e observações. O replay reconstruiu as projeções, 31 testes passaram e a verificação de contratos também passou. O runtime continua shadow: launcher/MCP, `session.closed`, writer e cutover de produção ainda não foram habilitados.

## Open questions

- Qual deve ser o contrato de lifecycle de Session, incluindo `session.closed`, reabertura e rollover?
- Como medir concordância entre lentes coarse sem transformar perfil, observação e fato na mesma taxonomia?

## Next steps

- Integrar Reference Scout e Observation Probe ao host/launcher como ferramentas invocáveis pelos agentes.
- Especificar e implementar o lifecycle de fechamento da Session antes de emitir `session.closed`.
- Criar `coarse-topic-granularity@1` com dois observadores, limiar de concordância e resultado `unresolved`.
- Adicionar fixtures negativas de evento órfão, receipt órfão e pares divergentes ao replay.

## Recommendation

Priorizar o lifecycle de Session e a integração ao host/launcher antes do cutover, porque receipts, replay e uma Sonda real já licenciam o runtime shadow, mas ainda não existe autoridade para fechar a Session nem ferramentas automaticamente disponíveis aos agentes.

## Files touched

- docs/features/agent-provenance-telemetry/README.md
- docs/features/agent-provenance-telemetry/session-registry.md
- docs/features/agent-provenance-telemetry/probes/README.md
- docs/features/agent-provenance-telemetry/probes/reference-probe-tool.md
- docs/features/agent-provenance-telemetry/probes/reference-scout-tool.md
- docs/features/agent-provenance-telemetry/probes/lenses/README.md
- docs/features/agent-provenance-telemetry/probes/lenses/agent-pool-scientist-tags@1.json
- docs/features/agent-provenance-telemetry/probes/results/observation-probe-agent-pool-coarse-20260723.md
- docs/features/agent-provenance-telemetry/specs/SPEC.md
- docs/features/agent-provenance-telemetry/specs/architecture.md
- docs/features/agent-provenance-telemetry/specs/glossary.md
- docs/features/agent-provenance-telemetry/specs/experimental-runtime-l0.md
- implementations/agent-runtime/README.md
- implementations/agent-runtime/agent_runtime/cli.py
- implementations/agent-runtime/agent_runtime/runtime.py
- implementations/agent-runtime/agent_runtime/schema.sql
- implementations/agent-runtime/tests/test_cli.py
- implementations/agent-runtime/tests/test_observation_probe.py
- implementations/agent-runtime/tests/test_runtime.py
- telemetry/runtime/reference-scout-e0.sqlite3

## Registered boundary

Scout e Sonda são ferramentas distintas: o primeiro recomenda referências e a segunda aplica uma lente a um alvo pinado. Emissões do agente, tags do perfil, facets da Knowledge Taxonomy, observações e fatos permanecem sinais separados. A execução inválida de digest permanece na telemetria como evidência negativa histórica; replay a aceita, mas novos comandos não podem reproduzi-la.
