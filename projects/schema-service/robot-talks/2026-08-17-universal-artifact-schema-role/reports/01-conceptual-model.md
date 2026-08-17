## Key Findings

- O menor núcleo coerente precisa separar **papéis**, não impor uma única árvore de objetos: `Domain`
  delimita discurso e governança; `Type` é uma distinção semântica reutilizável; `SchemaDefinition`
  publica um contrato versionado para uma distinção; `Artifact` é o sujeito durável governado;
  `Instance` é esse sujeito considerado sob um contrato; `InstanceManifest` registra as asserções
  dependentes do schema; e `Representation` é uma codificação ou projeção do artefato ou dessas
  asserções. O README já separa definição, manifesto e artefato, além de negar que localização ou
  digest sejam a identidade durável (`projects/schema-service/README.md:64-90`,
  `projects/schema-service/README.md:125-157`). A caracterização de `Domain` como fronteira de
  discurso e governança é uma **hipótese local**, explicitamente identificada como inferência na
  pesquisa anterior (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:35-53`).

- `Type` e `SchemaDefinition` não podem continuar como sinônimos sem deixar a identidade ambígua. O
  corpus chama schemas específicos de categorias, mas também exige revisões imutáveis e permite que
  revisões posteriores fortaleçam o contrato (`projects/schema-service/README.md:64-83`). Isso não
  diz se `document/research@0` e `document/research@1` realizam o mesmo tipo estável ou tipos
  diferentes. **Hipótese:** um tipo possui identidade semântica estável; cada revisão de schema é uma
  expressão normativa, revision-exact, desse tipo. Da mesma forma, `Subtype` deveria significar uma
  relação semântica de inclusão/substituibilidade entre tipos, enquanto `extends`, refinamento de
  contrato e reutilização de capability são relações distintas; o README já reconhece bases,
  capabilities e compatibilidade como problemas diferentes (`projects/schema-service/README.md:85-95`,
  `projects/schema-service/README.md:268-272`).

- `DomainPackage` não está demonstrado como entidade do núcleo. A pesquisa deixa explicitamente em
  aberto se um schema de domínio seria um artefato único, um package versionado ou uma view resolvida
  (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:230-238`).
  **Hipótese:** caso necessário, `DomainPackage` deve ser apenas a unidade versionada que publica ou
  importa definições de tipos, propriedades, relações e regras para um domínio; ele não é o domínio
  nem um supertipo de seus artefatos. Até haver evidência de ownership, lifecycle ou interface
  próprios, promovê-lo a primitiva violaria a cautela de bootstrap já declarada
  (`projects/schema-service/README.md:283-285`).

- `Property` e `Relation` exigem dois níveis: definição intensional e asserção extensional. Uma
  `PropertyDefinition` associa um tipo a valores admissíveis e ao significado da característica;
  uma `PropertyAssertion` atribui um valor a uma instância. Uma `RelationDefinition` declara papéis e
  participantes admissíveis; uma `RelationAssertion` conecta instâncias concretas. O README já
  distingue o que o schema permite/exige dos valores e alvos fornecidos pelo manifesto
  (`projects/schema-service/README.md:125-145`), e a pesquisa distingue assinatura de relação, aresta
  concreta, path e transformação de schema (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:151-165`).
  Portanto, “uma propriedade permanece interna ao artefato” é decisão de representação, não fato do
  modelo conceitual; uma asserção pode ser serializada no conteúdo sem perder seu papel lógico.

- `Rule` e `Composition` não são níveis intercambiáveis. `Rule` é uma restrição ou invariante sobre
  configurações admissíveis; sua publicação não determina sua consequência operacional, pois
  enforcement é separado (`projects/schema-service/README.md:174-178`). `Composition` é uma operação
  semanticamente justificada sobre relações composáveis, acompanhada das leis relevantes; relações
  tipadas ou uma sequência de arestas não a estabelecem (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:118-149`).
  **Hipótese:** o núcleo deve admitir regras sobre propriedades, relações e paths sem chamá-las de
  composição; uma capacidade composicional opcional acrescenta a operação e suas leis somente ao
  domínio que consegue observá-las.

## Gaps or Inconsistencies

- Não existe identidade explícita de `Type` separada de `SchemaId`, nem regra que diga o que permanece
  semanticamente igual entre revisões. A imutabilidade de revisão está confirmada, mas a identidade
  longitudinal da categoria não (`projects/schema-service/README.md:40-40`,
  `projects/schema-service/README.md:76-83`).

- Não está decidido se um artefato pode instanciar simultaneamente mais de um tipo ou schema. O
  envelope atual exige uma referência singular resolvível (`projects/schema-service/README.md:97-102`,
  `projects/schema-service/README.md:228-235`), enquanto a pesquisa considera tipos participando de
  domínios sobrepostos (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:232-238`).

- `Subtype`, refinamento monotônico, múltipla herança e capability reutilizável aparecem próximos,
  mas não possuem semânticas separadas. O próprio README limita a garantia atual a um core
  monotônico e adia compatibilidade mais rica (`projects/schema-service/README.md:85-95`).

- A unidade de ownership permanece indefinida: domínio, tipo, propriedade, relação, regra ou package.
  A pesquisa anterior registra essa pergunta sem resposta
  (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:230-245`).

- O modelo ainda não determina quando uma característica deixa de ser propriedade e passa a ser uma
  entidade ou relação com identidade própria; multiplicidade, recursão e relações muitos-para-muitos
  já são reconhecidas como questão aberta (`projects/schema-service/README.md:193-197`).

- “Qualquer artefato” é forte demais. O contrato atual limita a admissão ao escopo governado e deixa
  em aberto quais objetos gerados, vendorizados, em cache ou internos nem sequer entram nele
  (`projects/schema-service/README.md:17-20`, `projects/schema-service/README.md:287-295`).

## Local Tensions

- **Pertencimento único versus sobreposição.** A assunção aprovada diz que tipos pertencem a domínios
  (`projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/dialogue.md:23-34`),
  mas a pesquisa local admite domínios sobrepostos e tipos que importam capacidades de mais de um
  domínio como proposta ainda não resolvida
  (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:219-238`). O
  modelo mínimo deveria usar relações explícitas como `owned_by`, `defined_in` e `participates_in`,
  não contenção exclusiva. Esta solução é uma **hipótese**.

- **Instância versus manifesto.** A intenção inicial diz que uma instância popula a estrutura para um
  artefato concreto (`projects/schema-service/README.md:12-15`), mas a seção posterior define o
  manifesto como registro distinto do próprio artefato (`projects/schema-service/README.md:125-150`).
  Sem escolher se “instância” significa o artefato-em-um-tipo ou o registro que o descreve, as frases
  “validar a instância” e “versionar a instância” permanecem equívocas.

- **Escada de maturidade versus dimensões independentes.** O README apresenta
  `structured -> relational -> compositional` como progressão (`projects/schema-service/README.md:159-178`),
  mas a pesquisa conclui que composição é apenas uma dimensão e não fornece autoridade,
  temporalidade, evidência ou lifecycle (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:127-149`).
  A escada é útil como expressividade, mas não como maturidade global.

- **Regra sobre path versus composição.** O README chama requisitos sobre alcance a evidência de
  “composition rules” (`projects/schema-service/README.md:180-197`), enquanto a pesquisa exige
  identidade, operação e leis antes de alegar composição categórica
  (`projects/schema-service/research/artifact-schema-governance-landscape/findings.md:118-149`). Uma
  regra que inspeciona um path pode existir sem que paths componham semanticamente.

- **Novo rótulo versus novo tipo institucional.** O fallback permite criar artefatos e preservar
  vocabulário livre, mas declara que rótulos não conferem autoridade e que padrões recorrentes não
  publicam schemas automaticamente (`projects/schema-service/README.md:97-123`). Logo, “tipos novos
  surgem sem bloquear criação” só é verdadeiro se distinguirmos `type candidate` descritivo de
  `Type` publicado e governante. Essa distinção nominal é uma **hipótese**.

## Questions for Synthesis

- `Type` terá identidade estável independente das revisões de `SchemaDefinition`? Se não, como se
  expressa que duas revisões continuam falando da mesma distinção?

- Um artefato pode possuir múltiplas tipagens simultâneas em domínios diferentes, ou existe um schema
  primário com capabilities/perfis adicionais?

- `Subtype` significa inclusão semântica, substituibilidade, refinamento monotônico de contrato ou
  apenas classificação? Quais nomes devem separar essas relações?

- `Domain` é uma fronteira semântica, uma fronteira de autoridade ou ambas? Qual relação existe entre
  `Domain`, um eventual `DomainModel` e o opcional `DomainPackage`?

- Propriedades, relações e regras precisam de identidade, revisão e ownership próprios, ou pertencem
  indivisivelmente a uma revisão de schema de tipo?

- “Instância” deve nomear o artefato considerado sob um tipo, o manifesto que registra suas asserções
  ou um snapshot temporal? Quais desses objetos recebem identidade e versão?

- O termo `composition rule` será reservado para operação e leis composicionais, deixando
  `path constraint` para invariantes que apenas atravessam relações?

