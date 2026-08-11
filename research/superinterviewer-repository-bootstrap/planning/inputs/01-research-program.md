# Proposta de programa fundador de pesquisa — Superinterviewer

## Estatuto deste documento

Este é um input de planejamento, não uma autorização de implementação, um desenho de runtime ou
um scaffold de repositório. Seu objeto central é o **Superinterviewer como produto**: a principal
interface e parceira intelectual da pessoa enquanto uma intenção ainda incompleta é formada e
levada a um próximo passo. Infraestrutura de execução, governança de repositório e candidatos
formais entram somente quando ajudam a testar, preservar ou governar essa tese.

A proposta parte de três fontes: o Prompt-Mestre, que contém a direção de produto e o universo de
hipóteses; as `research-initial-definitions`, que delimitam o contexto informacional e as lacunas do
bootstrap; e os findings aceitos de Robot-Talks, que estabeleceram decisões humanas sobre
autoridade, separação de artefatos e fronteiras de integração. Nenhuma das três, isoladamente,
constitui evidência empírica de eficácia do produto.

## 1. Estados epistêmicos separados

### 1.1 Decisões confirmadas

As decisões abaixo são restrições do programa até que uma decisão humana posterior as revise:

1. O Superinterviewer, e não um framework genérico de framing, é o produto e a autoridade central.
2. Ele é a principal interface e parceira de trabalho da pessoa; não é apenas um entrevistador de
   requisitos ou chatbot que só pergunta.
3. Seu repertório inclui perguntar, trazer informação, sugerir e propor ou testar reframings e
   lentes. A completude e a separabilidade desse repertório continuam sendo hipóteses.
4. O programa deve admitir pesquisa ampla antes de fixar o desenho completo do sistema.
5. O produto terá um repositório limpo, fora de `cyberalchemy-orchestrator`; essa é uma decisão do
   responsável, com racional e condição de revisita, não uma necessidade demonstrada por pesquisa.
6. Charter de produto, contexto-mestre, plano de pesquisa, investigações delimitadas, findings e
   decisões são autoridades distintas.
7. O bootstrap não aplicará o pacote `mint` completo; somente elementos do molde sustentados por
   evidência poderão ser reutilizados proporcionalmente.
8. `subagent-work-infrastructure` (SWI) é candidato a peer/provider, não módulo subordinado nem
   proprietário dos conceitos do Superinterviewer.
9. Dependências iniciais usarão referências estreitas e fixadas ou contratos estreitos; imports
   amplos são negados por padrão.
10. Implementação de produto requer antes um gate discriminante de pesquisa ou experimento que
    nomeie a incerteza, a evidência esperada e a regra de aceitação.
11. Uma reformulação não pode substituir silenciosamente a intenção da pessoa; mudanças devem ser
    rastreáveis, explicáveis, contestáveis e reversíveis quando cabível.
12. Afirmações não podem ser mais fortes que sua evidência; analogias matemáticas não são fatos do
    produto.

### 1.2 Propostas deste plano

Estas disposições são recomendações para decisão, não compromissos já aceitos:

1. Organizar a pesquisa por perguntas de produto e failure modes, não por repositórios, tecnologias
   ou disciplinas acadêmicas.
2. Usar uma pergunta-mãe refutável e um conjunto de perguntas derivadas que possam ser divididas,
   fundidas ou encerradas conforme a evidência.
3. Começar pela reconstrução histórica e por comparadores simples; só depois estabilizar schemas,
   políticas de intervenção, experimentos implementados ou formalizações.
4. Exigir de cada investigação um contrato de evidência e um retorno tipado ao programa.
5. Manter um registro de contradições e resíduos ao lado da matriz de evidências, em vez de forçar
   síntese prematura.
6. Tratar precedentes encontrados como material `build-from-owned`, não como falha; apenas ausência
   de testemunha ou colapso definicional encerram uma hipótese como negativa tipada.
7. Autorizar protótipos apenas quando um protocolo discriminar a tese do Superinterviewer de uma
   alternativa mais simples.
8. Promover formalização somente quando os objetos e relações já tiverem testemunhas observáveis e
   o formalismo mudar uma previsão, um teste ou uma decisão.

### 1.3 Questões abertas de mais alta consequência

1. “Refinar intenção” nomeia um fenômeno distinto e observável ou apenas reembala memória,
   elicitação de requisitos, coaching ou boa conversação?
2. “Companheiro” é uma identidade útil ou induz antropomorfização, dependência e confiança
   excessiva?
3. O alvo é ajudar a pensar, decidir, agir ou alternar entre esses fins; para quem e em quais
   contextos?
4. Perguntar, informar e reenquadrar são classes suficientes e distinguíveis? Onde entram sugerir,
   confrontar, consolar, experimentar e agir?
5. O que constitui “próximo passo suficientemente claro” sem premiar velocidade, coerência ou
   confiança às custas de verdade, autonomia e segurança?
6. Como observar mudança de intenção sem produzi-la ou legitimá-la por meio da própria medição?
7. Quando uma intervenção descobre uma intenção, quando a constrói legitimamente e quando a induz?
8. Qual estado mínimo preserva intenção, versões, evidência, lentes rejeitadas e resíduos sem gerar
   contexto acumulativo incoerente?
9. Quais decisões de framing exigem explicação, consentimento, contestação ou outra governança?
10. Quando `local first, refine on demand` é eficiente e quando cria miopia ou risco global?
11. Que vínculo com execução externa preserva identidade e provenance sem importar a ontologia do
    provider como ontologia do produto?
12. Yoneda restrito, local–global/Selmer, categorias, funtores, pullbacks, schemas ou resíduos
    tipados acrescentam poder discriminante — ou permanecem analogias dispensáveis?

## 2. Pergunta-mãe e árvore refinável

### Q0 — pergunta-mãe proposta

> **Sob quais condições observáveis e governáveis o Superinterviewer ajuda uma pessoa a transformar
> uma intenção incompleta, mutável ou contraditória em clareza suficiente para um próximo passo
> adequado, melhor que alternativas mais simples, sem substituir silenciosamente sua intenção nem
> degradar sua autonomia?**

“Melhor”, “clareza suficiente”, “adequado” e “autonomia” são variáveis de pesquisa, não termos já
operacionalizados. Q0 deve ser refinada por contexto de uso e população antes de qualquer teste
comparativo. Se nenhum contexto produzir uma testemunha distinta, a tese deve ser reenquadrada ou
abandonada; ela não deve ser salva por definição.

### Perguntas-filhas

| id | pergunta refinável | principal collapse-test |
|---|---|---|
| Q1 | Qual fenômeno humano e qual trabalho do usuário o produto realmente serve? | Casos alegados são explicados integralmente por um assistente de memória, busca ou requisitos. |
| Q2 | O que muda quando uma intenção é “refinada”, e quem valida essa mudança? | Não há traço observável entre intenção inicial, intervenção, revisão e passo habilitado. |
| Q3 | Qual intervenção é mais apropriada agora: perguntar, informar, sugerir, reenquadrar, aguardar ou avançar? | As classes não produzem decisões ou efeitos distinguíveis e viram apenas rótulos pós-hoc. |
| Q4 | Quais sinais, probes, lentes e resíduos são necessários para escolher e revisar intervenções? | O vocabulário não permite previsão, correção ou auditoria além de prosa livre. |
| Q5 | Como avaliar benefício decisório sem otimizar proxies manipuláveis? | As métricas aumentam confiança, velocidade ou coerência sem melhorar escolha, agência ou resultado. |
| Q6 | Quais salvaguardas tornam framing, iniciativa, memória e continuidade contestáveis? | Risco de indução ou dependência não pode ser detectado, explicado ou limitado. |
| Q7 | Em quais contextos a estratégia local e adaptativa supera abordagens globais ou simples? | A visão local omite riscos decisivos ou custa tanto quanto o modelo amplo que pretende evitar. |
| Q8 | Que fronteiras com ferramentas, agentes e providers preservam autoridade e lineage? | O provider passa a definir o produto, ou a evidência perde identidade e reprodutibilidade. |
| Q9 | Quais formalizações têm testemunha e consequência operacional? | O candidato apenas renomeia conceitos, não faz previsão e não discrimina alternativas. |

Q1–Q7 sustentam diretamente Q0. Q8 sustenta a integridade do programa, mas não define o produto.
Q9 é deliberadamente tardia e subordinada aos objetos estabilizados por Q2–Q5.

## 3. Workstreams

### WS0 — Linhagem histórica e corpus de casos

**Pergunta:** o que a evolução “jogo de perguntas → companheiro → máquina de refinar intenção”
realmente testemunha, e quais saltos ainda são apenas narrativa retrospectiva?

**Trabalho:** reconstruir os últimos meses por episódio, preservando estado anterior, intervenção,
sinal, distinção, reframing, mudança de intenção, próximo passo e resíduo. Separar logs observados de
interpretação posterior. Usar o caso fundador para gerar hipóteses e schema inicial, nunca para
generalizar.

**Outputs:** corpus anotado; cronologia de mudanças conceituais; schema observacional v0; lacunas de
dados; lista de contraepisódios.

### WS1 — Identidade de produto, usuários, trabalhos e comparadores

**Perguntas:** Q1 e partes de Q0. Quais contextos pedem um Superinterviewer e quais pedem resposta
direta, busca, coaching, facilitação ou execução?

**Trabalho:** delimitar unidades de valor, populações e situações; fazer sweep de precedentes em
mixed-initiative systems, sensemaking, tutoring, coaching, motivational interviewing, shared
decision-making e conversational search; definir comparadores mínimos honestos.

**Outputs:** tese de produto refutável; mapa contexto × trabalho × alternativa; matriz de
precedentes e owners; critérios de exclusão; proposições de valor que não reivindiquem novidade sem
evidência.

### WS2 — Intenção, estado, mudança e validação

**Perguntas:** Q2. Como distinguir intenção declarada, inferida, revisada e operacional, bem como
objetivos, valores, restrições e intenção do sistema?

**Trabalho:** obter testemunhas concretas de mudança; comparar preference construction, goal/value
elicitation, framing effects e filosofia da ação; testar se maior especificidade é um proxy inválido;
identificar ambiguidades que devem permanecer.

**Outputs:** glossário operacional; schema observacional v1; padrões de versionamento conceitual;
tipos iniciais de conflito e resíduo; critérios de validação pela pessoa.

### WS3 — Dinâmica de intervenção: perguntas, informação, sugestão e reframing

**Perguntas:** Q3 e Q4. Quando cada movimento ajuda, quando prejudica e como movimentos híbridos são
classificados sem circularidade?

**Trabalho:** construir exemplos e contraexemplos; comparar taxonomias existentes; testar a
separabilidade das três classes iniciais; tratar “integrar” como obrigação transversal e “avançar”
como parada/handoff até que evidência diga o contrário; investigar silêncio/espera como ação.

**Outputs:** taxonomia candidata com casos-limite; catálogo de probes e sinais; protocolo de escolha
e revisão de intervenção; tipologia de falhas; hipóteses de política, não uma política implementada.

### WS4 — Avaliação, causalidade e experimentos discriminantes

**Perguntas:** Q5 e Q7. Que mudança importa, como atribuí-la e como comparar alternativas sem ground
truth total?

**Trabalho:** definir outcomes e contrapesos antes dos instrumentos; separar influência, incerteza,
controlabilidade, valor de informação e sensibilidade decisória; combinar avaliação de processo,
resultado, autonomia, custo, carga cognitiva e efeitos longitudinais; desenhar testes contra
alternativas simples e um humano competente quando apropriado.

**Outputs:** matriz claim → evidência → método → collapse-test; conjunto mínimo de outcomes e
guardrails; protocolos manuais/offline iniciais; backlog ordenado de experimentos; regras de parada
pré-registradas.

### WS5 — Autonomia, poder de framing e governança

**Perguntas:** Q6. Quem governa como uma intenção é transformada e como o poder de iniciativa é
limitado?

**Trabalho:** threat modeling de indução, antropomorfização, dependência, persuasão, omissão e captura;
pesquisa de consentimento, shared decision-making, persuasive technology, participatory design e
AI governance; tratar DAO como hipótese concorrente, não destino arquitetural.

**Outputs:** taxonomia de riscos; direitos e controles candidatos do usuário; matriz decisão ×
autoridade × consentimento × contestação; requisitos de provenance; experimentos de compreensão e
agência; condições que restringem contextos de uso.

### WS6 — Localidade, lentes, memória e resíduos

**Perguntas:** Q4 e Q7. Quais distinções precisam de uma lente local, quando compor outra lente e
quando escalar para contexto global?

**Trabalho:** distinguir os sentidos de “local”; testar ganhos e perdas marginais de contexto;
investigar order effects, conflito e redundância entre lentes; tipar resíduos por origem, testemunha,
impacto e reparo; confrontar o acúmulo de contexto e a vigilância excessiva.

**Outputs:** critérios de entrada/saída de lentes; mapa de riscos locais–globais; schema de resíduo
tipado; hipóteses sobre memória mínima; protocolos de comparação entre frames.

### WS7 — Fronteiras de evidência, execução e dependências

**Pergunta:** Q8. Como uma pesquisa ou ação externa retorna evidência atribuível sem redefinir o
produto?

**Trabalho:** manter separação de autoridade; avaliar precedentes por concern; expressar apenas os
campos semânticos mínimos de uma futura ligação (identidade da pergunta, fonte/versão, execução,
resultado, limitações e decisão que pode informar). Não selecionar runtime nem desenhar integração
detalhada nesta fase.

**Outputs:** política de import/dependência por concern; contrato conceitual de retorno de evidência;
matriz provider × capacidade × autoridade × risco; critérios para `build-from-owned`.

### WS8 — Formalização com obrigação de consequência

**Pergunta:** Q9. Qual candidato formal explica ou discrimina algo que os modelos mais simples não
explicam?

**Trabalho:** somente após testemunhas de WS2–WS6; comparar grafos tipados, modelos causais,
constraint systems e modelos probabilísticos com categorias, funtores, optics, Yoneda restrito,
sheaves/descent, local–global/Selmer e pullbacks; declarar objetos, mapas, estrutura preservada e
condições de falha.

**Outputs:** fichas de candidato formal; witness e anti-witness; previsão/teste habilitado; verdict
`build-from-owned`, `already-deployed`, `novel-attempt` ou negativa tipada; recomendação de promover,
manter como analogia ou encerrar.

## 4. Grafo de dependências

```text
Decisões fundadoras aceitas
          │
          ├──────────────▶ WS7 (fronteiras e lineage) ──────────────┐
          │                                                         │
          ▼                                                         │
WS0 (corpus histórico) ──▶ WS1 (produto/comparadores) ──┐          │
          │                         │                    │          │
          └──────────────▶ WS2 (intenção/estado) ───────┼──▶ WS3 (intervenções)
                                    │                    │          │
                                    ├──────────────▶ WS5 (governança/autonomia)
                                    │                    │          │
                                    └──────────────▶ WS6 (lentes/localidade/resíduos)
                                                         │          │
WS1 + WS2 + WS3 + WS5 + WS6 ─────────────────────────▶ WS4 (avaliação/experimentos)
                                                         │
WS2 + WS3 + WS4 + WS6 ── gate de testemunha ─────────▶ WS8 (formalização)
                                                         │
WS4 + WS5 + WS7 ─────── gate humano ──────────────────▶ protótipo discriminante
```

WS7 é uma trilha de integridade que suporta todas as ondas, sem adquirir autoridade sobre a tese de
produto. WS4 começa cedo no desenho de evidência, mas não pode fechar métricas antes de WS1 e WS2
definirem o fenômeno. WS8 não bloqueia experimentos de produto e não pode anteceder testemunhas.

## 5. Ondas do programa

### Onda 0 — Constituição epistêmica mínima

**Objetivo:** tornar perguntas, fontes, afirmações, resíduos e decisões distinguíveis.

**Entradas:** decisões aceitas, Prompt-Mestre, initial definitions e findings existentes.

**Saídas:** versão aceita da pergunta-mãe; mapa inicial de claims e refutações; regras de promoção de
status; contratos de abertura/retorno de investigação; registro inicial das tensões T1–T6.

**Gate G0 — prontidão de pesquisa:** cada afirmação fundadora aponta para decisão, evidência,
hipótese ou analogia; findings podem contradizer a tese sem editar o charter; fontes externas podem
ser identificadas por revisão e trecho relevante. Se falhar, corrigir a separação de autoridade,
sem compensar com mais scaffold.

### Onda 1 — Testemunhar o fenômeno antes de arquitetá-lo

**Workstreams:** WS0, início de WS1 e WS2.

**Saídas:** corpus fundador anotado; comparadores; glossário e schema observacional inicial;
contraexemplos; contextos nos quais a tese não se aplica.

**Gate G1 — não-vacuidade e distinção:** existem episódios rastreáveis em que uma intervenção muda
distinções relevantes e habilita ou corrige um próximo passo, e há uma hipótese plausível de como
isso difere de uma alternativa simples. Sem witness, encerrar ou reenquadrar “refinar intenção”.

### Onda 2 — Precedentes, mecanismos e riscos

**Workstreams:** WS1–WS3, WS5–WS7; desenho antecipado de WS4.

**Saídas:** matriz de ownership; taxonomia candidata de movimentos; modelo observacional de sinais,
probes, lentes e resíduos; threat model; outcomes e guardrails propostos.

**Gate G2 — solidez definicional:** os conceitos não colapsam integralmente em termos já existentes;
quando houver owner, ele está citado e o uso está rotulado `build-from-owned`. Colapso não é
remediado por novo nome.

**Gate G3 — avaliabilidade:** ao menos uma claim de produto possui contraste, unidade de análise,
outcomes, guardrails, fonte de dados e resultado que a enfraqueceria. Caso contrário, a claim fica
fora da implementação e retorna à definição.

### Onda 3 — Experimentos discriminantes de baixo compromisso

**Workstreams:** WS4 com WS3 e WS5. Começar por replay, codificação cega, estudos Wizard-of-Oz,
comparações manuais ou outros métodos que não fixem arquitetura. Um artefato executável só entra
depois de G4.

**Saídas:** protocolos e resultados; análise de efeito e falhas; atualizações da matriz de
evidências; decisão sobre qual contexto, se algum, merece protótipo.

**Gate G4 — autorização de protótipo:** uma incerteza discriminante, um comparador simples, evidência
esperada, riscos, critérios de parada e escolhas que o protótipo não está autorizado a resolver
estão explícitos. A autorização é humana e limitada ao experimento.

### Onda 4 — Consolidação, governança e formalização seletiva

**Workstreams:** síntese de WS1–WS7; WS8 apenas para conceitos que passaram G1–G3.

**Saídas:** formulação mais forte defensável; mapa de limites de uso; decisões propostas; candidatos
formais promovidos ou demovidos; backlog reordenado; próximo ciclo de Q0.

**Gate G5 — consequência formal:** o formalismo muda uma previsão, identifica uma impossibilidade,
gera uma probe/teste ou preserva uma estrutura cuja perda importa. Se não, fica rotulado analogia e
deixa o caminho crítico.

**Gate G6 — decisão de programa:** aceitar, restringir, reenquadrar ou abandonar cada claim principal;
revisar Q0 e as decisões somente por registro explícito, nunca por atualização silenciosa de texto.

## 6. Outputs canônicos e critérios de qualidade

| output | função | condição mínima de aceitação |
|---|---|---|
| Mapa de claims | ligar tese, hipótese, analogia e decisão | cada claim tem status, fonte, collapse-test e decisão que pode informar |
| Matriz de evidências | mostrar suporte e contradição | claims load-bearing citam evidência; ausência é visível |
| Corpus anotado | testemunhar episódios | observação e interpretação estão separadas; contraepisódios são preservados |
| Matriz de precedentes | localizar owners e artefatos reutilizáveis | owner ou `precedent-clean`; nenhuma novidade implícita |
| Registro de resíduos/contradições | impedir coerência forçada | tipo, origem, witness, impacto, responsável e possível reparo |
| Protocolo experimental | tornar a hipótese discriminante | contraste, população/contexto, medidas, guardrails e stopping rule antes do resultado |
| Findings de branch | devolver síntese citada | resposta direta, limites, negativos tipados e implicações separadas de decisão |
| Proposta de decisão | converter evidência em escolha revisável | opções, recomendação, evidência, riscos, responsável e revisit condition |
| Síntese de ciclo | reancorar o programa em Q0 | melhor formulação defensável, fragilidades, menor próximo teste e motivos para abandonar/reframar |

Nenhuma contagem de documentos, dispatches, agentes, probes ou turnos é proxy suficiente de
progresso. Progresso é redução explícita de uma incerteza que altera uma decisão, com os resíduos
preservados.

## 7. Decision gates e direitos de decisão

1. **Gate de abertura de investigação:** o programa aceita uma branch somente se pergunta, claim,
   dependências, corpus, evidência esperada e collapse-test estiverem explícitos.
2. **Gate de aceitação de findings:** cobertura e citations são verificadas; execução bem-sucedida
   não equivale a evidência aceita.
3. **Gate de promoção epistêmica:** uma hipótese só vira proposta de decisão quando seus suportes,
   contraevidências e limites estão expostos. Findings não alteram charter por si.
4. **Gate de produto:** decisão humana aceita, rejeita ou reenquadra a proposta e registra condição
   de revisita.
5. **Gate de implementação:** G4; autoriza apenas o teste declarado, não arquitetura geral.
6. **Gate de integração:** uma dependência externa só entra se sua capacidade, owner, revisão,
   contrato, autoridade, licença/uso e saída removível estiverem claros.
7. **Gate de formalização:** G5; analogias não adquirem autoridade por elegância.

O programa de pesquisa pode recomendar; a pessoa ou órgão explicitamente nomeado decide mudanças
de produto, autoridade, risco aceitável e implementação. A hipótese de DAO é assunto de WS5 até que
uma decisão estabeleça outro regime.

## 8. Condições de parada, abandono e reenquadramento

### Parar uma investigação e bancar o resultado

- A pergunta foi respondida no nível necessário para a decisão e nova coleta tem baixo valor
  marginal.
- Um owner e artefato adequado foram encontrados: registrar `build-from-owned` ou
  `already-deployed` e parar de procurar novidade, sem encerrar o uso.
- Não há witness concreto após o corpus e o teste pré-declarados: registrar `no-witness`.
- O conceito colapsa em um termo já estabelecido sem diferença operacional: registrar
  `tautological`.
- Uma dependência anterior foi invalidada; suspender trabalho downstream e retornar ao gate, em vez
  de produzir precisão fictícia.

### Reenquadrar a tese ou restringir o produto

- Benefícios aparecem apenas em contextos específicos: trocar uma tese universal por escopo
  explícito.
- Alternativas mais simples entregam resultados equivalentes com menor custo ou risco: reenquadrar o
  Superinterviewer como combinação seletiva, interface de coordenação ou capability estreita, se a
  evidência sustentar.
- Perguntar/informar/reenquadrar não são separáveis: substituir a taxonomia por dimensões ou outra
  estrutura observacional.
- Medir intenção a deforma de modo material: deslocar o foco para avaliação participativa de
  processo e outcomes, com menor inferência interna.
- `local first` falha em domínios de alto risco: exigir visão global, escalada ou excluir esses
  domínios.
- “Companheiro” eleva dependência ou confiança indevida: adotar identidade menos antropomórfica,
  modos explícitos ou limites de continuidade.
- Formalização não gera consequência: demovê-la a analogia histórica e removê-la do caminho crítico.

### Abandonar uma claim central ou o conceito atual

- Não existe fenômeno testemunhável além de memória, busca, elicitação ou conversa competente.
- Ganhos de clareza não se traduzem em melhor agência, decisão ou ação e persistem apenas como
  sensação de racionalidade.
- O framing necessário para produzir benefício cria risco de manipulação que os controles testados
  não tornam aceitável.
- O sistema não consegue preservar autoria e contestabilidade da intenção em mudanças relevantes.
- Um humano ou alternativa simples domina consistentemente o sistema nos critérios pré-declarados e
  não há nicho defensável que justifique a complexidade.

Essas condições devem ser operacionalizadas antes de cada experimento. Elas não autorizam salvar a
tese por trocar métricas após observar o resultado.

## 9. Como branches retornam ao programa

### 9.1 Contrato de saída para qualquer investigação

Cada branch retorna um pacote lógico, mesmo quando seus arquivos físicos variam:

1. pergunta e versão da claim respondida;
2. corpus, fontes, revisões e limites;
3. achados com citations por claim load-bearing;
4. melhor contraevidência e incertezas restantes;
5. verdict por candidato: GO ou negativa tipada; ownership em coluna separada;
6. impacto nas dependências e no registro de resíduos;
7. proposta de manter, dividir, fundir, reframar ou encerrar a pergunta;
8. decisão que o achado pode informar — sem tomar essa decisão implicitamente.

O fluxo de promoção é:

```text
contexto/questão → hipótese → investigação → findings citados → proposta de decisão
       ▲                                                         │
       └────────────── revisão/reframing ← decisão humana ───────┘
```

Uma branch pode contradizer o frame corrente. Essa contradição atualiza matriz de evidências e
registro de resíduos imediatamente, mas só altera charter, decisões ou escopo vinculante após o
gate humano correspondente.

### 9.2 Retorno de `research-initial-definitions.md`

As initial definitions entram como **contexto informacional versionado**, não como findings nem
como lei de produto. Seu retorno ao programa ocorre assim:

- a pergunta refinável alimenta Q0 e registra sua linhagem;
- constraints confirmadas entram no conjunto de decisões/restrições somente quando já têm base de
  decisão identificada;
- baseline de evidências vira índice de fontes, não confirmação das claims descritas;
- known gaps alimentam perguntas-filhas, workstreams e gates;
- mudanças propostas retornam como **delta de definição**: trecho anterior, evidência nova,
  contradição, formulação proposta e decisão necessária.

As initial definitions nunca absorvem o plano, os findings ou o charter. Uma revisão deve preservar
o que mudou e por quê.

### 9.3 Retorno dos findings de Robot-Talks já aceitos

Os findings de 2026-08-10 retornam em quatro canais diferentes:

1. **Direct Result:** funda a proposta de repositório de pesquisa product-owned e a separação de
   autoridades, mas não autoriza criação ou implementação.
2. **Tensões T1–T6:** tornam-se resíduos e perguntas de programa. T1 alimenta G0; T2 a condição de
   revisita da decisão de repositório; T3 G4; T4 a política de reutilização proporcional; T5 WS7; T6
   a política de lineage e dependências.
3. **Rejected Conclusions:** entram como negativas tipadas/guardrails contra herança wholesale,
   taxonomia universal prematura, equivalência entre execução e evidência, no-code permanente e
   fusão de autoridades.
4. **Human Gate:** as seis disposições aceitas entram no registro de decisões confirmadas, com data,
   racional e condição de revisita. Elas condicionam o plano; não viram evidência da eficácia do
   Superinterviewer.

Novos findings devem retornar pelo mesmo princípio: evidência, tensão, negativa e decisão são
objetos diferentes, mesmo quando aparecem no mesmo relatório.

## 10. Perguntas que implementação não pode responder acidentalmente

Antes de G4, nenhuma escolha técnica deve fixar por inércia:

- se a intenção é um campo único, uma hierarquia, uma distribuição ou um histórico narrativo;
- se as três intervenções são completas ou mutuamente exclusivas;
- se uma lente é prompt, schema, programa, grafo, modelo ou objeto formal;
- se o usuário é indivíduo, grupo ou organização;
- se “companheiro” é a identidade final;
- se memória contínua é sempre desejável;
- se localidade é computacional, informacional, temporal, decisória ou todas;
- se uma única métrica representa refinamento;
- se DAO é o mecanismo de governança;
- se SWI ou outro provider define o workflow interno do produto;
- se teoria das categorias, Yoneda, Selmer, sheaves ou pullbacks são necessários;
- se o primeiro contexto de teste é o mercado definitivo do produto.

## 11. Recomendação de partida

Aceitar Q0 como pergunta-mãe provisória e iniciar Onda 0 seguida de WS0, WS1 e WS2. O primeiro
marco substantivo não deve ser um scaffold nem um runtime: deve ser um corpus fundador anotado, uma
tese de produto comparável a alternativas simples e um schema observacional capaz de mostrar o que
mudou sem presumir que toda mudança seja refinamento bem-sucedido. Só então a taxonomia de
intervenções, os experimentos, a governança aplicada e os candidatos formais ganham base para
avançar.

## Âncoras de evidência

- `pasted-text.txt`, seções 0–19: direção de produto, disciplina epistêmica, três movimentos, sinais,
  probes, lentes, localidade, estado, candidatos formais, medição, governança e 15 refutações.
- `research/superinterviewer-repository-bootstrap/research-initial-definitions.md`: pergunta inicial,
  constraints confirmadas, baseline e lacunas do bootstrap.
- `research/superinterviewer-repository-bootstrap/robot-talks/2026-08-10-superinterviewer-repository-foundation/findings.md`:
  direct result, tensões T1–T6, conclusões rejeitadas e seis decisões humanas aceitas em 2026-08-10.
