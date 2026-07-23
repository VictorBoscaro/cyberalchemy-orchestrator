---
tags: [agents-communication-infra, protocols, skills, dispatch, anti-bias]
node_type: discovery
is_session: true
layer: [architecture, domain]
nature: [explanatory, technical]
status: active
veracity: medium
conviction: high
version: 0.1.1
created: 2026-07-22
last_updated: 2026-07-22
timestamp: 2026-07-22T18:02:59-03:00
expires: 2026-09-20
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "A sessão fixa o modelo conceitual obrigatório que liga revisão de skills, compilação de protocolos, higiene universal de julgamentos e DispatchSpec, tornando-se base de várias decisões futuras de SPEC e runtime, embora ainda não as ratifique nem implemente."
---

# Protocolos de skills e higiene universal de julgamentos

## Summary

A sessão refinou o discovery de protocolos obrigatórios para execução de skills. Foi decidido que cada revisão de skill possui um perfil imutável, confirmado pelo humano, com uma única recipe ativa no MVP e parâmetros concretos fornecidos pelo usuário ou inferidos no disparo. Identidade estável, digests separados de fonte e protocolo, binding ativo, migração de revisões e replay histórico foram esclarecidos. O snapshot passou a ser evidência congelada, enquanto somente o `DispatchSpec` controla a execução. Em vez de tags livres, cada unidade de trabalho ganhou um descritor tipado para subject, layer, operation, objective, question e `epistemic_kind`. Todo agregado de julgamentos — incluindo pesquisa de claims, arquitetura, review, severidade, aprovação, ranking, estratégia, votação e consenso — deve compilar para uma `JudgmentRound` selada com respostas discretas, agregação determinística e preservação de dissenso. Também foram registrados problemas ainda abertos sobre registry, transações, revogação, closure de dependências, parâmetros e independência dos avaliadores. O frontmatter do discovery foi alinhado à ontologia vigente e os probes foram separados entre discovery/harness e gates pós-implementação. Links locais e whitespace foram validados; nenhuma SPEC ou implementação foi alterada.

## Open questions

- Qual é o schema mínimo e o vocabulário adequado para representar onde/camada, ação, objetivo, pergunta, propriedades e função epistêmica de cada atividade sem criar tags redundantes ou um campo livre impossível de governar?
- Em qual autoridade deve viver a policy universal de higiene de decisão e como recipes provam cobertura completa dos julgamentos?
- Quais semânticas de revogação devem valer antes do launch, durante execução, em retry e em replay?
- Como fechar dependências dinâmicas de uma skill sem prometer reprodutibilidade que o runtime não consegue garantir?

## Next steps

- Executar os probes documentais e de harness classificados no discovery.
- Conduzir um decision gate entre as autoridades candidatas, usando a matriz de ownership do discovery, e registrar a policy e seu mecanismo de enforcement antes de promover contratos à SPEC.
- Harmonizar a skill `discovery-writing` e a validação automática de frontmatter com a ontologia vigente.

## Recommendation

Priorizar o decision gate de ownership e enforcement da policy de `JudgmentRound`, pois ela governa todos os casos de julgamento enumerados e antecede a promoção dos contratos à SPEC.

## Files touched

- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `sessions/2026-07-22-1802-skill-protocol-judgment-hygiene.md`

## Registered invariant

Avaliação de claims, escolha entre propostas, definição de arquitetura, review de documentos ou código, classificação de severidade, aprovação/reprovação, ranking, seleção de estratégia e qualquer votação ou consenso são julgamentos; quando duas ou mais posições forem agregadas, as submissões iniciais são independentes e seladas e qualquer reconsideração exige uma nova rodada selada.

## Connections

Nenhuma edge com um nó do vault foi validada, contradita ou questionada nesta sessão.
