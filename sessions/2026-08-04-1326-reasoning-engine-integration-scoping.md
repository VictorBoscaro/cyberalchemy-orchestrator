---
tags: [agent-reasoning-engine, agents-communication-infra, canonical-form, cross-repository, domainspec-v2, commit-grouping]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-04T13:26:21-03:00
updated_at: 2026-08-04T13:26:21-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Estabelece que o reaproveitamento entre os repositórios irmãos é de contrato e não de código, e abre com evidência a pergunta de posse da fronteira não-autoritativa que o repositório irmão já assumiu resolvida."
---

# Reasoning engine integration scoping

## Summary

A sessão começou pelo fechamento do working tree acumulado: agrupei as mudanças em três commits por
concern e expliquei por que uma divisão por camada não era possível sem produzir um commit cuja
documentação afirma resultados de teste inexistentes naquela revisão. Antes de commitar, rodei os
testes em vez de repetir o que o recibo Stage-E afirmava, e confirmei 13 focados e 131 de runtime
passando; os três commits foram para `origin/master` como `cd4eb0d`, `894c79d` e `5457ccc`. Em
seguida inventariei o `domainspec-v2` em `../domainspec-core` procurando reaproveitamento e
descobri que o motor de derivação de testes já existe aqui com o núcleo `rules/index.ts`
byte-idêntico, o que inverteu a resposta: o que dá para aproveitar é design e contrato, não código.
Recomendei o EVF como fonte de design do harness de fitness pendente e recusei `sfol/` e `bte/`,
que reabririam decisões já fechadas. O exame do `agent-reasoning-engine` mostrou que ele nasceu
apontando para este repositório e que a decisão de encaixe já foi tomada do lado irmão —
`ACI-BIND-A-SUBORDINATE`, com este repositório nomeado como dependência bloqueadora. Comparando as
duas canonicalizações encontrei divergência em NFC, float binário, limite de inteiro, ordenação de
chaves e formato do digest, com os bytes previstos para atravessar exatamente o seam que fecha em
`artifact_content_conflict`. Argumentei que "como eles se complementam" não pode falhar e propus
uma formulação falseável; o dono escolheu o escopo maior de viabilidade integral, e registrei a
objeção de cobertura parcial dentro do próprio documento em vez de silenciá-la. Criei o
`research-initial-definitions.md` sob a feature ACI, com o achado de canonicalização entrando como
evidência observada e não como hipótese, porque a própria skill proíbe hipóteses nesse artefato.
Deixei as arestas inversas por escrever e disse por quê: a spec de protocol-compilation está fixada
por SHA-256 num índice de contexto atestado horas antes, e um backlink invalidaria esse pino.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [agents-communication-infra](../docs/features/agents-communication-infra/README.md) | `is-part-of` | Os commits fecharam o slice ACI-PG-001 desta feature e a pesquisa aberta trata da fronteira de autoridade do próprio runtime ACI. |
| [protocol-governance-compiler](2026-08-04-1026-protocol-governance-compiler.md) | `derives-from` | O trabalho de commit desta sessão consistiu em versionar e publicar o slice que aquela sessão produziu e verificou. |

## Open questions

- Se os bytes de um recibo semântico de fato atravessam a fronteira de aceitação do ACI em algum
  caminho previsto: a divergência entre as duas canonicalizações foi lida em código-fonte, nunca
  reproduzida em execução conjunta, e se os bytes não atravessarem o achado perde consequência.
- Se as convenções de vault `veracity` e `conviction` continuam aplicáveis sob o guia de
  frontmatter atual, que não as lista mas também não as proíbe; mantive as duas no documento novo
  por julgamento próprio, sem autoridade que confirme.

## Next steps

1. Desenhar a pesquisa de viabilidade — fontes, lentes opostas, topologia e o enquadramento
   anti-viés do achado de canonicalização, que o documento informacional não podia carregar.
2. Commitar o `research-initial-definitions.md`, hoje ainda apenas no working tree.
3. Corrigir o `CRAFT.md` de `tools/test-derivation-engine`, que anuncia o gate INV-3 como próximo
   movimento P1 quando `roundtrip/negative-control.ts` já existe com teste.

## Recommendation

O desenho da pesquisa é a peça-chave, e o ponto de ataque é o enquadramento do achado de
canonicalização. Como eu o encontrei antes de a pesquisa começar, o risco dominante deixou de ser
falta de evidência e passou a ser viés de confirmação; o desenho deveria instruir explicitamente
uma lente a tentar mostrar que o achado é irrelevante — por bytes que nunca atravessam, ou por uma
re-canonicalização trivial na borda. Isso é recomendação de direção, não afirmação: não sei se o
achado sobrevive, e a segunda pergunta aberta acima é exatamente a que decide.

## Files touched

- docs/features/agents-communication-infra/research/agent-reasoning-engine-integration-viability/research-initial-definitions.md
