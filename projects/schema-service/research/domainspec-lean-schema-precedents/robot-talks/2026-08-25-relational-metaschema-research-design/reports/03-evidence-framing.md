# Enquadramento de evidência e literatura

## Key Findings

- O `Context` atual deve conservar somente o problema e o corpus: o Schema Service está em
  bootstrap, o primeiro experimento será com `skill` e a fronteira entre definição, pacote,
  instalação, tool, invocation e receipt segue aberta. Isso é sustentado pela decisão aceita, que
  muda apenas a ordem e recusa aprovar antecipadamente schema, critério, fixtures, resolver,
  registry ou runtime (`docs/decisions/schema-service-first-artifact-experiment.md:9-19,
  35-37, 44-58`). A frase de que o repositório irmão “may already distinguish” esses papéis
  (`research-initial-definitions.md:18-21`) deve ser neutralizada: ele **contém material a auditar**;
  qualquer distinção encontrada ainda precisa ter status e força reconstruídos.
- Em `Confirmed Product Constraints` cabem as decisões já possuídas: separar `Type` de
  `SchemaDefinitionRevision`; separar `Artifact` de manifesto e representações; preservar identidade
  durável fora de path/digest; exigir autoridade explícita para publicação; e dar ao objetivo do
  schema significado distinto do objetivo da instância (`README.md:20-35, 54-62, 96-100,
  120-144, 228-250, 347-353`). Não cabem ali “clabject”, deep instantiation, potency, níveis fixos,
  transitividade de `conformsTo`, self-hosting ou fechamento por kernel: o próprio diálogo os mantém
  como premissas sob contestação (`dialogue.md:15-33`).
- `Current Evidence Baseline` deve nomear fonte, status e alcance. A alegação local sobre precedentes
  parciais é sustentável apenas com referência ao findings que encontrou mecanismos reais, mas
  nenhum witness da cadeia completa (`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:10-27,
  31-41`). A decisão `skill-first` também é evidência explícita, não apenas contexto
  (`docs/decisions/schema-service-first-artifact-experiment.md:9-19`). Já “repetir `type` não é
  aceito” e a situação de `objective_ref`/`tags` (`research-initial-definitions.md:54-58`) precisam de
  uma decisão citável ou devem ser formuladas como questões; o README só registra `objective_ref`
  como candidato e `tags` como opcional (`README.md:333-357`).
- A formulação relacional deve entrar em `Known Gaps` como hipótese discriminável: uma
  `SchemaDefinitionRevision` pode exercer papel classificatório em relação a artefatos e papel de
  instância em relação à linguagem que a descreve, mas ainda não está provado que esses sejam o
  mesmo sentido de instanciação, a mesma relação de conformidade ou o mesmo objeto. O modelo local
  já separa referência de schema, validação e enforcement (`README.md:64-87, 198-225`), enquanto o
  Robot Talks exige testar satisfação, referência, validação, classificação, instanciação e
  meta-instanciação separadamente (`dialogue.md:59-69`).
- A sequência bibliográfica proposta não deve começar assumindo que `clabject` é a descrição do
  problema. Primeiro é necessário estabelecer os modelos concorrentes e o significado de cada
  relação: strict metamodeling/two-level typing como baseline, classificação linguística versus
  ontológica/OCA como possível decomposição em dois eixos, e somente então clabject, deep
  instantiation e potency como soluções candidatas. Powertypes e Type Object são contra-modelos ou
  mecanismos alternativos, não sinônimos; reflexão/self-description é uma questão posterior de
  bootstrap e não evidência de adequação semântica. Essa cautela segue a regra já registrada de não
  transferir terminologia de multilevel modeling sem verificar semântica e críticas
  (`dialogue.md:23-33, 71-76`).

## Gaps or Inconsistencies

- O documento inicial mistura três classes epistêmicas. “Schema Service pretende...” pertence ao
  `Context`; decisões aceitas e invariantes de produto pertencem a `Confirmed Product Constraints`;
  correspondências com DomainSpec Lean e com a literatura pertencem a `Current Evidence Baseline`
  somente depois de examinadas. Antes disso, devem aparecer em `Known Gaps` ou como perguntas.
- A literatura proposta está centrada em uma escola e em títulos lembrados de memória. Antes de
  ordenar papers, a pesquisa primária deve verificar autoria, ano, versão, venue e conteúdo exato de
  cada título. Em particular, não está verificado aqui que *The Essence of Multilevel Metamodeling*
  introduza exatamente deep instantiation e potency, que *Rearchitecting the UML Infrastructure*
  estabeleça os três problemas mencionados, nem que *Model-driven development: a metamodeling
  foundation* seja a fonte precisa da distinção linguística/ontológica. Essas são pistas de busca,
  não baseline.
- Faltam contra-posições que possam mostrar que multilevel modeling é desnecessário para o caso:
  strict/adjacent-level metamodeling; modelagem de dois níveis com schemas como dados ordinários;
  nominal versus structural typing; powertype; Type Object; múltipla classificação; e separação
  explícita entre linguagem de definição, contrato de domínio e registros de validação. Também
  faltam críticas a potency/deep instantiation e comparações que mostrem quando elas acrescentam
  poder ou apenas abreviam replicação.
- Faltam claims verificáveis sobre “schema residue”. A distinção entre perda de estrutura/invariantes
  de schema e corrupção de valores de instância é útil como hipótese, mas nenhum documento lido
  demonstra que a literatura usa esse termo, que as falhas são exaustivas, ou que exigem um
  metaschema reflexivo. Deve ser pesquisada como problema de preservação em schema mapping/model
  transformation e data migration, sem importar o rótulo como fato.
- A pesquisa precisa verificar, em fontes primárias, pelo menos: (1) definição formal de clabject e
  se a dualidade é do mesmo elemento ou de facetas distintas; (2) semântica e variantes de potency;
  (3) se deep instantiation permite ou obriga propagação de constraints por mais de um nível; (4)
  diferença formal entre classificação linguística e ontológica; (5) definição e restrições de
  strict metamodeling; (6) relação — equivalência, especialização ou alternativa — entre clabjects,
  powertypes e Type Object; (7) tratamento de identidade, múltipla classificação e relações
  cross-level; (8) o que um meta-metamodel self-describing realmente fecha; e (9) quais garantias
  ficam necessariamente fora dele (consistência, soundness, adequação semântica e autoridade).

## Local Tensions

- **Fechamento já afirmado versus fechamento reaberto.** O README diz que schemas são artifacts que
  conformam ao metaschema, que isso não requer torre infinita e que o metaschema é a fundação de
  bootstrap (`README.md:240-242`; também `README.md:106-116`). O diálogo, corretamente, trata kernel,
  self-hosting e outras arquiteturas como questões (`dialogue.md:17-19, 29`). Para a pesquisa, a
  posição segura é: existe uma **raiz de bootstrap proposta**, mas o mecanismo e as garantias de
  fechamento não estão demonstrados.
- **Papel relativo versus kind governado.** Dizer que “schema” e “instância” são papéis relativos
  ajuda a explicar `S0` em duas relações, mas não elimina kinds com identidade e lifecycle próprios.
  O README exige `Type`, `SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot` e
  `ValidationReport` separados (`README.md:20-35, 64-84, 198-250`). Colapsá-los sob `clabject`
  perderia precisamente as distinções que o produto quer testar.
- **Uma seta, vários compromissos.** A cadeia `x conformsTo S0 conformsTo S1` pode esconder
  `references_schema`, satisfação model-teórica, resultado de validação, classificação ontológica e
  conformidade linguística. O pipeline local não os trata como equivalentes
  (`README.md:75-83, 217-225`). A pesquisa não deve perguntar se a cadeia “existe” sem primeiro
  tipar cada aresta e negar transitividade por padrão.
- **Witness epistemológico versus decisão experimental.** `Claim`, `Evidence` ou `Hypothesis` podem
  servir como corpus de comparação, mas a decisão aceita escolheu `skill` para o primeiro
  experimento e manteve seu recorte em aberto (`docs/decisions/schema-service-first-artifact-experiment.md:11-19,
  35-37`). Promover Craft a “primeiro witness” alteraria a decisão; usá-lo como corpus secundário
  para testar expressividade não altera.
- **Bem-formado versus adequado/normativo.** Mesmo que `S0` seja aceito por `S1`, isso pode provar
  apenas que uma representação de schema satisfaz uma linguagem estrutural. Publicação e
  enforcement continuam operações autorizadas separadas (`README.md:137-144`), e o diálogo já
  contesta que conformidade com metaschema estabeleça adequação semântica (`dialogue.md:27-28`).

## Questions for Synthesis

- O `research-initial-definitions` deve manter dois tracks explícitos — precedente local no
  `domainspec-lean-formalization` e literatura primária — com matrizes de evidência separadas, ou a
  expansão de escopo justifica um segundo initial-definitions para evitar que analogia bibliográfica
  seja confundida com decisão de produto?
- Qual é a menor formulação neutra a adicionar ao `Context`: “schemas podem ser governados como
  artifacts e validados por uma linguagem de definição” em vez de “o sistema possui uma torre de
  níveis”?
- Quais relações serão pesquisadas separadamente: `references_schema`, `classifies`,
  `linguistically_conforms_to`, `satisfies`, `validated_against`, `extends` e `represents`? Quais
  delas têm evidência local, e quais são apenas vocabulário candidato?
- Que observação falsificaria a necessidade de multilevel modeling? Por exemplo: o skill-first
  witness funciona integralmente com tipos revisionados, schemas como artifacts e validações
  explícitas em uma arquitetura de dois níveis.
- Qual claim operacional justificaria adotar clabject ou potency? Sem uma necessidade observável de
  constraints atravessarem mais de um degrau, esses conceitos podem explicar a metáfora da torre
  sem melhorar o Schema Service.
- O review final exigirá fonte primária para claims históricos/definicionais e uma fonte crítica ou
  comparativa independente para claims de adequação? Sem esse critério, a pesquisa corre risco de
  confirmar a terminologia escolhida em vez de comparar arquiteturas.
