---
tags: [skills, agents, dispatch, orchestration, architecture]
node_type: discovery
is_session: true
layer: [architecture, domain]
nature: [explanatory, technical]
status: active
created: 2026-07-26
timestamp: 2026-07-26T02:21:48-03:00
expires: 2026-09-24
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "A sessão esclareceu a arquitetura conceitual Skill → ProtocolGraph → binding → DispatchSpec → runtime, mas os artefatos foram rejeitados e servem apenas como descoberta negativa e ponto de retomada."
---

# Rejected Skill Protocol Graph Prototype

## Summary

A sessão retomou o experimento de compilar uma skill em um protocolo de execução reutilizável. Foi esclarecida a cadeia Skill → ProtocolGraph → binding da invocação → DispatchSpec confirmado → runtime. A discussão separou o grafo semântico reutilizável do dispatch concreto e explorou Medium e High como partições estruturais diferentes, não como simples mudanças numéricas de review. Medium deveria agrupar mais responsabilidades em agentes persistentes; High deveria dividir arquitetura, glossário e aspectos em células paralelas após a SPEC. A sessão também distinguiu robot-talks dentro do grupo de review de zig-zag entre produtores e reviewers. Foram criados documentos de design e exemplos de dispatch e confirmação, mas o usuário rejeitou explicitamente o resultado como insatisfatório. Nenhum grafo, schema, protocolo, compiler ou DispatchSpec foi aceito ou ratificado. O trabalho foi adiado e deve recomeçar pelo grafo conceitual antes de qualquer nova serialização.

## Open questions

- Qual é a menor representação de grafo que captura ownership, dependências, reviews e invalidação sem misturar semântica, política e runtime?
- Quais são exatamente os nós e bundles de trabalho de Medium e High antes de qualquer schema ou formato de persistência?
- Quais decisões pertencem ao grafo da skill e quais devem permanecer como primitivas gerais do compilador?

## Next steps

- Retomar pelo desenho visual dos grafos Medium e High, sem YAML, exemplos de dispatch ou schema.
- Definir ownership e dependências de cada nó e obter aceitação humana do grafo antes de serializá-lo.
- Revisar e remover ou reescrever os artefatos rejeitados antes de qualquer promoção.

## Recommendation

Começar com um único diagrama de nós e arestas e critérios explícitos de aceitação; somente depois que essa topologia for aceita, escolher uma serialização mínima.

## Files touched

- .codex/dispatch-proposals/2026-07-26-skill-protocol-compilation-preregistration/structural.json
- .codex/dispatch-proposals/2026-07-26-skill-protocol-compilation-preregistration/concrete.json
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/README.md
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/README.md
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/protocol-design.md
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/source-coverage.md
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/examples/medium.dispatch.example.yaml
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/examples/high.dispatch.example.yaml
- docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/examples/confirmation-view.md
- sessions/2026-07-26-0221-rejected-skill-protocol-graph-prototype.md

## User direction

O desenho atual foi rejeitado. A próxima sessão deve pensar primeiro no grafo conceitual e não tratar os artefatos desta sessão como proposta aceita.
