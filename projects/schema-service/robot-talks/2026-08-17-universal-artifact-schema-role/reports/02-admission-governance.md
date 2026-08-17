# Admissão e governança

## Key Findings

- O mínimo universal sustentado hoje é semântico, não uma lista fechada de campos: dentro de um
  escopo governado, o artefato precisa ter identidade estável e uma instância/observação que
  referencie um `SchemaId` resolvível e revision-exact; um fallback satisfaz a referência. O campo
  `id` pode ser derivado de uma fonte confiável, `objective_ref` ainda é candidato, e tags não fazem
  parte do mínimo normativo (`projects/schema-service/README.md:17-20`,
  `projects/schema-service/README.md:223-235`). Portanto, a formulação segura de “todo artefato é
  governado por um schema” é: **todo artefato admitido no boundary governado é descrito por um
  manifesto/observação que aponta para um schema específico ou fallback resolvível** — não que todo
  artefato possua uma `SchemaDefinition` própria (`projects/schema-service/README.md:125-157`).

- A combinação de fallback e vocabulário descritivo permite admitir novidade sem criar um tipo
  normativo por artefato. `document/other@0` ou, sem família conhecida, `artifact/other@0` mantém a
  instância válida; `classification_label` e tags preservam a linguagem do autor, mas não autorizam
  validação ou comportamento. Estruturas repetidas podem motivar uma proposta, nunca publicação
  automática (`projects/schema-service/README.md:97-123`). Em paralelo, tipos publicados são
  extensões independentes descobertas pelo registry, não membros de uma enumeração fechada no schema
  base (`projects/schema-service/README.md:27-33`,
  `projects/schema-service/research/artifact-schema-governance-landscape/research-initial-definitions.md:35-41`).

- Autoridade normativa e consequência operacional já são separadas. Escrever uma definição não a
  publica: a publicação exige operação autorizada, owner, authority, revisão imutável e lifecycle;
  produtores podem propor, mas não publicar silenciosamente. Mesmo um schema publicado não decide
  sozinho se uma violação aconselha, alerta, obriga ou bloqueia — isso pertence a um
  `EnforcementProfile` versionado e ao owner da operação (`projects/schema-service/README.md:80-83`,
  `projects/schema-service/README.md:174-178`, `projects/schema-service/README.md:219-221`). Isso
  sustenta três estatutos distintos — descrição livre, regra publicada e enforcement ativo — mas
  não sustenta ainda um lifecycle completo entre eles.

- Reclassificação deve preservar identidade e proveniência, não reescrever o passado. A identidade
  durável é independente de path e digest; estes identificam uma observação/revisão. Trocar o schema
  aplicado cria nova observação ou revisão do manifesto, preserva a classificação anterior e não
  muta nem o artefato nem o significado dos `SchemaId`s envolvidos
  (`projects/schema-service/README.md:120-150`). Essa é a base necessária para inferir um tipo hoje e
  corrigi-lo amanhã sem fingir que a classificação anterior nunca existiu.

- A evolução de schemas preserva significado por identidade revision-exact: publicar depois não
  altera um `SchemaId` existente, e o effective schema é uma resolução derivada de bases e
  capabilities, não outra fonte autoral (`projects/schema-service/README.md:40-40`,
  `projects/schema-service/README.md:85-95`). No bootstrap, a garantia é deliberadamente limitada a
  um núcleo monotônico, no qual refinamentos apenas adicionam/conjugam restrições; conflitos de
  herança e linguagens mais ricas ainda não são decidíveis pelo contrato atual
  (`projects/schema-service/README.md:92-95`). Além disso, isso é intenção de design, não mecanismo
  implementado (`projects/schema-service/research/artifact-schema-governance-landscape/research-initial-definitions.md:45-48`).

## Gaps or Inconsistencies

- Não há contrato para `draft`, `candidate` ou `provisional`. O texto exige lifecycle no registro de
  publicação e permite que produtores proponham schemas, mas não define estados, transições,
  privilégios, validação local ou se uma instância pode referenciar uma definição ainda não
  normativa (`projects/schema-service/README.md:80-83`,
  `projects/schema-service/README.md:219-221`, `projects/schema-service/README.md:298-298`).

- Não existe critério de promoção capaz de conter explosão de tipos. Repetição é evidência possível,
  não condição necessária ou suficiente, e o processo de propor, revisar, publicar e migrar continua
  aberto (`projects/schema-service/README.md:120-123`,
  `projects/schema-service/README.md:287-299`). **Hipótese:** uma distinção candidata deveria provar
  reutilização ou diferença de contrato, declarar owner e apresentar casos de conformidade antes de
  receber autoridade; o corpus lido não estabelece esse gate.

- A política de fallback não está fechada. A seção normativa diz que cada família governada fornece
  seu próprio `other`, enquanto as perguntas abertas ainda perguntam quais famílias realmente
  precisam dele e o que o fallback pode preservar (`projects/schema-service/README.md:99-102`,
  `projects/schema-service/README.md:289-291`). Também não há regra para determinar ou inferir a
  “família mais próxima” sem transformar inferência em autoridade.

- A identidade estável é requisito, mas sua fonte é delegada ao runtime/operação e permanece
  desconhecida por família. O documento não resolve movimento, duplicação e revisão de conteúdo, nem
  diz quando duas observações representam o mesmo artefato (`projects/schema-service/README.md:147-150`,
  `projects/schema-service/README.md:278-280`, `projects/schema-service/README.md:294-295`).

- Versionamento de schema está separado de reclassificação de instância, mas adoção e migração não
  têm contrato. Não está definido se uma instância permanece indefinidamente em uma revisão antiga,
  como declara compatibilidade com revisão nova, ou como registra uma migração parcial
  (`projects/schema-service/README.md:257-262`, `projects/schema-service/README.md:298-299`;
  `projects/schema-service/research/artifact-schema-governance-landscape/research-initial-definitions.md:82-85`).

- O boundary universal ainda é indeterminado: nem todo objeto no repositório necessariamente será um
  artefato governado, e objetos gerados, vendored, cacheados ou internos podem ser excluídos ou apenas
  observados por registros derivados (`projects/schema-service/README.md:287-295`). Assim, “todo
  artefato” só é defensável depois de qualificar “admitido no escopo governado”.

## Local Tensions

- **Representação mínima versus schema por artefato.** A intenção diz que cada artefato recebe uma
  “minimal schema representation”, mas as camadas posteriores distinguem `SchemaDefinition` de
  `InstanceManifest` (`projects/schema-service/README.md:17-20`,
  `projects/schema-service/README.md:64-90`, `projects/schema-service/README.md:125-145`). Sem
  vocabulário mais preciso, a frase pode induzir exatamente a explosão que o fallback procura evitar:
  criar uma definição nova para cada instância singular.

- **Criação barata versus autoridade controlada.** Um schema customizado pode nascer só com nome,
  base e objetivo, mas publicar é uma operação autorizada e owned
  (`projects/schema-service/README.md:66-83`). A facilidade é compatível com autoria de candidatos,
  porém o texto não define a fronteira entre “criar uma definição” e “introduzir um tipo que governa
  outros artefatos”.

- **Classificação total versus política de família ainda aberta.** A garantia de que toda família tem
  fallback específico é apresentada como design vigente, mas a necessidade desses fallbacks continua
  explicitamente em aberto (`projects/schema-service/README.md:31-33`,
  `projects/schema-service/README.md:99-102`, `projects/schema-service/README.md:289-291`). O fallback
  universal basta para totalidade; os fallbacks de família introduzem semântica e ownership ainda não
  demonstrados.

- **Aprendizagem corretiva versus núcleo monotônico.** Imutabilidade protege o significado passado,
  e o resolver bootstrap proíbe refinamentos que removam garantias herdadas
  (`projects/schema-service/README.md:76-95`). Porém, conhecimento institucional pode descobrir que
  uma garantia anterior era errada. Uma nova identidade/revisão pode preservar o passado sem repeti-la,
  mas supersession, deprecation e migração corretiva ainda não estão definidos
  (`projects/schema-service/README.md:287-299`).

- **Envelope compartilhado versus admissão descentralizada.** Schema Service pretende possuir o
  envelope genérico e o registry, enquanto cada runtime/operação possui boundary de admissão, fonte
  de identidade e enforcement (`projects/schema-service/README.md:266-280`). Logo, o serviço não pode
  sozinho garantir admissão universal; essa garantia depende de contratos de integração ainda não
  especificados.

## Questions for Synthesis

- A síntese adota explicitamente “manifesto/observação com referência a schema” como mínimo de todo
  artefato governado, reservando “schema próprio” para distinções reutilizáveis?

- Quais estados e poderes separam `classification_label`, schema candidato/draft, schema publicado e
  enforcement ativo? Um draft pode validar localmente ou ser referenciado por instâncias sem adquirir
  autoridade sobre terceiros?

- Qual gate mínimo impede explosão de tipos sem bloquear novidade: diferença de contrato, múltiplas
  instâncias, owner explícito, casos de conformidade, ou alguma combinação? **Hipótese para síntese:**
  separar rigorosamente o baixo custo de criar um candidato do custo deliberado de publicá-lo.

- A política inicial deve oferecer apenas `artifact/other`, ou também fallbacks de família? Quem pode
  afirmar a família e como uma inferência é registrada sem se tornar classificação normativa?

- Qual é o modelo temporal mínimo que distingue revisão do conteúdo, nova observação do manifesto,
  reclassificação, migração de schema e correção/supersession de uma regra publicada?

- Como uma revisão posterior corrige conhecimento institucional sem mutar um `SchemaId` antigo e sem
  violar o núcleo monotônico de refinamento: novo tipo, nova linhagem, deprecation, transformação
  explícita, ou outra operação?

- Qual contrato de integração obriga runtimes e produtores a fornecer identidade, provenance e
  schema fallback para que a promessa de admissão universal seja verificável?
