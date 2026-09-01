# Precedentes de schema e metaschema em `domainspec-lean-formalization`

## Resposta curta

O repositório sustenta com força três disciplinas úteis para o Schema Service:

1. schema e instância precisam de tipagem explícita em cada relação;
2. validação estrutural, evidência, lifecycle e autoridade não podem ser colapsados;
3. representações derivadas precisam de identidade, snapshot, proveniência e um relatório externo de currentness.

Ele **não** contém, porém, um metaschema geral implementado que valide `SchemaDefinitionRevision`, nem prova que schemas formem uma torre uniforme de `conformsTo`, nem uma decisão entre kernel externo e self-hosting. A formulação antiga “schema e instância são papéis, não tipos” foi posteriormente corrigida: por nível, ambos são tipos; entre níveis, pode existir mudança de papel. Essa mudança de papel continua apenas documentada, não formalizada como multilevel metamodeling.

Consequência: o Schema Service pode reutilizar as disciplinas de separação, versionamento, relações tipadas e validação situada. Não pode tratar seu `MetaSchema`, seu `Type`, sua herança ou sua arquitetura reflexiva como resultados já estabelecidos por este repositório.

## Escala de evidência

- **Prova Lean:** teorema declarado em fonte Lean. O build não foi reexecutado nesta investigação, para preservar o repositório-alvo como somente leitura.
- **Contrato executável/testado:** schema, gerador ou validador com testes ou revisão operacional registrada.
- **Decisão documentada:** convenção ou boundary explicitamente adotada em documento vigente, mas não provada pelo kernel.
- **Proposta:** desenho marcado como candidato, experimento ou questão aberta.
- **Exemplo:** uso local do termo `schema`, sem autoridade para generalização.
- **Histórico superseded:** formulação preservada no histórico, mas corrigida ou demovida por evidência posterior.

## 1. O que “schema” significa de fato no repositório

### 1.1 Há uma convenção formal estreita, não um conceito universal único

No eixo V, o repositório adotou a convenção de bancos de dados categoriais:

- schema é uma categoria pequena;
- uma instância de `S` é um functor `S ⥤ Type`;
- um morfismo de schemas é um functor entre categorias-schema;
- pullback é precomposição e respeita identidade e composição.

**Força:** decisão documentada em `C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:19-40` e contrato/provas Lean em `C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:57-103`.

As declarações Lean relevantes são `Schema`, `Instance`, `SchemaMorphism`, `pullback`, `pullback_id` e `pullback_comp`. O próprio arquivo limita o escopo ao eixo V; H requer instâncias atribuídas e D não é tipado por esse arquivo (`SchemaInstance.lean:27-33`). A extensão H usa `Instance_T S T := S.carrier ⥤ Monad.Algebra T` (`SchemaInstance.lean:105-162`).

Isso não equivale ao sentido geral usado pelo Schema Service — “contrato versionado de propriedades, relações e constraints”. É um precedente formal para **tipagem dependente da instância pelo schema** e para transporte entre schemas, não uma implementação de `SchemaDefinitionRevision`.

### 1.2 “Schema” também aparece como nome local para contratos de corpus

Arquivos como `research-emergence/SCHEMA.md`, `research-bridges/SCHEMA.md` e `research-security/SCHEMA.md` definem frontmatter, vocabulários de closure e regras de admissão locais. Por exemplo, o primeiro requer `name`, `description`, `type`, `status` e `last_updated`, deixando `tags` entre campos adicionais (`C:/Users/victo/domainspec-lean-formalization/research-emergence/SCHEMA.md:69-91`). O schema de research-bridges herda vocabulário, mas corrige a mistura histórica entre lifecycle e closure (`C:/Users/victo/domainspec-lean-formalization/research-bridges/SCHEMA.md:66-78`).

**Força:** exemplo/contrato documental local. Não há nesses arquivos um metaschema executável comum, resolução genérica de herança ou prova de que todos seguem uma linguagem universal.

### 1.3 O repositório reconhece que esses sentidos não foram unificados

O memo da convenção Spivak diz que a formalização mínima “stands beside” `DomainSpecSystem`, `ReflectionTower` e o schema ad hoc anterior; não os subsume (`docs/schema-instance-typing.md:42-61`). O retrofit de `DomainSpecSystem` produz a menor categoria discreta que não inventa morfismos, e explicitamente não afirma exaurir o conteúdo do sistema (`C:/Users/victo/domainspec-lean-formalization/lean-formalization/DomainSpecSystemSpivakSchema.lean:20-27`, `:48-57`, `:72-96`).

**Força:** decisão documentada + contrato Lean. Isso é uma advertência contra chamar estruturas diferentes de “o mesmo schema” sem uma ponte tipada.

## 2. Schema e instância: tipos, papéis e níveis

### 2.1 A formulação vigente é “tipos por nível, role-shift entre níveis”

O documento vigente corrige notas mais antigas que falavam apenas em papéis:

> por nível, schema e instância são tipados; entre níveis, a distinção também pode sofrer role-shift.

Fonte: `C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:78-92`.

**Força:** decisão documentada.

Isso apoia a ressalva proposta na conversa: não é o “nível” que é simultaneamente schema e instância; são objetos que exercem papéis relativos em relações diferentes. Mas o apoio tem limite: o repositório não possui um tipo Lean de `Clabject`, `MetaSchema`, potência ou deep instantiation.

### 2.2 A frase antiga “papéis, não tipos” é histórica, não deve ser restaurada

A sessão de 20 de maio registrou que “schema/instance distinction is relative” e que um schema `S` seria instância de um meta-schema `M` via `M → Set` (`C:/Users/victo/domainspec-lean-formalization/theorem/sessions/2026-05-20-2201-framework-arcanum-bridge.md:19-28`).

**Força:** decisão documentada histórica, sem termo Lean correspondente.

O problema é que a codificação Lean posteriormente adotada define `Schema` como uma soma de carrier e instância de `Category`, e `Instance S` como `S.carrier ⥤ Type` (`SchemaInstance.lean:57-77`). Ela não exibe um `M` tal que uma categoria-schema concreta seja diretamente uma instância `M ⥤ Type`. Portanto, a frase da sessão é no máximo uma direção arquitetural ainda sem ponte formal; não é consequência da codificação Spivak presente.

O ensaio distilled que afirma que “which side you call schema depends on which question” (`C:/Users/victo/domainspec-lean-formalization/docs/distilled/reflexivity/reflexivity.md:37-43`) também não é fonte segura para elevar isso a teorema. Sua versão posterior foi demovida por overclaim: não havia functor nem adjunção exibidos para o pareamento prose/Lean (`C:/Users/victo/domainspec-lean-formalization/docs/framework-as-its-own-instance.md:15-37`, `:180-200`).

**Força:** histórico superseded/demovido.

### 2.3 Uma cadeia uniforme de `conformsTo` não está sustentada

A proposta de grafo tipado distingue explicitamente:

- `instanceOf : Instance → Dock`;
- `conformsTo : Instance → Schemaˢ`.

Ela determina que as duas relações não devem colapsar nem se compor como se fossem o mesmo storey (`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:91-99`, `:132-156`). Além disso, o storey `conformsTo` está explicitamente **deferred**.

**Força:** proposta, não contrato vigente.

Logo, o repositório não autoriza inferir:

```text
x conformsTo S0 conformsTo S1
```

como uma relação uniforme ou transitiva. Uma formulação mais segura para o Schema Service é separar:

```text
ManifestRevision --references_schema--> SchemaDefinitionRevision
SchemaDefinitionRepresentation --validated_against--> MetaSchemaRevision
ValidationReport --reports_on--> (subject revision, schema revision, validator revision)
```

“Referenciar” um schema não prova conformidade; conformidade é uma conclusão situada de validação.

## 3. Identidade semântica, revisão e representação

### 3.1 Há um precedente forte para referências imutáveis versionadas

O kernel de ontologia de especificação define `VersionedRef α` com:

- `logicalId`;
- `version`;
- `payloadDigest`.

O parâmetro fantasma impede substituição entre branches diferentes (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:40-64`). O mesmo kernel separa referências versionadas, payloads, composição, obrigações e evidência (`:66-122`).

**Força:** contrato Lean. Há ainda provas de que uma composição com lista de claims diferente é distinta e de que supersession válida aumenta estritamente a versão, impedindo ciclo de dois elementos (`SpecificationOntologyKernel.lean:211-219`, `:298-305`).

Isso é compatível com a separação do Schema Service entre identidade durável, revisão e digest. Mas é apenas compatibilidade parcial: `VersionedRef` agrega os três campos numa referência; não formaliza a distinção específica `TypeId` versus `SchemaId` nem prova qual identidade semântica sobrevive entre revisões.

### 3.2 Snapshot e currentness são externos à representação

O experimento `lean_file@0.2` é o precedente operacional mais forte encontrado. Ele gera uma projeção sobre todos os `.lean` rastreados pelo Git, com schema, ID, path, hash, classificação, imports, contexto, graph slots, snapshot, freshness, boundaries e tags (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:1-96`).

O contrato faz cada record dizer `requires_validation`; somente o relatório externo afirma currentness. O pacote registra 633 records, 21/21 testes e recomposição não mutante `current` com zero issues (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/README.md:9-40`; review independente em `C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research/lean-file-corpus-v0.2-review/review.md:67-97`).

**Força:** contrato executável/testado e revisado.

Isso apoia diretamente:

- representação/projeção não é o artifact em si;
- digest e snapshot limitam a validade temporal da observação;
- currentness pertence ao relatório externo, não ao record;
- links inferidos ou históricos permanecem candidatos sem adquirir standing.

O próprio experimento, porém, usa IDs derivados de path no v0.2 e um manifest para aliases do piloto (`lean-file-v0.2-proposal.md:82-88`). Portanto ele **não prova** identidade durável independente de localização; prova apenas uma identidade honesta para uma projeção delimitada pelo Git index.

### 3.3 Representações precisam registrar origem dos campos

O piloto `lean_file@0.1` distingue ocorrências `authored`, `generated`, `derived` e `schema` no record; o exemplo registra `/schema` e `/boundaries` como vindos do schema, hashes e inventários como generated e freshness como derived (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/records/lean-file-schema-indexed-observation.json:75-150`).

**Força:** exemplo gerado dentro de um contrato executável/revisado.

É um precedente concreto para a exigência do Schema Service de não deixar dados repetidos em manifest, narrativa e observação parecerem igualmente autorais.

## 4. Propriedades, relações, constraints e composição

### 4.1 Relações explícitas e tipadas têm suporte formal

`GovernedTypedGraph.lean` modela:

- identidade independente de vertices e edges, preservando edges paralelos;
- `VertexKind` e `RelationFamily`;
- domínio e codomínio por família;
- versão do edge;
- paths tipados;
- regras versionadas com assinatura de famílias;
- replay dependente de edge identities e regra exata.

Fonte: `C:/Users/victo/domainspec-lean-formalization/lean-engineer/GovernedTypedGraph.lean:30-110`.

As fixtures provam que remover um edge direto invalida replay, que um path de famílias diferentes não deriva autoridade sem regra explícita e que edges paralelos mantêm identidades distintas (`GovernedTypedGraph.lean:218-260`).

**Força:** prova Lean, relativa às definições e fixtures; o arquivo exclui adequação empírica, autoridade legítima e enforcement runtime (`:8-23`).

Isso é compatível com propriedades/relações e composition laws explícitas no Schema Service. Também exige uma correção de postura: reachability por si só não deve criar relação derivada nem autoridade.

### 4.2 Well-typed não significa verdadeiro, autorizado ou publicado

O kernel de ontologia define uma gramática fechada para `formalizes` e `derivedFrom` (`SpecificationOntologyKernel.lean:124-148`). O mesmo arquivo declara que habitar `FormalClaim` não implica verdade (`:71-74`) e que o kernel não autentica, não prova fidelidade, não autoriza admissão/publicação e não é schema oficial (`:26-35`).

**Força:** contrato Lean + boundary documentada.

Uma `IntegratedProjection` precisa negar explicitamente que reivindica autoridade, e há teoremas sobre esse predicado (`SpecificationOntologyKernel.lean:344-358`). Evidência também não determina discharge; o kernel constrói estados open e discharged com a mesma lista de evidências (`:326-342`).

**Força:** prova Lean.

Isso sustenta fortemente a separação do Schema Service entre:

- conformance estrutural;
- evidência;
- decisão de lifecycle;
- publicação/autorização;
- enforcement.

Não há, contudo, um registry de schemas ou operação geral de publicação nesse repositório. A política de “publicação autorizada e imutável” do Schema Service continua uma decisão própria a validar.

### 4.3 Herança e refinement de schemas gerais são lacunas

Há heranças documentais locais de vocabulário e vários preorders formais chamados “schema refinement”, mas não foi encontrado um contrato geral equivalente a:

```text
SchemaDefinitionRevision extends SchemaDefinitionRevision
resolve bases
detect cycles/conflicts
forbid weakening
```

O corpus-graph é apenas proposta; seus preorders `refines`, `generalizes`, `dominates` e `reusesMechanismOf` têm decisões em aberto (`experiments/corpus-typed-graph-schema/proposal.md:118-151`, `:176-191`).

**Força:** proposta. Portanto, `extends`, multiple inheritance, effective schema e monotonic weakening no README do Schema Service são lacunas a experimentar, não precedentes resolvidos.

## 5. Objetivo, tipo e tags

### 5.1 Não há evidência de um envelope universal `type + objective + tags`

O audit mais direto perguntou se `objective + tags` bastaria para admitir algo pouco entendido. O veredito foi **não**: tags não carregam peso epistêmico, e dois objetos de fontes diferentes podem compartilhar objetivo e tags, perdendo identidade, proveniência e correction handles (`C:/Users/victo/domainspec-lean-formalization/research/audits/emergent-minimal-schema-cyberalchemy-2026-08-12/research/findings.md:21-36`).

**Força:** findings de pesquisa com verdict, não prova Lean.

O mesmo resultado recomenda envelopes indexados pelo nível, não um mínimo universal. Além disso:

- `research-emergence/SCHEMA.md` deixa `tags` opcional (`:69-91`);
- `lean_file@0.2` exige `tags`, mas sua definição permite array vazio (`lean-file-v0.2.schema.json:8`, `:95-101`);
- o `purpose` da projeção pode ser `null` quando gerado por default (`lean-file-v0.2.schema.json:42-55`);
- um consumidor específico, Resonantos, exige tags não vazias, mas apenas no contrato daquele bundle (`C:/Users/victo/domainspec-lean-formalization/internal-tools/resonantos-document-sharing-pack/scripts/review/validate_bundle.py:133-153`).

**Força:** exemplos e contratos executáveis locais.

Portanto:

- exigir `objective` em toda **definição de schema** pode ser uma boa decisão de design do Schema Service, mas não é herdada deste repositório;
- exigir `objective_ref` em toda **instância** precisa de consumidor demonstrado;
- manter `tags` sempre presentes pode simplificar serialização, mas não deve ser justificado como propriedade universal nem como fonte de tipo/autoridade.

### 5.2 O repositório não separa universalmente objetivo do schema e objetivo da instância

Alguns contratos usam `description`, outros `purpose`, outros objetivos narrativos. Nenhum metaschema comum define os dois papéis. O research-state bootstrap impõe a regra mais defensável: um novo schema ou campo precisa de consumidor identificável e de uma distinção que não seja recuperável de records, fontes ou índices existentes (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research-initial-definitions.md:38-65`).

**Força:** constraint documentada de pesquisa.

Essa regra sugere testar separadamente:

- `SchemaDefinitionRevision.objective`: consumidor é revisão/promoção do contrato;
- `ArtifactManifestRevision.objective_ref`: consumidor é roteamento, avaliação ou traceability da instância.

Sem consumidores distintos, dois campos de objetivo podem ser duplicação semântica.

## 6. Metaschema, reflexividade e fechamento

### 6.1 Não foi encontrado um metaschema geral implementado

O repositório contém arquivos chamados `SCHEMA.md`/`meta-schema` e uma menção a um schema `(K,C,R,N)` importado de outro projeto, mas nenhum artefato local equivalente ao `MetaSchema` proposto no Schema Service: não há definição geral de identidade de schema revision, objetivo, bases, properties, relations, constraints, composition laws, publicação e expressivity que valide todas as definições.

**Força:** resultado negativo da busca local. Deve ser tratado como “não encontrado neste escopo”, não como prova de inexistência histórica absoluta.

### 6.2 A Reflection Tower não é uma torre de conformidade de metaschemas

O documento da Reflection Tower distingue explicitamente duas numerações independentes: meta-layers de arquitetura e níveis sucessivos de sistemas enriquecidos por residue (`C:/Users/victo/domainspec-lean-formalization/docs/reflection-tower.md:70-132`). Formalmente, a passagem amplia a apresentação fonte com `Carrier(μₙ)` e um promotion functor `Pₙ`; o lado alvo nem sequer é construído simetricamente (`docs/reflection-tower.md:495-539`).

**Força:** decisão/documentação apoiada por formalização parcial.

Os resultados sobre ausência de finite closure e refutação de absorption pertencem à construção K-only da Reflection Tower (`docs/reflection-tower.md:13-15`, `:214-224`). Eles não demonstram que um metaschema de artifacts precise de torre infinita, nem refutam um pequeno kernel externo, nem provam self-hosting.

Assim, usar a Reflection Tower para decidir entre:

1. kernel terminal externo;
2. metaschema self-hosted;
3. universos estratificados;

seria uma extrapolação não sustentada.

### 6.3 O melhor que o repositório oferece é uma hipótese relacional limitada

Há suporte documental para dizer:

> um objeto pode exercer papel classificatório em uma relação e papel de instância em outra, desde que os tipos e relações de cada degrau permaneçam explícitos.

Não há suporte para dizer:

> qualquer schema é automaticamente instância do schema acima; todas essas ligações usam o mesmo `conformsTo`; ou a cadeia tem fechamento reflexivo.

Esse é precisamente o espaço onde a pesquisa de multilevel modeling, clabject, deep instantiation e classificação linguística versus ontológica pode acrescentar referências externas. Ela deverá ser usada para formular hipóteses e discriminadores, não para retroativamente transformar a Reflection Tower em metamodeling.

## 7. Consumidores reais e o que eles demonstram

| consumidor | evidência | o que demonstra | o que não demonstra |
|---|---|---|---|
| `lean_file@0.2` | schema Draft 2020-12, gerador, 633 records, 21 testes, review `KEEP` | schema revision explícita, projeção gerada, snapshot, provenance, currentness externo, relações diagnostic-only | identidade semântica independente de path; metaschema universal; publicação normativa |
| AIR-P0 | schemas de receipt/output + validador estreito | JSON Schemas podem ser contratos normativos de interoperabilidade enquanto a implementação valida apenas um subconjunto declarado | engine geral de JSON Schema; autoridade derivada de conformance (`C:/Users/victo/domainspec-lean-formalization/internal-tools/agent_initialization_readiness/README.md:76-85`) |
| Resonantos document pack | schemas + `Draft202012Validator` + bundle validator | schema e consumer precisam evoluir juntos; versões legadas podem ser rejeitadas; tags obrigatórias podem fazer sentido em uma família concreta | envelope universal de artifacts (`C:/Users/victo/domainspec-lean-formalization/internal-tools/resonantos-document-sharing-pack/README.md:5-38`; `scripts/share/common.py:58-87`) |
| Mathematical Work Units | validador de keys, versão, IDs, hashes e evidência Lean | revisão exata, hash e tipo de evidência são verificações operacionais concretas | que validação estrutural regenere ou prove o conteúdo Lean (`C:/Users/victo/domainspec-lean-formalization/internal-tools/mathematical_work_units/mwu_validator.py:15-31`, `:100-161`) |

## 8. Comparação final com o README do Schema Service

### Compatibilidades fortes

1. **Referências revisionadas e digests.** Compatível com `VersionedRef` e receipts request-indexed (`SpecificationOntologyKernel.lean:40-64`, `:238-305`) e com a separação do README entre identidade e revisão (`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:56-62`).
2. **Manifest/representation/snapshot/report separados.** Fortemente compatível com `lean_file@0.2` e com o pipeline conceitual do README (`schema-service/README.md:64-84`, `:198-257`).
3. **Relações tipadas e composição explícita.** Compatível com `GovernedTypedGraph`; reachability ou labels não bastam (`schema-service/README.md:284-303`).
4. **Authority separada de validação.** Compatível com as provas de evidence-versus-discharge e projection-without-authority e com a distinção README entre authoring, publishing e enforcement (`schema-service/README.md:137-144`, `:277-281`).
5. **Tags sem autoridade.** Compatível com o research-state bootstrap (`research-initial-definitions.md:59-65`) e com `schema-service/README.md:342-353`.

### Compatibilidades apenas parciais

1. **Schema como instância de MetaSchema.** Existe como formulação documentada antiga, mas não na codificação Lean vigente. O README a afirma como arquitetura (`schema-service/README.md:106-122`); deve continuar hipótese de bootstrap.
2. **Type separado de SchemaDefinitionRevision.** `VersionedRef` apoia identidade/revisão/digest, mas não modela `TypeId` versus `SchemaId`. O README corretamente mantém o contrato exato aberto (`schema-service/README.md:96-100`).
3. **Artifact durável versus representação.** Os exemplos operacionais separam projeção e fonte, mas alguns IDs são path-derived. O requisito de identidade durável do README é desejável, ainda não demonstrado genericamente.
4. **Objetivo em schema e instância.** Há usos locais de `purpose`, mas não um contrato universal nem prova de consumidores separados.

### Contradições ou claims fortes demais

1. **“Isto não requer uma torre infinita; o metaschema é a fundação bootstrap governada.”** O trecho em `schema-service/README.md:240-242` pode ser válido como escolha operacional provisória, mas não como conclusão arquitetural. O corpus não decide kernel terminal versus self-hosting; a Reflection Tower trata outro objeto.
2. **MetaSchema como componente já determinado do kernel.** `schema-service/README.md:108-116` descreve campos e filling guidance sem precedente executável local. Isso deve ser rotulado como candidato a testar com o schema de skill.
3. **Herança monotônica e EffectiveSchema.** `schema-service/README.md:146-156` não tem precedente geral implementado no repositório-alvo.
4. **Fallback universal resolvível.** O repositório-alvo mostra schemas locais e records `requires_validation`, mas não prova uma classificação total/fallback global (`schema-service/README.md:158-196`).

### Lacunas do README reveladas pela comparação

1. Falta nomear a diferença entre `references_schema` e uma conclusão `conforms_to` sustentada por `ValidationReport`.
2. Falta tipar qual representação da `SchemaDefinitionRevision` é validada pelo MetaSchema; o `Type` semântico, a revisão, o effective schema e seus bytes não são o mesmo objeto.
3. Falta declarar que well-formedness de uma definição não prova consistência, satisfatibilidade, utilidade, publicação ou autoridade.
4. Falta uma política de origem por campo equivalente a `authored/generated/derived/schema`.
5. Falta dizer que “level” é, no máximo, profundidade derivada de um caminho; o modelo operacional provável é grafo tipado, não hierarquia global rígida.

## 9. Recomendações para melhorar `research-initial-definitions`

Para o experimento skill-first, o documento inicial deveria separar explicitamente estas hipóteses:

1. **H-M1 — Metaschema mínimo.** Uma `SchemaDefinitionRevision` de skill pode ser representada e validada por um metaschema pequeno sem alegar self-hosting.
2. **H-M2 — Papéis relacionais, kinds explícitos.** “Ser schema de” e “ser instância de” são papéis relacionais; `SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot` e `ValidationReport` continuam kinds distintos com invariantes próprios.
3. **H-M3 — Não transitividade.** `x` validado contra `S0` e a representação de `S0` validada contra `M0` não implicam que `x` seja validado contra `M0`.
4. **H-I1 — Identidade/revisão.** `TypeId`, `SchemaId`, digest de representação e `ArtifactId` precisam ser discriminados por fixtures onde dois deles permanecem iguais e outro muda.
5. **H-O1 — Objetivos distintos.** `schema.objective` e `artifact.objective_ref` só sobrevivem como campos separados se consumidores reais exigirem distinções diferentes.
6. **H-T1 — Tags descritivas.** `tags` podem estar sempre serializadas por ergonomia, mas `[]` deve ser válido e nenhuma rule, autoridade ou tipo pode derivar delas sem promoção explícita.
7. **H-R1 — Representação situada.** A fonte da skill, instalação e receipt são representações/records distintos; currentness vem de validação externa e revision-scoped.
8. **H-A1 — Autoridade independente.** Validar a forma de um schema de skill não o publica nem ativa enforcement.

O primeiro witness deveria ser deliberadamente pequeno:

```text
MetaSchemaRevision@0
  validates bytes of SkillSchemaDefinitionRevision@0

SkillManifestRevision
  references_schema SkillSchemaDefinitionRevision@0

SkillSourceSnapshot
  represents SkillArtifact

ValidationReport
  binds manifest revision + source snapshot + exact schema revision + validator revision
```

Esse witness testa a recursão mínima relevante sem alegar clabject, potency, uma torre infinita ou self-hosting.

## Conclusão

O material encontrado melhora o Schema Service principalmente por **subtração de claims**:

- schema/instância podem mudar de papel entre relações, mas continuam tipados;
- o `conformsTo` uniforme e transitivo deve ser rejeitado;
- a Reflection Tower não resolve a arquitetura do metaschema;
- `objective + tags` não é um mínimo universal demonstrado;
- `TypeId` versus `SchemaId`, `extends`, effective-schema e publicação continuam trabalho próprio.

O precedente positivo mais transferível não é uma “torre de schemas”. É o pacote formado por referências versionadas, relações tipadas, provenance por campo, snapshots, validação externa, authority separation e claims estritamente limitados ao que o consumer realmente verifica.
