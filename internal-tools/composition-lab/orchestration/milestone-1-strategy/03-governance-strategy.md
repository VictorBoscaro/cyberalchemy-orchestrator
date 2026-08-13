---
artifact_kind: orchestration-strategy
status: proposed
date: 2026-08-13
milestone: "Milestone 1 — Modelo observável da composição de lentes"
owner: strategy-governance-agent
---

# Estratégia de governança e execução — Milestone 1

## Objetivo e critério de conclusão

O programa deve produzir uma primeira formalização da composição de lentes fundada no uso real do
repositório, explicitando definição provisória, operações, dinâmica, efeitos observáveis, perdas,
hipóteses falsificáveis e experimentos seguintes. O milestone só termina quando os artefatos
canônicos sobreviverem a uma revisão independente persistida.

O agente principal não pesquisa, escreve, sintetiza, corrige nem revisa. Sua atuação permitida é
orquestração: resolver a rota, apresentar e obter gates, abrir/fechar o workflow, lançar e aguardar
seats autorizados, encaminhar artefatos congelados e relatar recibos e decisões humanas.

## Invariante de decisão assistida

Não haverá um dispatch substantivo cuja forma seja inventada pelo agente principal. Cada nova onda
precisa de um **pacote decisório anterior**, escrito por subagentes, que declare objetivo refinado,
corpus, exclusões, riscos, recomendação de lentes e condição de stop. Além disso, a própria onda
deve conter pelo menos dois julgamentos independentes antes da síntese ou aprovação.

Isso não cria regressão infinita: os helpers que aconselham uma onda são seats daquela onda ou da
onda preparatória imediatamente anterior, não novos dispatches governados autônomos. Quando um
work-owner é lançado diretamente pelo host, seu prompt exige que peça a pelo menos um helper uma
crítica de escopo antes de escrever; o helper retorna ao owner, e o owner preserva a influência
desse conselho no artefato permitido pelo contrato. O ledger registra o dispatch governado, não
cada helper.

Para toda onda, o pacote decisório deve responder:

1. Que pergunta única esta onda resolve?
2. Que evidência anterior autorizou essa pergunta?
3. Que alternativas de decomposição foram consideradas e por que uma foi rejeitada?
4. Que artefatos são somente leitura e qual é o único owner de cada escrita?
5. Que resultado dispara avanço, rework, stop ou gate humano?

## Fronteiras contratuais

- **Robot-Talks** é uma sessão investigativa direta, não um dispatch de ledger. Preserva somente
  `dialogue.md`, `findings.md` e relatórios independentes em `reports/` (mais `ring/` apenas se houver
  confronto). Não alegar que o runtime governado a executou.
- **Research** é dispatch governado. Cada pasta precisa conter previamente seu próprio
  `research-initial-definitions.md`; a execução produz `research.md` com retornos coletados e
  `findings.md` com síntese citada e matriz de veredictos.
- **Experiment** não será executado no Milestone 1. O backlog pode recomendar propostas futuras,
  mas uma pré-inscrição posterior exigirá `experiment-initial-definitions.md` e `criterion.md` em
  dispatch separado; a execução do probe será ainda outra etapa.
- **Review** ataca artefatos existentes, produz somente `review.md` e não persiste retornos dos
  atacantes. Para este milestone, o modo será `persisted` e sua pasta conterá apenas esse arquivo.
- `plan` é reservado e não roteável no registry atual. Conselhos de estratégia não devem ser
  mascarados como research. O trabalho governado usa somente rotas resolvidas pelo registry.
- Stdout do bridge, envelopes e recibos de binding ficam no journal/telemetria; nunca são copiados
  para a pasta de trabalho.

## Árvore de artefatos e owners

```text
internal-tools/composition-lab/
├── orchestration/milestone-1-strategy/
│   ├── 01-*.md, 02-*.md, 03-governance-strategy.md
│   ├── 04-integrated-program.md                 # um integrador subagente
│   └── decision-packets/
│       ├── 01-robot-talks.md                    # um estrategista subagente
│       ├── 02-repository-research.md             # writer/auditor da onda anterior
│       ├── 03-precedent-research.md              # writer/auditor da onda anterior
│       ├── 04-model-synthesis.md                 # writer/auditor da onda anterior
│       └── 05-final-review.md                    # advisers independentes; sem ataques
├── robot-talks/2026-08-13-lens-composition-in-practice/
│   ├── dialogue.md                              # session recorder único
│   ├── findings.md                              # synthesizer único
│   └── reports/01-*.md … 04-*.md                # um owner por relatório
├── research/
│   ├── 2026-08-13-repository-lens-composition/
│   │   ├── research-initial-definitions.md       # bootstrap writer único
│   │   ├── research.md                           # collector único
│   │   └── findings.md                           # research writer único
│   ├── 2026-08-13-lens-composition-precedents/
│   │   ├── research-initial-definitions.md
│   │   ├── research.md
│   │   └── findings.md
│   └── 2026-08-13-observable-lens-composition-model/
│       ├── research-initial-definitions.md
│       ├── research.md
│       └── findings.md                           # bundle canônico do milestone
└── reviews/2026-08-13-milestone-1/
    └── review.md                                 # único artefato de review
```

Os slugs de data podem mudar se a onda abrir em outro dia, mas não depois da confirmação. Nenhum
agente escreve fora de sua pasta autorizada. Relatórios paralelos têm caminhos distintos. Apenas o
owner nominal de um artefato agregado o edita; demais seats retornam material ao owner pelo canal
do runtime. Uma nova versão após review vai para uma pasta `-v2`; os alvos congelados não são
editados no lugar.

## Sequência de ondas

### Onda 0 — conselho de estratégia e integração

**Natureza:** bootstrap de orquestração, não fingir que é um tipo `plan` registrado.

Os estrategistas independentes já chamados produzem documentos numerados distintos. Depois, um
subagente integrador — ajudado por um helper crítico — lê somente esses documentos, resolve
contradições e escreve `04-integrated-program.md` e o primeiro decision packet. O agente principal
apenas apresenta a estratégia Robot-Talks ao usuário. A sessão só começa após aprovação específica
dos concerns, perguntas, exclusões e da decomposição rejeitada, como exige Robot-Talks.

**Gate:** estratégia integrada cobre contratos, paths, owners, gates e stop/rework sem pedir ao
agente principal que faça trabalho intelectual.

### Onda 1 — Robot-Talks sobre tensões do uso real

**Pergunta central proposta:** onde o repositório afirma ou pressupõe composição de lentes, como
essas lentes são representadas e combinadas, e que contradições existem entre representação,
dinâmica e evidência de efeito?

**Assunções a desafiar:** `concern`, `angle`, `role`, persona e prompt representam adequadamente uma
lente; diversidade nominal implica diversidade epistemológica; síntese de tensões demonstra
composição; e a telemetria atual permite atribuir efeito à combinação.

**Concerns independentes:**

- representação e identidade da lente;
- seleção, ordem, interação e síntese;
- observabilidade, atribuição causal e perdas;
- portabilidade para fora do mecanismo de agentes, sem projetar produto.

Cada investigador lê o corpus necessário ao concern inteiro, escreve um relatório no formato
obrigatório e inclui perguntas para a síntese. Um sintetizador separado, aconselhado pelos quatro
relatórios, escreve tensões — não uma colagem de resumos. Um recorder separado mantém
`dialogue.md`. Se houver confronto direto, somente `ring/` pode recebê-lo.

**Human gate obrigatório:** o usuário dispõe cada tensão como acionável, diferida,
mal-interpretada ou incerta. Nenhuma research subsequente abre antes dessa disposição. Tensões
incertas geram uma Robot-Talks de follow-up estreita; não alargam silenciosamente a sessão.

**Saída decisória:** o sintetizador e um crítico independente produzem, fora da pasta Robot-Talks,
o decision packet da pesquisa de repositório. Assim, a próxima forma continua decidida por agentes.

### Onda 2 — research: inventário evidenciado do repositório

Antes do dispatch, um bootstrap writer, aconselhado por um separador fato/hipótese, cria o
`research-initial-definitions.md` local a partir do contexto amplo já existente e das disposições
humanas da Onda 1. Ele não define métodos, roles, gates ou hipóteses.

**Explorers (3 perspectivas):**

1. representação: usos e diferenças entre lente, concern, angle, role, persona e prompt;
2. mecânica: seleção, fan-out, independência, sequência, feedback, zig-zag e síntese;
3. evidência: artefatos e telemetria capazes — ou incapazes — de mostrar cobertura, redundância,
   perda, complementaridade e contribuição marginal.

Um writer sintetiza. Três skeptics guardam, um por gate, precedente interno/ownership,
não-vacuidade e solidez definicional. Um approver dedicado, fora de grupos de trabalho, valida
citações e a matriz. A pesquisa deve terminar com uma seção explícita `Recommendation for next
dispatch`, usada como conselho para a Onda 3.

**Critério de avanço:** toda afirmação sobre uso real cita arquivo e linha; exemplos positivos e
negativos existem; ambiguidades são preservadas; e os candidatos na matriz recebem owner,
witness, soundness, verdict e use-mode. Se todos os candidatos sofrerem KILL confirmado por
no-witness/tautologia, fechar `resolved` com negativos tipados e parar o programa para decisão
humana — não fabricar um modelo.

### Onda 3 — research: precedentes e instrumentos conceituais

Um novo initial-definitions local é escrito por subagente a partir da Onda 2, mantendo métodos e
hipóteses fora dele. O decision packet deve recomendar perspectivas e corpus; o agente principal
somente o converte em uma proposta concreta para confirmação.

**Explorers (3–4 perspectivas):**

- formalisms de composição, interfaces e closure;
- composição de perspectivas em cognição, decisão e práticas colaborativas;
- ensembles, red teams e métodos multiagente com medidas de diversidade/contribuição;
- desenho experimental e atribuição causal de efeitos de interação.

O writer relaciona precedentes somente às lacunas comprovadas pela Onda 2. Skeptics distintos
executam precedent, non-vacuity e definitional-soundness; um approver dedicado verifica que
“owned” virou `build-from-owned` ou `already-deployed`, nunca KILL por si só.

**Critério de avanço:** nenhum empréstimo conceitual perde o owner; cada candidato informa o
artefato/job que pode construir; e os limites de transferência ao caso do repositório estão
explícitos. Ausência de precedente só autoriza `novel-attempt`, nunca alegação forte de novidade.

### Onda 4 — research: modelo observável e backlog de experimentos

Esta onda consome apenas artefatos congelados das Ondas 1–3. Um initial-definitions específico é
preparado por writer + fact-boundary critic. Explorers independentes tentam construir modelos
concorrentes, em vez de dividir a escrita final por arquivo:

- modelo relacional/estrutural;
- modelo processual/interacional;
- modelo causal/observacional;
- caso de colapso: “composição de lentes” é apenas seleção, agregação ou coordenação.

O writer produz em `findings.md` o bundle canônico com seções claramente identificáveis:

1. inventário consolidado dos usos reais;
2. vocabulário provisório, fronteiras e contraexemplos;
3. ciclo de composição de lentes;
4. tipologia de operações e topologias;
5. matriz hipótese → evidência existente → falsificador;
6. backlog priorizado de experimentos, sem fingir que foram pré-registrados ou executados;
7. desconhecidos, resíduos e decisões ainda não autorizadas.

Skeptics separados aplicam os três gates da research. Um auditor de rastreabilidade verifica que
cada seção deriva de retornos em `research.md` e de fontes congeladas. Um approver dedicado, sem
outro trabalho, aceita ou devolve.

**Critério de avanço:** os sete conteúdos existem; cada hipótese pode perder; a tipologia possui
casos que são e não são composição; e o backlog discrimina hipóteses concorrentes. Se o modelo
colapsar, preservar o KILL tipado e levar ao usuário a decisão de redefinir o milestone.

### Onda 5 — `/review` final persistido

Antes de abrir, dois advisers independentes propõem corpus congelado e lentes; um resolver
subagente escreve `decision-packets/05-final-review.md`. Esse pacote não contém ataques ou findings
e não entra na pasta de review.

**Corpus congelado:** `findings.md` da Robot-Talks; os três `findings.md` de research; seus três
initial-definitions; e o `README.md` do Composition Lab. `research.md` e relatórios são evidência
de apoio disponível aos verifiers, mas não devem inflar o corpus principal sem necessidade.

**Attackers (4, todos leem o corpus inteiro):**

- fidelity/governance;
- mechanics/correctness;
- ownership/reference integrity;
- operability.

`abuse/gaming` fica como lente candidata para uma review direcionada posterior caso os advisers
encontrem um risco concreto; não será combinada com outra lente, e o grupo canônico permanece no
limite de quatro attackers.

Um writer sintetiza; ao menos dois verifiers independentes refutam contra o artefato literal; um
coverage auditor checa cada alvo × lente, autoria a seção Coverage e dispara o zero-findings flag;
um approver dedicado, sem outro trabalho e distinto de todos os anteriores, aprova. O output é
`persisted`; a pasta contém somente `review.md`, sem transcript, `attacks.md` ou `findings.md`.

**Aceite:** cada finding sobrevivente cita path e quotation do alvo, tem severidade e correção de
uma linha; findings refutados somem; cada artefato recebe KEEP/FIX; a Coverage cobre a matriz
completa. Fechar `resolved` mesmo havendo FIX, pois FIX é deliverable, não falha do review.

## Rework e condições de parada

- **Robot-Talks incerta:** uma follow-up estreita, depois novo human gate. Não mais que duas
  follow-ups sobre a mesma tensão sem decisão explícita do usuário.
- **Research reviewer pede material faltante:** usar o feedback edge somente quando necessário,
  registrar prompts verbatim no close e respeitar `max_loops` confirmado (recomendação: 2).
- **KILL total confirmado:** fechar a research como `resolved`, preservar negativos tipados e
  parar; completion do Milestone 1 requer renegociação humana.
- **Review KEEP ou apenas MINOR:** milestone completo após aprovação dedicada e close.
- **Review FIX com CRITICAL/MAJOR:** review fecha `resolved`; um subagente transforma change
  requests em decision packet. Uma nova research de rework escreve pasta `-v2`, seguida de nova
  review persistida em pasta `-v2`.
- **Segunda review ainda com CRITICAL/MAJOR no mesmo fundamento:** parar para gate humano; não
  consumir loops indefinidamente.
- **Dissent irreconciliável, falha de binding, registry drift ou close impossível:** fail closed,
  preservar o último artefato válido e usar o `exit_reason` canônico aplicável. Nunca degradar para
  lançamento não governado.

## Telemetria e rastreabilidade

Cada research/review é registrado uma vez na abertura e uma vez no fechamento por
`dispatch_workflow`; o dispatch id segue `YYYY-MM-DD-<slug>`. O registro inclui rota resolvida,
grupos, conexões, prompts, budgets, approver, pasta/modo de saída e `anti_bias_mode` explícito. Se o
usuário quiser anti-bias, a opção precisa ser confirmada separadamente para cada abertura; não é
herdada.

No close, registrar `exit_reason`, total/tree de agents, `loops_used` e todo feedback prompt
verbatim. Nomes vêm de `telemetry/agents/agent-pool.yaml`, escolhidos por `role_fit` e field, sem
reuso dentro do dispatch e sem auto-verificação. Antes do review, congelar o corpus por pares
path/hash no input manifest. A evidência de sucesso do programa é a cadeia:

```text
estratégia de agentes
→ tensões + disposições humanas
→ inventário citado
→ precedentes com owner
→ modelo/hipóteses/backlog rastreáveis
→ review.md verificado
```

## Gate final do milestone

O agente principal pode declarar o Milestone 1 alcançado somente quando um approver independente
aceitar o `review.md`, não houver CRITICAL/MAJOR pendente (ou uma rework `-v2` aceita os tiver
removido), todos os dispatches governados estiverem terminalmente fechados e os sete conteúdos
canônicos estiverem localizáveis no `findings.md` da Onda 4. A declaração deve listar os paths,
`exit_reason` e contagem real de agentes; não pode afirmar que hipóteses foram validadas quando o
programa apenas as formalizou e priorizou para teste.
