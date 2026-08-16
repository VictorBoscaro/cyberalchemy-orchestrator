---
tags: [cyberalchemy-mvp-proposal, orchestrator, dispatch, craft, scout]
artifact_kind: session
layer: project
version: 0.1.1
created_at: 2026-08-14T17:56:15-03:00
updated_at: 2026-08-15T14:03:57-03:00
expires: 2026-10-13
decisions_made: true
contradictions_found: true
specs_updated: [projects/cyberalchemy-mvp-proposal/README.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "A sessão estabeleceu as primeiras fronteiras do produto integrado e expôs uma incompatibilidade operacional entre a skill review e o runtime governado."
---

# CyberAlchemy MVP Proposal — fundação inicial

## Summary

Este repositório busca manter trabalho de agentes ligado aos objetivos, decisões, ações e evidências que lhe dão sentido. A sessão refinou a ideia de um primeiro produto integrado em que o Orchestrator permanece no chat, conversa, escolhe rotas e sintetiza resultados sem executar trabalho especializado na própria janela. Foi decidido separar o Orchestrator da infraestrutura determinística de coordenação, que materializa invocações, aplica limites e registra lifecycle, grafo e receipts. O Superinterviewer permaneceu uma capacidade independente, utilizável diretamente por pessoas ou agentes e autorizada a invocar Scouts. Scouts foram definidos como a única capacidade de subagente universalmente invocável e como nós terminais que não delegam. Workers especializados foram limitados ao interior de Dispatches, com `subagents-strategy` responsável pela decomposição de skills e pela forma da delegação. Craft foi confirmado como sistema canônico de estado do projeto, operado por um Craft Runtime que será o único writer e receberá propostas tipadas e receipts. Essas decisões foram preservadas no [README inicial](../projects/cyberalchemy-mvp-proposal/README.md), agora identificado como CyberAlchemy MVP Proposal. A tentativa de revisar o README pelo fluxo governado foi bloqueada porque a skill `review` exige `zig-zag`, enquanto o compilador atual admite apenas conexões `sequential`. A revisão não abriu Dispatch, não lançou agentes e não alterou o ledger.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [CyberAlchemy MVP Proposal README](../projects/cyberalchemy-mvp-proposal/README.md) | `contextualizes` | Esta sessão preserva as decisões conversacionais e os limites que produziram a definição inicial do produto. |
| [Proposta de review bloqueada](../.codex/dispatch-proposals/2026-08-14-cyberalchemy-mvp-proposal-readme-review.json) | `derives-from` | O registro do encerramento deriva o blocker operacional da proposta congelada que o runtime recusou compilar. |

## Open questions

- Como o Orchestrator seleciona, resume, invalida e recupera apenas contexto relevante?
- Quais ferramentas, efeitos, orçamento e formato de retorno pertencem ao contrato do Scout?
- Quais tipos e transições o Craft precisa acrescentar para tarefas, perguntas, assumptions e contradições?
- `.craft/ledger.yml` permanece fonte operacional ou passa a ser projeção de um journal governado?
- A topologia canônica de `review` deve mudar ou o Coordination Runtime deve implementar `zig-zag` e seus handoffs?

## Next steps

1. Continuar o refinamento pela menor jornada de valor do produto, confirmando cada decisão material com o usuário.
2. Inventariar `cyberalchemy-orchestrator`, `superinterviewer`, `Arcanum` e `domainspec` depois que a jornada conceitual estiver suficientemente delimitada.
3. Reexecutar o review governado somente após resolver a incompatibilidade entre sua topologia e o runtime.

## Recommendation

Tratar a incompatibilidade entre `review` e o runtime como evidência direta para o produto: antes de confiar em Dispatches compostos, alinhar a topologia prometida pelas skills com as conexões que a infraestrutura realmente consegue compilar e observar.

## Files touched

- `.codex/dispatch-proposals/2026-08-14-cyberalchemy-mvp-proposal-readme-review.json`
- `projects/README.md`
- `projects/cyberalchemy-mvp-proposal/README.md`
- `sessions/2026-08-14-1756-cyberalchemy-mvp-proposal.md`
