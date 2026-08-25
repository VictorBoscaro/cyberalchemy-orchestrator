---
artifact_kind: research-findings
status: candidate
date: 2026-08-18
topic: experimental-type-staging-rule
---

# Findings — experimental type staging rule

## Resposta

Tipos e revisões de schema experimentais podem ser armazenados dentro do pacote de seu experimento,
mas a localização fornece apenas custódia. Eles permanecem fora do registry, usam uma referência
experimental distinta de `schema`, resolvem somente por uma capacidade explicitamente experimental
e não adquirem autoridade por descoberta, uso, digest ou promoção posterior.

## Verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
| --- | --- | --- | --- | --- | --- |
| Staging experimental confinado por experimento | O lote local `candidate_batch_not_registry` e a negação `resolution_eligible: false` são precedentes limitados; o Schema Service já separa autoria, publicação e enforcement ([precedentes](reports/01-staging-precedents.md#precedentes-locais-necessários)). | Sim, como regra de custódia e resolução local; os casos `analysis`, skill e folder atravessam a fronteira sem exigir publicação ([teste de aplicação](reports/01-staging-precedents.md#teste-de-aplicação-sem-desenhar-os-três-schemas)). | Sim, somente com capacidades, referências e identidades distintas. Confinamento físico isolado falha o collapse-test ([revisão](reports/02-authority-leak-review.md#veredito)). | **GO condicionado** | `build-from-owned`: reutilizar a inelegibilidade explícita e acrescentar os seis guardrails contratuais. |

O condicionamento é material: um consumidor normativo deve rejeitar o candidato mesmo que conheça
seu caminho e digest. Se ele puder resolvê-lo por nome, varredura, fallback, dependência ou estado
posterior, a regra falhou ([collapse-test](reports/02-authority-leak-review.md#collapse-test-operacional)).

## Regra provisória para o experimentation plan

1. Cada experimento possui `candidate-types/` dentro de seu próprio pacote. Esse caminho é custódia,
   não identidade nem autoridade.
2. O manifesto do experimento declara `experiment_ref`, owner, estado e a raiz candidata admitida.
3. Uma definição candidata separa `candidate_type_id`, `candidate_revision_id` e
   `proposed_type_id`; não emite `SchemaId` normativo.
4. Fixtures usam `experimental_schema_ref` com `experiment_ref`, `candidate_revision_id` e digest.
   O campo normativo `schema` permanece reservado a uma publicação autorizada.
5. Somente uma resolução experimental explícita aceita a referência. Resolução normativa, busca
   global e fallback entre modos falham fechado.
6. Alterações criam nova revisão candidata. Runs fixam candidato, digest, modo e validador.
7. O lifecycle inicial é `active`, `superseded`, `abandoned` ou `promoted`. Somente `active` atende
   novos runs; estados terminais permanecem apenas para replay revision-exact.
8. Promoção produz um registro autorizado e um mapeamento candidato → publicação. Não converte nem
   reescreve runs anteriores.
9. Um schema normativo não pode depender de candidato. Qualquer resultado derivado de dependência
   experimental preserva `experiment_ref` e inelegibilidade normativa.

Os campos finais de `TypeId`/`SchemaId`, o registry definitivo, a autoridade humana concreta e o
gate probatório de promoção continuam abertos; esta regra existe para aprender antes de congelá-los
([decisões abertas](reports/02-authority-leak-review.md#decisões-que-devem-permanecer-abertas)).

## Resposta de uma linha ao goal

Guardar candidatos no pacote do experimento é seguro apenas quando custódia, resolução e autoridade
são separadas contratualmente e consumidores normativos rejeitam toda referência experimental.
