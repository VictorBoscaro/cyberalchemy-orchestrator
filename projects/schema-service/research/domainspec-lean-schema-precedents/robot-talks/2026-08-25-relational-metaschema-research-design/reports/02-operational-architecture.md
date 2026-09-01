# Key Findings

- **Papéis relativos coexistem com kinds governados; não os substituem.** O modelo já distingue o
  `Type`, que retém identidade semântica no tempo, da `SchemaDefinitionRevision`, que é sua expressão
  imutável e revision-exacta (`projects/schema-service/README.md:20-25`, `:96-100`). A mesma
  `SchemaDefinitionRevision` pode exercer o papel de contrato diante de um artifact concreto e o
  papel de instância diante do `MetaSchema`, mas continua sendo um record com lifecycle e autoridade
  próprios: autoria, publicação e ativação de enforcement são atos distintos
  (`projects/schema-service/README.md:118-145`). Portanto, “schema de” e “instância de” podem ser
  relações relativas sem tornar relativos os kinds `Type`, `SchemaDefinitionRevision`, `Artifact`,
  `ManifestRevision`, `RepresentationSnapshot` e `ValidationReport`.

- **A torre proposta deve ser desdobrada em relações operacionais não equivalentes.** No modelo
  corrente, um `ManifestRevision` **referencia** uma `SchemaDefinitionRevision`; esta resolve um
  `EffectiveSchema`; `EffectiveSchema + ManifestRevision + RepresentationSnapshot` produzem um
  `ValidationReport`; e um `EnforcementProfile` interpreta esse relatório
  (`projects/schema-service/README.md:64-84`, `:146-156`). Escrever tudo como
  `x conformsTo S0 conformsTo S1` esconde ao menos declaração, resolução, observação, validação e
  decisão operacional. Também sugere transitividade sem suporte: a conformidade de uma definição
  com o metaschema não implica a conformidade de uma skill com essa definição, nem qualquer delas
  autoriza publicação ou enforcement (`projects/schema-service/README.md:137-145`, `:277-282`).

- **O mapeamento completo é um grafo tipado, não uma pilha uniforme.** Um `Type` é a distinção
  semântica; uma `SchemaDefinitionRevision` a expressa; um `EffectiveSchema` é sua closure derivada;
  um `Artifact` é o sujeito durável; um `ManifestRevision` contém suas asserções extensionais e
  referencia a revisão de schema; uma `Representation` torna o artifact acessível; uma
  `RepresentationSnapshot` fixa o estado observado; um `ValidationReport` registra o resultado
  revision-scoped; e o `EnforcementProfile` decide o efeito operacional
  (`projects/schema-service/README.md:198-231`, `:244-257`, `:359-379`). “Nível” não identifica qual
  desses objetos está em jogo e tampouco captura que vários schemas independentes podem coexistir
  no mundo aberto (`projects/schema-service/README.md:43-49`).

- **`skill-first` pode testemunhar duas ordens de validação sem construir uma Reflection Tower.** O
  corte mínimo defensável é: uma `SkillSchemaDefinitionRevision` expressa um `SkillType` e é
  verificada sob uma revisão do metaschema; um `SkillArtifact` tem um `ManifestRevision` que
  referencia aquela revisão, uma representação observada como snapshot, um `ValidationReport`
  produzido contra o `EffectiveSchema` e uma interpretação por `EnforcementProfile`. Isso exercita
  a revisão de skill como contrato “para baixo” e como objeto governado “para cima”, mas não testa
  self-hosting nem exige `S2`. A decisão aceita apenas a ordem `skill-first` e exige primeiro separar
  skill de source package, release, installation, invocation e receipt
  (`docs/decisions/schema-service-first-artifact-experiment.md:11-16`, `:35-37`, `:44-58`).

# Gaps or Inconsistencies

- O README afirma que schema definitions são artifacts, com identidade, objetivo, proveniência e
  revisões imutáveis (`projects/schema-service/README.md:233-242`), enquanto também exige que todo
  artifact admitido tenha um manifest que referencia um schema resolvível
  (`projects/schema-service/README.md:27-31`). Não está definido se uma
  `SchemaDefinitionRevision`-como-artifact precisa de `ManifestRevision`, qual schema esse manifest
  referencia, nem se o conteúdo normativo da definição vive no manifest ou em uma representação.
- A formulação “MetaSchema validates SchemaDefinitionRevision” (`projects/schema-service/README.md:71-73`)
  conflita em granularidade com o pipeline geral, que valida `EffectiveSchema + ManifestRevision +
  RepresentationSnapshot` (`projects/schema-service/README.md:81-84`). Falta declarar o alvo
  canônico da meta-validação: o record lógico, seus bytes representados, seu manifest, ou uma
  composição desses elementos.
- “Conforms to the metaschema” é usado como propriedade da revisão de schema
  (`projects/schema-service/README.md:240-242`), mas o mesmo documento exige que relatórios indiquem
  artifact, observação/digest, `SchemaId` e validator version (`projects/schema-service/README.md:374-379`).
  Não há ainda contrato que aplique essa evidência situada à meta-validação.
- A pesquisa inicial lista a separação entre schema, artifact, manifest e snapshot como constraint
  confirmada, porém ainda não explicita as hipóteses novas sobre papéis relativos, não-transitividade
  ou dois possíveis alvos de validação (`projects/schema-service/research/domainspec-lean-schema-precedents/research-initial-definitions.md:34-45`).

# Local Tensions

- **Universalidade versus bootstrap:** exigir manifest e schema resolvível de todo artifact pode
  gerar uma obrigação recursiva para o próprio metaschema; excetuá-lo cria um kernel confiado que o
  texto atual chama de bootstrap root, mas ainda não formaliza operacionalmente
  (`projects/schema-service/README.md:106-116`, `:233-242`). Self-hosting não decorre dessas linhas.
- **Referência versus prova:** o campo `schema` é requisito de admissão, mas a validade só surge de
  uma observação e de um `ValidationReport`; usar `conformsTo` no dado autoral transformaria uma
  alegação/referência em conclusão (`projects/schema-service/README.md:333-357`, `:359-379`).
- **Conformidade versus autoridade:** uma definição bem formada pode continuar candidata e
  não normativa; publicação exige owner, authority e lifecycle, e enforcement pertence à operação
  governante (`projects/schema-service/README.md:137-145`, `:383-401`). Um único arco de
  `conformsTo` não preserva essas fronteiras.
- **Testemunha pequena versus sujeito indefinido:** `skill-first` oferece um caso operacional forte,
  mas o próprio decision record proíbe inferir uma skill inteira e composta antes de distinguir seus
  papéis (`docs/decisions/schema-service-first-artifact-experiment.md:14-16`, `:35-37`, `:55-58`).
  A meta-validação pode ser demonstrada com uma definição mínima; isso não demonstra que package,
  installation, invocation e receipt compartilham um schema ou uma identidade.

# Questions for Synthesis

- Qual objeto exato o `MetaSchema` valida: a `SchemaDefinitionRevision` lógica, seu
  `ManifestRevision`, uma `RepresentationSnapshot`, ou uma composição explicitamente definida?
- A linguagem deve reservar relações distintas — por exemplo, `references_schema`,
  `validated_against`, `expresses_type`, `represents` e `interprets_report` — e tratar
  `conforms_to` apenas como conclusão de um relatório?
- Uma schema definition admitida como artifact segue integralmente o envelope universal? Se sim,
  qual revisão de schema governa seu manifest sem confundir o metaschema com o conteúdo normativo;
  se não, qual exceção de bootstrap é aceita e onde termina?
- Qual é o menor fixture de skill que contém `Type`, definição, artifact, manifest, representação,
  snapshot, validação e enforcement sem introduzir prematuramente release, installation ou runtime?
- Que afirmação experimental seria suficiente: apenas “uma revisão de skill é bem formada sob o
  metaschema” ou também “ela governa uma instância observada sem que referência, validação e
  autoridade colapsem”?
