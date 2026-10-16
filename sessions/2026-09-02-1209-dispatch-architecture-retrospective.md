---
tags: [dispatch, handoff, orchestration, runtime-architecture]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-09-02T12:09:23-03:00
updated_at: 2026-09-02T12:09:23-03:00
expires: 2026-11-01
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "A sessão fundamenta a decisão de abandonar a evolução incremental do lifecycle atual e recomeçar com uma autoridade de ponta a ponta."
---

# Retrospectiva da arquitetura de dispatch

## Summary

O objetivo maior do repositório é manter trabalho de agentes ligado a objetivos, decisões e evidências, e esta sessão avaliou por que o lifecycle atual deixou de cumprir esse objetivo de forma compreensível. A sessão começou pelo problema de handoff e pela pergunta sobre corrigir código ou spec, mas ampliou a investigação quando o fluxo mostrou responsabilidades distribuídas demais. Foi confirmado que nenhum serviço monta o dispatch: o agente pai aplica as skills, escreve manualmente o `opening.json` e também agenda as chamadas descritas pelo plano compilado. O caminho real foi mapeado desde capability routing e compilação até YAML, SQLite, hooks, bindings e fechamento, incluindo a rota paralela de dispatches sintéticos de compatibilidade. A conclusão central foi que correções locais acrescentaram novas autoridades sem retirar as antigas, deixando o lifecycle sem um dono de ponta a ponta. A alteração local de handoff expôs uma contradição direta entre compilação antecipada e outputs que só existem depois da execução do produtor. Código, Git, contratos, ledger, SQLite, estados de hooks e testes também evidenciaram janelas cross-store, continuidade não demonstrada e predominância do caminho de compatibilidade. O usuário decidiu começar outro repositório do zero, em vez de continuar acumulando correções sobre esse desenho. A sessão produziu uma única retrospectiva técnica com as evidências, limites das conclusões e princípios para o recomeço.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Retrospectiva técnica da arquitetura de dispatch](../docs/dispatch-architecture-postmortem.md) | `contextualizes` | Preserva o objetivo, a decisão e os registros de continuidade da auditoria produzida nesta sessão. |

## Open questions

- Qual será o store autoritativo e a menor interface pública do lifecycle no novo repositório?
- Qual host deve ser suportado primeiro para provar o golden path sem reintroduzir uma camada prematura de compatibilidade?

## Next steps

1. Criar o novo repositório com uma única fronteira proprietária do lifecycle.
2. Escrever um contrato curto para o golden path: confirmar, liberar o frontier pronto, executar, aceitar output, liberar dependentes, recuperar e fechar.
3. Implementar primeiro um teste end-to-end com dois grupos sequenciais, um follow-up e falhas simuladas nos efeitos externos.

## Recommendation

Começar pelo menor fluxo em que o agente pai entrega um único JSON confirmado a um único lifecycle owner, e impedir a expansão de registries, overlays ou modos de compatibilidade até esse fluxo passar de ponta a ponta e sob recovery.

## Files touched

- `docs/dispatch-architecture-postmortem.md`
- `sessions/2026-09-02-1209-dispatch-architecture-retrospective.md`
