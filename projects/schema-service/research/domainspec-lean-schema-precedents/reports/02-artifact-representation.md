# Artefato, instância e representação em `domainspec-lean-formalization`

## Conclusão executiva

O repositório fornece precedentes úteis, mas **não fornece o modelo completo do
Schema Service**. O que ele sustenta com mais força é uma disciplina de
separação:

1. schema e instância têm tipos formais próprios dentro do modelo Spivak;
2. identidade lógica, versão e digest podem formar uma referência exata sem
   reduzir a identidade ao digest;
3. capability, pacote/superfície instalada, ação de invocação, operação nativa
   do host e receipt aparecem como unidades diferentes em contratos
   executáveis;
4. validação e currentness são escopadas por inputs e snapshots, não são
   propriedades intrínsecas do arquivo ou do receipt;
5. representação, artifact e generator não devem ser transformados em classes
   ontológicas universais e mutuamente exclusivas sem um contrato local.

O principal resultado negativo é igualmente importante: não há no corpus uma
implementação de `MetaSchema`, `SchemaDefinitionRevision`, `ManifestRevision`,
`RepresentationSnapshot`, `ArtifactId` ou `SchemaId` com os sentidos propostos
pelo Schema Service. Há várias coisas chamadas “schema”, “manifest”,
“representation” e “receipt”, mas elas não constituem uma cadeia universal.

Para o experimento `skill-first`, o corpus favorece um corte com pelo menos
estas unidades lógicas:

```text
Capability/SkillDefinitionRevision
    -> é materializada por SourcePackageSnapshot
    -> é instalada como InstallationSnapshot
    -> é selecionada por Invocation/Action
    -> é realizada por HostOperation/ToolBinding
    -> produz Receipt e output artifacts
```

Isso é uma hipótese de transferência, não uma equivalência já demonstrada. Em
particular, `ToolBinding` pode continuar sendo uma relação/configuração em vez
de um artifact autônomo até aparecer lifecycle ou identidade independente.

## Escopo e força da evidência

Foram lidos os `AGENTS.md` aplicáveis, o README atual do Schema Service e um
corpus dirigido no repositório-alvo: definições Lean, JSON Schemas, geradores,
records, manifests, receipts, revisões adversariais e documentos que registram
propostas ou reversões. Não houve pesquisa web nem edição do repositório-alvo.

Classificação usada:

| força | significado neste relatório |
|---|---|
| **alta** | definição/teorema Lean, schema ou código consumidor executável |
| **média-alta** | pacote executável acompanhado por testes e revisão adversarial registrada |
| **média** | decisão ou síntese de pesquisa explicitamente escopada |
| **baixa** | backlog, proposta não validada ou analogia |
| **ausência delimitada** | busca textual no corpus inspecionado; não prova inexistência histórica ou externa |

O `check` não mutante do mapa `lean_file@0.2` foi iniciado, mas interrompido antes
de emitir resultado para manter o escopo bounded. Portanto, este relatório não
alega uma reprodução independente. A evidência de `current` é a revisão
existente, que registra 21/21 testes, recomposição não mutante e aprovação
limitada ao pacote v0.2
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/research/lean-file-corpus-v0.2-review/review.md:67-97`).

## 1. “Schema” e “instance” têm um contrato formal, mas não o contrato do Schema Service

### O que está formalizado

No namespace `SchemaInstance`, um `Schema` é um tipo portando uma instância de
`Category`; `Instance S` é um functor de `S.carrier` para `Type`; e
`SchemaMorphism S T` é um functor entre os carriers. O arquivo também implementa
pullback por precomposição e prova identidade e composição
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:57-103`).

**Força: alta.** Esses são tipos Lean e teoremas concretos. Porém, o próprio
arquivo limita a construção ao eixo V e diz que a torre não é diretamente
tipada ali
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/SchemaInstance.lean:27-41`).

### O que não deve ser importado por analogia

O `Schema` de Spivak não é uma `SchemaDefinitionRevision` serializada com
`type`, `objective`, bases, propriedades e lifecycle. A palavra é a mesma, o
objeto não. Uma auditoria local encontrou três noções Lean diferentes chamadas
“Schema”: categoria pequena, carrier de predicates de uma `ResidueStructure` e
wrapper de preorder; ela recomenda higiene de nomes justamente porque não são
intercambiáveis
(`C:/Users/victo/domainspec-lean-formalization/_residue/schema-definition-audit-2026-05-22.md:12-38`,
`:66-80`).

O corpus também contém a tese de que schema/instância são papéis relativos
através de níveis, mas ela está marcada como “Captured, not integrated” e exige
uma decisão de escopo
(`C:/Users/victo/domainspec-lean-formalization/BACKLOG.md:23-33`). O memo posterior
faz uma formulação mais cuidadosa: por nível, schema e instância são tipados;
através de níveis, há uma proposta de role-shift
(`C:/Users/victo/domainspec-lean-formalization/docs/schema-instance-typing.md:78-92`).

**Força do role-shift: baixa a média.** É uma reconciliação documental, não uma
formalização de metaschema, `conformsTo` multinível ou self-hosting.

### Implicação para o metaschema

A busca delimitada não encontrou as entidades exatas `MetaSchema`,
`SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot`,
`ArtifactId` ou `SchemaId` no repositório-alvo. O corpus não decide qual objeto
um metaschema do Schema Service deve validar. Ele tampouco demonstra que uma
definição de schema possa validar a si própria.

Portanto, a afirmação atual do Schema Service — uma schema-definition revision
é instância do metaschema — permanece uma hipótese de produto local
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:106-122`),
não um precedente implementado pelo sibling repo.

## 2. Identidade, versão, digest e path

### Referência versionada: distinção forte

`SpecificationOntology.VersionedRef α` guarda separadamente `logicalId`,
`version` e `payloadDigest`; seu parâmetro phantom impede substituição entre
branches ontológicas, e a igualdade examina os três campos
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:40-64`).

Esse é o precedente mais próximo para a separação do Schema Service entre
identidade semântica, revisão e bytes. Ele sustenta a **forma da separação**, mas
não prova:

- que `logicalId` permaneça estável através de rename/move;
- que `version` seja imutável após publicação;
- que qualquer string seja uma identidade autorizada;
- que `payloadDigest` seja a identidade do artifact.

**Força: alta para a independência dos campos; média para transferência ao
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
Markdown, lakefiles, policy, schemas e versões dos próprios geradores
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:678-691`).

Isso é apropriado porque o artefato se declara uma **projeção do Git index**,
não uma identidade durável: arquivos fora do index não recebem record canônico,
e cada record tem ID derivado do path
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-v0.2-proposal.md:3-10`,
`:82-88`).

**Força: média-alta como precedente operacional; negativa para identidade
durável.** Um rename cria outro ID. Logo, não se deve copiar esse mecanismo para
`ArtifactId`. Ele confirma a distinção do README atual: path e digest podem
identificar uma representação/snapshot sem identificar o artifact durável
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:57-62`).

### Currentness não mora no record

Cada record fixa `freshness.state = requires_validation`; currentness pertence
ao relatório externo
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:85-96`).
O gerador recompõe records e manifest; diferença de bytes produz `stale`, erros
produzem `invalid`/`unresolved`, e igualdade completa produz `current`
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:905-936`).

O mesmo princípio aparece formalmente em `VerificationReceipt.CurrentFor`: o
receipt deve corresponder a request, package digest, subject digest e scope, e
não estar superseded; currentness não é recuperada dos bytes do receipt sozinho
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:238-305`).

**Transferência recomendada:** um `ValidationReport` do Schema Service deve ser
revision/snapshot-scoped e nunca virar um badge intrínseco do artifact.

## 3. “Manifest” é hoje um nome para contratos diferentes

O corpus sustenta pelo menos três usos distintos:

1. **Corpus manifest.** `manifest-v0.2.json` indexa records, paths, aliases,
   imports reversos, owner projections e o snapshot do corpus
   (`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/tools/lean_corpus_map.py:784-795`).
2. **Context manifest.** `ContextManifest` contém a identidade exata dos
   `SourceVersion` selecionados e bytes renderizados; a seleção depende de
   versões de selector/policy/renderer, adapter e budget
   (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/ContextManifestIntegrity.lean:41-109`).
3. **Generation manifest.** o package Orchestrate registra canonical root,
   source `SKILL.md`, policy de geração, support/excluded paths e superfícies
   instaláveis para Codex, repo-local e Claude
   (`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/generation-manifest.json:1-23`).

Esses manifests colapsam operacionalmente apenas dentro de seus contratos
locais. Nenhum é o `ManifestRevision` universal do Schema Service. O nome não
autoriza unificação.

Há, contudo, uma regra transferível: o contexto materializado fecha sobre a
identidade e a versão exatas das fontes selecionadas, não apenas sobre seus
paths
(`C:/Users/victo/domainspec-lean-formalization/lean-engineer/ContextManifestIntegrity.lean:71-109`).

## 4. Representation, carrier, snapshot e observation

### O núcleo formal é menor que um artifact model

`RepresentationEdgeTyping.lean` distingue `EmbeddingEdge` e `QuotientEdge` por
leis: injectividade versus sobrejetividade. Ambas têm identidade e composição,
e witnesses finitos mostram que uma não implica a outra. O próprio arquivo
nega que isso estabeleça satisfaction, refinement observacional ou uma rede
global de representações
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/RepresentationEdgeTyping.lean:8-20`,
`:24-90`).

**Força: alta e estreita.** O precedente é “relações diferentes exigem leis
diferentes”, não “toda representation é um carrier edge”.

### A reversão mais relevante

A síntese de representation-composition rejeitou três universais:

- representação não é apenas sua relação de fibras;
- projection não é sinônimo de qualquer transformação nem implica perda
  estrita;
- generator, representation e artifact não são classes ontológicas universais
  disjuntas
  (`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:595-617`).

Ela substitui a desigualdade rígida “representação semântica ≠ artifact
concreto” por uma formulação relacional: um artifact pode carregar, realizar,
evidenciar ou gerar uma representação em edges diferentes
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:608-612`).

Isso está alinhado ao Schema Service, que já permite que um objeto seja artifact,
representação de outro artifact, ou ambos por identidades e relações explícitas
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:233-251`).

### O que permanece aberto

A mesma síntese registra que não há owner universal de `representation`; mapa,
factorization order e typed edges têm owners separados. Ela adia um tipo
universal e uma API `StructuredRepresentation`
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:322-335`,
`:580-617`).

O stress test de Task Session interpreta context pack, ticket, receipt e
closeout como artifacts parciais sincronizados, mas explicita que não existe
uma interface comum `Representation`
(`C:/Users/victo/domainspec-lean-formalization/experiments/representation-composition/README.md:410-418`).

**Consequência:** `Representation` e `RepresentationSnapshot` no Schema Service
devem continuar como papéis lógicos e interfaces por família. Não há evidência
para congelar um record universal contendo path, digest, context, consumer,
authority e provenance em uma única estrutura.

## 5. Artifact, evidence, validation e lifecycle não colapsam

O kernel de specification separa:

- `EvidenceArtifact`, ligado a uma referência exata de artifact e a uma
  obrigação exata, com producer role e result digest
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:81-92`);
- receipts formais e de fidelity, de owners diferentes, que precisam estar
  ligados à mesma assertion para eligibility
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:150-207`);
- `VerificationReceipt`, request e currentness
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:238-305`);
- `EvidenceReceipt` e a decisão de discharge, com theorem explícito de que a
  mesma evidence permite decisions de lifecycle diferentes
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:307-342`);
- `IntegratedProjection`, que pode declarar não possuir authority, sem que isso
  complete um judgment de admissibilidade
  (`C:/Users/victo/domainspec-lean-formalization/lean-engineer/SpecificationOntologyKernel.lean:344-358`).

**Força: alta.** A consequência para Schema Service é não inferir conformance,
publicação, enforcement ou lifecycle apenas da presença de artifact, digest ou
receipt. Isso apoia a separação atual entre schema reference, validation report
e enforcement profile
(`C:/Users/victo/cyberalchemy-orchestrator/projects/schema-service/README.md:277-282`).

## 6. Como uma skill realmente aparece no corpus

### Capability versus package/path

O registry executável distingue `capability_ref`, `capability_path` e
`tool_profile_ref`; alguns dispatch types não têm capability/path apesar de
existirem como valores reservados ou não roteáveis
(`C:/Users/victo/domainspec-lean-formalization/implementations/contracts/dispatch-type-registry.v1.json:4-74`).

Um package separado registra `canonical_source`, `package_version` e hashes de
cada arquivo do runtime package
(`C:/Users/victo/domainspec-lean-formalization/implementations/contracts/register-dispatch-runtime-package.v1.json:1-24`).

O `SKILL.md` instalado de Orchestrate se declara
`generated-native-runtime-package`, aponta para `canonical_source`, registra o
gerador e manda regenerar em vez de editar localmente
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/SKILL.md:1-9`).

**Distinção sustentada:** capacidade semântica, path de resolução e package
materializado não são o mesmo campo. **Lacuna:** não há uma identidade estável e
revisionada de `SkillDefinition` nem de `SkillInstallation` já pronta para
reuso.

### Installation/surface

O generation manifest enumera três superfícies (`repo-codex`, `repo-local`,
`claude`) e seus package paths, preservando uma fonte canônica comum; também
adverte que parity de geração não prova parity de execução no host
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/generation-manifest.json:17-23`).

Isso fornece um witness concreto para separar:

```text
canonical skill package
    != generated/installed surface
    != runtime capability availability
```

Mas “installation” ainda colapsa operacionalmente em surface + path +
provenance de geração. Não há `InstallationId`, lifecycle ou histórico de
revisões.

### Tool binding

O host profile mapeia ações abstratas (`spawn`, `wait`, `interrupt`,
`inventory`, `message`) para operações nativas do Codex e exige que
disponibilidade venha do catálogo ativo de tools, não de documentação ou de um
adapter instalado
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/hosts/codex-native.md:1-20`,
`:49-67`).

Logo, a tool é uma realização host-specific de uma operação requerida pela
capability; não é a própria skill. `ToolBinding` só merece artifact próprio se
adquirir owner, identidade e lifecycle independentes. Por enquanto uma relação
versionada entre installation/profile e operação é suficiente.

### Invocation/action

Uma ação persistida possui IDs separados para action, dispatch, run, wave e
step, além de `capability_ref`, target, mode, scopes e input/output refs
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/schemas/action.schema.json:6-48`).
Um run real instancia exatamente essa forma
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/native-runs/2026-08-21-attempt-workspace-provenance/run-001/run-plan.json:10-45`).

**Distinção sustentada:** invocation/action não deve herdar a identidade da
skill nem da tool. Ela tem contexto causal e autorização próprios.

### Receipt

O receipt de ação repete os IDs de action/dispatch/run/wave/step,
`capability_ref` e `agent_id`, e acrescenta status, artifacts, validation,
blockers e tempos
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/schemas/receipt.schema.json:1-28`).
Um receipt persistido confirma que o contrato é usado operacionalmente
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/native-runs/2026-08-21-attempt-workspace-provenance/run-001/receipts-wave2/r07-synthesis.json:1-3`).

Há ainda um witness Lean mais estreito: `PassReceipt` é indexado pelo work pack
oferecido em uma phase e sua existência seleciona a próxima phase; o arquivo
nega runtime enforcement e snapshot final
(`C:/Users/victo/domainspec-lean-formalization/lean-formalization/ReceiptIndexedWorkPackProtocol.lean:6-20`,
`:32-76`).

**Distinção sustentada:** receipt evidencia uma execução situada; ele não é uma
revision da skill, não é a installation e não ganha authority para novo trabalho.

## 7. Tabela de encaixe para `skill-first`

| candidato no Schema Service | precedente mais próximo | o que o precedente sustenta | o que continua aberto |
|---|---|---|---|
| `SkillType` | `capability_ref` | identidade semântica usada para routing | owner, estabilidade temporal, relação com `type` |
| `SkillSchemaDefinitionRevision` | nenhum equivalente | apenas que capability e package/path são separáveis | metaschema, objective normativo, bases, publicação |
| `SkillSourcePackageSnapshot` | runtime package + file hashes | package versionado por conteúdo e fonte canônica | identidade durável do package, revisão/publicação |
| `SkillInstallationSnapshot` | generated surface/package path | mesma fonte pode gerar superfícies distintas; parity de bytes não prova parity operacional | `InstallationId`, lifecycle, freshness, múltiplos hosts |
| `ToolBinding` | host operation map | operação abstrata e tool nativa são separadas | artifact ou relação? owner e revisão |
| `SkillInvocation` | persisted action | IDs e contexto causal próprios; capability é referência | artifact identity e vínculo exato à installation/package revision |
| `InvocationReceipt` | action receipt + `PassReceipt` | receipt é outcome escopado a action/context | digests de inputs/outputs, validator version, supersession |
| output `Artifact` | receipt `artifacts[]` | execução pode retornar múltiplos outputs | hoje são paths; falta enrollment, stable ID, schema e snapshots |

## 8. Comparação direta com o README do Schema Service

### Alinhamentos sustentados

- **Identity ≠ representation.** O path-derived ID de `lean_file@0.2` funciona
  apenas para uma projeção regenerável, oferecendo um bom negative control para
  o `ArtifactId` durável.
- **Artifact pode exercer papéis combinados.** A reversão de
  representation-composition rejeita classes disjuntas, alinhada ao README.
- **Manifest e representation são papéis lógicos.** O corpus materializa várias
  combinações locais; não há uma serialização universal.
- **Validation é escopada.** Request, package/subject digests, exact scope,
  snapshot e supersession participam de currentness.
- **Skill, tool, invocation e receipt são diferentes.** Os contratos de runtime
  tornam a separação operacional, não apenas nominal.

### Afirmações do Schema Service ainda sem precedente suficiente

- `MetaSchema` como bootstrap root;
- schema definition como artifact que conforma ao metaschema;
- `Type` semântico separado de `SchemaDefinitionRevision` com publicação
  imutável;
- `ManifestRevision` universal;
- `RepresentationSnapshot` universal ou por família com interface comum;
- stable artifact identity independente de location;
- resolver de effective schema e weakening;
- fallback schemas universais;
- aquisição uniforme de `objective_ref` e `tags`.

O `lean_file@0.2` exige `tags`, mas isso é contrato de uma projeção específica,
não evidência para tornar `tags` universal
(`C:/Users/victo/domainspec-lean-formalization/experiments/research-state-schema-bootstrap/lean-file-map/schemas/lean-file-v0.2.schema.json:8-20`,
`:85-96`). Já a skill Orchestrate possui um bloco textual `<objective>`, mas seu
schema/frontmatter não demonstra uma propriedade universal de metaschema
(`C:/Users/victo/domainspec-lean-formalization/.arcanum/runtime/orchestrate/SKILL.md:59-70`).

## 9. Relações: o que nomear e o que não colapsar

Uma proposta não validada do próprio corpus já separa `instanceOf` (construção
Lean que habita um dock) de `conformsTo` (leg Spivak) e adia completamente o
segundo storey
(`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:74-99`,
`:132-169`). Como o arquivo se declara `proposal`, `veracidade: low` e diz que
nada foi validado, isso vale como warning, não como contrato
(`C:/Users/victo/domainspec-lean-formalization/experiments/corpus-typed-graph-schema/proposal.md:1-21`).

Para o experimento de skill, a gramática mínima a testar deveria manter estas
relações distintas:

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

Não registrar `conforms_to` como fato autoral simples. Uma referência ao schema
não prova conformance, e conformance estrutural não prova publicação,
enforcement ou adequação semântica.

## 10. Melhorias propostas para `research-initial-definitions.md`

O documento inicial já formula corretamente a maior parte das lacunas. Esta
exploração permite torná-las mais testáveis:

1. **Adicionar um eixo “unidades operacionais da skill”.** Perguntar
   separadamente pela identidade e lifecycle de definition, source package,
   installation, host/tool binding, invocation/action e receipt.
2. **Registrar dois precedentes positivos e um negative control.** Positivos:
   `VersionedRef(logicalId, version, digest)` e o conjunto
   capability/package/action/receipt do runtime. Negative control:
   `lean_file@0.2` com ID derivado de path.
3. **Não usar “manifest” sem qualificador.** Distinguir artifact manifest,
   corpus manifest, context manifest e generation/install manifest.
4. **Tornar currentness um problema explícito.** A pesquisa deve perguntar qual
   request, schema revision, representation snapshot, validator version e
   supersession state limitam cada validation report.
5. **Adicionar um teste de não-colapso.** Duas installations da mesma capability
   em paths/hosts diferentes devem preservar skill identity, mas ter snapshots
   e operational availability diferentes.
6. **Adicionar outro teste de não-colapso.** A mesma invocation semanticamente
   pretendida, executada por duas host operations, não deve produzir receipts
   intercambiáveis sem bindings exatos de action/run/installation/tool.
7. **Manter `ToolBinding` como hipótese de relação.** Promovê-lo a artifact só se
   um corpus mostrar owner, identity, lifecycle ou referências independentes.
8. **Não usar o sibling repo como prova de metaschema.** O seu `Schema` formal é
   uma categoria pequena; seus JSON Schemas e generation manifests não compõem
   um `SchemaDefinitionRevision` self-describing.
9. **Separar obrigatoriedade de presença da origem do valor.** O fato de
   `lean_file@0.2` exigir `tags`, ou uma skill conter `<objective>`, não decide se
   o envelope universal deve materializar, herdar ou derivar esses valores.

## Veredito de transferência

| proposição | veredito |
|---|---|
| Reusar a tríade identidade lógica + versão + digest | **GO como forma**, política exata ainda aberta |
| Separar skill definition, package/installation, invocation, tool binding e receipt | **GO para o experimento** |
| Tratar path/digest como `ArtifactId` | **KILL**; só serve ao snapshot/projeção local |
| Reusar um “manifest” do sibling repo como envelope universal | **KILL**; contratos homônimos e diferentes |
| Criar `Representation` universal agora | **DEFER**; revisão local rejeitou o universal sem consumer/laws |
| Tratar artifact e representation como kinds disjuntos | **KILL**; papéis podem coexistir por edge |
| Alegar que o sibling repo implementa metaschema/reflection closure | **KILL**; nenhum witness correspondente foi encontrado |
| Usar a skill como primeira witness do metaschema | **GO como hipótese experimental**, não como conclusão herdada |

O menor resultado responsável é: **o sibling repo sustenta a decomposição
operacional da skill e a disciplina de identidade/snapshot/receipt, mas deixa o
metaschema, o artifact manifest universal e a identidade durável para o Schema
Service realmente projetar e testar.**
