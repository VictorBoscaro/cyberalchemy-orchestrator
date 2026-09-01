---
artifact_kind: research-collected-returns
status: collected
date: 2026-08-25
topic: domainspec-lean-schema-precedents
---

# Research — DomainSpec Lean schema precedents and multilevel metamodeling

The following three returns are preserved verbatim from the independent explorer seats.


---

## 01 — schema e metaschema no repositório irmão

# Precedentes de schema e metaschema em `domainspec-lean-formalization`

## Resposta curta

O repositÃ³rio sustenta com forÃ§a trÃªs disciplinas Ãºteis para o Schema Service:

1. schema e instÃ¢ncia precisam de tipagem explÃ­cita em cada relaÃ§Ã£o;
2. validaÃ§Ã£o estrutural, evidÃªncia, lifecycle e autoridade nÃ£o podem ser colapsados;
3. representaÃ§Ãµes derivadas precisam de identidade, snapshot, proveniÃªncia e um relatÃ³rio externo de currentness.

Ele **nÃ£o** contÃ©m, porÃ©m, um metaschema geral implementado que valide `SchemaDefinitionRevision`, nem prova que schemas formem uma torre uniforme de `conformsTo`, nem uma decisÃ£o entre kernel externo e self-hosting. A formulaÃ§Ã£o antiga â€œschema e instÃ¢ncia sÃ£o papÃ©is, nÃ£o tiposâ€ foi posteriormente corrigida: por nÃ­vel, ambos sÃ£o tipos; entre nÃ­veis, pode existir mudanÃ§a de papel. Essa mudanÃ§a de papel continua apenas documentada, nÃ£o formalizada como multilevel metamodeling.

ConsequÃªncia: o Schema Service pode reutilizar as disciplinas de separaÃ§Ã£o, versionamento, relaÃ§Ãµes tipadas e validaÃ§Ã£o situada. NÃ£o pode tratar seu `MetaSchema`, seu `Type`, sua heranÃ§a ou sua arquitetura reflexiva como resultados jÃ¡ estabelecidos por este repositÃ³rio.

## Escala de evidÃªncia

- **Prova Lean:** teorema declarado em fonte Lean. O build nÃ£o foi reexecutado nesta investigaÃ§Ã£o, para preservar o repositÃ³rio-alvo como somente leitura.
- **Contrato executÃ¡vel/testado:** schema, gerador ou validador com testes ou revisÃ£o operacional registrada.
- **DecisÃ£o documentada:** convenÃ§Ã£o ou boundary explicitamente adotada em documento vigente, mas nÃ£o provada pelo kernel.
- **Proposta:** desenho marcado como candidato, experimento ou questÃ£o aberta.
- **Exemplo:** uso local do termo `schema`, sem autoridade para generalizaÃ§Ã£o.
- **HistÃ³rico superseded:** formulaÃ§Ã£o preservada no histÃ³rico, mas corrigida ou demovida por evidÃªncia posterior.

## 1. O que â€œschemaâ€ significa de fato no repositÃ³rio

### 1.1 HÃ¡ uma convenÃ§Ã£o formal estreita, nÃ£o um conceito universal Ãºnico

No eixo V, o repositÃ³rio adotou a convenÃ§Ã£o de bancos de dados categoriais:

- schema Ã© uma categoria pequena;
- uma instÃ¢ncia de `S` Ã© um functor `S â¥¤ Type`;
- um morfismo de schemas Ã© um functor entre categorias-schema;
- pullback Ã© precomposiÃ§Ã£o e respeita identidade e composiÃ§Ã£o.

**ForÃ§a:** decisÃ£o documentada em `C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:19-40` e contrato/provas Lean em `C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:57-103`.

As declaraÃ§Ãµes Lean relevantes sÃ£o `Schema`, `Instance`, `SchemaMorphism`, `pullback`, `pullback_id` e `pullback_comp`. O prÃ³prio arquivo limita o escopo ao eixo V; H requer instÃ¢ncias atribuÃ­das e D nÃ£o Ã© tipado por esse arquivo (`SchemaInstance.lean:27-33`). A extensÃ£o H usa `Instance_T S T := S.carrier â¥¤ Monad.Algebra T` (`SchemaInstance.lean:105-162`).

Isso nÃ£o equivale ao sentido geral usado pelo Schema Service â€” â€œcontrato versionado de propriedades, relaÃ§Ãµes e constraintsâ€. Ã‰ um precedente formal para **tipagem dependente da instÃ¢ncia pelo schema** e para transporte entre schemas, nÃ£o uma implementaÃ§Ã£o de `SchemaDefinitionRevision`.

### 1.2 â€œSchemaâ€ tambÃ©m aparece como nome local para contratos de corpus

Arquivos como `research-emergence/SCHEMA.md`, `research-bridges/SCHEMA.md` e `research-security/SCHEMA.md` definem frontmatter, vocabulÃ¡rios de closure e regras de admissÃ£o locais. Por exemplo, o primeiro requer `name`, `description`, `type`, `status` e `last_updated`, deixando `tags` entre campos adicionais (`C:/Users/victo/domainspec-lean-formalization/research-emergence/SCHEMA.md:69-91`). O schema de research-bridges herda vocabulÃ¡rio, mas corrige a mistura histÃ³rica entre lifecycle e closure (`C:/Users/victo/domainspec-lean-formalization/research-bridges/SCHEMA.md:66-78`).

**ForÃ§a:** exemplo/contrato documental local. NÃ£o hÃ¡ nesses arquivos um metaschema executÃ¡vel comum, resoluÃ§Ã£o genÃ©rica de heranÃ§a ou prova de que todos seguem uma linguagem universal.

### 1.3 O repositÃ³rio reconhece que esses sentidos nÃ£o foram unificados

O memo da convenÃ§Ã£o Spivak diz que a formalizaÃ§Ã£o mÃ­nima â€œstands besideâ€ `DomainSpecSystem`, `ReflectionTower` e o schema ad hoc anterior; nÃ£o os subsume (`docs/schema-instance-typing.md:42-61`). O retrofit de `DomainSpecSystem` produz a menor categoria discreta que nÃ£o inventa morfismos, e explicitamente nÃ£o afirma exaurir o conteÃºdo do sistema (`C:/Users/victo/domainspec-lean-formalization/lean-formalization/DomainSpecSystemSpivakSchema.lean:20-27`, `:48-57`, `:72-96`).

**ForÃ§a:** decisÃ£o documentada + contrato Lean. Isso Ã© uma advertÃªncia contra chamar estruturas diferentes de â€œo mesmo schemaâ€ sem uma ponte tipada.

## 2. Schema e instÃ¢ncia: tipos, papÃ©is e nÃ­veis

### 2.1 A formulaÃ§Ã£o vigente Ã© â€œtipos por nÃ­vel, role-shift entre nÃ­veisâ€

O documento vigente corrige notas mais antigas que falavam apenas em papÃ©is:

> por nÃ­vel, schema e instÃ¢ncia sÃ£o tipados; entre nÃ­veis, a distinÃ§Ã£o tambÃ©m pode sofrer role-shift.

Fonte: `C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:78-92`.

**ForÃ§a:** decisÃ£o documentada.

Isso apoia a ressalva proposta na conversa: nÃ£o Ã© o â€œnÃ­velâ€ que Ã© simultaneamente schema e instÃ¢ncia; sÃ£o objetos que exercem papÃ©is relativos em relaÃ§Ãµes diferentes. Mas o apoio tem limite: o repositÃ³rio nÃ£o possui um tipo Lean de `Clabject`, `MetaSchema`, potÃªncia ou deep instantiation.

### 2.2 A frase antiga â€œpapÃ©is, nÃ£o tiposâ€ Ã© histÃ³rica, nÃ£o deve ser restaurada

A sessÃ£o de 20 de maio registrou que â€œschema/instance distinction is relativeâ€ e que um schema `S` seria instÃ¢ncia de um meta-schema `M` via `M â†’ Set` (`C:/Users/victo/domainspec-lean-formalization/theorem/sessions/2026-05-20-2201-framework-arcanum-bridge.md:19-28`).

**ForÃ§a:** decisÃ£o documentada histÃ³rica, sem termo Lean correspondente.

O problema Ã© que a codificaÃ§Ã£o Lean posteriormente adotada define `Schema` como uma soma de carrier e instÃ¢ncia de `Category`, e `Instance S` como `S.carrier â¥¤ Type` (`SchemaInstance.lean:57-77`). Ela nÃ£o exibe um `M` tal que uma categoria-schema concreta seja diretamente uma instÃ¢ncia `M â¥¤ Type`. Portanto, a frase da sessÃ£o Ã© no mÃ¡ximo uma direÃ§Ã£o arquitetural ainda sem ponte formal; nÃ£o Ã© consequÃªncia da codificaÃ§Ã£o Spivak presente.

O ensaio distilled que afirma que â€œwhich side you call schema depends on which questionâ€ (`C:/Users/victo/domainspec-lean-formalization/docs/distilled/reflexivity/reflexivity.md:37-43`) tambÃ©m nÃ£o Ã© fonte segura para elevar isso a teorema. Sua versÃ£o posterior foi demovida por overclaim: nÃ£o havia functor nem adjunÃ§Ã£o exibidos para o pareamento prose/Lean (`C:/Users/victo/domainspec-lean-formalization/docs/framework-as-its-own-instance.md:15-37`, `:180-200`).

**ForÃ§a:** histÃ³rico superseded/demovido.

### 2.3 Uma cadeia uniforme de `conformsTo` nÃ£o estÃ¡ sustentada

A proposta de grafo tipado distingue explicitamente:

- `instanceOf : Instance â†’ Dock`;
- `conformsTo : Instance â†’ SchemaË¢`.

Ela determina que as duas relaÃ§Ãµes nÃ£o devem colapsar nem se compor como se fossem o mesmo storey (`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:91-99`, `:132-156`). AlÃ©m disso, o storey `conformsTo` estÃ¡ explicitamente **deferred**.

**ForÃ§a:** proposta, nÃ£o contrato vigente.

Logo, o repositÃ³rio nÃ£o autoriza inferir:

```text
x conformsTo S0 conformsTo S1
```

como uma relaÃ§Ã£o uniforme ou transitiva. Uma formulaÃ§Ã£o mais segura para o Schema Service Ã© separar:

```text
ManifestRevision --references_schema--> SchemaDefinitionRevision
SchemaDefinitionRepresentation --validated_against--> MetaSchemaRevision
ValidationReport --reports_on--> (subject revision, schema revision, validator revision)
```

â€œReferenciarâ€ um schema nÃ£o prova conformidade; conformidade Ã© uma conclusÃ£o situada de validaÃ§Ã£o.

## 3. Identidade semÃ¢ntica, revisÃ£o e representaÃ§Ã£o

### 3.1 HÃ¡ um precedente forte para referÃªncias imutÃ¡veis versionadas

O kernel de ontologia de especificaÃ§Ã£o define `VersionedRef Î±` com:

- `logicalId`;
- `version`;
- `payloadDigest`.

O parÃ¢metro fantasma impede substituiÃ§Ã£o entre branches diferentes (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:40-64`). O mesmo kernel separa referÃªncias versionadas, payloads, composiÃ§Ã£o, obrigaÃ§Ãµes e evidÃªncia (`:66-122`).

**ForÃ§a:** contrato Lean. HÃ¡ ainda provas de que uma composiÃ§Ã£o com lista de claims diferente Ã© distinta e de que supersession vÃ¡lida aumenta estritamente a versÃ£o, impedindo ciclo de dois elementos (`SpecificationOntologyKernel.lean:211-219`, `:298-305`).

Isso Ã© compatÃ­vel com a separaÃ§Ã£o do Schema Service entre identidade durÃ¡vel, revisÃ£o e digest. Mas Ã© apenas compatibilidade parcial: `VersionedRef` agrega os trÃªs campos numa referÃªncia; nÃ£o formaliza a distinÃ§Ã£o especÃ­fica `TypeId` versus `SchemaId` nem prova qual identidade semÃ¢ntica sobrevive entre revisÃµes.

### 3.2 Snapshot e currentness sÃ£o externos Ã  representaÃ§Ã£o

O experimento `lean_file@0.2` Ã© o precedente operacional mais forte encontrado. Ele gera uma projeÃ§Ã£o sobre todos os `.lean` rastreados pelo Git, com schema, ID, path, hash, classificaÃ§Ã£o, imports, contexto, graph slots, snapshot, freshness, boundaries e tags (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:1-96`).

O contrato faz cada record dizer `requires_validation`; somente o relatÃ³rio externo afirma currentness. O pacote registra 633 records, 21/21 testes e recomposiÃ§Ã£o nÃ£o mutante `current` com zero issues (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/README.md:9-40`; review independente em `C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research/lean-file-corpus-v0.2-review/review.md:67-97`).

**ForÃ§a:** contrato executÃ¡vel/testado e revisado.

Isso apoia diretamente:

- representaÃ§Ã£o/projeÃ§Ã£o nÃ£o Ã© o artifact em si;
- digest e snapshot limitam a validade temporal da observaÃ§Ã£o;
- currentness pertence ao relatÃ³rio externo, nÃ£o ao record;
- links inferidos ou histÃ³ricos permanecem candidatos sem adquirir standing.

O prÃ³prio experimento, porÃ©m, usa IDs derivados de path no v0.2 e um manifest para aliases do piloto (`lean-file-v0.2-proposal.md:82-88`). Portanto ele **nÃ£o prova** identidade durÃ¡vel independente de localizaÃ§Ã£o; prova apenas uma identidade honesta para uma projeÃ§Ã£o delimitada pelo Git index.

### 3.3 RepresentaÃ§Ãµes precisam registrar origem dos campos

O piloto `lean_file@0.1` distingue ocorrÃªncias `authored`, `generated`, `derived` e `schema` no record; o exemplo registra `/schema` e `/boundaries` como vindos do schema, hashes e inventÃ¡rios como generated e freshness como derived (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/records/lean-file-schema-indexed-observation.json:75-150`).

**ForÃ§a:** exemplo gerado dentro de um contrato executÃ¡vel/revisado.

Ã‰ um precedente concreto para a exigÃªncia do Schema Service de nÃ£o deixar dados repetidos em manifest, narrativa e observaÃ§Ã£o parecerem igualmente autorais.

## 4. Propriedades, relaÃ§Ãµes, constraints e composiÃ§Ã£o

### 4.1 RelaÃ§Ãµes explÃ­citas e tipadas tÃªm suporte formal

`GovernedTypedGraph.lean` modela:

- identidade independente de vertices e edges, preservando edges paralelos;
- `VertexKind` e `RelationFamily`;
- domÃ­nio e codomÃ­nio por famÃ­lia;
- versÃ£o do edge;
- paths tipados;
- regras versionadas com assinatura de famÃ­lias;
- replay dependente de edge identities e regra exata.

Fonte: `C:/Users/victo/domainspec-lean-formalization/lean-engineer/GovernedTypedGraph.lean:30-110`.

As fixtures provam que remover um edge direto invalida replay, que um path de famÃ­lias diferentes nÃ£o deriva autoridade sem regra explÃ­cita e que edges paralelos mantÃªm identidades distintas (`GovernedTypedGraph.lean:218-260`).

**ForÃ§a:** prova Lean, relativa Ã s definiÃ§Ãµes e fixtures; o arquivo exclui adequaÃ§Ã£o empÃ­rica, autoridade legÃ­tima e enforcement runtime (`:8-23`).

Isso Ã© compatÃ­vel com propriedades/relaÃ§Ãµes e composition laws explÃ­citas no Schema Service. TambÃ©m exige uma correÃ§Ã£o de postura: reachability por si sÃ³ nÃ£o deve criar relaÃ§Ã£o derivada nem autoridade.

### 4.2 Well-typed nÃ£o significa verdadeiro, autorizado ou publicado

O kernel de ontologia define uma gramÃ¡tica fechada para `formalizes` e `derivedFrom` (`SpecificationOntologyKernel.lean:124-148`). O mesmo arquivo declara que habitar `FormalClaim` nÃ£o implica verdade (`:71-74`) e que o kernel nÃ£o autentica, nÃ£o prova fidelidade, nÃ£o autoriza admissÃ£o/publicaÃ§Ã£o e nÃ£o Ã© schema oficial (`:26-35`).

**ForÃ§a:** contrato Lean + boundary documentada.

Uma `IntegratedProjection` precisa negar explicitamente que reivindica autoridade, e hÃ¡ teoremas sobre esse predicado (`SpecificationOntologyKernel.lean:344-358`). EvidÃªncia tambÃ©m nÃ£o determina discharge; o kernel constrÃ³i estados open e discharged com a mesma lista de evidÃªncias (`:326-342`).

**ForÃ§a:** prova Lean.

Isso sustenta fortemente a separaÃ§Ã£o do Schema Service entre:

- conformance estrutural;
- evidÃªncia;
- decisÃ£o de lifecycle;
- publicaÃ§Ã£o/autorizaÃ§Ã£o;
- enforcement.

NÃ£o hÃ¡, contudo, um registry de schemas ou operaÃ§Ã£o geral de publicaÃ§Ã£o nesse repositÃ³rio. A polÃ­tica de â€œpublicaÃ§Ã£o autorizada e imutÃ¡velâ€ do Schema Service continua uma decisÃ£o prÃ³pria a validar.

### 4.3 HeranÃ§a e refinement de schemas gerais sÃ£o lacunas

HÃ¡ heranÃ§as documentais locais de vocabulÃ¡rio e vÃ¡rios preorders formais chamados â€œschema refinementâ€, mas nÃ£o foi encontrado um contrato geral equivalente a:

```text
SchemaDefinitionRevision extends SchemaDefinitionRevision
resolve bases
detect cycles/conflicts
forbid weakening
```

O corpus-graph Ã© apenas proposta; seus preorders `refines`, `generalizes`, `dominates` e `reusesMechanismOf` tÃªm decisÃµes em aberto (`experiments/corpus-typed-graph-schema/proposal.md:118-151`, `:176-191`).

**ForÃ§a:** proposta. Portanto, `extends`, multiple inheritance, effective schema e monotonic weakening no README do Schema Service sÃ£o lacunas a experimentar, nÃ£o precedentes resolvidos.

## 5. Objetivo, tipo e tags

### 5.1 NÃ£o hÃ¡ evidÃªncia de um envelope universal `type + objective + tags`

O audit mais direto perguntou se `objective + tags` bastaria para admitir algo pouco entendido. O veredito foi **nÃ£o**: tags nÃ£o carregam peso epistÃªmico, e dois objetos de fontes diferentes podem compartilhar objetivo e tags, perdendo identidade, proveniÃªncia e correction handles (`C:/Users/victo/domainspec-lean-formalization/research/audits/emergent-minimal-schema-cyberalchemy-2026-08-12/research/findings.md:21-36`).

**ForÃ§a:** findings de pesquisa com verdict, nÃ£o prova Lean.

O mesmo resultado recomenda envelopes indexados pelo nÃ­vel, nÃ£o um mÃ­nimo universal. AlÃ©m disso:

- `research-emergence/SCHEMA.md` deixa `tags` opcional (`:69-91`);
- `lean_file@0.2` exige `tags`, mas sua definiÃ§Ã£o permite array vazio (`lean-file-v0.2.schema.json:8`, `:95-101`);
- o `purpose` da projeÃ§Ã£o pode ser `null` quando gerado por default (`lean-file-v0.2.schema.json:42-55`);
- um consumidor especÃ­fico, Resonantos, exige tags nÃ£o vazias, mas apenas no contrato daquele bundle (`C:/Users/victo/domainspec-lean-formalization/internal-tools/resonantos-document-sharing-pack/scripts/review/validate_bundle.py:133-153`).

**ForÃ§a:** exemplos e contratos executÃ¡veis locais.

Portanto:

- exigir `objective` em toda **definiÃ§Ã£o de schema** pode ser uma boa decisÃ£o de design do Schema Service, mas nÃ£o Ã© herdada deste repositÃ³rio;
- exigir `objective_ref` em toda **instÃ¢ncia** precisa de consumidor demonstrado;
- manter `tags` sempre presentes pode simplificar serializaÃ§Ã£o, mas nÃ£o deve ser justificado como propriedade universal nem como fonte de tipo/autoridade.

### 5.2 O repositÃ³rio nÃ£o separa universalmente objetivo do schema e objetivo da instÃ¢ncia

Alguns contratos usam `description`, outros `purpose`, outros objetivos narrativos. Nenhum metaschema comum define os dois papÃ©is. O research-state bootstrap impÃµe a regra mais defensÃ¡vel: um novo schema ou campo precisa de consumidor identificÃ¡vel e de uma distinÃ§Ã£o que nÃ£o seja recuperÃ¡vel de records, fontes ou Ã­ndices existentes (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research-initial-definitions.md:38-65`).

**ForÃ§a:** constraint documentada de pesquisa.

Essa regra sugere testar separadamente:

- `SchemaDefinitionRevision.objective`: consumidor Ã© revisÃ£o/promoÃ§Ã£o do contrato;
- `ArtifactManifestRevision.objective_ref`: consumidor Ã© roteamento, avaliaÃ§Ã£o ou traceability da instÃ¢ncia.

Sem consumidores distintos, dois campos de objetivo podem ser duplicaÃ§Ã£o semÃ¢ntica.

## 6. Metaschema, reflexividade e fechamento

### 6.1 NÃ£o foi encontrado um metaschema geral implementado

O repositÃ³rio contÃ©m arquivos chamados `SCHEMA.md`/`meta-schema` e uma menÃ§Ã£o a um schema `(K,C,R,N)` importado de outro projeto, mas nenhum artefato local equivalente ao `MetaSchema` proposto no Schema Service: nÃ£o hÃ¡ definiÃ§Ã£o geral de identidade de schema revision, objetivo, bases, properties, relations, constraints, composition laws, publicaÃ§Ã£o e expressivity que valide todas as definiÃ§Ãµes.

**ForÃ§a:** resultado negativo da busca local. Deve ser tratado como â€œnÃ£o encontrado neste escopoâ€, nÃ£o como prova de inexistÃªncia histÃ³rica absoluta.

### 6.2 A Reflection Tower nÃ£o Ã© uma torre de conformidade de metaschemas

O documento da Reflection Tower distingue explicitamente duas numeraÃ§Ãµes independentes: meta-layers de arquitetura e nÃ­veis sucessivos de sistemas enriquecidos por residue (`C:/Users/victo/domainspec-lean-formalization/docs/reflection-tower.md:70-132`). Formalmente, a passagem amplia a apresentaÃ§Ã£o fonte com `Carrier(Î¼â‚™)` e um promotion functor `Pâ‚™`; o lado alvo nem sequer Ã© construÃ­do simetricamente (`docs/reflection-tower.md:495-539`).

**ForÃ§a:** decisÃ£o/documentaÃ§Ã£o apoiada por formalizaÃ§Ã£o parcial.

Os resultados sobre ausÃªncia de finite closure e refutaÃ§Ã£o de absorption pertencem Ã  construÃ§Ã£o K-only da Reflection Tower (`docs/reflection-tower.md:13-15`, `:214-224`). Eles nÃ£o demonstram que um metaschema de artifacts precise de torre infinita, nem refutam um pequeno kernel externo, nem provam self-hosting.

Assim, usar a Reflection Tower para decidir entre:

1. kernel terminal externo;
2. metaschema self-hosted;
3. universos estratificados;

seria uma extrapolaÃ§Ã£o nÃ£o sustentada.

### 6.3 O melhor que o repositÃ³rio oferece Ã© uma hipÃ³tese relacional limitada

HÃ¡ suporte documental para dizer:

> um objeto pode exercer papel classificatÃ³rio em uma relaÃ§Ã£o e papel de instÃ¢ncia em outra, desde que os tipos e relaÃ§Ãµes de cada degrau permaneÃ§am explÃ­citos.

NÃ£o hÃ¡ suporte para dizer:

> qualquer schema Ã© automaticamente instÃ¢ncia do schema acima; todas essas ligaÃ§Ãµes usam o mesmo `conformsTo`; ou a cadeia tem fechamento reflexivo.

Esse Ã© precisamente o espaÃ§o onde a pesquisa de multilevel modeling, clabject, deep instantiation e classificaÃ§Ã£o linguÃ­stica versus ontolÃ³gica pode acrescentar referÃªncias externas. Ela deverÃ¡ ser usada para formular hipÃ³teses e discriminadores, nÃ£o para retroativamente transformar a Reflection Tower em metamodeling.

## 7. Consumidores reais e o que eles demonstram

| consumidor | evidÃªncia | o que demonstra | o que nÃ£o demonstra |
|---|---|---|---|
| `lean_file@0.2` | schema Draft 2020-12, gerador, 633 records, 21 testes, review `KEEP` | schema revision explÃ­cita, projeÃ§Ã£o gerada, snapshot, provenance, currentness externo, relaÃ§Ãµes diagnostic-only | identidade semÃ¢ntica independente de path; metaschema universal; publicaÃ§Ã£o normativa |
| AIR-P0 | schemas de receipt/output + validador estreito | JSON Schemas podem ser contratos normativos de interoperabilidade enquanto a implementaÃ§Ã£o valida apenas um subconjunto declarado | engine geral de JSON Schema; autoridade derivada de conformance (`C:/Users/victo/domainspec-lean-formalization/internal-tools/agent_initialization_readiness/README.md:76-85`) |
| Resonantos document pack | schemas + `Draft202012Validator` + bundle validator | schema e consumer precisam evoluir juntos; versÃµes legadas podem ser rejeitadas; tags obrigatÃ³rias podem fazer sentido em uma famÃ­lia concreta | envelope universal de artifacts (`C:/Users/victo/domainspec-lean-formalization/internal-tools/resonantos-document-sharing-pack/README.md:5-38`; `scripts/share/common.py:58-87`) |
| Mathematical Work Units | validador de keys, versÃ£o, IDs, hashes e evidÃªncia Lean | revisÃ£o exata, hash e tipo de evidÃªncia sÃ£o verificaÃ§Ãµes operacionais concretas | que validaÃ§Ã£o estrutural regenere ou prove o conteÃºdo Lean (`C:/Users/victo/domainspec-lean-formalization/internal-tools/mathematical_work_units/mwu_validator.py:15-31`, `:100-161`) |

## 8. ComparaÃ§Ã£o final com o README do Schema Service

### Compatibilidades fortes

1. **ReferÃªncias revisionadas e digests.** CompatÃ­vel com `VersionedRef` e receipts request-indexed (`SpecificationOntologyKernel.lean:40-64`, `:238-305`) e com a separaÃ§Ã£o do README entre identidade e revisÃ£o (`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:56-62`).
2. **Manifest/representation/snapshot/report separados.** Fortemente compatÃ­vel com `lean_file@0.2` e com o pipeline conceitual do README (`schema-service/README.md:64-84`, `:198-257`).
3. **RelaÃ§Ãµes tipadas e composiÃ§Ã£o explÃ­cita.** CompatÃ­vel com `GovernedTypedGraph`; reachability ou labels nÃ£o bastam (`schema-service/README.md:284-303`).
4. **Authority separada de validaÃ§Ã£o.** CompatÃ­vel com as provas de evidence-versus-discharge e projection-without-authority e com a distinÃ§Ã£o README entre authoring, publishing e enforcement (`schema-service/README.md:137-144`, `:277-281`).
5. **Tags sem autoridade.** CompatÃ­vel com o research-state bootstrap (`research-initial-definitions.md:59-65`) e com `schema-service/README.md:342-353`.

### Compatibilidades apenas parciais

1. **Schema como instÃ¢ncia de MetaSchema.** Existe como formulaÃ§Ã£o documentada antiga, mas nÃ£o na codificaÃ§Ã£o Lean vigente. O README a afirma como arquitetura (`schema-service/README.md:106-122`); deve continuar hipÃ³tese de bootstrap.
2. **Type separado de SchemaDefinitionRevision.** `VersionedRef` apoia identidade/revisÃ£o/digest, mas nÃ£o modela `TypeId` versus `SchemaId`. O README corretamente mantÃ©m o contrato exato aberto (`schema-service/README.md:96-100`).
3. **Artifact durÃ¡vel versus representaÃ§Ã£o.** Os exemplos operacionais separam projeÃ§Ã£o e fonte, mas alguns IDs sÃ£o path-derived. O requisito de identidade durÃ¡vel do README Ã© desejÃ¡vel, ainda nÃ£o demonstrado genericamente.
4. **Objetivo em schema e instÃ¢ncia.** HÃ¡ usos locais de `purpose`, mas nÃ£o um contrato universal nem prova de consumidores separados.

### ContradiÃ§Ãµes ou claims fortes demais

1. **â€œIsto nÃ£o requer uma torre infinita; o metaschema Ã© a fundaÃ§Ã£o bootstrap governada.â€** O trecho em `schema-service/README.md:240-242` pode ser vÃ¡lido como escolha operacional provisÃ³ria, mas nÃ£o como conclusÃ£o arquitetural. O corpus nÃ£o decide kernel terminal versus self-hosting; a Reflection Tower trata outro objeto.
2. **MetaSchema como componente jÃ¡ determinado do kernel.** `schema-service/README.md:108-116` descreve campos e filling guidance sem precedente executÃ¡vel local. Isso deve ser rotulado como candidato a testar com o schema de skill.
3. **HeranÃ§a monotÃ´nica e EffectiveSchema.** `schema-service/README.md:146-156` nÃ£o tem precedente geral implementado no repositÃ³rio-alvo.
4. **Fallback universal resolvÃ­vel.** O repositÃ³rio-alvo mostra schemas locais e records `requires_validation`, mas nÃ£o prova uma classificaÃ§Ã£o total/fallback global (`schema-service/README.md:158-196`).

### Lacunas do README reveladas pela comparaÃ§Ã£o

1. Falta nomear a diferenÃ§a entre `references_schema` e uma conclusÃ£o `conforms_to` sustentada por `ValidationReport`.
2. Falta tipar qual representaÃ§Ã£o da `SchemaDefinitionRevision` Ã© validada pelo MetaSchema; o `Type` semÃ¢ntico, a revisÃ£o, o effective schema e seus bytes nÃ£o sÃ£o o mesmo objeto.
3. Falta declarar que well-formedness de uma definiÃ§Ã£o nÃ£o prova consistÃªncia, satisfatibilidade, utilidade, publicaÃ§Ã£o ou autoridade.
4. Falta uma polÃ­tica de origem por campo equivalente a `authored/generated/derived/schema`.
5. Falta dizer que â€œlevelâ€ Ã©, no mÃ¡ximo, profundidade derivada de um caminho; o modelo operacional provÃ¡vel Ã© grafo tipado, nÃ£o hierarquia global rÃ­gida.

## 9. RecomendaÃ§Ãµes para melhorar `research-initial-definitions`

Para o experimento skill-first, o documento inicial deveria separar explicitamente estas hipÃ³teses:

1. **H-M1 â€” Metaschema mÃ­nimo.** Uma `SchemaDefinitionRevision` de skill pode ser representada e validada por um metaschema pequeno sem alegar self-hosting.
2. **H-M2 â€” PapÃ©is relacionais, kinds explÃ­citos.** â€œSer schema deâ€ e â€œser instÃ¢ncia deâ€ sÃ£o papÃ©is relacionais; `SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot` e `ValidationReport` continuam kinds distintos com invariantes prÃ³prios.
3. **H-M3 â€” NÃ£o transitividade.** `x` validado contra `S0` e a representaÃ§Ã£o de `S0` validada contra `M0` nÃ£o implicam que `x` seja validado contra `M0`.
4. **H-I1 â€” Identidade/revisÃ£o.** `TypeId`, `SchemaId`, digest de representaÃ§Ã£o e `ArtifactId` precisam ser discriminados por fixtures onde dois deles permanecem iguais e outro muda.
5. **H-O1 â€” Objetivos distintos.** `schema.objective` e `artifact.objective_ref` sÃ³ sobrevivem como campos separados se consumidores reais exigirem distinÃ§Ãµes diferentes.
6. **H-T1 â€” Tags descritivas.** `tags` podem estar sempre serializadas por ergonomia, mas `[]` deve ser vÃ¡lido e nenhuma rule, autoridade ou tipo pode derivar delas sem promoÃ§Ã£o explÃ­cita.
7. **H-R1 â€” RepresentaÃ§Ã£o situada.** A fonte da skill, instalaÃ§Ã£o e receipt sÃ£o representaÃ§Ãµes/records distintos; currentness vem de validaÃ§Ã£o externa e revision-scoped.
8. **H-A1 â€” Autoridade independente.** Validar a forma de um schema de skill nÃ£o o publica nem ativa enforcement.

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

Esse witness testa a recursÃ£o mÃ­nima relevante sem alegar clabject, potency, uma torre infinita ou self-hosting.

## ConclusÃ£o

O material encontrado melhora o Schema Service principalmente por **subtraÃ§Ã£o de claims**:

- schema/instÃ¢ncia podem mudar de papel entre relaÃ§Ãµes, mas continuam tipados;
- o `conformsTo` uniforme e transitivo deve ser rejeitado;
- a Reflection Tower nÃ£o resolve a arquitetura do metaschema;
- `objective + tags` nÃ£o Ã© um mÃ­nimo universal demonstrado;
- `TypeId` versus `SchemaId`, `extends`, effective-schema e publicaÃ§Ã£o continuam trabalho prÃ³prio.

O precedente positivo mais transferÃ­vel nÃ£o Ã© uma â€œtorre de schemasâ€. Ã‰ o pacote formado por referÃªncias versionadas, relaÃ§Ãµes tipadas, provenance por campo, snapshots, validaÃ§Ã£o externa, authority separation e claims estritamente limitados ao que o consumer realmente verifica.


---

## 02 — artifact e representation no repositório irmão

# Artefato, instÃ¢ncia e representaÃ§Ã£o em `domainspec-lean-formalization`

## ConclusÃ£o executiva

O repositÃ³rio fornece precedentes Ãºteis, mas **nÃ£o fornece o modelo completo do
Schema Service**. O que ele sustenta com mais forÃ§a Ã© uma disciplina de
separaÃ§Ã£o:

1. schema e instÃ¢ncia tÃªm tipos formais prÃ³prios dentro do modelo Spivak;
2. identidade lÃ³gica, versÃ£o e digest podem formar uma referÃªncia exata sem
   reduzir a identidade ao digest;
3. capability, pacote/superfÃ­cie instalada, aÃ§Ã£o de invocaÃ§Ã£o, operaÃ§Ã£o nativa
   do host e receipt aparecem como unidades diferentes em contratos
   executÃ¡veis;
4. validaÃ§Ã£o e currentness sÃ£o escopadas por inputs e snapshots, nÃ£o sÃ£o
   propriedades intrÃ­nsecas do arquivo ou do receipt;
5. representaÃ§Ã£o, artifact e generator nÃ£o devem ser transformados em classes
   ontolÃ³gicas universais e mutuamente exclusivas sem um contrato local.

O principal resultado negativo Ã© igualmente importante: nÃ£o hÃ¡ no corpus uma
implementaÃ§Ã£o de `MetaSchema`, `SchemaDefinitionRevision`, `ManifestRevision`,
`RepresentationSnapshot`, `ArtifactId` ou `SchemaId` com os sentidos propostos
pelo Schema Service. HÃ¡ vÃ¡rias coisas chamadas â€œschemaâ€, â€œmanifestâ€,
â€œrepresentationâ€ e â€œreceiptâ€, mas elas nÃ£o constituem uma cadeia universal.

Para o experimento `skill-first`, o corpus favorece um corte com pelo menos
estas unidades lÃ³gicas:

```text
Capability/SkillDefinitionRevision
    -> Ã© materializada por SourcePackageSnapshot
    -> Ã© instalada como InstallationSnapshot
    -> Ã© selecionada por Invocation/Action
    -> Ã© realizada por HostOperation/ToolBinding
    -> produz Receipt e output artifacts
```

Isso Ã© uma hipÃ³tese de transferÃªncia, nÃ£o uma equivalÃªncia jÃ¡ demonstrada. Em
particular, `ToolBinding` pode continuar sendo uma relaÃ§Ã£o/configuraÃ§Ã£o em vez
de um artifact autÃ´nomo atÃ© aparecer lifecycle ou identidade independente.

## Escopo e forÃ§a da evidÃªncia

Foram lidos os `AGENTS.md` aplicÃ¡veis, o README atual do Schema Service e um
corpus dirigido no repositÃ³rio-alvo: definiÃ§Ãµes Lean, JSON Schemas, geradores,
records, manifests, receipts, revisÃµes adversariais e documentos que registram
propostas ou reversÃµes. NÃ£o houve pesquisa web nem ediÃ§Ã£o do repositÃ³rio-alvo.

ClassificaÃ§Ã£o usada:

| forÃ§a | significado neste relatÃ³rio |
|---|---|
| **alta** | definiÃ§Ã£o/teorema Lean, schema ou cÃ³digo consumidor executÃ¡vel |
| **mÃ©dia-alta** | pacote executÃ¡vel acompanhado por testes e revisÃ£o adversarial registrada |
| **mÃ©dia** | decisÃ£o ou sÃ­ntese de pesquisa explicitamente escopada |
| **baixa** | backlog, proposta nÃ£o validada ou analogia |
| **ausÃªncia delimitada** | busca textual no corpus inspecionado; nÃ£o prova inexistÃªncia histÃ³rica ou externa |

O `check` nÃ£o mutante do mapa `lean_file@0.2` foi iniciado, mas interrompido antes
de emitir resultado para manter o escopo bounded. Portanto, este relatÃ³rio nÃ£o
alega uma reproduÃ§Ã£o independente. A evidÃªncia de `current` Ã© a revisÃ£o
existente, que registra 21/21 testes, recomposiÃ§Ã£o nÃ£o mutante e aprovaÃ§Ã£o
limitada ao pacote v0.2
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research/lean-file-corpus-v0.2-review/review.md:67-97`).

## 1. â€œSchemaâ€ e â€œinstanceâ€ tÃªm um contrato formal, mas nÃ£o o contrato do Schema Service

### O que estÃ¡ formalizado

No namespace `SchemaInstance`, um `Schema` Ã© um tipo portando uma instÃ¢ncia de
`Category`; `Instance S` Ã© um functor de `S.carrier` para `Type`; e
`SchemaMorphism S T` Ã© um functor entre os carriers. O arquivo tambÃ©m implementa
pullback por precomposiÃ§Ã£o e prova identidade e composiÃ§Ã£o
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:57-103`).

**ForÃ§a: alta.** Esses sÃ£o tipos Lean e teoremas concretos. PorÃ©m, o prÃ³prio
arquivo limita a construÃ§Ã£o ao eixo V e diz que a torre nÃ£o Ã© diretamente
tipada ali
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:27-41`).

### O que nÃ£o deve ser importado por analogia

O `Schema` de Spivak nÃ£o Ã© uma `SchemaDefinitionRevision` serializada com
`type`, `objective`, bases, propriedades e lifecycle. A palavra Ã© a mesma, o
objeto nÃ£o. Uma auditoria local encontrou trÃªs noÃ§Ãµes Lean diferentes chamadas
â€œSchemaâ€: categoria pequena, carrier de predicates de uma `ResidueStructure` e
wrapper de preorder; ela recomenda higiene de nomes justamente porque nÃ£o sÃ£o
intercambiÃ¡veis
(`C:/Users/victo/domainspec-lean-formalization/_residue/schema-definition-audit-2026-05-22.md:12-38`,
`:66-80`).

O corpus tambÃ©m contÃ©m a tese de que schema/instÃ¢ncia sÃ£o papÃ©is relativos
atravÃ©s de nÃ­veis, mas ela estÃ¡ marcada como â€œCaptured, not integratedâ€ e exige
uma decisÃ£o de escopo
(`C:/Users/victo/domainspec-lean-formalization/BACKLOG.md:23-33`). O memo posterior
faz uma formulaÃ§Ã£o mais cuidadosa: por nÃ­vel, schema e instÃ¢ncia sÃ£o tipados;
atravÃ©s de nÃ­veis, hÃ¡ uma proposta de role-shift
(`C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:78-92`).

**ForÃ§a do role-shift: baixa a mÃ©dia.** Ã‰ uma reconciliaÃ§Ã£o documental, nÃ£o uma
formalizaÃ§Ã£o de metaschema, `conformsTo` multinÃ­vel ou self-hosting.

### ImplicaÃ§Ã£o para o metaschema

A busca delimitada nÃ£o encontrou as entidades exatas `MetaSchema`,
`SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot`,
`ArtifactId` ou `SchemaId` no repositÃ³rio-alvo. O corpus nÃ£o decide qual objeto
um metaschema do Schema Service deve validar. Ele tampouco demonstra que uma
definiÃ§Ã£o de schema possa validar a si prÃ³pria.

Portanto, a afirmaÃ§Ã£o atual do Schema Service â€” uma schema-definition revision
Ã© instÃ¢ncia do metaschema â€” permanece uma hipÃ³tese de produto local
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:106-122`),
nÃ£o um precedente implementado pelo sibling repo.

## 2. Identidade, versÃ£o, digest e path

### ReferÃªncia versionada: distinÃ§Ã£o forte

`SpecificationOntology.VersionedRef Î±` guarda separadamente `logicalId`,
`version` e `payloadDigest`; seu parÃ¢metro phantom impede substituiÃ§Ã£o entre
branches ontolÃ³gicas, e a igualdade examina os trÃªs campos
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:40-64`).

Esse Ã© o precedente mais prÃ³ximo para a separaÃ§Ã£o do Schema Service entre
identidade semÃ¢ntica, revisÃ£o e bytes. Ele sustenta a **forma da separaÃ§Ã£o**, mas
nÃ£o prova:

- que `logicalId` permaneÃ§a estÃ¡vel atravÃ©s de rename/move;
- que `version` seja imutÃ¡vel apÃ³s publicaÃ§Ã£o;
- que qualquer string seja uma identidade autorizada;
- que `payloadDigest` seja a identidade do artifact.

**ForÃ§a: alta para a independÃªncia dos campos; mÃ©dia para transferÃªncia ao
Schema Service.**

### O contraexemplo operacional: `lean_file@0.2`

O mapa v0.2 cria IDs como hash truncado do path:

```python
return "lean-file-v0.2-" + digest(path.encode("utf-8"))[:24]
```

(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:132-141`).

O record guarda path e SHA-256 do source, repete o digest no snapshot e aponta
para um `corpus_snapshot_id`
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/records-v0.2/lean-file-v0.2-623026b5a0f89dc8eb070261.json:183-250`).
O generator calcula o snapshot do corpus a partir de paths, source hashes,
Markdown, lakefiles, policy, schemas e versÃµes dos prÃ³prios geradores
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:678-691`).

Isso Ã© apropriado porque o artefato se declara uma **projeÃ§Ã£o do Git index**,
nÃ£o uma identidade durÃ¡vel: arquivos fora do index nÃ£o recebem record canÃ´nico,
e cada record tem ID derivado do path
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-v0.2-proposal.md:3-10`,
`:82-88`).

**ForÃ§a: mÃ©dia-alta como precedente operacional; negativa para identidade
durÃ¡vel.** Um rename cria outro ID. Logo, nÃ£o se deve copiar esse mecanismo para
`ArtifactId`. Ele confirma a distinÃ§Ã£o do README atual: path e digest podem
identificar uma representaÃ§Ã£o/snapshot sem identificar o artifact durÃ¡vel
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:57-62`).

### Currentness nÃ£o mora no record

Cada record fixa `freshness.state = requires_validation`; currentness pertence
ao relatÃ³rio externo
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:85-96`).
O gerador recompÃµe records e manifest; diferenÃ§a de bytes produz `stale`, erros
produzem `invalid`/`unresolved`, e igualdade completa produz `current`
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:905-936`).

O mesmo princÃ­pio aparece formalmente em `VerificationReceipt.CurrentFor`: o
receipt deve corresponder a request, package digest, subject digest e scope, e
nÃ£o estar superseded; currentness nÃ£o Ã© recuperada dos bytes do receipt sozinho
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:238-305`).

**TransferÃªncia recomendada:** um `ValidationReport` do Schema Service deve ser
revision/snapshot-scoped e nunca virar um badge intrÃ­nseco do artifact.

## 3. â€œManifestâ€ Ã© hoje um nome para contratos diferentes

O corpus sustenta pelo menos trÃªs usos distintos:

1. **Corpus manifest.** `manifest-v0.2.json` indexa records, paths, aliases,
   imports reversos, owner projections e o snapshot do corpus
   (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:784-795`).
2. **Context manifest.** `ContextManifest` contÃ©m a identidade exata dos
   `SourceVersion` selecionados e bytes renderizados; a seleÃ§Ã£o depende de
   versÃµes de selector/policy/renderer, adapter e budget
   (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/ContextManifestIntegrity.lean:41-109`).
3. **Generation manifest.** o package Orchestrate registra canonical root,
   source `SKILL.md`, policy de geraÃ§Ã£o, support/excluded paths e superfÃ­cies
   instalÃ¡veis para Codex, repo-local e Claude
   (`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/generation-manifest.json:1-23`).

Esses manifests colapsam operacionalmente apenas dentro de seus contratos
locais. Nenhum Ã© o `ManifestRevision` universal do Schema Service. O nome nÃ£o
autoriza unificaÃ§Ã£o.

HÃ¡, contudo, uma regra transferÃ­vel: o contexto materializado fecha sobre a
identidade e a versÃ£o exatas das fontes selecionadas, nÃ£o apenas sobre seus
paths
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/ContextManifestIntegrity.lean:71-109`).

## 4. Representation, carrier, snapshot e observation

### O nÃºcleo formal Ã© menor que um artifact model

`RepresentationEdgeTyping.lean` distingue `EmbeddingEdge` e `QuotientEdge` por
leis: injectividade versus sobrejetividade. Ambas tÃªm identidade e composiÃ§Ã£o,
e witnesses finitos mostram que uma nÃ£o implica a outra. O prÃ³prio arquivo
nega que isso estabeleÃ§a satisfaction, refinement observacional ou uma rede
global de representaÃ§Ãµes
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/RepresentationEdgeTyping.lean:8-20`,
`:24-90`).

**ForÃ§a: alta e estreita.** O precedente Ã© â€œrelaÃ§Ãµes diferentes exigem leis
diferentesâ€, nÃ£o â€œtoda representation Ã© um carrier edgeâ€.

### A reversÃ£o mais relevante

A sÃ­ntese de representation-composition rejeitou trÃªs universais:

- representaÃ§Ã£o nÃ£o Ã© apenas sua relaÃ§Ã£o de fibras;
- projection nÃ£o Ã© sinÃ´nimo de qualquer transformaÃ§Ã£o nem implica perda
  estrita;
- generator, representation e artifact nÃ£o sÃ£o classes ontolÃ³gicas universais
  disjuntas
  (`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:595-617`).

Ela substitui a desigualdade rÃ­gida â€œrepresentaÃ§Ã£o semÃ¢ntica â‰  artifact
concretoâ€ por uma formulaÃ§Ã£o relacional: um artifact pode carregar, realizar,
evidenciar ou gerar uma representaÃ§Ã£o em edges diferentes
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:608-612`).

Isso estÃ¡ alinhado ao Schema Service, que jÃ¡ permite que um objeto seja artifact,
representaÃ§Ã£o de outro artifact, ou ambos por identidades e relaÃ§Ãµes explÃ­citas
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:233-251`).

### O que permanece aberto

A mesma sÃ­ntese registra que nÃ£o hÃ¡ owner universal de `representation`; mapa,
factorization order e typed edges tÃªm owners separados. Ela adia um tipo
universal e uma API `StructuredRepresentation`
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:322-335`,
`:580-617`).

O stress test de Task Session interpreta context pack, ticket, receipt e
closeout como artifacts parciais sincronizados, mas explicita que nÃ£o existe
uma interface comum `Representation`
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:410-418`).

**ConsequÃªncia:** `Representation` e `RepresentationSnapshot` no Schema Service
devem continuar como papÃ©is lÃ³gicos e interfaces por famÃ­lia. NÃ£o hÃ¡ evidÃªncia
para congelar um record universal contendo path, digest, context, consumer,
authority e provenance em uma Ãºnica estrutura.

## 5. Artifact, evidence, validation e lifecycle nÃ£o colapsam

O kernel de specification separa:

- `EvidenceArtifact`, ligado a uma referÃªncia exata de artifact e a uma
  obrigaÃ§Ã£o exata, com producer role e result digest
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:81-92`);
- receipts formais e de fidelity, de owners diferentes, que precisam estar
  ligados Ã  mesma assertion para eligibility
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:150-207`);
- `VerificationReceipt`, request e currentness
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:238-305`);
- `EvidenceReceipt` e a decisÃ£o de discharge, com theorem explÃ­cito de que a
  mesma evidence permite decisions de lifecycle diferentes
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:307-342`);
- `IntegratedProjection`, que pode declarar nÃ£o possuir authority, sem que isso
  complete um judgment de admissibilidade
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:344-358`).

**ForÃ§a: alta.** A consequÃªncia para Schema Service Ã© nÃ£o inferir conformance,
publicaÃ§Ã£o, enforcement ou lifecycle apenas da presenÃ§a de artifact, digest ou
receipt. Isso apoia a separaÃ§Ã£o atual entre schema reference, validation report
e enforcement profile
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:277-282`).

## 6. Como uma skill realmente aparece no corpus

### Capability versus package/path

O registry executÃ¡vel distingue `capability_ref`, `capability_path` e
`tool_profile_ref`; alguns dispatch types nÃ£o tÃªm capability/path apesar de
existirem como valores reservados ou nÃ£o roteÃ¡veis
(`C:/Users/victo/domainspec-lean-formalization/implementations/contracts/dispatch-type-registry.v1.json:4-74`).

Um package separado registra `canonical_source`, `package_version` e hashes de
cada arquivo do runtime package
(`C:/Users/victo/domainspec-lean-formalization/implementations/contracts/register-dispatch-runtime-package.v1.json:1-24`).

O `SKILL.md` instalado de Orchestrate se declara
`generated-native-runtime-package`, aponta para `canonical_source`, registra o
gerador e manda regenerar em vez de editar localmente
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/SKILL.md:1-9`).

**DistinÃ§Ã£o sustentada:** capacidade semÃ¢ntica, path de resoluÃ§Ã£o e package
materializado nÃ£o sÃ£o o mesmo campo. **Lacuna:** nÃ£o hÃ¡ uma identidade estÃ¡vel e
revisionada de `SkillDefinition` nem de `SkillInstallation` jÃ¡ pronta para
reuso.

### Installation/surface

O generation manifest enumera trÃªs superfÃ­cies (`repo-codex`, `repo-local`,
`claude`) e seus package paths, preservando uma fonte canÃ´nica comum; tambÃ©m
adverte que parity de geraÃ§Ã£o nÃ£o prova parity de execuÃ§Ã£o no host
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/generation-manifest.json:17-23`).

Isso fornece um witness concreto para separar:

```text
canonical skill package
    != generated/installed surface
    != runtime capability availability
```

Mas â€œinstallationâ€ ainda colapsa operacionalmente em surface + path +
provenance de geraÃ§Ã£o. NÃ£o hÃ¡ `InstallationId`, lifecycle ou histÃ³rico de
revisÃµes.

### Tool binding

O host profile mapeia aÃ§Ãµes abstratas (`spawn`, `wait`, `interrupt`,
`inventory`, `message`) para operaÃ§Ãµes nativas do Codex e exige que
disponibilidade venha do catÃ¡logo ativo de tools, nÃ£o de documentaÃ§Ã£o ou de um
adapter instalado
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/hosts/codex-native.md:1-20`,
`:49-67`).

Logo, a tool Ã© uma realizaÃ§Ã£o host-specific de uma operaÃ§Ã£o requerida pela
capability; nÃ£o Ã© a prÃ³pria skill. `ToolBinding` sÃ³ merece artifact prÃ³prio se
adquirir owner, identidade e lifecycle independentes. Por enquanto uma relaÃ§Ã£o
versionada entre installation/profile e operaÃ§Ã£o Ã© suficiente.

### Invocation/action

Uma aÃ§Ã£o persistida possui IDs separados para action, dispatch, run, wave e
step, alÃ©m de `capability_ref`, target, mode, scopes e input/output refs
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/schemas/action.schema.json:6-48`).
Um run real instancia exatamente essa forma
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/native-runs/2026-08-21-attempt-workspace-provenance/run-001/run-plan.json:10-45`).

**DistinÃ§Ã£o sustentada:** invocation/action nÃ£o deve herdar a identidade da
skill nem da tool. Ela tem contexto causal e autorizaÃ§Ã£o prÃ³prios.

### Receipt

O receipt de aÃ§Ã£o repete os IDs de action/dispatch/run/wave/step,
`capability_ref` e `agent_id`, e acrescenta status, artifacts, validation,
blockers e tempos
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/schemas/receipt.schema.json:1-28`).
Um receipt persistido confirma que o contrato Ã© usado operacionalmente
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/native-runs/2026-08-21-attempt-workspace-provenance/run-001/receipts-wave2/r07-synthesis.json:1-3`).

HÃ¡ ainda um witness Lean mais estreito: `PassReceipt` Ã© indexado pelo work pack
oferecido em uma phase e sua existÃªncia seleciona a prÃ³xima phase; o arquivo
nega runtime enforcement e snapshot final
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/ReceiptIndexedWorkPackProtocol.lean:6-20`,
`:32-76`).

**DistinÃ§Ã£o sustentada:** receipt evidencia uma execuÃ§Ã£o situada; ele nÃ£o Ã© uma
revision da skill, nÃ£o Ã© a installation e nÃ£o ganha authority para novo trabalho.

## 7. Tabela de encaixe para `skill-first`

| candidato no Schema Service | precedente mais prÃ³ximo | o que o precedente sustenta | o que continua aberto |
|---|---|---|---|
| `SkillType` | `capability_ref` | identidade semÃ¢ntica usada para routing | owner, estabilidade temporal, relaÃ§Ã£o com `type` |
| `SkillSchemaDefinitionRevision` | nenhum equivalente | apenas que capability e package/path sÃ£o separÃ¡veis | metaschema, objective normativo, bases, publicaÃ§Ã£o |
| `SkillSourcePackageSnapshot` | runtime package + file hashes | package versionado por conteÃºdo e fonte canÃ´nica | identidade durÃ¡vel do package, revisÃ£o/publicaÃ§Ã£o |
| `SkillInstallationSnapshot` | generated surface/package path | mesma fonte pode gerar superfÃ­cies distintas; parity de bytes nÃ£o prova parity operacional | `InstallationId`, lifecycle, freshness, mÃºltiplos hosts |
| `ToolBinding` | host operation map | operaÃ§Ã£o abstrata e tool nativa sÃ£o separadas | artifact ou relaÃ§Ã£o? owner e revisÃ£o |
| `SkillInvocation` | persisted action | IDs e contexto causal prÃ³prios; capability Ã© referÃªncia | artifact identity e vÃ­nculo exato Ã  installation/package revision |
| `InvocationReceipt` | action receipt + `PassReceipt` | receipt Ã© outcome escopado a action/context | digests de inputs/outputs, validator version, supersession |
| output `Artifact` | receipt `artifacts[]` | execuÃ§Ã£o pode retornar mÃºltiplos outputs | hoje sÃ£o paths; falta enrollment, stable ID, schema e snapshots |

## 8. ComparaÃ§Ã£o direta com o README do Schema Service

### Alinhamentos sustentados

- **Identity â‰  representation.** O path-derived ID de `lean_file@0.2` funciona
  apenas para uma projeÃ§Ã£o regenerÃ¡vel, oferecendo um bom negative control para
  o `ArtifactId` durÃ¡vel.
- **Artifact pode exercer papÃ©is combinados.** A reversÃ£o de
  representation-composition rejeita classes disjuntas, alinhada ao README.
- **Manifest e representation sÃ£o papÃ©is lÃ³gicos.** O corpus materializa vÃ¡rias
  combinaÃ§Ãµes locais; nÃ£o hÃ¡ uma serializaÃ§Ã£o universal.
- **Validation Ã© escopada.** Request, package/subject digests, exact scope,
  snapshot e supersession participam de currentness.
- **Skill, tool, invocation e receipt sÃ£o diferentes.** Os contratos de runtime
  tornam a separaÃ§Ã£o operacional, nÃ£o apenas nominal.

### AfirmaÃ§Ãµes do Schema Service ainda sem precedente suficiente

- `MetaSchema` como bootstrap root;
- schema definition como artifact que conforma ao metaschema;
- `Type` semÃ¢ntico separado de `SchemaDefinitionRevision` com publicaÃ§Ã£o
  imutÃ¡vel;
- `ManifestRevision` universal;
- `RepresentationSnapshot` universal ou por famÃ­lia com interface comum;
- stable artifact identity independente de location;
- resolver de effective schema e weakening;
- fallback schemas universais;
- aquisiÃ§Ã£o uniforme de `objective_ref` e `tags`.

O `lean_file@0.2` exige `tags`, mas isso Ã© contrato de uma projeÃ§Ã£o especÃ­fica,
nÃ£o evidÃªncia para tornar `tags` universal
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:8-20`,
`:85-96`). JÃ¡ a skill Orchestrate possui um bloco textual `<objective>`, mas seu
schema/frontmatter nÃ£o demonstra uma propriedade universal de metaschema
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/SKILL.md:59-70`).

## 9. RelaÃ§Ãµes: o que nomear e o que nÃ£o colapsar

Uma proposta nÃ£o validada do prÃ³prio corpus jÃ¡ separa `instanceOf` (construÃ§Ã£o
Lean que habita um dock) de `conformsTo` (leg Spivak) e adia completamente o
segundo storey
(`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:74-99`,
`:132-169`). Como o arquivo se declara `proposal`, `veracidade: low` e diz que
nada foi validado, isso vale como warning, nÃ£o como contrato
(`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:1-21`).

Para o experimento de skill, a gramÃ¡tica mÃ­nima a testar deveria manter estas
relaÃ§Ãµes distintas:

```text
manifest/schema_definition  --references_schema--> schema_revision
validation_report           --validated_against--> schema_revision + snapshot
source_package_snapshot      --materializes-------> skill_definition_revision
installation_snapshot       --generated_from-----> source_package_snapshot
invocation                  --selects------------> capability/skill revision
invocation                  --runs_against--------> installation snapshot
host_profile                --maps_operation_to---> native tool
receipt                     --reports_on----------> invocation/action
receipt                     --produces------------> artifact refs
representation_snapshot     --observes------------> representation
representation              --represents----------> artifact
```

NÃ£o registrar `conforms_to` como fato autoral simples. Uma referÃªncia ao schema
nÃ£o prova conformance, e conformance estrutural nÃ£o prova publicaÃ§Ã£o,
enforcement ou adequaÃ§Ã£o semÃ¢ntica.

## 10. Melhorias propostas para `research-initial-definitions.md`

O documento inicial jÃ¡ formula corretamente a maior parte das lacunas. Esta
exploraÃ§Ã£o permite tornÃ¡-las mais testÃ¡veis:

1. **Adicionar um eixo â€œunidades operacionais da skillâ€.** Perguntar
   separadamente pela identidade e lifecycle de definition, source package,
   installation, host/tool binding, invocation/action e receipt.
2. **Registrar dois precedentes positivos e um negative control.** Positivos:
   `VersionedRef(logicalId, version, digest)` e o conjunto
   capability/package/action/receipt do runtime. Negative control:
   `lean_file@0.2` com ID derivado de path.
3. **NÃ£o usar â€œmanifestâ€ sem qualificador.** Distinguir artifact manifest,
   corpus manifest, context manifest e generation/install manifest.
4. **Tornar currentness um problema explÃ­cito.** A pesquisa deve perguntar qual
   request, schema revision, representation snapshot, validator version e
   supersession state limitam cada validation report.
5. **Adicionar um teste de nÃ£o-colapso.** Duas installations da mesma capability
   em paths/hosts diferentes devem preservar skill identity, mas ter snapshots
   e operational availability diferentes.
6. **Adicionar outro teste de nÃ£o-colapso.** A mesma invocation semanticamente
   pretendida, executada por duas host operations, nÃ£o deve produzir receipts
   intercambiÃ¡veis sem bindings exatos de action/run/installation/tool.
7. **Manter `ToolBinding` como hipÃ³tese de relaÃ§Ã£o.** PromovÃª-lo a artifact sÃ³ se
   um corpus mostrar owner, identity, lifecycle ou referÃªncias independentes.
8. **NÃ£o usar o sibling repo como prova de metaschema.** O seu `Schema` formal Ã©
   uma categoria pequena; seus JSON Schemas e generation manifests nÃ£o compÃµem
   um `SchemaDefinitionRevision` self-describing.
9. **Separar obrigatoriedade de presenÃ§a da origem do valor.** O fato de
   `lean_file@0.2` exigir `tags`, ou uma skill conter `<objective>`, nÃ£o decide se
   o envelope universal deve materializar, herdar ou derivar esses valores.

## Veredito de transferÃªncia

| proposiÃ§Ã£o | veredito |
|---|---|
| Reusar a trÃ­ade identidade lÃ³gica + versÃ£o + digest | **GO como forma**, polÃ­tica exata ainda aberta |
| Separar skill definition, package/installation, invocation, tool binding e receipt | **GO para o experimento** |
| Tratar path/digest como `ArtifactId` | **KILL**; sÃ³ serve ao snapshot/projeÃ§Ã£o local |
| Reusar um â€œmanifestâ€ do sibling repo como envelope universal | **KILL**; contratos homÃ´nimos e diferentes |
| Criar `Representation` universal agora | **DEFER**; revisÃ£o local rejeitou o universal sem consumer/laws |
| Tratar artifact e representation como kinds disjuntos | **KILL**; papÃ©is podem coexistir por edge |
| Alegar que o sibling repo implementa metaschema/reflection closure | **KILL**; nenhum witness correspondente foi encontrado |
| Usar a skill como primeira witness do metaschema | **GO como hipÃ³tese experimental**, nÃ£o como conclusÃ£o herdada |

O menor resultado responsÃ¡vel Ã©: **o sibling repo sustenta a decomposiÃ§Ã£o
operacional da skill e a disciplina de identidade/snapshot/receipt, mas deixa o
metaschema, o artifact manifest universal e a identidade durÃ¡vel para o Schema
Service realmente projetar e testar.**


---

## 03 — literatura primária de multilevel metamodeling

---
artifact_kind: research-report
status: candidate-evidence
date: 2026-08-25
topic: multilevel-metamodeling-literature
scope: primary-literature-comparison
---

# Literatura de multilevel modeling e metamodeling

## Resposta curta

A literatura confirma que um elemento pode ter uma faceta de instÃ¢ncia em relaÃ§Ã£o ao que o
classifica e uma faceta de tipo em relaÃ§Ã£o ao que ele prÃ³prio classifica. Ela **nÃ£o** confirma,
porÃ©m, que o Schema Service precise representar isso por nÃ­veis globais, `clabjects`, potÃªncia ou
uma Ãºnica relaÃ§Ã£o transitiva `conforms_to`.

HÃ¡ pelo menos trÃªs soluÃ§Ãµes estruturalmente diferentes para o caso que nos interessa:

1. representar definiÃ§Ãµes de schema como dados tipados por um metaschema, mantendo referÃªncias e
   validaÃ§Ãµes de cada salto separadas;
2. separar classificaÃ§Ã£o linguÃ­stica e ontolÃ³gica em dois eixos;
3. adotar instanciaÃ§Ã£o profunda, na qual caracterÃ­sticas definidas acima podem governar instÃ¢ncias
   indiretas vÃ¡rios saltos abaixo.

O primeiro witness de `skill` ainda nÃ£o demonstrou a necessidade das capacidades extras de 2 ou 3.
Assim, `clabject`, deep instantiation e potency devem entrar nas definiÃ§Ãµes iniciais como candidatos
com collapse-tests, nÃ£o como vocabulÃ¡rio aceito.

## Escopo e mÃ©todo

Este levantamento comparou fontes primÃ¡rias indicadas pelo usuÃ¡rio com trabalhos primÃ¡rios sobre
Type Object, MOF, meta-arquiteturas reflexivas e evoluÃ§Ã£o de metamodelos/schemas. PÃ¡ginas editoriais
foram usadas somente para confirmar metadados quando o PDF de autor nÃ£o os trazia claramente.

Os termos mudam entre abordagens. Em particular, â€œlogical/physicalâ€ em 2001â€“2002 passa a
â€œontological/linguisticâ€ no artigo de 2003, e a literatura posterior nÃ£o possui terminologia
unificada. Logo, equivalÃªncias terminolÃ³gicas abaixo sÃ£o contextualizadas, nÃ£o presumidas.

## VerificaÃ§Ã£o dos quatro tÃ­tulos sugeridos

| tÃ­tulo | autoria, ano e venue verificados | conteÃºdo que o trabalho efetivamente sustenta |
| --- | --- | --- |
| *The Essence of Multilevel Metamodeling* | Colin Atkinson e Thomas KÃ¼hne, 2001, *Â«UMLÂ» 2001*, LNCS 2185, pp. 19â€“33, DOI 10.1007/3-540-45441-1_3 | Diagnostica ambiguous classification e replication of concepts na instanciaÃ§Ã£o rasa; propÃµe deep instantiation, potÃªncia, campos e um MoMM preliminar. O prÃ³prio artigo diz que o trabalho era preliminar. [PDF dos autores, seÃ§Ãµes 2â€“5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) |
| *Rearchitecting the UML Infrastructure* | Colin Atkinson e Thomas KÃ¼hne, 2002, *ACM Transactions on Modeling and Computer Simulation* 12(4), pp. 290â€“321, DOI 10.1145/643120.643123 | Separa classificaÃ§Ã£o lÃ³gica/fÃ­sica, unifica facetas classe/objeto e discute deep instantiation. Importante: termina deixando em aberto se Ã© melhor manter dois eixos ou realinhÃ¡-los por deep instantiation. [PDF dos autores, especialmente seÃ§Ãµes 4.1â€“5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) |
| *Model-Driven Development: A Metamodeling Foundation* | **Colin Atkinson e Thomas KÃ¼hne**, nÃ£o KÃ¼hne sozinho; 2003, *IEEE Software* 20(5), pp. 36â€“41, DOI 10.1109/MS.2003.1231149 | Argumenta que metamodelagem apenas como definiÃ§Ã£o de linguagem Ã© insuficiente para MDD e distingue instanciaÃ§Ã£o linguÃ­stica e ontolÃ³gica. NÃ£o apresenta um teorema de correÃ§Ã£o da Orthogonal Classification Architecture. [VersÃ£o publicada dos autores, seÃ§Ãµes 3.1â€“3.3](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/mda-foundation-real.pdf) |
| *Multi-level modeling: cornerstones of a rationale* | Ulrich Frank, versÃ£o de registro de 2022, *Software and Systems Modeling* 21, pp. 451â€“480, DOI 10.1007/s10270-021-00955-1 | Ã‰ uma avaliaÃ§Ã£o argumentativa multiperspectiva, nÃ£o uma unificaÃ§Ã£o formal do campo. Identifica conceitos recorrentes, variaÃ§Ãµes e benefÃ­cios, mas tambÃ©m falta de terminologia comum, ferramentas maduras, mÃ©todos de design e integraÃ§Ã£o adequada com linguagens de programaÃ§Ã£o. [Artigo open access, seÃ§Ãµes 2, 3.1.6 e 6](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) |

## DistinÃ§Ãµes que a literatura obriga a preservar

### Um â€œnÃ­velâ€ nÃ£o Ã© um objeto

A correÃ§Ã£o proposta na conversa Ã© vÃ¡lida: uma populaÃ§Ã£o pode ser organizada em nÃ­veis, mas sÃ£o os
elementos que entram em relaÃ§Ãµes de classificaÃ§Ã£o. A definiÃ§Ã£o clÃ¡ssica de strict metamodeling de
Atkinson e KÃ¼hne exige que cada elemento de `M_m` seja instÃ¢ncia de exatamente um elemento de
`M_(m+1)` e que relaÃ§Ãµes nÃ£o-instanciaÃ§Ã£o permaneÃ§am no mesmo nÃ­vel. O nÃ­vel Ã©, portanto, uma
partiÃ§Ã£o arquitetural derivada dessas regras, nÃ£o a entidade que desempenha as facetas classe/objeto.
[Rearchitecting, seÃ§Ã£o 2.2, pp. 293â€“294 da versÃ£o publicada](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf)

Isso nÃ£o autoriza a cadeia sem qualificaÃ§Ã£o:

```text
x conforms_to S0 conforms_to S1
```

Nos trabalhos examinados, â€œinstance-ofâ€ jÃ¡ se divide em sabores diferentes. No Schema Service,
`schema_ref`, classificaÃ§Ã£o de domÃ­nio, satisfaÃ§Ã£o de constraints, execuÃ§Ã£o de validaÃ§Ã£o e conclusÃ£o
de um relatÃ³rio acrescentam ainda outros atos. Nenhuma fonte sustenta que eles sejam equivalentes ou
transitivos.

### Facetas relativas nÃ£o eliminam kinds governados

*Meta-level Independent Modelling* introduz `clabject` como um elemento instanciÃ¡vel que possui ao
mesmo tempo faceta de objeto â€” caracterÃ­sticas recebidas de seu tipo â€” e faceta de classe â€”
caracterÃ­sticas destinadas Ã s suas instÃ¢ncias. Isso Ã© mais especÃ­fico do que a afirmaÃ§Ã£o geral â€œalgo
pode ser schema e instÃ¢ncia em relaÃ§Ãµes diferentesâ€. [Atkinson e KÃ¼hne 2000, seÃ§Ã£o 3.2](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/level-indep.pdf)

Portanto, a literatura apoia a relatividade dos papÃ©is, mas nÃ£o a conclusÃ£o de que kinds como
`SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot` e `ValidationReport`
devam desaparecer. Um record pode conservar kind, identidade e lifecycle prÃ³prios enquanto participa
de relaÃ§Ãµes relativas.

### ClassificaÃ§Ã£o linguÃ­stica e ontolÃ³gica nÃ£o sÃ£o a mesma pergunta

Na Orthogonal Classification Architecture (OCA):

- a classificaÃ§Ã£o linguÃ­stica diz com quais construtos da linguagem um elemento foi expresso â€” por
  exemplo, `SkillSchemaRevision` como instÃ¢ncia de `SchemaDefinition`;
- a classificaÃ§Ã£o ontolÃ³gica diz qual papel ou conceito de domÃ­nio o elemento instancia â€” por
  exemplo, uma definiÃ§Ã£o concreta classificando uma famÃ­lia de skills.

O artigo de 2003 afirma que as duas formas ocorrem simultaneamente e localizam o elemento no espaÃ§o
linguagemâ€“ontologia. O artigo de 2002, contudo, deixa aberta a alternativa entre manter os dois eixos e
realinhÃ¡-los por deep instantiation. A OCA Ã© assim uma proposta arquitetural com explicaÃ§Ã£o forte para
dual classification, nÃ£o um resultado inevitÃ¡vel. [MDD Foundation, seÃ§Ã£o 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/mda-foundation-real.pdf) [Rearchitecting, seÃ§Ã£o 5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf)

## ComparaÃ§Ã£o das abordagens

| abordagem | problema que resolve | entidades e relaÃ§Ãµes principais | garantia efetiva | limites/crÃ­ticas nas fontes | collapse-test para Schema Service |
| --- | --- | --- | --- | --- | --- |
| Strict/adjacent-level metamodeling | Impedir levels arbitrÃ¡rios ou semanticamente misturados. | Modelos `M_m`; elementos; `instance-of` Ãºnico para elemento no nÃ­vel imediatamente superior; relaÃ§Ãµes ordinÃ¡rias intranÃ­vel. | Se a disciplina for obedecida, a localizaÃ§Ã£o por nÃ­vel e a fronteira entre levels ficam determinadas pela instanciaÃ§Ã£o. | A combinaÃ§Ã£o de strictness, hierarquia linear e classificaÃ§Ã£o dupla produziu violaÃ§Ãµes e duplicaÃ§Ã£o na UML. O topo requer uma exceÃ§Ã£o/fechamento. [Rearchitecting, seÃ§Ãµes 2.2 e 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) | Se tipos sobrepostos, mÃºltiplas referÃªncias ou relaÃ§Ãµes cross-domain forem legÃ­timos, uma rankeaÃ§Ã£o global deixa de explicar o grafo; strictness pode sobreviver apenas como invariante local de uma relaÃ§Ã£o bem definida. |
| Schemas-as-data / Type Object | Criar novos â€œtiposâ€ em runtime sem gerar subclasses do host. | `TypeClass`, `TypeObject`, `Class`, `Object`; cada `Object` referencia seu `TypeObject` e delega comportamento comum. | Reduz explosÃ£o de subclasses e permite tipos/reclassificaÃ§Ã£o dinÃ¢micos no domÃ­nio da aplicaÃ§Ã£o. | O host nÃ£o trata `TypeObject` como classe real; a aplicaÃ§Ã£o mantÃ©m referÃªncia, delegaÃ§Ã£o e type checking. Os autores alertam para complexidade de design, implementaÃ§Ã£o e composiÃ§Ã£o. [Johnson e Woolf 1998, seÃ§Ãµes Structure e Consequences](https://www.cs.ox.ac.uk/jeremy.gibbons/dpa/typeobject.pdf) | Se `SchemaDefinitionRevision` + interpretador/validador + referÃªncia exata bastarem para o witness de skill, o caso multilevel colapsa para este padrÃ£o estrutural. Se forem necessÃ¡rias constraints herdadas por instÃ¢ncias indiretas, o padrÃ£o sozinho Ã© insuficiente. |
| OCA / classificaÃ§Ã£o ortogonal | Evitar que â€œescrito na linguagem Xâ€ e â€œinstancia conceito Y do domÃ­nioâ€ disputem uma Ãºnica relaÃ§Ã£o `instance-of`. | Eixo linguÃ­stico, eixo ontolÃ³gico; classificadores fÃ­sicos/linguÃ­sticos e lÃ³gicos/ontolÃ³gicos. | Torna explÃ­citas duas classificaÃ§Ãµes simultÃ¢neas e permite aplicar strictness separadamente em cada eixo. | NÃ£o decide automaticamente quantos eixos adicionais existem; o artigo de 2002 pergunta isso explicitamente. Deep instantiation pode realinhar os eixos, e a escolha ficou aberta. [Rearchitecting, seÃ§Ãµes 4.1.3â€“4.1.4 e 5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) | Se cada schema e artifact usa a mesma linguagem estrutural e nenhuma decisÃ£o depende de distinguir classificador linguÃ­stico de ontolÃ³gico, OCA apenas renomeia relaÃ§Ãµes jÃ¡ separadas. Um caso em que os dois classificadores variam independentemente Ã© necessÃ¡rio para nÃ£o colapsar. |
| Clabject / class-object duality | Representar uniformemente um elemento que recebeu caracterÃ­sticas como instÃ¢ncia e ainda define caracterÃ­sticas para suas instÃ¢ncias. | Um `clabject` com faceta de instÃ¢ncia e faceta de tipo; `instance-of` entre clabjects. | Oferece uma unidade conceitual/notacional para as duas facetas. NÃ£o garante por si sÃ³ validaÃ§Ã£o, autoridade ou propagaÃ§Ã£o multissalto. | A formulaÃ§Ã£o original estÃ¡ acoplada a strict metamodeling e a uma semÃ¢ntica uniforme de instanciaÃ§Ã£o. Frank registra que a Ã¡rea nÃ£o tem terminologia Ãºnica. [Meta-level Independent Modelling, seÃ§Ãµes 3.1â€“3.3](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/level-indep.pdf) [Frank 2022, seÃ§Ã£o 2.1](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) | Se uma `SchemaDefinitionRevision` puder ser tratada simplesmente como record governado validado por um metaschema e referenciado por manifests, sem uma operaÃ§Ã£o uniforme sobre suas duas facetas, `clabject` nÃ£o acrescenta capacidade operacional. |
| Deep instantiation + potÃªncia | Permitir que uma definiÃ§Ã£o afete instÃ¢ncias indiretas, evitando replicar conceitos/constraints em cada salto. | Elementos/clabjects, fields e relaÃ§Ãµes; potÃªncia inteira; instanciaÃ§Ã£o reduz level e potÃªncia na proposta original. MetaDepth estende potÃªncia a modelos, constraints e derived attributes e admite potÃªncia ilimitada. | Na semÃ¢ntica especÃ­fica, controla quantos saltos uma caracterÃ­stica atravessa e em que salto exige valor; ferramentas podem verificar essa regra. [Essence, seÃ§Ã£o 4.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) [MetaDepth, seÃ§Ãµes 2â€“3](https://metadepth.org/papers/TOOLS.pdf) | PotÃªncia nÃ£o Ã© uma ideia Ãºnica: ferramentas variam no alvo, na extensÃ£o linguÃ­stica, em associaÃ§Ãµes e constraints. Frank observa que nem associaÃ§Ãµes cross-level fazem parte de um nÃºcleo comum. [Frank 2022, seÃ§Ãµes 2.1â€“2.2](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) | Exigir um exemplo de skill no qual uma propriedade declarada no metaschema governe diretamente uma instÃ¢ncia de skill dois saltos abaixo e nÃ£o possa ser expressa como duas validaÃ§Ãµes/composiÃ§Ãµes explÃ­citas. Sem esse exemplo, potency Ã© excesso de mecanismo. |
| Powertype | Modelar um tipo cujas instÃ¢ncias sÃ£o subtipos de outro tipo, combinando classificaÃ§Ã£o e especializaÃ§Ã£o. | Powertype `P`, tipo particionado `T`, instÃ¢ncias de `P` que sÃ£o subtipos de `T`. | Captura uma forma especÃ­fica de higher-order classification e evita um segundo `instance-of` direto em alguns modelos. | Na anÃ¡lise de Atkinson e KÃ¼hne, powertypes nÃ£o se encaixavam diretamente no stack estrito da UML e nÃ£o resolviam replication of concepts; sÃ£o mais estreitos que deep instantiation. [Essence, seÃ§Ã£o 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) | Se revisÃµes de schema classificam manifests, mas nÃ£o tÃªm instÃ¢ncias que sÃ£o subtipos de um tipo particionado, powertype nÃ£o modela o nosso vÃ­nculo; colapsa para referÃªncia a tipo/schema. |
| Type Object recursivo | Obter mais de dois estratos usando o mesmo padrÃ£o de objetos e delegaÃ§Ã£o. | Cadeia `Object â†’ TypeObject`, repetida: no exemplo, `Videotape â†’ Movie â†’ MovieCategory`. | Permite nesting arbitrÃ¡rio na aplicaÃ§Ã£o sem exigir metaclasses do host. | Cada salto adiciona delegaÃ§Ã£o e manutenÃ§Ã£o manual; o prÃ³prio paper mostra que a composiÃ§Ã£o pode ficar complexa. NÃ£o fornece semÃ¢ntica formal uniforme de propagaÃ§Ã£o. [Johnson e Woolf 1998, â€œNested Type Objectsâ€](https://www.cs.ox.ac.uk/jeremy.gibbons/dpa/typeobject.pdf) | Se duas referÃªncias exatas e dois relatÃ³rios de validaÃ§Ã£o explicarem `skill â†’ skill-schema â†’ metaschema`, nesting basta como representaÃ§Ã£o; isso ainda nÃ£o prova deep instantiation. |
| Self-describing / meta-circular / reflective | Encerrar a escalada de metanÃ­veis preservando introspecÃ§Ã£o e manipulaÃ§Ã£o homogÃªnea do topo. | MetanÃ­vel superior descrito por seus prÃ³prios conceitos; ciclo de compliance; bootstrap a partir de um core mÃ­nimo. | Demonstra fechamento estrutural em implementaÃ§Ãµes como MOF: o metalanguage pode representar sua prÃ³pria definiÃ§Ã£o. [Emerson, Sztipanovits e Bapty 2004, seÃ§Ã£o 3.1](https://www.jucs.org/jucs_10_10/a_mof_based_metamodeling/Emerson_M_J.pdf) | Self-description cria dependÃªncia circular e bootstrapping; reflexÃ£o semÃ¢ntica pode ameaÃ§ar decidibilidade. Um primeiro â€œblindâ€ bootstrap ou kernel externo ainda Ã© necessÃ¡rio. [Ferreira et al. 2010, â€œClosing the Roofâ€ e â€œBootstrappingâ€](https://hillside.net/plop/2010/papers/ACMVersions/papers/ferreira.pdf) | Se o Schema Service nÃ£o precisa editar/introspectar o kernel em runtime, um kernel externo pequeno encerra operacionalmente o bootstrap. Self-description sÃ³ nÃ£o prova self-validation, consistÃªncia, soundness ou autoridade. |

## O que Ã© e nÃ£o Ã© â€œclabjectâ€ para este projeto

O seguinte fato relacional Ã© compatÃ­vel com todas as abordagens examinadas:

```text
SkillManifestRevision â”€â”€references_schemaâ”€â”€â–¶ SkillSchemaRevision
SkillSchemaRevision   â”€â”€references_metaschemaâ”€â”€â–¶ MetaSchemaRevision
```

Isso, sozinho, nÃ£o Ã© witness de clabject. Para justificar o conceito mais forte, seria preciso mostrar
que `SkillSchemaRevision` precisa ser operada uniformemente por duas facetas:

```text
faceta recebida: valores/constraints que caracterizam a revisÃ£o como instÃ¢ncia do metaschema
faceta tipante:  caracterÃ­sticas que a revisÃ£o transmite Ã s suas prÃ³prias instÃ¢ncias
```

Mesmo esse witness ainda nÃ£o justificaria potÃªncia. PotÃªncia sÃ³ acrescenta poder se uma caracterÃ­stica
precisar atravessar mais de uma instanciaÃ§Ã£o sob semÃ¢ntica governada, em vez de ser aplicada por duas
validaÃ§Ãµes explÃ­citas.

## Schema transformation, â€œschema residueâ€ e data migration

### O que estÃ¡ estabelecido

A literatura trata como problemas distintos, mas acoplados:

- **evoluÃ§Ã£o de metamodelo/schema:** mudanÃ§a da estrutura, constraints ou linguagem que governa
  instÃ¢ncias;
- **migraÃ§Ã£o/co-evoluÃ§Ã£o de modelos ou dados:** atualizaÃ§Ã£o das instÃ¢ncias para recuperar conformidade
  ou preservar a semÃ¢ntica pretendida apÃ³s a mudanÃ§a;
- **adaptaÃ§Ã£o de dependentes:** queries, updates, transformaÃ§Ãµes e ferramentas tambÃ©m podem precisar
  mudar.

Rose et al. definem model migration precisamente como atualizar instance models para restabelecer
conformidade apÃ³s evoluÃ§Ã£o do metamodelo e observam que co-evolution Ã© distinta da transformaÃ§Ã£o
model-to-model genÃ©rica. [*Model Migration Case for TTC 2010*, seÃ§Ã£o 1](https://ris.utwente.nl/ws/files/5096115/wp10-03.pdf)

Vermolen, Wachsmuth e Visser mostram uma distinÃ§Ã£o adicional relevante: a mesma diferenÃ§a final entre
dois metamodelos pode resultar de operadores complexos diferentes, e esses operadores podem produzir
efeitos de migraÃ§Ã£o diferentes. Um diff estrutural final nÃ£o preserva sozinho a intenÃ§Ã£o da mudanÃ§a.
[*Reconstructing Complex Metamodel Evolution*, resumo e seÃ§Ã£o 1](https://eelcovisser.org/publications/2011/VermolenWV11sle.pdf)

No domÃ­nio de bancos, PRISM++ separa mudanÃ§as estruturais de schema, evoluÃ§Ã£o de integrity
constraints, migraÃ§Ã£o de dados e reescrita de queries/updates. O paper fornece uma condiÃ§Ã£o formal de
soundness para update rewriting sob mappings invertÃ­veis; nÃ£o promete preservaÃ§Ã£o geral para mappings
arbitrÃ¡rios. [Curino et al. 2010, seÃ§Ãµes 1 e 4.2](https://www.vldb.org/pvldb/vol4/p117-curino.pdf)

Frank tambÃ©m separa dois riscos: deletar conceitos de um schema ameaÃ§a a integridade das Ã¡rvores de
schemas; mapear modelos a linguagens menos expressivas pode perder abstraÃ§Ã£o e informaÃ§Ã£o.
[*Cornerstones*, seÃ§Ãµes 3.1.2â€“3.1.3](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf)

### O que nÃ£o estÃ¡ estabelecido

No corpus primÃ¡rio delimitado, **`schema residue` nÃ£o aparece como termo tÃ©cnico para â€œconceitos,
distinÃ§Ãµes, relaÃ§Ãµes ou invariantes perdidos numa transformaÃ§Ã£oâ€**. Buscas pela expressÃ£o exata nÃ£o
encontraram ownership relevante; ocorrÃªncias de â€œresidueâ€ pertenciam a outros conceitos. Isso nÃ£o prova
inexistÃªncia na literatura inteira, mas impede importar o termo como se jÃ¡ tivesse definiÃ§Ã£o estabelecida.

Se o projeto mantiver `schema residue`, deve marcÃ¡-lo como termo local provisÃ³rio e fornecer um predicado
operacional, por exemplo:

```text
hÃ¡ resÃ­duo de schema em uma transformaÃ§Ã£o T apenas se uma obrigaÃ§Ã£o declarada
do schema-fonte nÃ£o possui preservaÃ§Ã£o, traduÃ§Ã£o explÃ­cita ou perda registrada no alvo
```

Esse predicado ainda precisaria distinguir ao menos: perda intencional, incompatibilidade expressiva,
erro de mapping e obrigaÃ§Ã£o nÃ£o decidida. Sem isso, â€œresidueâ€ apenas renomeia â€œalgo se perdeuâ€ e falha
o teste de soundness definicional.

## ImplicaÃ§Ãµes para `research-initial-definitions.md`

Estas sÃ£o melhorias de enquadramento, nÃ£o decisÃµes de adoÃ§Ã£o.

### 1. Substituir a pergunta â€œqual torre?â€ por trÃªs perguntas discriminantes

1. O witness de skill exige somente schemas-as-data e validaÃ§Ãµes adjacentes independentes?
2. Existe um caso concreto em que classificaÃ§Ã£o linguÃ­stica e ontolÃ³gica variam independentemente e
   afetam uma operaÃ§Ã£o?
3. Existe uma caracterÃ­stica que precisa governar instÃ¢ncias indiretas, tornando deep instantiation
   observavelmente diferente de composiÃ§Ã£o de schemas e validaÃ§Ãµes separadas?

Se 2 e 3 nÃ£o tiverem witness, OCA, clabject e potÃªncia nÃ£o ganham justificativa operacional.

### 2. Tornar as hipÃ³teses concorrentes explÃ­citas

```text
H1 â€” two-level/schema-as-data:
     SchemaDefinitionRevision Ã© um record tipado pelo MetaSchema e interpretado por validaÃ§Ã£o.

H2 â€” classificaÃ§Ã£o ortogonal:
     o sistema precisa representar separadamente classificadores linguÃ­sticos e ontolÃ³gicos.

H3 â€” deep instantiation:
     regras de um elemento superior precisam atravessar mais de um salto de instanciaÃ§Ã£o.

H4 â€” fechamento externo:
     um kernel confiado encerra o bootstrap; schemas acima continuam sendo artifacts ordinÃ¡rios.

H5 â€” fechamento meta-circular:
     o kernel representa a si prÃ³prio e hÃ¡ um procedimento explÃ­cito de bootstrap.
```

H1â€“H3 nÃ£o sÃ£o mutuamente exclusivas, mas cada capacidade adicional precisa vencer seu collapse-test.
H4 e H5 sÃ£o alternativas de fechamento atÃ© que se especifiquem os componentes hÃ­bridos.

### 3. Separar relaÃ§Ãµes e seus domÃ­nios

As definiÃ§Ãµes iniciais deveriam exigir assinaturas candidatas, sem ainda escolher nomes finais:

```text
references_schema(ManifestRevision, SchemaDefinitionRevision)
references_metaschema(SchemaDefinitionRevision, MetaSchemaRevision)
linguistically_classified_by(RepresentedElement, LanguageClassifier)
ontologically_classified_by(DomainElement, DomainClassifier)
validated_against(ValidationRun, exact target tuple)
concludes_conformance(ValidationReport, scoped claim)
extends(SchemaDefinitionRevision, SchemaDefinitionRevision)
represents(RepresentationSnapshot, ArtifactRevision or Artifact)
```

Nenhuma transitividade deve ser presumida. Em particular, duas referÃªncias nÃ£o constituem uma prova
de conformidade, e conformidade estrutural com o metaschema nÃ£o concede publicaÃ§Ã£o ou enforcement.

### 4. Especificar o alvo exato da meta-validaÃ§Ã£o

A literatura de metamodelagem costuma falar do â€œmodeloâ€ como instÃ¢ncia do metamodelo, mas o Schema
Service distingue definiÃ§Ã£o lÃ³gica, manifest, representaÃ§Ã£o e snapshot. O primeiro experimento deve
comparar explicitamente candidatos como:

```text
validate(logical SchemaDefinitionRevision, MetaSchemaRevision)
validate(RepresentationSnapshot, MetaSchemaRevision)
validate((logical revision, representation snapshot, resolver context), MetaSchemaRevision)
```

Sem essa escolha, afirmar `SkillSchemaRevision conforms_to MetaSchema` omite o objeto realmente
observado e o contexto do veredito.

### 5. Adicionar um witness mÃ­nimo e um anti-witness

Witness mÃ­nimo:

```text
uma skill concreta
â†’ uma ManifestRevision com schema_ref exato
â†’ uma SkillSchemaRevision imutÃ¡vel
â†’ uma MetaSchemaRevision imutÃ¡vel
â†’ dois ValidationReports separados e revision-scoped
```

Anti-witness:

```text
schema_ref resolvÃ­vel, mas artifact invÃ¡lido
ou
SkillSchemaRevision bem formada pelo metaschema, mas semanticamente inadequada/nÃ£o publicada
```

O anti-witness impede o colapso de referÃªncia, validaÃ§Ã£o, adequaÃ§Ã£o e autoridade em `conforms_to`.

## ConclusÃ£o

A literatura possui owners claros para todos os candidatos principais, portanto nenhum deve ser
apresentado como novidade do Schema Service. O resultado Ãºtil Ã© comparativo:

- **GO / build-from-owned** para schemas-as-data como baseline testÃ¡vel, com Type Object e MOF como
  precedentes estruturais, sem inferir que sejam suficientes;
- **GO / build-from-owned condicionado a witness** para OCA, clabject e deep instantiation;
- **GO / build-from-owned condicionado a necessidade de classificaÃ§Ã£o de subtipos** para powertype;
- **DEFER** para fechamento reflexivo/meta-circular, pois self-description nÃ£o implica self-validation,
  consistÃªncia ou autoridade;
- **nÃ£o estabelecido** para `schema residue` como termo da literatura; a distinÃ§Ã£o entre evoluÃ§Ã£o de
  schema/metamodelo e migraÃ§Ã£o de instÃ¢ncias Ã© bem estabelecida, mas o nome e a taxonomia proposta
  ainda sÃ£o locais.

O melhor ganho para as definiÃ§Ãµes iniciais Ã© transformar â€œtorre reflexivaâ€ em uma bateria de perguntas
que compare dois saltos explÃ­citos, dois eixos de classificaÃ§Ã£o, propagaÃ§Ã£o multissalto e fechamento.
Isso permite que o experimento de skill descubra qual capacidade Ã© necessÃ¡ria, em vez de pressupor a
arquitetura que deveria testar.

