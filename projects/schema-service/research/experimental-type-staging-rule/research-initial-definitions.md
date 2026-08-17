---
artifact_kind: research-initial-definitions
status: candidate
date: 2026-08-17
topic: experimental-type-staging-rule
---

# Initial definitions — experimental type staging rule

## Context

O Schema Service ainda está em bootstrap. Ele distingue um tipo semanticamente estável de uma
revisão imutável de schema e afirma que publicar é uma operação autorizada do registry, não o
efeito colateral de gravar um arquivo. Ao mesmo tempo, os primeiros experimentos precisam usar
definições de tipo ainda não publicadas para produzir evidência antes de decidir se elas merecem
autoridade normativa.

O trabalho atual propõe um `experimentation-plan` com três experimentos sequenciais: primeiro uma
família documental `analysis`, depois skills e por fim pastas. Falta uma regra explícita para
localizar, identificar, resolver e eventualmente promover as definições usadas nesses experimentos
sem confundi-las com o registry do Schema Service.

## Purpose

Determinar a menor regra de staging que permita a um experimento usar definições de tipo e schema
repetíveis, revision-exact e inspecionáveis, mantendo-as inelegíveis para resolução normativa fora
do próprio experimento até uma promoção autorizada.

## Research question

Onde e sob quais restrições uma definição de tipo experimental deve ser armazenada e referenciada
para ser utilizável por fixtures e validações locais sem adquirir autoridade de registry, e qual
operação explícita deve ser exigida para sua promoção?

## Confirmed constraints

- Escrever um arquivo não publica um tipo nem uma revisão de schema.
- Estado experimental deve ser explícito; “não registrado” sozinho é ambíguo e não é lifecycle.
- Definições experimentais podem ser usadas apenas no escopo declarado do experimento.
- Um consumidor normativo não pode resolver silenciosamente uma referência experimental.
- Identidade do tipo e identidade revision-exact do schema não devem ser colapsadas.
- Promoção não pode reclassificar retroativamente execuções anteriores nem alterar o significado de
  uma revisão já observada.
- A regra deve funcionar inicialmente para `analysis` e não bloquear sua extensão posterior para
  skills e pastas.

## Current evidence baseline

- `projects/schema-service/README.md` descreve a rota
  `fallback + descriptive classification -> candidate type/schema definition -> authorized
  publication -> new manifest revision`, mas deixa aberto o lifecycle de candidate/draft e se uma
  instância pode referenciar schema não publicado para validação local.
- `docs/features/agent-provenance-telemetry/contracts/fixtures/seed-registry-candidates-v01.json`
  separa um lote candidato do registry por `status: candidate_batch_not_registry` e marca seus itens
  como `resolution_eligible: false`.
- `docs/features/agent-provenance-telemetry/research/seed-registry-gate.md` permite entrada inicial
  como `candidate`/`lookup_only` e restringe resolução canônica a itens `accepted` e
  `resolution_eligible`.
- Os experimentos existentes usam diretórios locais, initial definitions e critérios
  pré-registrados; isso prova uma convenção de confinamento, mas não estabelece por si só uma regra
  de autoridade para schemas.
- A pesquisa de precedentes do Schema Service recomenda começar por um pacote documental e só
  depois testar o pacote composto de skill/tool/folder.

## Known gaps

- Não há nome e localização canônicos para um catálogo de tipos experimentais do Schema Service.
- Não foi decidido se a referência experimental usa o mesmo namespace de um futuro `TypeId` ou um
  namespace explicitamente distinto.
- Não há contrato de resolução que defina quem pode enxergar candidatos e por qual `experiment_ref`.
- Não foi definida a promoção: copiar, reautorizar ou publicar a mesma revisão; nem quais digests e
  proveniências precisam ser preservados.
- Não há regra de expiração, abandono ou supersessão de candidatos que nunca forem promovidos.
- Não foi demonstrado que a mesma regra evita vazamento de autoridade em famílias compostas como
  skill e condicionais como folder.

## Decision this research must support

Adotar uma regra provisória de staging para o primeiro `experimentation-plan`, com caminho,
metadados mínimos, escopo de resolução, proibições e gate de promoção suficientemente precisos para
que o experimento `analysis` possa ser desenhado sem antecipar um registry definitivo.
