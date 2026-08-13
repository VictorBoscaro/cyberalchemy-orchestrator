---
tags: [composition, lenses, research, orchestration]
artifact_kind: session
layer: domain
version: 0.1.0
created_at: 2026-08-13T16:24:46-03:00
updated_at: 2026-08-13T16:29:13-03:00
expires: 2026-10-12
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "A sessao estabeleceu a primeira base aceita para investigar composicao sem transforma-la prematuramente em teoria, arquitetura ou produto."
---

# Primeira baseline de pesquisa sobre composicao

## Summary

Esta sessao conectou o objetivo geral do repositorio — manter trabalho de agentes ligado a objetivos, decisoes, acoes e evidencias — ao problema de entender como maneiras de trabalhar sao compostas. O objetivo foi estruturar o Composition Lab como pesquisa sobre composicao em geral, usando lentes somente como Caso 1, sem presumir uma teoria, interface ou ferramenta. A pesquisa externa aceita encontrou varias operacoes locais para formar, admitir, conectar, resolver, interpretar ou verificar totalidades, mas nenhuma operacao compartilhada nem uma teoria geral de composicao. Ela tambem mostrou que copresenca nao basta nos casos estudados, que admissibilidade e falhas sao especificas de cada dominio e que afirmacoes sobre o todo exigem evidencia adicional, sempre sob o caveat de selecao e schema do corpus. O lote interno D1 aceito encontrou em tres documentos de `domainspec-v2` uma progressao declarada entre unidades e artefatos, invariantes pretendidos, retencao de adjudicacao e residuo, autoridade separada e observabilidade enumerada, sem demonstrar execucao ou provar que lanes ou lentes sejam composicao. O programa passou a separar evidencia aceita, hipoteses, desconhecidos e quatro gates deferidos: unidade conceitual, representacao, evidencia sobre o todo e autoridade. As tentativas de infraestrutura por harness e snapshot foram rejeitadas e nao foram reabertas, porque seus controles nao sustentaram uma rota confiavel de execucao. A consequencia e uma base investigativa mais rigorosa, mas ainda parcial: nenhuma decisao de produto ou arquitetura foi autorizada, e a escolha entre D2 e D3 permanece aberta para ampliar a evidencia interna.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Composition Lab](../internal-tools/composition-lab/README.md) | `is-part-of` | Esta sessao registra a formacao e o estado da investigacao conduzida pelo Composition Lab. |
| [Programa de pesquisa](../internal-tools/composition-lab/research-program.md) | `derives-from` | O fechamento deriva do estado, dos limites, dos gates e do proximo passo preservados no programa. |
| [Sintese externa aceita](../internal-tools/composition-lab/research/external-composition-precedents/comparison/findings.md) | `derives-from` | As conclusoes externas resumidas aqui foram extraidas da baseline comparativa aceita. |
| [Findings internos D1](../internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/findings.md) | `derives-from` | As conclusoes internas resumidas aqui foram extraidas do rerun D1 aceito. |

## Open questions

- A composicao deve ser tratada como um modelo comum, uma familia tipada ou varios fenomenos separados?
- D2 ou D3 cobre melhor a proxima lacuna sobre lentes, skills, interfaces, artefatos, conhecimento e evidencia de execucao?
- O que e preservado, perdido ou recuperavel, e quando ordem, agrupamento ou interacao alteram o resultado?
- Onde devem residir as autoridades de admissao, execucao, avaliacao e revisao de uma composicao?

## Next steps

1. Selecionar D2 ou D3 pelo ganho de cobertura sobre as lacunas internas ainda abertas.
2. Executar e revisar independentemente o lote escolhido sem reabrir os harnesses ou snapshots rejeitados.
3. Comparar os proximos findings internos aceitos com a baseline externa sem impor o vocabulario externo ao corpus.
4. Manter os quatro gates deferidos ate que evidencia comparavel permita avaliar alternativas e suas perdas.

## Recommendation

Priorizar o lote interno que ofereca evidencia observada de execucao e cubra mais diretamente lentes, skills e interfaces, porque essa e a lacuna que hoje mais limita qualquer comparacao interna–externa; decidir entre D2 e D3 somente apos verificar seus corpus e criterios de saida.

## Files touched

- internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/record/d1-dispatch-sheet.md
- internal-tools/composition-lab/orchestration/milestone-1-strategy/d1-readiness/runtime-blocker/inventory-bootstrap/04-execution-sheet.md
- internal-tools/composition-lab/research-program.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/external/advice.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/external/human-confirmation-sheet.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/external/opening-record.json
- internal-tools/composition-lab/orchestration/dispatch-proposals/external/review.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/external/route-receipt.json
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/domainspec-v2/corpus-manifest.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/domainspec-v2/review.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/launch-readiness.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/lifecycle-resolution.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/regeneration-result.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/regeneration-review.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/review.md
- internal-tools/composition-lab/orchestration/dispatch-proposals/internal/route-advisor.md
- internal-tools/composition-lab/orchestration/execution-redesign/advisor-existing-primitives.md
- internal-tools/composition-lab/orchestration/execution-redesign/advisor-snapshot.md
- internal-tools/composition-lab/orchestration/execution-redesign/external-small-batch-plan.md
- internal-tools/composition-lab/orchestration/execution-redesign/internal-d3-d4-manifest-review.md
- internal-tools/composition-lab/orchestration/execution-redesign/internal-d3-d4-manifest.md
- internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan-review.md
- internal-tools/composition-lab/orchestration/execution-redesign/internal-small-batch-plan.md
- internal-tools/composition-lab/orchestration/execution-redesign/review.md
- internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/audit.md
- internal-tools/composition-lab/orchestration/execution-redesign/runs/d1-domainspec-research-structure/scout-return.md
- internal-tools/composition-lab/orchestration/execution-redesign/source-snapshot-manifest.json
- internal-tools/composition-lab/orchestration/execution-redesign/tools/Capture-RunBaseline.ps1
- internal-tools/composition-lab/orchestration/execution-redesign/tools/Invoke-SourceSnapshot.ps1
- internal-tools/composition-lab/orchestration/execution-redesign/tools/Test-Capture-RunBaseline.ps1
- internal-tools/composition-lab/orchestration/execution-redesign/tools/Test-SourceSnapshot.ps1
- internal-tools/composition-lab/orchestration/execution-redesign/tools/review.md
- internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/explorer-formal.md
- internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/explorer-operational.md
- internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/findings.md
- internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/research.md
- internal-tools/composition-lab/research/2026-08-13-person-agent-lens-relations/reviewer.md
- internal-tools/composition-lab/research/d1-program-integration-review.md
- internal-tools/composition-lab/research/external-composition-precedents/comparison/correspondences.md
- internal-tools/composition-lab/research/external-composition-precedents/comparison/findings.md
- internal-tools/composition-lab/research/external-composition-precedents/comparison/review.md
- internal-tools/composition-lab/research/external-composition-precedents/comparison/transfer-skeptic.md
- internal-tools/composition-lab/research/external-composition-precedents/dispatch-proposal.md
- internal-tools/composition-lab/research/external-composition-precedents/research-initial-definitions.md
- internal-tools/composition-lab/research/external-composition-precedents/review.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/engineered-systems-owner-map/advisor.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/engineered-systems-owner-map/findings.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/engineered-systems-owner-map/review.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/formal-structural-owner-map/advisor.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/formal-structural-owner-map/findings.md
- internal-tools/composition-lab/research/external-composition-precedents/runs/formal-structural-owner-map/review.md
- internal-tools/composition-lab/research/internal-composition-uses/dispatch-proposal.md
- internal-tools/composition-lab/research/internal-composition-uses/research-initial-definitions.md
- internal-tools/composition-lab/research/internal-composition-uses/review.md
- internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/findings.md
- internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/identity-review.md
- internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/materialization-receipt.md
- internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/review.md
- internal-tools/composition-lab/research/internal-composition-uses/runs/d1-domainspec-research-structure/accepted-rerun/source-receipt.md
- internal-tools/composition-lab/research/program-decision-review.md
- internal-tools/composition-lab/research/program-epistemic-review.md
- sessions/2026-08-13-1623-composition-research-baseline.md
