---
artifact_kind: research-findings
status: candidate
date: 2026-08-25
topic: domainspec-lean-schema-precedents
---

# Findings — schemas, metaschemas and multilevel modeling precedents

## Resposta executiva

O melhor ponto de partida para o experimento `skill-first` não é uma torre de clabjects. É uma
arquitetura mais fraca e testável: schema definitions como records/artifacts versionados, duas
referências exatas (`skill manifest → skill schema → metaschema`) e dois relatórios de validação
independentes. `Clabject`, OCA, potency, deep instantiation e fechamento meta-circular só ganham
função se um fixture concreto demonstrar uma capacidade que essa baseline não consegue expressar
([precedentes locais](reports/01-schema-metaschema.md),
[representations](reports/02-artifact-representation.md),
[literatura](reports/03-literature-multilevel-metamodeling.md)).

O repositório irmão possui precedentes fortes para referências versionadas, relações tipadas,
replay, snapshots, currentness externo, proveniência de campos e separação entre validação,
evidência, lifecycle e autoridade. Ele não implementa o `MetaSchema`, a
`SchemaDefinitionRevision`, o `ManifestRevision` ou a torre reflexiva nos sentidos propostos pelo
Schema Service. A literatura, por sua vez, fornece owners para as arquiteturas candidatas, mas não
prova que alguma delas seja necessária para nosso caso.

## Verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
| --- | --- | --- | --- | --- | --- |
| Referências revision-exact separando identidade lógica, versão e digest | `VersionedRef` no kernel Lean e `lean_file@0.2` no sibling repo ([relatório 01](reports/01-schema-metaschema.md), [relatório 02](reports/02-artifact-representation.md)) | Sim; existem records, provas locais e validação/currentness revision-scoped. | Sim, desde que digest não seja confundido com identidade semântica. | **GO** | `build-from-owned`: adaptar a disciplina, não importar os tipos como equivalentes. |
| Relações tipadas separando referência, validação e autoridade | `GovernedTypedGraph` e kernels de ontology no sibling repo ([relatório 01](reports/01-schema-metaschema.md)) | Sim; domínio/codomínio, edge identity, regra revisionada e replay são formalizados. | Sim; reachability não cria autoridade e well-typed não implica verdade. | **GO** | `build-from-owned`: definir assinaturas exatas e relatórios situados. |
| Separação operacional da família skill | Pacotes e receipts existentes no sibling repo ([relatório 02](reports/02-artifact-representation.md)) | Sim para capability, source/runtime package, installed surface, invocation/tool binding e receipt; não para o lifecycle universal do Schema Service. | Sim se os papéis não forem colapsados numa única identidade. | **GO condicionado** | `build-from-owned`: usar como corpus do primeiro witness. |
| Schemas-as-data com referências e validações adjacentes | Type Object, nesting e metamodel languages ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Sim como padrão estrutural; ainda não como implementação local completa. | Sim como baseline, desde que o aplicativo assuma interpretação e consistência explicitamente. | **GO condicionado** | `build-from-owned`: baseline a tentar antes de mecanismos multinível mais fortes. |
| O sibling repo já possui o MetaSchema geral do Schema Service | Busca sobre schemas, Lean, decisões e consumidores ([relatório 01](reports/01-schema-metaschema.md)) | Não foi encontrado um validator geral com identidade, objective, bases, properties, relations, constraints, composition, publication e expressivity. | O uso local de `schema` tem vários sentidos não unificados. | **KILL** | `typed-negative: no-witness`; reutilizar somente mecanismos concretos. |
| Uma `SchemaDefinitionRevision` precisa ser um clabject | Atkinson e Kühne; literatura posterior comparativa ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Não há fixture local que exija operar uniformemente facetas recebida e tipante. | “Ser schema para baixo e record para cima” é mais fraco que clabject. | **KILL** | `typed-negative: no-witness`; reabrir somente com operação de dupla faceta. |
| Potency/deep instantiation é necessária | Atkinson e Kühne; MetaDepth; comparações modernas ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Nenhuma propriedade do witness atual precisa atravessar mais de um salto. | Sem propagação multissalto, potency apenas redescreve duas validações. | **KILL** | `typed-negative: no-witness`; exigir um constraint impossível de expressar por composição adjacente. |
| OCA é necessária | Atkinson e Kühne ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Ainda não há caso onde classificadores linguístico e ontológico variem independentemente e mudem uma operação. | Os dois eixos são distintos na literatura, mas sua necessidade local não decorre da distinção. | **KILL** | `typed-negative: no-witness`; reabrir com fixture que force independência dos eixos. |
| Fechamento self-describing/meta-circular resolve a regressão | MOF e abordagens reflexivas ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Há witnesses de self-description, não de self-validation, soundness ou autoridade para este projeto. | Self-description, self-validation, self-hosting e bootstrap não são sinônimos. | **KILL** | `typed-negative: no-witness` para adoção atual; manter como hipótese posterior. |
| `schema residue` é termo técnico estabelecido para perda estrutural | Busca delimitada em evolução de metamodelos, model migration e schema evolution ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Não foi encontrado owner para o termo com esse significado. | Sem predicado operacional, o termo pode apenas renomear “algo se perdeu”. | **KILL** | `typed-negative: no-witness`; se mantido, marcar como termo local e defini-lo operacionalmente. |
| Evolução de schema e migração de instâncias são problemas distintos | Model migration, metamodel co-evolution e PRISM++ ([relatório 03](reports/03-literature-multilevel-metamodeling.md)) | Sim; mudanças estruturais, migração de instâncias e adaptação de dependentes aparecem separadas e acopladas. | Sim; nenhuma delas implica preservação automática da outra. | **GO** | `build-from-owned`: separar relatórios de transformação de schema e de migração/validação de instâncias. |
| `type + objective + tags` é envelope universal já sustentado | Audit local e contratos de corpus do sibling repo ([relatório 01](reports/01-schema-metaschema.md), [relatório 02](reports/02-artifact-representation.md)) | Não; tags variam entre opcionais, vazias e obrigatórias por consumidor, e objective tem usos locais diferentes. | A tríade perde identidade, provenance e correction handles. | **KILL** | `typed-negative: no-witness`; admitir cada campo somente com consumidor e acquisition mode. |

`KILL` elimina apenas a alegação de necessidade ou de precedente já estabelecido. Não proíbe testar
novamente OCA, clabject ou potency quando um fixture concreto fornecer o witness hoje ausente.

## O modelo mínimo que sobreviveu

```text
SkillArtifact
    -> described_by SkillManifestRevision
        -> references_schema SkillSchemaDefinitionRevision

SkillSchemaDefinitionRevision
    -> expresses SkillType
    -> represented_by SchemaDefinitionRepresentationSnapshot
    -> references_metaschema MetaSchemaRevision

ValidationReport A
    -> evaluates (SkillManifestRevision + SkillRepresentationSnapshot
                  + EffectiveSkillSchema + validator revision)

ValidationReport B
    -> evaluates (exact schema-definition target tuple
                  + MetaSchemaRevision + validator revision)
```

Os dois reports podem falhar independentemente. O schema pode ser bem formado sob o metaschema e
continuar semanticamente ruim, não publicado ou não autorizado; a skill pode referenciar um schema
resolvível e ainda ser inválida. Isso impede que `conformsTo` colapse declaração, evidência e
autoridade.

## Hipóteses que o experimento deve discriminar

1. **H1 — schemas-as-data:** duas referências exatas e duas validações independentes são
   suficientes.
2. **H2 — classificação ortogonal:** uma operação exige classificadores linguístico e ontológico
   independentes.
3. **H3 — deep instantiation:** uma propriedade ou constraint precisa atravessar mais de um salto e
   não pode ser expressa por composição adjacente.
4. **H4 — trusted cutoff:** parser, resolver e validator externos encerram provisoriamente o
   bootstrap.
5. **H5 — meta-circular closure:** self-description é operacionalmente necessária e possui
   procedimento explícito de bootstrap.

H1 é a baseline. H2, H3 e H5 introduzem obrigações adicionais e só sobrevivem quando seu
collapse-test falha. H4 é uma decisão operacional possível, não uma prova de fechamento lógico.

## Implicações imediatas

- Não armazenar `level` como propriedade intrínseca; no máximo derivar profundidade de uma relação
  explicitamente escolhida.
- Não usar uma cadeia transitiva de `conformsTo`. Separar ao menos `references_schema`,
  `references_metaschema`, `expresses_type`, `validated_against`, `concludes_conformance`,
  `extends` e `represents`.
- O metaschema precisa declarar qual alvo observa: revisão lógica, manifest, snapshot, closure ou
  uma tupla. “Valida o schema” é insuficiente.
- Preservar provenance de aquisição (`authored`, `generated`, `derived`, `schema`) para campos
  repetidos entre manifest, representação e contexto.
- Manter `skill-first`; Craft pode ser corpus secundário, não substituto silencioso.
- Não decidir ainda que tags são universais ou que `type` deve ser repetido no manifest.

## Evidence boundary

O sibling repo foi mantido somente leitura; suas provas e suites não foram reexecutadas nesta
pesquisa. Um agente se apoiou na revisão existente que registrava 21/21 checks e `current`, após um
check não mutante próprio ser interrompido. A literatura foi delimitada às fontes primárias e
comparativas citadas no relatório; ausência de `schema residue` nesse corpus não prova ausência na
literatura inteira.

## Resposta de uma linha ao goal

Reutilize identidade revisionada, relações tipadas, validação situada e separação de autoridade;
teste primeiro schemas-as-data no witness de skill e trate multilevel/reflection como capacidades
que precisam provar necessidade, não como arquitetura já escolhida.
