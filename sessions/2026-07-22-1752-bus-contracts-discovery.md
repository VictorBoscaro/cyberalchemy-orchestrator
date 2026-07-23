---
tags: [orchestration, agents, dispatch, skills]
node_type: discovery
is_session: true
layer: [architecture, domain, application]
nature: explanatory
status: active
veracity: medium
conviction: medium
version: 0.1.0
created: 2026-07-22
last_updated: 2026-07-22
timestamp: 2026-07-22T17:52:06-03:00
expires: 2026-09-20
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "Consolidates a reviewed architectural contract for agent work exchange and closes major ambiguities, while still awaiting executable probes, SPEC promotion, and runtime implementation."
---

# Agents Communication Infra — discovery de contratos do Work Bus

## Summary

A sessão retomou o discovery de Agents Communication Infra para definir o contrato mínimo pelo qual agentes publicam e consomem outputs de trabalho. A arquitetura foi reduzida a um único Work Bus com operações tipadas `submit_work` e `submit_review`; control plane, handoff, realtime e o futuro knowledge channel ficaram fora da taxonomia de buses ativos. Knowledge foi explicitamente adiado, preservando apenas um extension seam versionado e fail-closed. O contrato passou a derivar identidade, routing, prompt, skills, arquivos e evidência do runtime, mantendo no payload do agente apenas o conteúdo semântico. Artifacts operacionais ficam fora do Git, enquanto mudanças de implementation usam workspace isolado, `ChangeSetArtifact` e promoção atômica. Routing foi dividido entre `RoutingPlan` imutável e `RoutingState` dinâmico, e o consumo ocorre por `ConsumerInputManifest`, sem leitura livre do bus. Foram definidos schemas candidatos para research, implementation e review, lifecycle candidate–receipt–acceptance, release gates, generations, retries e compatibilidade obrigatória com `work_kind`. Uma revisão formal com quatro atacantes e dois verificadores produziu 18 findings consolidados em 15 change requests, todas remediadas; uma revisão pós-remediação confirmou essas correções e encontrou oito lacunas adicionais, também incorporadas. Os dois dispatches foram registrados e fechados, e os relatórios de review permaneceram imutáveis como evidência histórica. O resultado é o discovery `bus-contracts` v0.3.0; nenhuma mudança foi promovida à SPEC nem implementada no runtime.

## Open questions

- Qual estratégia de persistência, retenção e redação deve governar prompts exatos e observações de execução potencialmente sensíveis?
- Quais semânticas de quorum, conflito e timeout devem governar múltiplos reviewers?
- Quais `work_kind`s adicionais são necessários sem enfraquecer a regra de um único tipo de trabalho por dispatch?

## Next steps

- Executar os treze probes definidos no discovery, começando por lifecycle/crash, workspace isolado e release/consumption.
- Submeter os resultados dos probes a revisão independente.
- Promover para a SPEC ou ADRs somente os contratos que sobreviverem aos probes e à revisão.
- Implementar o runtime apenas depois da promoção dos contratos aceitos e dos gates W0 aplicáveis.

## Recommendation

Começar pelos probes de lifecycle/crash, workspace isolado e release/consumption antes dos demais probes e da promoção à SPEC.

## Files touched

- `docs/features/agents-communication-infra/discovery/bus-contracts/README.md`
- `docs/features/agents-communication-infra/reviews/2026-07-22-bus-contracts/review.md`
- `docs/features/agents-communication-infra/discovery/bus-contracts/review/review.md`
- `telemetry/agents/subagents-dispatch.yaml`
