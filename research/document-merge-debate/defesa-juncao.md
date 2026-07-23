# Defesa da junção de `agents-communication-protocols` e `bus-contracts`

## Tese e escopo da decisão

**Tese:** os dois discoveries devem ser consolidados em um único documento de descoberta, com seções
internas explicitamente modulares. A junção aqui defendida é documental e de autoridade semântica;
ela **não** implica transformar Work Bus, command plane, journal, artifact store e kernel em um único
componente de runtime. Essa distinção é necessária porque `bus-contracts` já exige que essas
superfícies permaneçam separadas (`bus-contracts/README.md`, linhas 373–383 e 431–474), enquanto
`agents-communication-protocols` proíbe a criação de um runtime paralelo e mantém o `DispatchSpec`
como autoridade executável única (`agents-communication-protocols/README.md`, linhas 26–29, 87–99 e
745–751).

O objeto da junção é, portanto, a **especificação de discovery do ciclo de trabalho governado**: como
uma intenção compilada vira atribuições, inputs, outputs, reviews, rework, decisões e resultados
auditáveis. O texto unificado deve conservar capítulos e owners conceituais distintos, mas oferecer
uma única taxonomia, uma única matriz de invariantes e um único conjunto de critérios de promoção.

Todos os argumentos abaixo usam evidência dos três arquivos lidos integralmente:

- `agents-communication-protocols/README.md` (doravante **ACP**);
- `bus-contracts/README.md` (doravante **BC**);
- `bus-contracts/review/review.md` (doravante **BCR**).

As referências indicam linhas da revisão presente em 2026-07-22. Não uso autoridade externa: as
conclusões são inferências explícitas a partir do próprio corpus.

## Premissas verificáveis

**P1 — Ambos são proposals do mesmo estágio e ainda não são autoridade ratificada.** ACP se declara
`status: draft`, `veracity: low`, versão 0.3.0 (ACP, linhas 1–11), e BC também é `draft`, versão 0.3.0,
na mesma data (BC, linhas 1–10). ACP diz que seus schemas são hipóteses, não schemas ratificados
(ACP, linhas 66–68), e BC declara que não altera a SPEC por si só (BC, linhas 38–39). Logo, este é o
momento de menor custo institucional para eliminar duplicação; nenhuma autoridade promovida precisa
ser desfeita.

**P2 — BC se define como aprofundamento de uma fronteira interna de ACP.** BC identifica ACP como o
discovery do fluxo completo e a si mesmo como o aprofundamento da fronteira entre atribuição, input,
submissão, artifact, roteamento e consumo (BC, linhas 28–39). Não é uma semelhança inferida apenas
pelo nome: é uma relação de especialização declarada pelo próprio documento.

**P3 — ACP já inclui essa fronteira em seu objeto e em seus resultados obrigatórios.** ACP exige
contratos de input, `Contribution`, `Artifact`, submission manifest e review versionado (ACP, linhas
369–398); exige ainda pesquisar a fronteira barramento–journal e suas propriedades de entrega,
persistência, idempotência e visibilidade (ACP, linhas 599–609). Seus resultados esperados incluem
contratos mínimos de atribuição, submissão, discussão, review e rework, além da fronteira entre bus e
journal (ACP, linhas 689–702). Portanto, BC não está apenas “próximo”: ele ocupa uma obrigação já
contida no deliverable de ACP.

**P4 — As duas partes precisam ser promovidas como um sistema de invariantes, não como escolhas
independentes.** ACP só pode avançar após comprovar separação transporte/autoridade, versionamento,
invalidação e autoridade única no `DispatchSpec` (ACP, linhas 735–751). BC só pode propor mudança na
SPEC após comprovar, entre outros pontos, gates corretos, roteamento sem destinatário arbitrário,
imutabilidade de topologia e rejeição de combinações não autorizadas (BC, linhas 626–642). Um contrato
de bus que passe seus testes mas viole o protocolo de julgamento ou de dispatch não é aceitável; um
protocolo que passe seus testes mas não possua submissão/retry/consumo implementável tampouco o é.

## Argumento 1 — Há identidade de problema, não mera afinidade temática

ACP define o problema como preservar independência, registrar versões sem sobrescrever evidência,
limitar correções e vincular aprovação à versão exata analisada (ACP, linhas 16–29). BC materializa
precisamente essas obrigações: separa candidata persistida, receipt, aceitação por CAS e abandono
(BC, linhas 62–94), vincula review a submission, generation e digest exatos (BC, linhas 517–532) e
separa submissão aceita de resultado comprometido (BC, linhas 96–109).

Isso forma uma cadeia causal única:

```text
perfil/recipe confirmados
  -> DispatchSpec + RoutingPlan
  -> assignment + input materializado
  -> candidata + artifact + receipt
  -> aceitação versionada
  -> julgamento/review
  -> rework ou commit
  -> consumer/handoff autorizado
```

Cada seta é sustentada pelos próprios textos: perfil e autoridade do `DispatchSpec` em ACP, linhas
58–64 e 87–99; planejamento e confirmação antes da execução em ACP, linhas 410–412; `RoutingPlan` e
estado derivado em BC, linhas 345–366; lifecycle de publicação em BC, linhas 62–109; review/rework em
ACP, linhas 369–398 e BC, linhas 517–532; handoff somente após commit em BC, linhas 441–449.

Separar documentalmente a metade “por que/quem/quando” da metade “qual objeto/fato libera a próxima
fase” corta essa cadeia no ponto de maior acoplamento semântico. Um único documento permite afirmar
o invariante ponta a ponta e associar-lhe um probe ponta a ponta.

## Argumento 2 — A duplicação já criou duas taxonomias para os mesmos objetos

ACP propõe um descritor de atividade que compila para `task_ref`, `policy_ref`, Contributions,
Artifacts e GroupResults existentes (ACP, linhas 303–328). Para retornos, fala em `Contribution`
tipada cujo payload referencia `Artifact` imutável, mas admite que paths, hashes e base snapshot ainda
não são campos ratificados de `Artifact` (ACP, linhas 369–383). BC, sobre a mesma fronteira, propõe
`WorkArtifact`, `WorkPublicationCandidate`, `WorkSubmission`, `ReviewSubmission`,
`ChangeSetArtifact`, `OutputContract` e outros objetos (BC, linhas 41–60 e 534–551).

Esses vocabulários podem ser compatíveis, mas o corpus ainda não contém o mapeamento total e
funcional entre eles. Em particular:

- ACP: `Contribution -> Artifact`; BC: `WorkPublicationCandidate -> WorkSubmission`, contendo refs de
  `WorkArtifact` (ACP, linhas 377–383; BC, linhas 45–60).
- ACP: recipe realiza dependências, gates e review/rework; BC: `RoutingPlan` contém topologia,
  templates, edges/release gates e matriz de responsabilidade (ACP, linhas 87–92 e 260–270; BC,
  linhas 345–371).
- ACP: skill tem identidade transitiva, protocolo compilado e binding ativo; BC: `SkillBinding`
  congela skills por papel, mas ainda pergunta como resolver skills e se mudança invalida assignment
  ou attempt (ACP, linhas 101–131; BC, linhas 296–315 e 553–562).
- ACP: review agregado exige `JudgmentRound` selada; BC: Work Bus inclui reviews e deliberação, mas
  deixa fan-out, quorum, conflito e timeout como questão aberta (ACP, linhas 330–367; BC, linhas
  373–425 e 553–566).

Enquanto houver dois documents of record, existem quatro resultados possíveis para cada conceito:
`definido só em ACP`, `definido só em BC`, `definido consistentemente em ambos`, `definido em tensão`.
A terceira categoria ainda exige manutenção duplicada; a quarta exige adjudicação. Um documento
unificado reduz o espaço de estados a `definido canonicamente` ou `aberto`, sem fingir que duas
formulações independentes são automaticamente equivalentes.

## Argumento 3 — As interfaces críticas só podem ser validadas em conjunto

Considere os conjuntos de invariantes:

- \(P\): invariantes de protocolo (identidade, independência, gates, ownership, versão);
- \(B\): invariantes de publicação/consumo (schema, receipt, CAS, routing, release);
- \(X\): invariantes de interface que mencionam elementos dos dois conjuntos.

Exemplos concretos de \(X\) são: “reviewer avalia a versão exata” (ACP, linhas 377–398; BC, linhas
423–425 e 531–532), “mudança de topologia exige nova confirmação” (ACP, linhas 410–412; BC, linhas
352–355) e “o agente não escolhe o destinatário da correção” (ACP, linhas 599–609; BC, linhas
368–371 e 427–429).

Se os critérios de promoção forem executados isoladamente, comprovar todos os predicados internos
\(P\setminus X\) e \(B\setminus X\) não prova \(X\). Formalmente:

\[
\bigwedge(P\setminus X) \land \bigwedge(B\setminus X)
\not\Rightarrow \bigwedge X.
\]

Contraexemplo construtivo: BC pode aceitar um `review.accepted: changes_required` e liberar rework
da mesma topologia (BC, linhas 96–109), mas, sem importar a regra de ACP, uma implementação poderia
agregar dois reviews sem posições seladas e independentes. Todos os invariantes locais de receipt e
routing ainda passariam, mas a higiene obrigatória da `JudgmentRound` seria violada (ACP, linhas
347–367). Logo, conformidade local não implica conformidade do sistema.

A junção permite uma matriz única `invariante -> objetos -> transições -> probes -> autoridade`, em
que cada elemento de \(X\) recebe um owner textual e um teste. Essa é a forma mais simples de fechar a
lacuna lógica acima.

## Argumento 4 — O histórico de review demonstra que detalhes locais alteram garantias globais

BCR registra oito falhas encontradas por uma revisão clean-room: escrita antes da aceitação,
liberação prematura de consumers, confusão entre plano imutável e reabertura, consumo não
especificado, schemas incompletos, estados de verificação colapsados, output incompatível com
`work_kind` e observação incremental confundida com artifact imutável (BCR, linhas 17–41). O próprio
review informa que essas falhas eram novas lacunas apesar de 18/18 findings anteriores e 15/15 change
requests terem sido remediados (BCR, linhas 3–15).

Não se segue daí que revisão separada seja inútil; segue-se algo mais preciso: completude local é
frágil quando as garantias dependem de fronteiras. Várias correções de BC mudam diretamente a
semântica de ACP:

- workspace isolado e promoção atômica dão execução concreta ao ownership exclusivo e à autoridade
  de integração de ACP (BC, linhas 172–194; ACP, linhas 281–301);
- release gates distinguem evidência local de resultado oficial, condição necessária para que
  `GroupResult` não se confunda com aprovação final (BC, linhas 96–109; ACP, linhas 347–367);
- `ConsumerInputManifest` concretiza a exigência de inputs exatos e versionados (BC, linhas 395–419;
  ACP, linhas 369–375);
- state/generation/CAS concretizam invalidação e rework sem sobrescrever história (BC, linhas 517–532;
  ACP, linhas 586–597).

Manter essas correções apenas em BC deixa ACP descritivamente atrasado; copiá-las para ACP cria
duplicação. Incorporá-las como subcapítulos de uma única descoberta preserva a especialização sem
criar duas verdades.

## Argumento 5 — A própria decomposição proposta pelos textos favorece um “monólito modular” de
documentação

ACP quer um conjunto pequeno de recipes reutilizáveis e rejeita branches ad hoc no kernel (ACP,
linhas 400–408). BC quer um Work Bus lógico único, mas insiste em operações, schemas e capabilities
distintos, além de manter command plane e handoff fora do envelope de autoria (BC, linhas 373–474).
O princípio compartilhado é: **uma superfície de autoridade, módulos internos tipados**.

Aplicar o mesmo princípio à documentação não é analogia decorativa; é manter isomorfismo entre a
arquitetura descrita e a autoridade que a descreve. Um único discovery pode conter módulos de:

1. identidade, perfis e compilação;
2. atividades, assignments e routing;
3. invocação e inputs materializados;
4. submissions, artifacts, receipt e acceptance;
5. julgamento, review e rework;
6. commit, delivery e handoff;
7. segurança, ownership e isolamento;
8. registry de invariantes, questões abertas e probes.

Essa estrutura preserva a estreiteza operacional de BC, explicitamente limitada ao Work Bus (BC,
linhas 15–26), ao mesmo tempo que a posiciona dentro do lifecycle completo que ACP já reivindica
(ACP, linhas 16–36). Junção não requer que a seção de bus passe a decidir knowledge, broker ou schema
final — itens que BC corretamente mantém fora de escopo (BC, linhas 617–624).

## Quantificação honesta da decisão

Não há dados de manutenção suficientes para alegar uma economia numérica específica. É possível,
porém, formular uma condição falseável, sem fingir precisão inexistente.

Defina, por ciclo de mudança:

- \(D\): custo de detectar drift entre os documentos;
- \(S\): custo de sincronizar conceitos repetidos;
- \(V\): custo de verificar invariantes de interface em dois critérios de promoção;
- \(N\): custo adicional de navegação/review causado por um documento unificado maior;
- \(R\): custo de refatoração inicial da junção.

Em um horizonte de \(k\) ciclos, a junção é economicamente preferível quando:

\[
k(D+S+V-N) > R.
\]

O corpus prova que \(D,S,V\) não são identicamente zero: há conceitos duplicados e questões ainda não
mapeadas (Argumento 2), critérios de promoção separados com invariantes cruzados (Argumento 3) e um
review que encontrou oito lacunas de fronteira após uma rodada extensa de remediação (BCR, linhas
3–41). O corpus não mede \(N\) nem \(R\); por isso, a recomendação deve ser confirmada com um probe de
edição/review, não apresentada como teorema de produtividade.

Uma métrica mínima seria selecionar dez mudanças representativas dos probes de ambos os documentos,
aplicá-las em versões branch separada e unificada, e medir: arquivos tocados, referências quebradas,
invariantes contraditórios detectados por review, tempo de navegação e findings por mudança. Os probes
já enumeram cenários compartilhados de retry, drift, review, paths, receipts e routing (ACP, linhas
623–687; BC, linhas 570–599), portanto o experimento não precisa inventar uma workload artificial.

## Tentativa de falsear a tese

### Objeção forte 1 — Os níveis de abstração são diferentes

ACP se classifica nas camadas arquitetura/domínio (ACP, linhas 1–6), enquanto BC se classifica nas
camadas aplicação/orquestração (BC, linhas 1–6). Além disso, BC declara escopo estreito no Work Bus
(BC, linhas 23–26). Isso é evidência real contra uma fusão sem estrutura.

**Resposta limitada:** diferença de camada justifica capítulos e ownership diferentes; não prova a
necessidade de duas autoridades de discovery quando BC se autodefine como aprofundamento de ACP (BC,
linhas 28–39) e ACP exige como resultado justamente os contratos e a fronteira tratados por BC (ACP,
linhas 689–702). A tese seria refutada se a maior parte de BC pudesse evoluir sem alterar qualquer
invariante, vocabulário, probe ou critério de ACP. Os cruzamentos documentados nos Argumentos 1–4
fornecem contraevidência atual.

### Objeção forte 2 — Um documento de mais de mil linhas prejudica revisão independente

ACP tem 756 linhas e BC, 642; a consolidação bruta seria extensa. O risco é especialmente relevante
porque ambos exigem revisão independente antes de promoção (ACP, linhas 735–751; BC, linhas 626–642),
e BCR mostra que clean-room review encontra lacunas importantes (BCR, linhas 3–30).

**Resposta limitada:** concatenação não é junção adequada. A consolidação deve eliminar objetivos,
vocabulários, perguntas, probes e critérios duplicados, manter sumário e fornecer matrizes por
capítulo. A tese deve ser rejeitada se um protótipo consolidado, após deduplicação, aumentar de forma
material e repetível o tempo para encontrar uma regra ou reduzir a detecção de findings em review
cego. Esse é um teste empírico válido; ainda não há evidência no corpus de que o custo de navegação
supere o custo de inconsistência.

### Objeção forte 3 — Separação permite promoção parcial de contratos maduros

BC tem contratos operacionais detalhados e review próprio; ACP mantém 34 perguntas principais e
várias hipóteses abertas (ACP, linhas 437–485). Poderia ser útil promover apenas o bus.

**Refutação:** os critérios atuais já impedem promoção segura puramente local. BC depende de
`DispatchSpec`, `RoutingPlan`, assignments, skills, reviewers e regras de conclusão (BC, linhas
96–109, 296–340 e 345–371); ACP ainda decide ownership, protocolo ativo, recipe, roles, julgamento e
aprovação (ACP, linhas 70–131, 228–270 e 330–398). Promover nomes de BC enquanto suas relações com as
entidades de ACP continuam abertas cristalizaria uma das taxonomias antes da adjudicação. O próprio BC
diz que seu resultado pode alterar ACP antes de promover contratos à SPEC (BC, linhas 28–39).
É possível marcar capítulos internos com maturidade distinta sem dar-lhes documentos de autoridade
separados.

### Objeção forte 4 — A junção pode expandir indevidamente o escopo do Work Bus

BC exclui knowledge, telemetria e controle e reserva apenas uma extension seam futura (BC, linhas
23–26 e 451–474). ACP abrange pesquisa, síntese, decisão e execução. Uma fusão mal desenhada poderia
fazer toda comunicação parecer operação do Work Bus.

**Resposta:** esta objeção condiciona a forma da junção, não a invalida. O documento unificado deve
conservar a tabela que distingue Work Bus, command plane, handoff, projection e knowledge futuro (BC,
linhas 373–383) como invariante transversal. A tese deve ser considerada falha se o texto consolidado
não permitir responder, para cada mensagem/efeito, qual superfície tem autoridade — exatamente a
separação que ACP já exige como critério de avanço (ACP, linhas 737–751).

## Critérios objetivos que fariam esta recomendação ser abandonada

A defesa da junção é falsificável. Deve-se manter os documentos separados se um protótipo e uma
revisão independente demonstrarem qualquer um destes fatos:

1. menos de um limiar previamente fixado (sugestão: 20%) dos invariantes de BC possui dependência
   semântica real em objetos/gates de ACP, depois de excluir referências meramente contextuais;
2. não é possível criar um vocabulário canônico sem apagar distinções necessárias como
   candidate/submission/result, plano/estado ou worker/reviewer/final approver — distinções exigidas
   em BC, linhas 62–109 e 345–371, e ACP, linhas 385–398;
3. review cego encontra significativamente menos conflitos de interface no texto unificado do que nos
   documentos separados **ou**, inversamente, encontra queda significativa na localizabilidade e
   compreensão das regras;
4. os owners reais e ciclos de release das duas partes forem independentes a ponto de toda alteração
   conjunta exigir bloqueio organizacional, condição que os documentos atuais não registram;
5. uma matriz de rastreabilidade provar que os critérios de promoção podem ser satisfeitos
   independentemente sem deixar qualquer elemento de \(X\) sem owner/teste.

O limiar de 20% é uma proposta de desenho experimental, não um fato derivado. Ele deve ser acordado
antes da classificação para evitar escolha oportunista após observar os dados.

## Forma recomendada da junção

A consolidação deve ocorrer como refatoração rastreável, não como simples remoção de BC:

1. criar um novo documento canônico do “governed work lifecycle” e preservar redirects/histórico dos
   paths atuais;
2. importar a distinção de superfícies de BC sem enfraquecê-la (BC, linhas 373–474);
3. criar tabela canônica que mapeie `Activity/Contribution/Artifact/GroupResult` de ACP aos objetos
   `WorkAssignment/WorkPublicationCandidate/WorkSubmission/ReviewSubmission` de BC, decidindo quais
   são entidades, envelopes ou fatos;
4. unir as perguntas abertas por dependência, especialmente identidade de skill, routing,
   julgamento agregado e invalidação (ACP, linhas 437–485; BC, linhas 553–568);
5. unir probes em cenários ponta a ponta e manter o gate de execução apropriado — ACP já diferencia
   probes de discovery daqueles pós-implementação (ACP, linhas 623–687), enquanto BC oferece casos
   implementáveis de lifecycle, routing e schemas (BC, linhas 570–599);
6. adotar um único critério de promoção, com subgates por capítulo, incorporando integralmente os
   requisitos atuais de ACP e BC (ACP, linhas 735–751; BC, linhas 626–642);
7. anexar a história de BCR como evidência de revisão, sem transformar findings remediados em regras
   órfãs (BCR, linhas 3–46).

## Conclusão

A posição favorável à junção não depende da máxima genérica “menos documentos é melhor”. Ela depende
de quatro fatos verificáveis: BC declara ser aprofundamento de ACP; ACP já inclui os contratos do bus
em seu escopo e deliverables; os dois textos definem partes interdependentes das mesmas cadeias de
estado e autoridade; e o review de BC demonstra que detalhes da fronteira alteram garantias globais.

Manter documentos separados é defensável apenas se a separação corresponder a independência de
invariantes, promoção e mudança. O corpus atual mostra o contrário. A decisão mais racional, sujeita
aos testes de falsificação acima, é consolidar os dois discoveries em um documento modular com uma
única taxonomia, uma única matriz de interfaces e um único gate de promoção — preservando, dentro
dele, a separação rigorosa dos componentes de runtime.
