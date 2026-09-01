---
artifact_kind: research-report
status: candidate-evidence
date: 2026-08-25
topic: multilevel-metamodeling-literature
scope: primary-literature-comparison
---

# Literatura de multilevel modeling e metamodeling

## Resposta curta

A literatura confirma que um elemento pode ter uma faceta de instância em relação ao que o
classifica e uma faceta de tipo em relação ao que ele próprio classifica. Ela **não** confirma,
porém, que o Schema Service precise representar isso por níveis globais, `clabjects`, potência ou
uma única relação transitiva `conforms_to`.

Há pelo menos três soluções estruturalmente diferentes para o caso que nos interessa:

1. representar definições de schema como dados tipados por um metaschema, mantendo referências e
   validações de cada salto separadas;
2. separar classificação linguística e ontológica em dois eixos;
3. adotar instanciação profunda, na qual características definidas acima podem governar instâncias
   indiretas vários saltos abaixo.

O primeiro witness de `skill` ainda não demonstrou a necessidade das capacidades extras de 2 ou 3.
Assim, `clabject`, deep instantiation e potency devem entrar nas definições iniciais como candidatos
com collapse-tests, não como vocabulário aceito.

## Escopo e método

Este levantamento comparou fontes primárias indicadas pelo usuário com trabalhos primários sobre
Type Object, MOF, meta-arquiteturas reflexivas e evolução de metamodelos/schemas. Páginas editoriais
foram usadas somente para confirmar metadados quando o PDF de autor não os trazia claramente.

Os termos mudam entre abordagens. Em particular, “logical/physical” em 2001–2002 passa a
“ontological/linguistic” no artigo de 2003, e a literatura posterior não possui terminologia
unificada. Logo, equivalências terminológicas abaixo são contextualizadas, não presumidas.

## Verificação dos quatro títulos sugeridos

| título | autoria, ano e venue verificados | conteúdo que o trabalho efetivamente sustenta |
| --- | --- | --- |
| *The Essence of Multilevel Metamodeling* | Colin Atkinson e Thomas Kühne, 2001, *«UML» 2001*, LNCS 2185, pp. 19–33, DOI 10.1007/3-540-45441-1_3 | Diagnostica ambiguous classification e replication of concepts na instanciação rasa; propõe deep instantiation, potência, campos e um MoMM preliminar. O próprio artigo diz que o trabalho era preliminar. [PDF dos autores, seções 2–5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) |
| *Rearchitecting the UML Infrastructure* | Colin Atkinson e Thomas Kühne, 2002, *ACM Transactions on Modeling and Computer Simulation* 12(4), pp. 290–321, DOI 10.1145/643120.643123 | Separa classificação lógica/física, unifica facetas classe/objeto e discute deep instantiation. Importante: termina deixando em aberto se é melhor manter dois eixos ou realinhá-los por deep instantiation. [PDF dos autores, especialmente seções 4.1–5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) |
| *Model-Driven Development: A Metamodeling Foundation* | **Colin Atkinson e Thomas Kühne**, não Kühne sozinho; 2003, *IEEE Software* 20(5), pp. 36–41, DOI 10.1109/MS.2003.1231149 | Argumenta que metamodelagem apenas como definição de linguagem é insuficiente para MDD e distingue instanciação linguística e ontológica. Não apresenta um teorema de correção da Orthogonal Classification Architecture. [Versão publicada dos autores, seções 3.1–3.3](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/mda-foundation-real.pdf) |
| *Multi-level modeling: cornerstones of a rationale* | Ulrich Frank, versão de registro de 2022, *Software and Systems Modeling* 21, pp. 451–480, DOI 10.1007/s10270-021-00955-1 | É uma avaliação argumentativa multiperspectiva, não uma unificação formal do campo. Identifica conceitos recorrentes, variações e benefícios, mas também falta de terminologia comum, ferramentas maduras, métodos de design e integração adequada com linguagens de programação. [Artigo open access, seções 2, 3.1.6 e 6](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) |

## Distinções que a literatura obriga a preservar

### Um “nível” não é um objeto

A correção proposta na conversa é válida: uma população pode ser organizada em níveis, mas são os
elementos que entram em relações de classificação. A definição clássica de strict metamodeling de
Atkinson e Kühne exige que cada elemento de `M_m` seja instância de exatamente um elemento de
`M_(m+1)` e que relações não-instanciação permaneçam no mesmo nível. O nível é, portanto, uma
partição arquitetural derivada dessas regras, não a entidade que desempenha as facetas classe/objeto.
[Rearchitecting, seção 2.2, pp. 293–294 da versão publicada](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf)

Isso não autoriza a cadeia sem qualificação:

```text
x conforms_to S0 conforms_to S1
```

Nos trabalhos examinados, “instance-of” já se divide em sabores diferentes. No Schema Service,
`schema_ref`, classificação de domínio, satisfação de constraints, execução de validação e conclusão
de um relatório acrescentam ainda outros atos. Nenhuma fonte sustenta que eles sejam equivalentes ou
transitivos.

### Facetas relativas não eliminam kinds governados

*Meta-level Independent Modelling* introduz `clabject` como um elemento instanciável que possui ao
mesmo tempo faceta de objeto — características recebidas de seu tipo — e faceta de classe —
características destinadas às suas instâncias. Isso é mais específico do que a afirmação geral “algo
pode ser schema e instância em relações diferentes”. [Atkinson e Kühne 2000, seção 3.2](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/level-indep.pdf)

Portanto, a literatura apoia a relatividade dos papéis, mas não a conclusão de que kinds como
`SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot` e `ValidationReport`
devam desaparecer. Um record pode conservar kind, identidade e lifecycle próprios enquanto participa
de relações relativas.

### Classificação linguística e ontológica não são a mesma pergunta

Na Orthogonal Classification Architecture (OCA):

- a classificação linguística diz com quais construtos da linguagem um elemento foi expresso — por
  exemplo, `SkillSchemaRevision` como instância de `SchemaDefinition`;
- a classificação ontológica diz qual papel ou conceito de domínio o elemento instancia — por
  exemplo, uma definição concreta classificando uma família de skills.

O artigo de 2003 afirma que as duas formas ocorrem simultaneamente e localizam o elemento no espaço
linguagem–ontologia. O artigo de 2002, contudo, deixa aberta a alternativa entre manter os dois eixos e
realinhá-los por deep instantiation. A OCA é assim uma proposta arquitetural com explicação forte para
dual classification, não um resultado inevitável. [MDD Foundation, seção 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/mda-foundation-real.pdf) [Rearchitecting, seção 5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf)

## Comparação das abordagens

| abordagem | problema que resolve | entidades e relações principais | garantia efetiva | limites/críticas nas fontes | collapse-test para Schema Service |
| --- | --- | --- | --- | --- | --- |
| Strict/adjacent-level metamodeling | Impedir levels arbitrários ou semanticamente misturados. | Modelos `M_m`; elementos; `instance-of` único para elemento no nível imediatamente superior; relações ordinárias intranível. | Se a disciplina for obedecida, a localização por nível e a fronteira entre levels ficam determinadas pela instanciação. | A combinação de strictness, hierarquia linear e classificação dupla produziu violações e duplicação na UML. O topo requer uma exceção/fechamento. [Rearchitecting, seções 2.2 e 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) | Se tipos sobrepostos, múltiplas referências ou relações cross-domain forem legítimos, uma rankeação global deixa de explicar o grafo; strictness pode sobreviver apenas como invariante local de uma relação bem definida. |
| Schemas-as-data / Type Object | Criar novos “tipos” em runtime sem gerar subclasses do host. | `TypeClass`, `TypeObject`, `Class`, `Object`; cada `Object` referencia seu `TypeObject` e delega comportamento comum. | Reduz explosão de subclasses e permite tipos/reclassificação dinâmicos no domínio da aplicação. | O host não trata `TypeObject` como classe real; a aplicação mantém referência, delegação e type checking. Os autores alertam para complexidade de design, implementação e composição. [Johnson e Woolf 1998, seções Structure e Consequences](https://www.cs.ox.ac.uk/jeremy.gibbons/dpa/typeobject.pdf) | Se `SchemaDefinitionRevision` + interpretador/validador + referência exata bastarem para o witness de skill, o caso multilevel colapsa para este padrão estrutural. Se forem necessárias constraints herdadas por instâncias indiretas, o padrão sozinho é insuficiente. |
| OCA / classificação ortogonal | Evitar que “escrito na linguagem X” e “instancia conceito Y do domínio” disputem uma única relação `instance-of`. | Eixo linguístico, eixo ontológico; classificadores físicos/linguísticos e lógicos/ontológicos. | Torna explícitas duas classificações simultâneas e permite aplicar strictness separadamente em cada eixo. | Não decide automaticamente quantos eixos adicionais existem; o artigo de 2002 pergunta isso explicitamente. Deep instantiation pode realinhar os eixos, e a escolha ficou aberta. [Rearchitecting, seções 4.1.3–4.1.4 e 5.5](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/rearchitecting.pdf) | Se cada schema e artifact usa a mesma linguagem estrutural e nenhuma decisão depende de distinguir classificador linguístico de ontológico, OCA apenas renomeia relações já separadas. Um caso em que os dois classificadores variam independentemente é necessário para não colapsar. |
| Clabject / class-object duality | Representar uniformemente um elemento que recebeu características como instância e ainda define características para suas instâncias. | Um `clabject` com faceta de instância e faceta de tipo; `instance-of` entre clabjects. | Oferece uma unidade conceitual/notacional para as duas facetas. Não garante por si só validação, autoridade ou propagação multissalto. | A formulação original está acoplada a strict metamodeling e a uma semântica uniforme de instanciação. Frank registra que a área não tem terminologia única. [Meta-level Independent Modelling, seções 3.1–3.3](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/level-indep.pdf) [Frank 2022, seção 2.1](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) | Se uma `SchemaDefinitionRevision` puder ser tratada simplesmente como record governado validado por um metaschema e referenciado por manifests, sem uma operação uniforme sobre suas duas facetas, `clabject` não acrescenta capacidade operacional. |
| Deep instantiation + potência | Permitir que uma definição afete instâncias indiretas, evitando replicar conceitos/constraints em cada salto. | Elementos/clabjects, fields e relações; potência inteira; instanciação reduz level e potência na proposta original. MetaDepth estende potência a modelos, constraints e derived attributes e admite potência ilimitada. | Na semântica específica, controla quantos saltos uma característica atravessa e em que salto exige valor; ferramentas podem verificar essa regra. [Essence, seção 4.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) [MetaDepth, seções 2–3](https://metadepth.org/papers/TOOLS.pdf) | Potência não é uma ideia única: ferramentas variam no alvo, na extensão linguística, em associações e constraints. Frank observa que nem associações cross-level fazem parte de um núcleo comum. [Frank 2022, seções 2.1–2.2](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf) | Exigir um exemplo de skill no qual uma propriedade declarada no metaschema governe diretamente uma instância de skill dois saltos abaixo e não possa ser expressa como duas validações/composições explícitas. Sem esse exemplo, potency é excesso de mecanismo. |
| Powertype | Modelar um tipo cujas instâncias são subtipos de outro tipo, combinando classificação e especialização. | Powertype `P`, tipo particionado `T`, instâncias de `P` que são subtipos de `T`. | Captura uma forma específica de higher-order classification e evita um segundo `instance-of` direto em alguns modelos. | Na análise de Atkinson e Kühne, powertypes não se encaixavam diretamente no stack estrito da UML e não resolviam replication of concepts; são mais estreitos que deep instantiation. [Essence, seção 3.1](https://homepages.ecs.vuw.ac.nz/~tk/publications/papers/essence.pdf) | Se revisões de schema classificam manifests, mas não têm instâncias que são subtipos de um tipo particionado, powertype não modela o nosso vínculo; colapsa para referência a tipo/schema. |
| Type Object recursivo | Obter mais de dois estratos usando o mesmo padrão de objetos e delegação. | Cadeia `Object → TypeObject`, repetida: no exemplo, `Videotape → Movie → MovieCategory`. | Permite nesting arbitrário na aplicação sem exigir metaclasses do host. | Cada salto adiciona delegação e manutenção manual; o próprio paper mostra que a composição pode ficar complexa. Não fornece semântica formal uniforme de propagação. [Johnson e Woolf 1998, “Nested Type Objects”](https://www.cs.ox.ac.uk/jeremy.gibbons/dpa/typeobject.pdf) | Se duas referências exatas e dois relatórios de validação explicarem `skill → skill-schema → metaschema`, nesting basta como representação; isso ainda não prova deep instantiation. |
| Self-describing / meta-circular / reflective | Encerrar a escalada de metaníveis preservando introspecção e manipulação homogênea do topo. | Metanível superior descrito por seus próprios conceitos; ciclo de compliance; bootstrap a partir de um core mínimo. | Demonstra fechamento estrutural em implementações como MOF: o metalanguage pode representar sua própria definição. [Emerson, Sztipanovits e Bapty 2004, seção 3.1](https://www.jucs.org/jucs_10_10/a_mof_based_metamodeling/Emerson_M_J.pdf) | Self-description cria dependência circular e bootstrapping; reflexão semântica pode ameaçar decidibilidade. Um primeiro “blind” bootstrap ou kernel externo ainda é necessário. [Ferreira et al. 2010, “Closing the Roof” e “Bootstrapping”](https://hillside.net/plop/2010/papers/ACMVersions/papers/ferreira.pdf) | Se o Schema Service não precisa editar/introspectar o kernel em runtime, um kernel externo pequeno encerra operacionalmente o bootstrap. Self-description só não prova self-validation, consistência, soundness ou autoridade. |

## O que é e não é “clabject” para este projeto

O seguinte fato relacional é compatível com todas as abordagens examinadas:

```text
SkillManifestRevision ──references_schema──▶ SkillSchemaRevision
SkillSchemaRevision   ──references_metaschema──▶ MetaSchemaRevision
```

Isso, sozinho, não é witness de clabject. Para justificar o conceito mais forte, seria preciso mostrar
que `SkillSchemaRevision` precisa ser operada uniformemente por duas facetas:

```text
faceta recebida: valores/constraints que caracterizam a revisão como instância do metaschema
faceta tipante:  características que a revisão transmite às suas próprias instâncias
```

Mesmo esse witness ainda não justificaria potência. Potência só acrescenta poder se uma característica
precisar atravessar mais de uma instanciação sob semântica governada, em vez de ser aplicada por duas
validações explícitas.

## Schema transformation, “schema residue” e data migration

### O que está estabelecido

A literatura trata como problemas distintos, mas acoplados:

- **evolução de metamodelo/schema:** mudança da estrutura, constraints ou linguagem que governa
  instâncias;
- **migração/co-evolução de modelos ou dados:** atualização das instâncias para recuperar conformidade
  ou preservar a semântica pretendida após a mudança;
- **adaptação de dependentes:** queries, updates, transformações e ferramentas também podem precisar
  mudar.

Rose et al. definem model migration precisamente como atualizar instance models para restabelecer
conformidade após evolução do metamodelo e observam que co-evolution é distinta da transformação
model-to-model genérica. [*Model Migration Case for TTC 2010*, seção 1](https://ris.utwente.nl/ws/files/5096115/wp10-03.pdf)

Vermolen, Wachsmuth e Visser mostram uma distinção adicional relevante: a mesma diferença final entre
dois metamodelos pode resultar de operadores complexos diferentes, e esses operadores podem produzir
efeitos de migração diferentes. Um diff estrutural final não preserva sozinho a intenção da mudança.
[*Reconstructing Complex Metamodel Evolution*, resumo e seção 1](https://eelcovisser.org/publications/2011/VermolenWV11sle.pdf)

No domínio de bancos, PRISM++ separa mudanças estruturais de schema, evolução de integrity
constraints, migração de dados e reescrita de queries/updates. O paper fornece uma condição formal de
soundness para update rewriting sob mappings invertíveis; não promete preservação geral para mappings
arbitrários. [Curino et al. 2010, seções 1 e 4.2](https://www.vldb.org/pvldb/vol4/p117-curino.pdf)

Frank também separa dois riscos: deletar conceitos de um schema ameaça a integridade das árvores de
schemas; mapear modelos a linguagens menos expressivas pode perder abstração e informação.
[*Cornerstones*, seções 3.1.2–3.1.3](https://umo.ris.uni-due.de/fileadmin/fileupload/WI-UMO/Frank2022_Article_Multi-levelModelingCornerstone.pdf)

### O que não está estabelecido

No corpus primário delimitado, **`schema residue` não aparece como termo técnico para “conceitos,
distinções, relações ou invariantes perdidos numa transformação”**. Buscas pela expressão exata não
encontraram ownership relevante; ocorrências de “residue” pertenciam a outros conceitos. Isso não prova
inexistência na literatura inteira, mas impede importar o termo como se já tivesse definição estabelecida.

Se o projeto mantiver `schema residue`, deve marcá-lo como termo local provisório e fornecer um predicado
operacional, por exemplo:

```text
há resíduo de schema em uma transformação T apenas se uma obrigação declarada
do schema-fonte não possui preservação, tradução explícita ou perda registrada no alvo
```

Esse predicado ainda precisaria distinguir ao menos: perda intencional, incompatibilidade expressiva,
erro de mapping e obrigação não decidida. Sem isso, “residue” apenas renomeia “algo se perdeu” e falha
o teste de soundness definicional.

## Implicações para `research-initial-definitions.md`

Estas são melhorias de enquadramento, não decisões de adoção.

### 1. Substituir a pergunta “qual torre?” por três perguntas discriminantes

1. O witness de skill exige somente schemas-as-data e validações adjacentes independentes?
2. Existe um caso concreto em que classificação linguística e ontológica variam independentemente e
   afetam uma operação?
3. Existe uma característica que precisa governar instâncias indiretas, tornando deep instantiation
   observavelmente diferente de composição de schemas e validações separadas?

Se 2 e 3 não tiverem witness, OCA, clabject e potência não ganham justificativa operacional.

### 2. Tornar as hipóteses concorrentes explícitas

```text
H1 — two-level/schema-as-data:
     SchemaDefinitionRevision é um record tipado pelo MetaSchema e interpretado por validação.

H2 — classificação ortogonal:
     o sistema precisa representar separadamente classificadores linguísticos e ontológicos.

H3 — deep instantiation:
     regras de um elemento superior precisam atravessar mais de um salto de instanciação.

H4 — fechamento externo:
     um kernel confiado encerra o bootstrap; schemas acima continuam sendo artifacts ordinários.

H5 — fechamento meta-circular:
     o kernel representa a si próprio e há um procedimento explícito de bootstrap.
```

H1–H3 não são mutuamente exclusivas, mas cada capacidade adicional precisa vencer seu collapse-test.
H4 e H5 são alternativas de fechamento até que se especifiquem os componentes híbridos.

### 3. Separar relações e seus domínios

As definições iniciais deveriam exigir assinaturas candidatas, sem ainda escolher nomes finais:

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

Nenhuma transitividade deve ser presumida. Em particular, duas referências não constituem uma prova
de conformidade, e conformidade estrutural com o metaschema não concede publicação ou enforcement.

### 4. Especificar o alvo exato da meta-validação

A literatura de metamodelagem costuma falar do “modelo” como instância do metamodelo, mas o Schema
Service distingue definição lógica, manifest, representação e snapshot. O primeiro experimento deve
comparar explicitamente candidatos como:

```text
validate(logical SchemaDefinitionRevision, MetaSchemaRevision)
validate(RepresentationSnapshot, MetaSchemaRevision)
validate((logical revision, representation snapshot, resolver context), MetaSchemaRevision)
```

Sem essa escolha, afirmar `SkillSchemaRevision conforms_to MetaSchema` omite o objeto realmente
observado e o contexto do veredito.

### 5. Adicionar um witness mínimo e um anti-witness

Witness mínimo:

```text
uma skill concreta
→ uma ManifestRevision com schema_ref exato
→ uma SkillSchemaRevision imutável
→ uma MetaSchemaRevision imutável
→ dois ValidationReports separados e revision-scoped
```

Anti-witness:

```text
schema_ref resolvível, mas artifact inválido
ou
SkillSchemaRevision bem formada pelo metaschema, mas semanticamente inadequada/não publicada
```

O anti-witness impede o colapso de referência, validação, adequação e autoridade em `conforms_to`.

## Conclusão

A literatura possui owners claros para todos os candidatos principais, portanto nenhum deve ser
apresentado como novidade do Schema Service. O resultado útil é comparativo:

- **GO / build-from-owned** para schemas-as-data como baseline testável, com Type Object e MOF como
  precedentes estruturais, sem inferir que sejam suficientes;
- **GO / build-from-owned condicionado a witness** para OCA, clabject e deep instantiation;
- **GO / build-from-owned condicionado a necessidade de classificação de subtipos** para powertype;
- **DEFER** para fechamento reflexivo/meta-circular, pois self-description não implica self-validation,
  consistência ou autoridade;
- **não estabelecido** para `schema residue` como termo da literatura; a distinção entre evolução de
  schema/metamodelo e migração de instâncias é bem estabelecida, mas o nome e a taxonomia proposta
  ainda são locais.

O melhor ganho para as definições iniciais é transformar “torre reflexiva” em uma bateria de perguntas
que compare dois saltos explícitos, dois eixos de classificação, propagação multissalto e fechamento.
Isso permite que o experimento de skill descubra qual capacidade é necessária, em vez de pressupor a
arquitetura que deveria testar.
