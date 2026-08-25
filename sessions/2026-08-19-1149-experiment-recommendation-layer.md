---
tags: [ledger, experiment, recommendation, observability]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-19T11:49:19-03:00
updated_at: 2026-08-19T11:49:19-03:00
expires: 2026-10-18
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "A decisão de separar sinais de capacidade de decisão do histórico operacional evita inferências fracas e estabiliza o critério de recomendação."
---

# Camada de recomendação em cima do ledger para experimento

## Summary

A sessão foi para fechar uma decisão de arquitetura no fluxo da pesquisa, conectada ao objetivo geral do repositório de elevar o valor de decisão dos agentes.  
A sessão testou se o ledger atual consegue, sozinho, decidir o momento certo de sugerir experimentos, conectando essa pergunta à prática de recomendação operacional já em uso.  
Concluímos que hoje o ledger por si só não determina o momento ideal, pois falta informação semântica sobre progresso observável e lacunas de evidência.  
Propusemos, portanto, uma camada acima do ledger com estado de evidência (claims, artefatos, classificações e ofertas) para transformar logs brutos em sinais acionáveis.  
Essa camada foi definida como responsável por gerar apenas sugestões com risco explicitado e estado `offer/decline/defer`, mantendo o usuário como agente de fechamento.  
O resultado foi uma diretriz clara: a recomendação passa a ser uma hipótese de ação, não uma inferência absoluta, e só deve avançar após revisão de custo, reversibilidade e ausência de cobertura já feita.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [research/experiment-recommendation-trigger/research.md](research/experiment-recommendation-trigger/research.md) | `grounds` | O plano desta sessão fixa a base de decisão para o fluxo de recomendação do gatilho de experimento. |

## Open questions

- Qual limiar de confiança e quais custos de erro o sistema deve otimizar para o primeiro rollout de recomendações automáticas?

## Next steps

1. Definir eventos mínimos da nova camada (`research_claim_updated`, `artifact_receipt`, `experiment_offer`) e os campos de incerteza exigidos para cada um.
2. Implementar um avaliador em modo shadow usando dados reais de sessão para medir ruído, recusa e ganhos de produtividade antes de qualquer sugestão ativa.
3. Incluir uma trilha de auditoria de decisão e permitir reversão/contestação por usuário em todas as ofertas.

## Recommendation

O keystone entre os itens acima é o próximo passo 2, porque ele valida empiricamente se a nova camada melhora decisão sem aumentar interferência indevida.  
Ele é licenciado pelo próprio estado atual: evidência de limitação do ledger sem metadados semânticos e pela necessidade de evitar regressão de autonomia do usuário.

## Files touched

- docs/features/agents-communication-infra/research/interaction-relations/findings.md
- projects/schema-service/README.md
- research/experiment-recommendation-trigger/dispatch-opening.json
