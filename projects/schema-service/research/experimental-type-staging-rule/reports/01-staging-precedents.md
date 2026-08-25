---
artifact_kind: research-report
status: candidate
date: 2026-08-18
topic: experimental-type-staging-rule
---

# Precedentes para staging de tipos experimentais

## Resposta

A menor regra candidata é guardar cada definição experimental abaixo do próprio
experimento, em um catálogo explicitamente não normativo, e só permiti-la a um
resolvedor que receba o mesmo `experiment_ref`. O caminho proposto é:

```text
projects/schema-service/research/experimental-type-staging-rule/staging/<experiment_ref>/
  catalog.yaml
  definitions/<schema_revision>.yaml
  fixtures/
```

Esse caminho é **proposta desta pesquisa**, não convenção já instalada. Ele explora o
confinamento por diretório que os experimentos locais já usam, sem afirmar que path é
identidade: o README diz que arranjos físicos permanecem abertos e que path/digest não
são identidade durável (`projects/schema-service/README.md:33-36,228-231`). A separação
é necessária porque o Schema Service ainda está em bootstrap, não implementado
(`projects/schema-service/README.md:11-16`), e porque escrever uma definição não é
publicação (`projects/schema-service/research/experimental-type-staging-rule/research-initial-definitions.md:35-40`).

## Precedentes locais necessários

| Classe | Precedente | O que sustenta | Limite |
| --- | --- | --- | --- |
| Operacional | O lote `seed-registry-candidates-v01` identifica-se como `candidate_batch_not_registry`; cada candidato é `resolution_eligible: false` (`docs/features/agent-provenance-telemetry/contracts/fixtures/seed-registry-candidates-v01.json:2-7`). | Candidato pode ser um artefato inspecionável separado do registry e inelegível à resolução. | Trata tags, não `TypeId`/`SchemaId`; não define resolução local. |
| Operacional | A regra de seed aceita entrada `candidate`/`lookup_only` e limita a métrica de IDs resolvidos a itens `accepted` e `resolution_eligible` (`docs/features/agent-provenance-telemetry/research/seed-registry-gate.md:21-32`). | Lifecycle e elegibilidade de resolução devem ser campos explícitos, não inferências do local do arquivo. | O documento está `superseded` e descreve desenho descartado; é precedente limitado, não autoridade para o Schema Service (`docs/features/agent-provenance-telemetry/research/seed-registry-gate.md:1-11`). |
| Convenção local | O experimento de protocolos mantém `experiment-initial-definitions.md` antes do schema/experimento e declara lacunas de forma e de quem revisa/ativa/revoga (`docs/features/agents-communication-infra/experiments/skill-protocol-compilation/experiment-initial-definitions.md:15-20,56-69`). | Experimentos locais separam contexto, estado ainda não decidido e posterior desenho. | Não há registry, fixture de execução nem runtime naquele experimento (`docs/features/agents-communication-infra/experiments/skill-protocol-compilation/README.md:1-6`); a convenção não cria autoridade de schema. |
| Convenção local | A pesquisa de famílias recomenda primeiro um pacote documental e depois o pacote composto `inventory` (`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:77-105,115-123`). | A ordem `analysis` → skill → folder é uma sequência de evidência econômica. | A recomendação não estabelece catálogo, namespace ou resolvedor. |
| Regra de promoção/resolução | O README separa label, candidato, publicação normativa e enforcement; publicação exige operação autorizada, domínio owner, autoridade publicadora, revisão imutável e lifecycle (`projects/schema-service/README.md:137-144`). | Arquivo staged não pode adquirir autoridade por existir. | O lifecycle `candidate`/`draft` e a referência local a não publicado ainda estão em aberto (`projects/schema-service/README.md:142-144`). |
| Regra de promoção/resolução | A rota declarada é fallback/classificação → candidato → publicação autorizada → nova revisão de manifesto; reclassificação preserva proveniência anterior (`projects/schema-service/README.md:181-196`). | Promoção deve ser explícita e os usos anteriores não podem ser reinterpretados. | Não decide se a publicação copia, reautoriza ou reutiliza bytes staged. |

O README também exige distinguir a identidade semântica do tipo da identidade
revision-exact do schema (`projects/schema-service/README.md:56-60,96-100`). Portanto,
um namespace experimental não deve fingir ser o `TypeId` definitivo.

## Regra candidata: `experimental-type-staging/v0`

Esta seção é **proposta desta pesquisa**. Ela não cria registry, runtime ou schema
normativo.

1. `catalog.yaml` declara `experiment_ref`, `status: staged_experimental`, `owner_ref`,
   `objective_ref`, `review_by` e `resolution_scope: experiment_local_only`. Cada arquivo
   em `definitions/` declara, no mínimo, `experiment_ref`, `candidate_type_ref`,
   `schema_revision_ref`, `base_schema_ref`, `objective`, `definition_digest`,
   `status`, `review_by` e `source_ref`.
2. `candidate_type_ref` usa namespace separado, por exemplo
   `experimental:<experiment_ref>:analysis`; `schema_revision_ref` é revision-exact,
   por exemplo `experimental:<experiment_ref>:analysis@0`. Os dois campos são
   obrigatoriamente distintos. Isto preserva a separação exigida pelo README sem decidir
   a futura serialização do `TypeId` (`projects/schema-service/README.md:120-135`).
3. A resolução staged requer a tupla exata `(experiment_ref, schema_revision_ref,
   definition_digest)` e procura somente no `staging/<experiment_ref>/catalog.yaml`.
   Fixture, validador e relatório do mesmo experimento podem usar essa tupla. Um
   consumidor normativo, um experimento com `experiment_ref` diferente e qualquer lookup
   sem `experiment_ref` devem falhar fechado; jamais podem fazer fallback para o catálogo
   staged. A exigência responde à proibição já confirmada de resolução normativa silenciosa
   (`projects/schema-service/research/experimental-type-staging-rule/research-initial-definitions.md:37-43`)
   e espelha, sem extrapolá-lo, o precedente `resolution_eligible: false`.
4. Revisão é obrigatória até `review_by`: o owner registra `keep`, `supersede`,
   `abandon` ou `propose_promotion`, mais `reviewed_at` e `review_record_ref`. Ao vencer
   sem decisão, o resolvedor staged também falha fechado. `abandon` e `supersede` mantêm
   o arquivo e digest para reprodução, mas o tornam inelegível para novos runs; `supersede`
   aponta ao sucessor. Esta expiração é proposta para fechar uma lacuna reconhecida,
   não precedente já provado (`projects/schema-service/research/experimental-type-staging-rule/research-initial-definitions.md:65-75`).
5. Promoção exige uma operação de publicação autorizada fora de `staging/`, decidida pelo
   owner do domínio. O registro de promoção deve ligar `experiment_ref`,
   `candidate_type_ref`, `schema_revision_ref`, `definition_digest`, `review_record_ref`,
   `publishing_authority_ref` e o `published_schema_id` resultante. Só depois uma nova
   revisão de manifesto pode apontar ao schema publicado. A regra não presume se o
   conteúdo será copiado ou reautorizado: essa decisão permanece aberta, mas a ligação
   digestada impede que a promoção altere o que um run staged observou.

Os metadados de owner, lifecycle, definição, proveniência e digest são compatíveis com o
gate empírico de seed (`docs/features/agent-provenance-telemetry/research/seed-registry-gate.md:21-28`),
mas `experiment_ref`, escopo local e expiração são adições desta proposta. O `base_schema_ref`
mantém a regra de que refinamentos não removem silenciosamente garantias herdadas
(`projects/schema-service/README.md:132-156`); se a base ainda não for resolvível, o
experimento deve usar um fallback publicado, não uma cadeia staged implícita
(`projects/schema-service/README.md:158-179`).

## Teste de aplicação, sem desenhar os três schemas

| Família | Aplicação da regra | Resultado e fronteira |
| --- | --- | --- |
| `analysis` | A fixture declara a tupla staged e o validador recebe aquele `experiment_ref`; a definição pode refinar um fallback publicado. | Passa o confinamento e dá repetibilidade revision-exact sem publicar a família. Uma execução posterior promovida recebe nova revisão de manifesto, preservando a observação anterior (`projects/schema-service/README.md:181-193`). |
| skill | A definição staged descreve somente a capability/revisão sob teste; a fixture distingue definição, pacote, instalação e invocação. | Passa sem chamar `SKILL.md` de schema por renomeação. O precedente exige essa separação e recomenda testar o pacote composto (`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:61-72,90-105`). |
| folder | O catálogo pode referir o diretório como representação ou fixture, sem lhe atribuir `candidate_type_ref` automaticamente. | Passa porque folder só vira artefato se demonstrar owner, lifecycle e interface independentes; caso contrário, o staging permanece no experimento e o folder é container (`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:67-69,104-105`). |

O teste não demonstra ainda que os três contratos sejam bons schemas; demonstra apenas que a
mesma fronteira de autoridade não vaza entre eles. Isso é suficiente para o primeiro
experimento e deixa a promoção dependente de evidência e decisão posteriores, como exige o
limite de bootstrap (`projects/schema-service/README.md:427-457`).
