# Findings — enquadramento de schema a partir de `research-domainspec`

## Resposta direta

**Parcialmente.** A pesquisa recente em `domainspec-lean-formalization/research-domainspec`
já estabelece distinções importantes para o Schema Service, mas não responde integralmente à
pergunta atual.

Ela sustenta que:

- `schema`, ontologia, taxonomia, knowledge graph, instância, carrier grafal e view são papéis
  diferentes, mesmo quando compartilham a mesma representação;
- “schema” não possui um único sentido universal: pode ser contrato estrutural, schema categórico,
  espaço de predicados ou ordem de refinamento;
- uma instância concreta não é um novo conceito ou schema apenas por conter informação própria;
- relações tipadas não fornecem, por si sós, identidade, composição, associatividade ou equações de
  caminhos;
- regras de schema podem ser normativas, mas sua existência não concede autoridade institucional
  nem determina automaticamente enforcement;
- schemas e instâncias podem ser transformados, mas cada transformação precisa declarar o que
  preserva e possuir testemunha operacional ou formal.

Ela **não** estabelece uma taxonomia explícita chamada “schema de domínio / schema de tipo / schema
de instância”, nem explica o ciclo pelo qual observações sobre artefatos se tornam conhecimento
institucional e depois regras normativas. Portanto, a pesquisa menor proposta não precisa repetir o
sweep conceitual já feito; deve concentrar-se nessas duas lacunas.

Evidência do escopo e do limite: o baseline já exigia separar objeto, representação, schema da
representação, instância e transformação
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/research-initial-definitions.md:21-29`),
enquanto a auditoria final concluiu que não há identidade universal entre os papéis nem arquitetura
única
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/findings.md:11-22`).

## O sentido de domínio

O corpus não define uma tipologia fechada de “diferentes tipos de domínio”. A leitura mais segura é
que um domínio é uma **fronteira escolhida de discurso e governança**: delimita os objetos,
distinções, relações, operações, owners e critérios de validade relevantes para certo propósito.
Documentos, skills, dispatches, código e bancos de dados podem ser domínios, subdomínios ou perfis
sobrepostos; a decisão depende do que precisa ser governado junto, não apenas do formato dos
artefatos.

Essa formulação é uma **inferência para o Schema Service**, não um resultado nominal da pesquisa.
Ela deriva do resultado auditado de que artefatos sobre o mesmo carrier continuam diferentes quando
mudam admissibilidade, semântica, inferência, atualização ou autoridade
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/agents/02-explorer-minsky.md:78-95`)
e de que o carrier comum somente é sustentado sob contratos relativos ao perfil
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/agents/09-auditor-codd.md:85-99`).

Consequência: “domínios podem ser arbitrários” é aceitável no sentido de que a organização pode
delimitar novos domínios. Não deve significar que qualquer agrupamento adquire automaticamente
semântica ou autoridade. Uma fronteira governada precisa ao menos de propósito, escopo e owner.

## Camadas que convém distinguir

| Camada | Papel | Status no corpus |
|---|---|---|
| **Metaschema** | Define a linguagem na qual schemas são expressos. | Já existe como proposta explícita no Schema Service, não como conclusão de `research-domainspec` (`projects/schema-service/README.md:42-62`). |
| **Schema de domínio** | Explicita o vocabulário do domínio: tipos de objetos, relações admissíveis e, quando justificadas, leis ou regras de composição. Pode também registrar o propósito e a fronteira do domínio. | **Síntese proposta aqui.** O corpus fornece os ingredientes — ontologia, grafo tipado, categoria apresentada, regras e autoridade — mas não os reúne sob esse nome. |
| **Schema de tipo** | Define a forma admissível de uma classe específica, como `Research`, `Discovery`, `Skill` ou `Dispatch`: propriedades, cardinalidades, relações e invariantes. | **Sustentado como papel estrutural.** Schema de dados/contrato delimita campos, tipos e relações e licencia validação, parsing, geração ou rejeição (`agents/02-explorer-minsky.md:123-141`). |
| **Schema composicional** | Acrescenta identidades, composição, equações de caminhos ou outras leis necessárias ao domínio. | **Sustentado como possibilidade formal, não como maturidade universal ou runtime implantado.** O Lean possui categoria-schema e uma testemunha de equação de paths, mas o runtime não possui composição categórica geral (`agents/03-explorer-goguen.md:76-95`; `morphisms-and-relations/findings.md:46-54`). |
| **Instância / manifesto** | Registra um artefato concreto, seus valores e suas relações observadas ou declaradas. | **Distinção sustentada.** Instância materializa um contrato com identidade e valores concretos; não cria novo conceito por si só (`agents/02-explorer-minsky.md:123-141`). |
| **Política de autoridade e enforcement** | Decide quem publica uma regra e qual consequência operacional uma não conformidade produz. | **Deve permanecer distinguida do schema.** Standards e estruturas não decidem quem pode promover uma definição (`agents/02-explorer-minsky.md:176-204`); a auditoria preserva a barreira entre projeção e autoridade (`findings.md:5-22`). |

Os caminhos abreviados na tabela que começam por `agents/` e `morphisms-and-relations/` pertencem a
`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/`
e `C:/Users/victo/domainspec-lean-formalization/research-domainspec/`, respectivamente.

## Schema, conhecimento e regra

A formulação “o schema é a parte mínima do conhecimento” não é sustentada pelo corpus e mistura
duas coisas.

Uma distinção mais precisa é:

- o **schema contém conhecimento intensional**: o que a organização reconhece como tipo, relação,
  propriedade, invariável ou composição possível/obrigatória;
- a **instância contém conhecimento extensional ou afirmações concretas**: esta pesquisa existe,
  possui esta pergunta, serve este objetivo e relaciona-se com estes artefatos;
- evidência e proveniência registram por que essas afirmações são confiáveis ou de onde vieram;
- autoridade registra quem pode converter uma hipótese descritiva em regra institucional;
- enforcement decide o efeito operacional da regra.

Assim, o conhecimento governado não é apenas o schema:

```text
conhecimento governado
  = schemas + instâncias/afirmações + relações + evidência/proveniência
    + decisões de autoridade + histórico de revisão
```

O schema é a parcela **generalizada, reutilizável e normativamente publicável** desse conhecimento.
Uma afirmação ou relação concreta pode ser menor que um schema; portanto “mínimo” não é uma boa
caracterização sem definir uma ordem específica de granularidade.

Aplicado ao exemplo: uma pesquisa concreta com pergunta, objetivo e relações é normalmente uma
**instância de `Research`**, não “o schema daquela pesquisa”. Ela passa a ter um schema próprio
somente se introduzir uma distinção reutilizável — por exemplo, um subtipo com novas propriedades ou
invariantes. Isso coincide com a separação já escrita no Schema Service entre schema definition e
instance manifest (`projects/schema-service/README.md:64-90,125-150`).

## Conhecimento descritivo e regra normativa

O mesmo schema pode exercer dois papéis compatíveis:

1. **descrever um modelo institucional do domínio** — por exemplo, `Plan`, `Research`, `Discovery` e
   `Spec` existem, e `Discovery informs Spec` é uma relação reconhecida;
2. **prescrever invariantes** — por exemplo, uma `Spec` aceita deve possuir uma `Discovery` anterior
   ou ligada a ela.

Mas a passagem de descrição a obrigação não é automática. O corpus sustenta três separações:

- semântica da relação não é a mesma coisa que sua representação como aresta;
- regra declarada não é a mesma coisa que enforcement executado;
- proveniência ou ontology não concede autoridade de promoção.

O `morphisms-and-relations` formula essa prudência diretamente: endpoints tipados ou relações em
sequência não estabelecem composição categórica, e leis mais fortes só devem entrar quando o domínio
as justifica
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/morphisms-and-relations/research-initial-definitions.md:34-47`).
A auditoria operacional encontrou apenas admissão finita de arestas DS-D8 e uma tradução estreita de
`creates`; não encontrou composição categórica, transformação geral de schemas ou álgebra de
proveniência implantadas
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/morphisms-and-relations/findings.md:11-24`).

## Quiver, categoria e níveis de maturidade

O corpus confirma uma progressão estrutural possível:

```text
tipos isolados
  -> grafo/quiver tipado
    -> caminhos
      -> identidades + composição + leis/equações
        -> categoria ou outra estrutura composicional adequada
```

Porém, **categoria não é o nível máximo de todo schema**. É um nível possível de maturidade na
dimensão composicional. Autoridade, temporalidade, evidência, proveniência, validação e política de
atualização são dimensões independentes que uma categoria não fornece sozinha. A pesquisa formal
mostra precisamente que uma categoria-schema possui identidade e composição, mas não fornece por
isso linguagem lógica, lifecycle ou authority
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/agents/03-explorer-goguen.md:76-87`).

Também não basta “subir” de um quiver para uma categoria livre. Os paths e suas leis podem ser apenas
sintaxe até que um consumidor do domínio observe seu significado. A pesquisa recomenda introduzir
`Path(G)` somente quando houver uma obrigação de nível de path observável
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/morphisms-and-relations/findings.md:46-71`).

## Morfismos e transformações

O corpus distingue pelo menos quatro coisas que não devem compartilhar o nome `morphism` sem perfil:

- assinatura de uma relação possível entre tipos;
- aresta concreta entre duas instâncias;
- path potencialmente composável;
- transformação entre schemas, capaz de induzir migração de instâncias.

Essa distinção é a pergunta explícita da pesquisa
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/morphisms-and-relations/research-initial-definitions.md:27-32`).
Formalmente, o repositório possui schema como pequena categoria, instância como funtor, morphism de
schema como funtor e pullback por precomposição; isso não prova preservação de satisfação, evidência
ou autoridade
(`C:/Users/victo/domainspec-lean-formalization/research-domainspec/ontologies-schemas-and-taxonomy/agents/03-explorer-goguen.md:76-85`).

O diretório `research-domainspec/morphism-contracts` está vazio nesta checkout. Logo ele não adiciona
evidência à síntese.

## Relação com criação e evolução de conhecimento

Há material parcial, mas não uma teoria completa de aprendizagem organizacional.

Resultados existentes:

- a pesquisa começa do objetivo de tornar explícitas as estruturas pelas quais informação,
  decisão, evidência, autoridade e execução tornam-se conhecimento operacional
  (`ontologies-schemas-and-taxonomy/research-initial-definitions.md:3-11`);
- o Lean contém refinamento de schemas de observação e um witness no qual probes mais refinados
  distinguem setas antes indistinguíveis, mas isso formaliza perda/revelação observacional sob um
  mapa específico, não governança de evolução do conhecimento
  (`ontologies-schemas-and-taxonomy/agents/03-explorer-goguen.md:103-113`);
- views são derivadas e não se tornam fontes autorizadas apenas por existir
  (`ontologies-schemas-and-taxonomy/findings.md:7-22`).

Lacuna: o corpus não define o processo

```text
observação de instâncias
  -> padrão recorrente
    -> hipótese de domínio
      -> proposta de schema
        -> revisão/decisão de owner
          -> regra versionada
            -> validação e nova evidência
```

Esse processo é central para o objetivo atual do Schema Service e deve ser tratado como pesquisa ou
decisão própria, sem ser atribuído ao trabalho anterior.

## O que pode ser importado para o Schema Service

### Resultados sustentados

1. **Não definir schema apenas pela serialização ou carrier.** O mesmo YAML, JSON ou grafo pode
   desempenhar papéis distintos conforme semântica, validação, identidade, atualização e autoridade.
2. **Manter instância distinta de schema.** A pesquisa concreta é conhecimento, mas normalmente é
   uma instância; seu tipo reutilizável é o schema.
3. **Separar relação possível, aresta concreta, path e transformação de schema.** Cada uma precisa de
   identidade, admissibilidade e validação próprias.
4. **Tratar composição como capacidade justificada pelo domínio.** Relações tipadas são úteis antes
   de existir uma categoria; composição deve ser adicionada somente onde produz uma obrigação ou
   comportamento observável.
5. **Separar norma de autoridade e enforcement.** O schema pode conter regras normativas; publicação
   autorizada e consequência operacional pertencem a contratos cooperantes.
6. **Exigir preservação explícita nas transformações.** Migrar, projetar ou refinar não pode ser
   tratado como simples cópia de estrutura.

### Propostas locais, ainda não resultados da pesquisa anterior

1. Adotar `DomainSchema`, `ArtifactTypeSchema` e `InstanceManifest` como nomes provisórios de três
   granularidades diferentes.
2. Permitir que domínios se sobreponham e que um tipo importe capacidades de mais de um domínio,
   desde que ownership e conflitos sejam explícitos.
3. Modelar o conhecimento institucional como conjunto coordenado de schemas, instâncias, evidência,
   proveniência e decisões — não como um único “schema total”.
4. Tratar `relational -> compositional` como uma dimensão de expressividade, separada de confiança
   epistêmica, autoridade normativa e força de enforcement.

## Perguntas ainda abertas

- Qual é a identidade de um domínio e quando dois recortes são domínios separados, subdomínios ou
  apenas perfis do mesmo domínio?
- Um schema de domínio é um artefato único, um package versionado de schemas de tipo ou uma view
  resolvida sobre vários owners?
- Como schemas de tipo importam relações e invariantes do domínio sem duplicá-las?
- Como lidar com um tipo que participa simultaneamente dos domínios de documentos, workflow,
  proveniência e execução?
- Qual unidade mínima deve receber autoridade: campo, predicado, relação, invariável, schema de tipo
  ou package de domínio?
- Como registrar separadamente observação, hipótese, regra aceita e enforcement ativo?
- Quais evidências justificam promover uma regularidade de instâncias a uma regra de schema?
- Como versionar e migrar instâncias quando o conhecimento institucional muda?
- Quais regras são estruturais, temporais, relacionais, de capacidade, de composição ou de processo,
  e quais precisam de mecanismos além do schema estrutural?
- Em que domínios categorias, sketches, institutions, constraint languages ou workflow models são o
  formalismo adequado?

## Recomendação para a pesquisa de landscape

Não repetir a pergunta ampla “o que são schema, ontologia e taxonomia?”. Reformular o próximo passo
em duas pesquisas encadeadas:

1. **Granularidade e modularidade:** como metamodelos, schema packages, conceptual schemas,
   artifact/type schemas e instance data distinguem domínio, tipo e instância, inclusive em domínios
   sobrepostos?
2. **Institucionalização do conhecimento:** como sistemas transformam observações e evidências em
   vocabulário, constraints e regras versionadas, preservando a separação entre hipótese, autoridade
   e enforcement?

Depois disso, a pesquisa de sistemas contemporâneos pode avaliar registry, identidade, fallback,
validação, proveniência e migração com um vocabulário mais preciso. O resultado anterior reduz o
espaço de busca, mas não elimina a necessidade dessa pesquisa: ele oferece fronteiras conceituais e
alguns precedentes formais, não uma arquitetura de gestão de conhecimento por artefatos.
