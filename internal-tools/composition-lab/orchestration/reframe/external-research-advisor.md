---
artifact_kind: external-research-advice
status: proposed
topic: composition-boundaries-and-precedents
last_updated: 2026-08-13
---

# Parecer para a próxima pesquisa externa

## Recomendação executiva

Executar uma pesquisa externa comparativa e limitada sobre os diferentes trabalhos que o termo
“composição” realiza em tradições que modelam partes, relações e todos. A pesquisa não deve procurar
uma definição universal nem usar “lente” como modelo geral. Seu resultado deve ser um mapa de
precedentes, compromissos observáveis, fronteiras e limites de transferência que possa ser
confrontado depois com a pesquisa interna do repositório.

A trilha externa pode começar junto da pesquisa interna, desde que as duas permaneçam cegas aos
rótulos analíticos uma da outra até entregarem seus primeiros findings. Antecipar a comparação reduz
o risco de circularidade; antecipar a síntese o aumenta.

## Pergunta refinável

> Em tradições autoritativas que tratam explicitamente da formação de todos a partir de partes, que
> trabalho conceitual e operacional “composição” realiza, como ela é distinguida de agregação,
> montagem, combinação, integração, coordenação e síntese, e quais desses compromissos podem ser
> transferidos — com quais limites — para estudar skills, interfaces, artefatos, conhecimento,
> trabalho e lentes neste projeto?

A pesquisa responde a essa pergunta por comparação de famílias. Ela não deve responder “o que é
composição em geral” nem declarar uma teoria escolhida.

## Famílias de fontes

Usar fontes primárias ou autoridades normativas. Revisões e enciclopédias podem orientar a busca,
mas não sustentar sozinhas claims centrais.

1. **Parte–todo e composição formal.** Mereologia e a “special composition question”; teoria das
   categorias, estruturas monoidais, operads, álgebras de processos e teorias de tipos quando elas
   explicitam operador, identidade, ordem, associatividade, fechamento ou decomposição. Priorizar
   monografias originais, artigos fundadores e textos canônicos dos autores das construções.
2. **Composição técnica, montagem e integração.** Arquitetura de software, component-based software,
   semântica composicional, engenharia de sistemas e padrões formais de arquitetura. Priorizar
   standards oficiais, especificações e artigos que definem interface, compatibilidade,
   substituição, acoplamento, integração e verificação do todo.
3. **Composição situada de atividade e trabalho.** Cognição distribuída, atividade mediada,
   coordination studies, design participativo e end-user composition. Priorizar estudos empíricos
   originais e formulações fundadoras que mostrem como materiais, agentes, ferramentas, regras,
   propósito e ambiente participam da formação de uma prática.
4. **Composição expressiva e interpretativa.** Estudos de composição textual/retórica, design e
   música quando tratam processo, forma, coerência, sequência, transformação, autoria e recepção.
   Priorizar tratados, modelos primários e estudos de processo; não usar analogias estéticas como
   prova de mecanismos técnicos.
5. **Composição de conhecimento.** Modularidade de ontologias, imports, alinhamento, integração de
   dados e construção de argumentos. Priorizar recomendações W3C/standards, especificações e artigos
   que tornam explícitos identidade, conflito, proveniência, inferência e perda.

Não é necessário cobrir toda a bibliografia de cada família. O corpus deve parar quando houver
owner suficiente para representar posições materialmente diferentes e testar os candidatos; volume
sem contraste não melhora o resultado.

## Perspectivas e concerns

Quatro explorers, cada qual protegendo uma diferença epistemológica, são suficientes:

1. **Constituição formal:** quais entidades, operadores e leis fazem um todo ser derivável das
   partes; o que conta como identidade, fechamento e decomposição.
2. **Realização técnico-material:** quais interfaces, restrições, adaptações e verificações tornam
   partes interoperáveis ou integradas; quando montagem ou conexão ainda não constitui composição.
3. **Formação situada da prática:** como propósito, ambiente, agentes e história transformam a
   composição durante o uso; onde autoria e emergência desafiam uma operação pré-definida.
4. **Coerência, significado e preservação:** como relações, ordem, ênfase e interpretação fazem um
   todo expressivo; o que é preservado, criado, obscurecido ou perdido.

Depois, um writer compara as perspectivas sem fundi-las. Três skeptics aplicam, separadamente, os
gates de `precedent`, `non-vacuity` e `definitional-soundness`. Um auditor independente mantém a
matriz de verdicts e verifica citações e limites de transferência. Se o runtime não puder realizar
essas dependências honestamente, preservar os estágios como dispatches separados; não declarar uma
topologia que não ocorreu.

## Hipóteses que a pesquisa deve tentar derrubar

- Composição é uma única espécie de fenômeno transferível entre todos os domínios.
- Partes precisam existir com identidade estável antes de serem compostas.
- Toda composição requer operador, interface ou regra explicitamente declarada.
- Intenção ou propósito de um autor é necessário para haver composição.
- Propriedade emergente do todo é necessária ou suficiente para caracterizar composição.
- Um todo só foi composto quando funciona, fecha ou satisfaz um critério de sucesso.
- Composição é associativa, reversível ou decomponível sem perda relevante.
- Agregação, montagem, combinação, integração, coordenação e síntese formam uma taxonomia única e
  comparável entre domínios.
- Compor materiais homogêneos e heterogêneos demanda o mesmo tipo de relação.
- O processo de compor e o resultado composto podem ser representados pela mesma entidade.
- Uma distinção lexical feita por uma fonte corresponde a uma diferença observável no projeto.

Cada hipótese sobrevivente precisa indicar a menor evidência que ainda a sustentaria e o fato que a
zeraria. Hipóteses derrotadas são resultados, não falhas do sweep.

## Outputs esperados

Em uma pasta própria de pesquisa, criar:

- `research-initial-definitions.md`, atualizado para este recorte antes do desenho do dispatch;
- `research.md`, preservando os retornos dos explorers e as citações de fontes;
- `findings.md`, com síntese citada e a matriz canônica de verdicts.

Dentro de `findings.md`, exigir também quatro projeções concisas:

1. **Mapa de precedentes:** família, owner, termo usado, unidade, partes, relação/operação,
   restrições, critério do todo e resultado.
2. **Matriz de fronteiras:** composição versus cada termo vizinho, com witness, não-exemplo,
   diferença observável, colapso possível e divergência entre domínios.
3. **Ledger de transferência:** conceito externo, job que pode cumprir no Composition Lab,
   evidência necessária, limite de transferência e classificação `build-from-owned`,
   `already-deployed` ou `novel-attempt`.
4. **Questões abertas:** incompatibilidades que a literatura não resolve e que exigem corpus interno
   ou experimento.

Não criar uma taxonomia canônica, glossário governado, schema ou especificação de produto.

## Gates

1. **Gate de entrada:** existe initial definition local; pergunta, escopo e exclusões estão
   congelados; cada família tem razão explícita para entrar.
2. **Gate de fonte:** toda claim estrutural depende de fonte primária ou autoridade normativa;
   fontes secundárias são marcadas como navegação ou interpretação; owner e contexto estão citados.
3. **Gate de contraste:** cada candidato tem witness concreto, não-exemplo, vizinho mais próximo e
   collapse-test. Diferença meramente lexical não avança.
4. **Gate de não-universalização:** divergências entre tradições são preservadas; nenhum conceito é
   projetado sobre skills, trabalho ou lentes só porque sua formulação é elegante.
5. **Gate de transferência:** cada empréstimo nomeia o job local que pode construir, a evidência
   ainda ausente e o limite além do qual a transferência deixa de ser justificada.
6. **Gate adversarial:** os três skeptics e o auditor completam a matriz
   candidato → owner → witness → soundness → verdict → use-mode. `Owned` nunca é KILL;
   `no-witness` e `tautological` são os únicos KILLs.
7. **Gate de saída:** a resposta final é um mapa de opções e obrigações, não “a definição de
   composição”. Claims sem apoio suficiente são demovidas ou mantidas como desconhecidas.

## Relação com o documento progressivo

Os pesquisadores externos não devem editar o documento objetivo diretamente. O documento é uma
projeção editorial posterior, não o depósito bruto da pesquisa.

Um writer dedicado deve importar somente findings aceitos, por IDs estáveis, mantendo quatro
camadas visíveis:

1. problema e relevância para o projeto;
2. evidência interna de como o repositório compõe hoje, começando por lentes;
3. precedentes externos e diferenças entre domínios;
4. hipóteses provisórias, decisões e perguntas ainda abertas.

Cada afirmação importada deve conservar owner, citação, força da evidência e limite. Quando a
evidência interna e externa discordarem, o documento deve registrar a tensão; não escolher uma por
autoridade ou maioria. O caso de lentes deve permanecer “primeiro caso estudado”, nunca sinônimo do
programa geral.

## Riscos principais

- **Ecletismo ornamental:** colecionar vocabulário de muitos campos sem comparar seus compromissos.
- **Universalização prematura:** transformar recorrência verbal em mecanismo comum.
- **Imperialismo formal:** usar uma álgebra útil como ontologia de todo trabalho humano.
- **Analogia sem transferência:** importar metáforas de música, texto ou design como explicação.
- **Norma confundida com prática:** tratar specification como evidência de realização ou efeito.
- **Sucesso confundido com ocorrência:** excluir composições falhas ou atribuir qualidade à operação
  sem controle.
- **Tradução retrospectiva do corpus:** renomear práticas locais para confirmar o mapa externo.
- **Documento inchado:** permitir que o material bruto substitua a explicação objetiva pedida pelo
  usuário.

## Ordem recomendada

1. Atualizar o objetivo geral do Composition Lab e criar a initial definition local desta pesquisa.
2. Congelar separadamente o recorte da pesquisa interna e o protocolo externo.
3. Executar as duas trilhas em paralelo e sem compartilhar categorias candidatas durante a coleta.
4. Rodar síntese e gates adversariais dentro de cada trilha.
5. Fazer um dispatch de comparação cruzada: convergências, incompatibilidades, lacunas e limites de
   transferência.
6. Encaminhar apenas claims aceitos a um writer do documento progressivo.
7. Submeter a versão resultante a `/review`; revisar a pesquisa ou o documento conforme o tipo do
   finding, sem corrigir os dois silenciosamente no mesmo artefato.

Essa ordem preserva independência sem atrasar o aprendizado externo. Ela substitui a regra anterior
de “pesquisa externa somente após o modelo de lentes” por uma regra mais adequada ao objetivo geral:
**coleta externa pode começar agora; importação conceitual só acontece depois do confronto com a
evidência interna**.
