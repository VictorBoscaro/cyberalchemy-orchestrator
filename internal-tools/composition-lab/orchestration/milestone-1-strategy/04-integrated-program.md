---
artifact_kind: milestone-integrated-program
status: preserved-pilot
milestone: 1
topic: observable-lens-composition
last_updated: 2026-08-13
inputs:
  - 01-evidence-strategy.md
  - 02-composition-strategy.md
  - 03-governance-strategy.md
---

# Programa integrado — Milestone 1: modelo observável da composição de lentes

> **Histórico preservado:** este programa agora é o **Caso 1 — piloto de composição de lentes** do
> programa geral do Composition Lab. Seus contratos continuam úteis para esse caso, mas sua
> pergunta, sequência e deliverables não definem composição em geral. A direção atual está em
> [`../../research-program.md`](../../research-program.md).
> **Este artefato está superseded e não autoriza execução:** nenhuma onda, gate ou dispatch abaixo
> permanece ativo sem nova proposta e confirmação pelo programa atual.

## Decisão executiva

O milestone será executado como uma cadeia dependente de investigações preservadas. O primeiro
trabalho substantivo será um **inventário reproduzível do uso real de lentes no repositório**.
Robot-Talks virá depois, para confrontar tensões encontradas nesse inventário, e não para substituir
a coleta de evidência. Vocabulário, modelos, precedentes e experimentos só serão tratados depois que
os casos e contracasos internos estiverem congelados.

O agente principal será apenas orquestrador. Ele pode confirmar rota, apresentar gates, lançar e
aguardar agentes, encaminhar artefatos congelados, registrar e fechar dispatches e relatar decisões.
Ele não pesquisa, classifica ocorrências, sintetiza, arbitra findings, corrige artefatos ou aprova o
próprio programa.

Cada onda terá decisão assistida por agentes. Antes de qualquer julgamento substantivo, o owner
despachado deverá consultar pelo menos um helper independente sobre escopo, corpus, decomposição,
riscos e condição de parada; o artefato do owner registrará quais recomendações foram aceitas ou
rejeitadas. Essa consulta é atividade de seat, não um novo tipo de dispatch nem uma regressão
infinita. O principal nunca substitui esse conselho por decisão própria.

## Como os três pareceres foram integrados

### Convergências adotadas

Os três pareceres concordam que:

- o repositório oferece precedentes e prescrições, não prova causal de eficácia;
- “lente” não pode ser inferida da palavra `lens`, nem confundida automaticamente com `concern`,
  `angle`, `role`, persona, método ou prompt;
- prescrição, instanciação, execução e efeito devem permanecer separados;
- casos positivos, negativos, ambiguidades, perdas e resíduos precisam ser preservados;
- hipóteses concorrentes precisam poder perder;
- pesquisa, Robot-Talks, experimento e review têm contratos incompatíveis e não devem ser
  misturados;
- a revisão final deve ser independente, persistida e seguida de rework quando houver findings
  CRITICAL ou MAJOR;
- nenhuma interface, schema, runtime ou extração de produto é autorizada por este milestone.

### Divergências resolvidas

1. **Inventário ou Robot-Talks primeiro.** `01` e `02` colocam o inventário primeiro; `03` propõe
   Robot-Talks primeiro. Fica escolhido o inventário. A skill Robot-Talks existe para tensões entre
   findings evidenciados, não para censo ou descoberta aberta de exemplos. O valor de `03` é
   preservado colocando Robot-Talks imediatamente após o inventário, com seu gate humano próprio.
2. **Vocabulário antes ou depois do confronto.** O inventário pode emitir somente rótulos
   descritivos provisórios. A delimitação de vocabulário e o modelo vêm depois de Robot-Talks, para
   não cristalizar o schema atual como ontologia.
3. **Pesquisa externa.** Não haverá varredura externa ampla antes do inventário. Precedentes externos
   serão uma pesquisa separada e condicionada às lacunas demonstradas pelo corpus interno. Encontrar
   owner gera `build-from-owned` ou `already-deployed`, nunca KILL.
4. **Experimentos no milestone.** O milestone exige backlog experimental discriminante, não prova
   causal. Pré-registros e runs são uma ramificação condicional: só entram antes da síntese se dois
   modelos que mudam a formalização não puderem ser separados pela evidência existente. Proposta e
   run nunca compartilham dispatch.
5. **Formato do review.** O review final produz somente `review.md` em pasta própria. Retornos de
   attackers/verifiers não são persistidos, e `research.md`/`findings.md` não são criados nessa rota.

## Definição operacional do milestone

### Pergunta

> Como lentes são declaradas, realizadas e relacionadas nas práticas do repositório; quais operações
> distinguem composição de pluralidade, partição, agregação, seleção e coordenação; o que pode ser
> observado sem alegar causalidade indevida; e qual modelo provisório preserva os casos, limites,
> perdas e hipóteses que a evidência exige?

### Unidade observacional provisória

Uma ocorrência candidata requer, sem ainda defini-la como composição:

1. alvo ou pergunta comum identificável;
2. duas ou mais perspectivas distinguíveis;
3. diferença pretendida registrada antes ou durante o trabalho;
4. operação relacional observável — por exemplo síntese, confronto, reveal, reavaliação,
   verificação, projeção ou seleção;
5. traço preservado do resultado dessa operação.

Casos com apenas 1–3 são **pluralidade declarada**. Uso isolado da palavra é **menção**. Divisão por
fontes ou arquivos sem perspectiva comum é **partição de trabalho**. Esses rótulos são protocolo de
inventário, não teoria ratificada.

Para cada caso, registrar separadamente:

- **prescrição:** o mecanismo é recomendado;
- **instanciação:** foi configurado neste caso;
- **execução:** há traço de que as etapas ocorreram;
- **efeito:** há delta atribuível, controle, contrafactual ou avaliação independente.

Nenhuma claim sobe de nível por inferência. `close: resolved` prova fechamento, não utilidade.

### Deliverables necessários

O milestone só pode ser declarado alcançado quando existirem e forem rastreáveis:

1. inventário citado dos usos reais, controles negativos e ambiguidades;
2. vocabulário provisório com fronteiras, vizinhos, testemunhas, não-exemplos e collapse-tests;
3. ciclo observável da composição de lentes;
4. tipologia provisória de operações e topologias;
5. matriz hipótese → evidência → contraevidência → falsificador → estado;
6. backlog priorizado de experimentos discriminantes;
7. síntese explícita do que sobreviveu, morreu e permanece desconhecido;
8. `/review` persistido sem CRITICAL/MAJOR pendente.

Não é requisito demonstrar mecanismo causal universal, executar todo o backlog, provar
portabilidade ou construir produto. Toda afirmação de portabilidade deve ser `demonstrada`,
`candidata` ou `não sustentada`.

## Invariantes de execução e preservação

- Cada research tem `research-initial-definitions.md` local antes de seu desenho formal e produz
  `research.md` + `findings.md` quando `n >= 2`.
- Robot-Talks é sessão autônoma, não entrada do ledger; preserva `dialogue.md`, `findings.md`,
  relatórios independentes e, somente se usado, `ring/`. Exige aprovação de estratégia antes do
  lançamento e disposição humana das tensões antes do downstream.
- Cada experiment proposal contém uma hipótese e produz somente `criterion.md`, precedido por
  `experiment-initial-definitions.md`. O criterion é congelado antes do resultado.
- Um experiment run posterior consome o criterion read-only e produz `experiment.md` +
  `findings.md`; runner e adjudicator são distintos dos autores da proposta.
- Review ataca corpus existente, lê o corpus inteiro por attacker, produz somente `review.md` e não
  implementa correções.
- Um artefato agregado tem um único writer. Seats paralelos não editam o mesmo arquivo.
- Inputs de cada onda são congelados por path/hash. Revisões são gravadas em pasta `-v2`; não se
  edita o alvo congelado no lugar.
- Binding receipts, stdout do bridge e envelopes permanecem no journal/telemetria, nunca na pasta
  de trabalho.
- Em dispatch governado, o seat prompt respeita o host binding obrigatório. Falha de hook fecha por
  segurança ou usa a bridge diretamente com a lacuna registrada no close; não deixa recibos em
  arquivo local.

## Programa canônico

### Onda 0 — integração e preparação

**Estado:** este documento integra os três pareceres. Um challenger e um verificador de compliance
devem revisar o programa antes da abertura substantiva. O agente principal apenas encaminha seus
resultados a um resolver subagente se houver conflito.

**Gate 0:** programa aceito quando sequência, contratos, owners, paths e stop/rework não exigirem
trabalho substantivo do principal.

### Onda 1 — inventário reproduzível do repositório (`research`)

**Dependência:** Gate 0 e initial definitions locais. O pacote completo está na seção seguinte.

**Owners:** advisers de escopo aconselham; bootstrap writer cria as definições locais; explorers
coletam; collector preserva retornos; writer sintetiza; skeptics aplicam gates separados; coverage
auditor verifica corpus/citações; approver dedicado apenas aprova.

**Gate 1:** tabela citada, corpus reproduzível, níveis de evidência separados, positivos e negativos
presentes e ausência de claims causais apoiadas apenas por configuração.

### Onda 2 — tensões composicionais (`Robot-Talks`)

**Dependência:** Gate 1 e corpus congelado do inventário.

Um strategist subagente, aconselhado por helpers independentes, transforma findings do inventário
em proposta de concerns não sobrepostos, perguntas, exclusões e decomposição rejeitada. O principal
apresenta essa proposta ao usuário; nenhum investigador é lançado antes da aprovação específica.

Concerns candidatos, a confirmar à luz da Onda 1:

1. lente declarada versus lente realizada;
2. independência versus transformação por interação;
3. síntese versus seleção e preservação de resíduo;
4. observabilidade versus atribuição causal.

**Owners:** recorder único de `dialogue.md`; um investigador por relatório; synthesizer único de
`findings.md`; human owner da disposição de cada tensão.

**Gate 2:** toda tensão contém lados contraditórios, impacto e evidência; o usuário a dispõe como
acionável, diferida, mal interpretada ou incerta. Incerta gera follow-up estreita, no máximo duas
vezes sem novo gate humano.

### Onda 3 — vocabulário, modelos e hipóteses concorrentes (`research`)

**Dependências:** Gates 1–2 e nova initial definition local.

Explorers propõem modelos concorrentes — declarativo, transformacional, relacional e caso de
colapso — sobre o mesmo corpus. O writer mantém separados definição, operação e efeito. Skeptics
aplicam precedent interno, non-vacuity e definitional-soundness; auditor mantém a matriz de verdicts.

**Gate 3:** todo termo tem testemunhas de estratos distintos, não-exemplo, vizinho, collapse-test e
estado; toda hipótese pode perder; KILL total por no-witness/tautologia interrompe o programa para
decisão humana, sem fabricar teoria.

### Onda 4 — precedentes externos direcionados (`research`, condicional mas recomendado)

**Dependência:** lacunas e candidatos congelados da Onda 3; nova initial definition local.

A pesquisa cobre somente owners necessários aos candidatos sobreviventes: composição formal e
interfaces; framing/cognição/deliberação; ensembles e diversidade; ablation e atribuição causal.
Não deve importar uma taxonomia inteira nem procurar novidade como objetivo.

**Gate 4:** cada empréstimo cita owner, declara o job que pode construir e explicita limites de
transferência. `precedent-clean` autoriza apenas `novel-attempt` modesto.

### Onda 5 — matriz de hipóteses e backlog experimental (`research`)

**Dependências:** Ondas 1–4 aceitas; se a Onda 4 for dispensada por decisão de agentes, a justificativa
fica no decision packet.

Designers independentes propõem experimentos mínimos e um risk critic procura falso positivo,
contaminação e custo. O writer prioriza por poder discriminante, viabilidade e reversibilidade.
O backlog deve comparar pelo menos: ablação de representação; lentes distintas versus duplicadas;
topologias e ordem; síntese versus seleção; conjunto versus agente único com informação/orçamento
equivalentes; preservação de resíduo e contribuição marginal.

**Gate 5:** cada item nomeia hipóteses concorrentes, unidade de análise, baseline, observáveis,
confounds, falsificador, invalidações e menor versão executável. Isso é backlog, não pré-registro.

### Ramo E — propostas e runs experimentais (somente por gate)

Abrir apenas se os agentes demonstrarem que uma escolha entre modelos muda o bundle e não pode ser
resolvida por evidência existente.

1. **E-propose (`experiment`):** uma hipótese por dispatch; designer ↔ skeptic; `criterion.md`
   congelado; approver dedicado.
2. **E-run (downstream separado):** runner → adjudicator; criterion read-only; produz resultado bruto
   e SURVIVED/FALSIFIED rederivável.

Um criterion INVALID volta a novo proposal, não é corrigido em lugar. Código necessário usa rota de
code separada; não é contrabandeado para `experiment`.

### Onda 6 — síntese canônica (`research`)

**Dependências:** Gates 1–5 e, quando aberto, Ramo E encerrado.

Dois leitores independentes recomendam o que sobrevive, morre ou deve ser demovido; um writer cria o
bundle; skeptics verificam claims load-bearing; auditor produz matriz de rastreabilidade; approver
dedicado aceita ou devolve.

**Gate 6:** os oito deliverables do milestone estão localizáveis; fatos, inferências e hipóteses
estão rotulados; propostas são separadas de execuções; causalidade e portabilidade não excedem prova.

### Onda 7 — `/review` final persistido (`review`)

**Dependência:** bundle fechado da Onda 6 e decision packet de review produzido por advisers que não
atacam o corpus.

Quatro attackers independentes leem o corpus inteiro, um por lente: fidelity/governance;
definitional/mechanics; ownership/reference integrity; operability/abuse. Um writer sintetiza; ao
menos dois verifiers distintos tentam refutar; um coverage auditor verifica alvo × lente e dispara
o zero-findings red flag; um approver dedicado, sem outra função, aceita.

**Output:** `internal-tools/composition-lab/reviews/<date>-milestone-1/review.md`, e nenhum outro
arquivo nessa pasta.

**Gate 7:** cada finding sobrevivente contém path, quotation, severity e fix de uma linha; findings
refutados desaparecem; todos os alvos recebem KEEP/FIX; coverage está completa. Review fecha
`resolved` mesmo com FIX, pois FIX é deliverable.

### Onda 8 — rework e novo review (condicional)

- KEEP ou somente MINOR: milestone pode fechar após aprovação e closes.
- CRITICAL/MAJOR: agentes convertem change requests em decision packet; novos writers produzem
  bundle `-v2`; nova review ataca o corpus revisado em pasta `-v2`.
- Segunda review com CRITICAL/MAJOR no mesmo fundamento: parar para gate humano. Não declarar
  completion por exaustão de loops.

## Árvore canônica de artefatos

```text
internal-tools/composition-lab/
├── orchestration/milestone-1-strategy/
│   ├── 01-evidence-strategy.md
│   ├── 02-composition-strategy.md
│   ├── 03-governance-strategy.md
│   ├── 04-integrated-program.md
│   └── decision-packets/
│       ├── 01-repository-inventory.md
│       ├── 02-robot-talks.md
│       ├── 03-models-vocabulary.md
│       ├── 04-precedents.md
│       ├── 05-experiment-backlog.md
│       ├── 06-synthesis.md
│       └── 07-final-review.md
├── research/milestone-1/
│   ├── 01-repository-inventory/
│   │   ├── research-initial-definitions.md
│   │   ├── research.md
│   │   └── findings.md
│   ├── 03-models-vocabulary/{research-initial-definitions.md,research.md,findings.md}
│   ├── 04-precedents/{research-initial-definitions.md,research.md,findings.md}
│   ├── 05-experiment-backlog/{research-initial-definitions.md,research.md,findings.md}
│   └── 06-synthesis/{research-initial-definitions.md,research.md,findings.md}
├── robot-talks/<date>-lens-composition-tensions/
│   ├── dialogue.md
│   ├── findings.md
│   └── reports/<NN-concern>.md
├── experiments/milestone-1/<experiment-slug>/
│   ├── experiment-initial-definitions.md
│   ├── criterion.md
│   └── run/<experiment.md,findings.md>       # only if Ramo E opens
└── reviews/<date>-milestone-1/
    └── review.md
```

## Pacote decisório — primeiro dispatch substantivo

### Identidade e precondição

**Nome:** `repository-lens-composition-inventory`

**Tipo:** `research`, corpus interno, read-only.

**Working folder:**
`internal-tools/composition-lab/research/milestone-1/01-repository-inventory/`.

Antes de desenhar e confirmar o dispatch no lifecycle, um bootstrap writer, aconselhado por um
fact-boundary helper, deve criar nessa pasta `research-initial-definitions.md`. Ele deriva somente
contexto, propósito, pergunta refinável, constraints confirmadas, baseline já conhecido e gaps do
README, das definições amplas existentes e deste programa; não inclui métodos, corpus, roles,
topologia, hipóteses, gates ou outputs. Depois, um resolver subagente lê o documento inteiro e
confirma que este pacote continua compatível; o principal apenas apresenta o dispatch final ao gate.

### Pergunta única

> Onde o repositório declara, instancia, executa e preserva perspectivas distinguíveis sobre um alvo
> comum, e que evidência existe de operações que relacionam essas perspectivas sem confundir
> menção, partição, pluralidade, agregação ou encerramento com efeito composicional?

### Corpus a congelar

O corpus manifest deve registrar commit/digest, path e hash e cobrir:

1. `telemetry/agents/subagents-dispatch.yaml`, incluindo aberturas e closes;
2. manifests e propostas em `.codex/workflow-inputs/**` e `.codex/dispatch-proposals/**`, quando
   existentes;
3. skills ativas que prescrevem lenses, concerns, angles ou topologias, especialmente research,
   review, Robot-Talks, experiment e estratégias de subagentes;
4. sessões preservadas em `**/robot-talks/**`;
5. reviews persistidos em `**/review.md`;
6. specs, probes e resultados em `docs/features/agent-provenance-telemetry/**`;
7. outputs referenciados pelo ledger e casos históricos necessários para distinguir mudança de
   schema;
8. `internal-tools/composition-lab/README.md` e suas definições iniciais como limites da claim.

Duplicatas `.agents`/`.codex`/históricas não contam como ocorrências independentes sem proveniência
distinta. Propostas nunca executadas e closes sem outputs entram como controles, não são excluídos.

### Protocolo comum de ocorrência

Cada linha candidata registra: id; alvo/pergunta; data/schema; perspectiva declarada; concern;
angle; role; persona/método; prompt/exclusões; fontes; topologia e ordem; informação vista;
operação relacional; output; traço preservado; passagem à síntese; nível máximo de evidência;
perdas/resíduo; classificação; evidência path:line; confiança e razão.

Classificações mínimas: menção; partição; pluralidade declarada; candidata observada; ambígua;
controle negativo. Níveis: prescrição; instanciação; execução; efeito.

### Perspectivas e owners

O dispatch começa com advisers de forma independentes; seu resolver registra recomendações aceitas
e rejeitadas no input confirmado. Depois:

- **Explorer A — declaração/configuração:** ledger, manifests e prompts; procura como diferenças são
  declaradas e ligadas a objetivos, sem inferir execução.
- **Explorer B — execução/preservação:** outputs, reports, dialogues, handoffs e closes; procura
  traços de interação, before/after, síntese e resíduo, sem inferir causa.
- **Explorer C — normas/mecanismos:** skills, specs e probes; distingue prescrição, mecanismo
  proposto e execução demonstrada.
- **Explorer D — contracasos/drift:** procura partição, diversidade nominal, propostas não executadas,
  agregação sem transformação, schema histórico e dupla contagem.
- **Collector owner:** preserva todos os retornos verbatim em `research.md`.
- **Writer owner:** cruza as quatro perspectivas numa tabela única e escreve `findings.md` sem
  normalizar ambiguidades.
- **Skeptic 1:** gate precedent/ownership interno; localiza owners e provenance.
- **Skeptic 2:** gate non-vacuity; exige testemunha concreta por categoria.
- **Skeptic 3:** gate definitional-soundness; força colapso para role/prompt/view/aggregation quando a
  distinção não se sustenta.
- **Coverage auditor:** verifica manifest, hashes, estratos, controles e citações; não aprova.
- **Final approver dedicado:** não participa de grupo nem escreve; aceita ou devolve o bundle.

Os nomes concretos devem vir de `telemetry/agents/agent-pool.yaml`, sem reuso dentro do dispatch e
sem self-verification. A topologia segue explorers → writer ↔ skeptics, auditor downstream; feedback
é condicional e `loop_cap` recomendado é 2.

### Amostragem e controles

Fazer censo estrutural do ledger. Para inspeção profunda, usar máxima variação determinística por:
review; Robot-Talks; reveal/reavaliação; research; probes/lentes observacionais; e casos inscritos
somente em angle/role/prompt. Inspecionar todos os casos raros de reveal e probes. Nos estratos
numerosos, começar com ao menos três casos variados e ampliar até duas inclusões consecutivas não
criarem nova operação ou falha; chamar isso apenas de saturação do vocabulário da amostra.

Controles obrigatórios:

- agentes divididos apenas por fontes/arquivos;
- instruções nominalmente distintas pedindo o mesmo julgamento;
- agente único usando “lens” em prosa;
- retornos apenas concatenados;
- proposta não executada;
- close sem output que mostre interação.

### Outputs

- `research-initial-definitions.md` — precondição informacional, não output da pesquisa;
- `research.md` — retornos verbatim;
- `findings.md` — manifest do corpus; protocolo; tabela de ocorrências; contagens estruturais;
  controles; tipologia descritiva; mapa prescrição→instanciação→execução→efeito; matriz de verdicts;
  limites, ambiguidades e recomendação evidenciada para o próximo dispatch.

Toda claim load-bearing em `findings.md` cita `research.md` e o source path:line que a sustenta.

### Exclusões

O dispatch não deve:

- definir canonicamente “lente” ou “composição”;
- medir eficácia por frequência de fields ou por `resolved`;
- alegar causalidade sem contrafactual;
- fazer pesquisa externa ampla;
- propor schema, UI, runtime, tool ou migração;
- alterar corpus fonte ou telemetria;
- universalizar de agentes para trabalho, conhecimento ou interfaces;
- tratar discordância como diversidade útil, ou síntese como composição por definição.

### Critério de avanço

Avança quando:

1. todo item tem citação verificável e identidade de ocorrência que evita dupla contagem;
2. corpus e amostra são reproduzíveis;
3. prescrição, instanciação, execução e efeito estão separados;
4. cada estrato tem caso, contracaso ou lacuna explícita;
5. positivos, negativos e ambiguidades sobrevivem à síntese;
6. nenhum efeito é inferido apenas de configuração, fechamento ou frequência;
7. skeptics e auditor completam seus checks e o approver dedicado aceita.

### Stop e rework

- Citação ou corpus faltante: feedback dirigido ao explorer responsável, máximo de dois loops.
- Dupla contagem ou drift histórico não resolvido: rework do manifest antes da síntese.
- Categoria sem testemunha: marcar KILL/no-witness; não fabricar exemplo.
- Categoria que colapsa: marcar KILL/tautological; preservar o negativo tipado.
- Todos os candidatos mortos: fechar research como `resolved`, preservar os negativos e parar o
  programa para gate humano.
- Falha de binding, registry drift ou impossibilidade de close: fail closed; preservar último
  artefato válido e registrar a lacuna no close, sem lançamento órfão.
- Gate não satisfeito após dois loops: fechar com lacuna explícita e pedir decisão humana; não
  avançar silenciosamente para Robot-Talks.

## Riscos ainda não resolvidos

1. **Viabilidade do corpus:** paths históricos podem ter sido movidos ou outputs citados pelo ledger
   podem não existir; o manifest precisa tratar ausência como dado.
2. **Schema drift:** campos atuais podem ser aplicados retroativamente a dispatches antigos.
3. **Dupla contagem:** proposal, manifest, ledger e report podem representar a mesma ocorrência.
4. **Viés de sobrevivência:** outputs persistidos favorecem sessões cuidadas e fechadas.
5. **Independência aparente:** agentes podem ter visto retornos alheios antes do primeiro output.
6. **Autoria do sintetizador:** relações novas podem ser criação do writer, não interação de lentes.
7. **Diversidade nominal:** nomes, roles ou personas distintos podem realizar o mesmo julgamento.
8. **Observabilidade insuficiente:** o repo pode sustentar somente claims de prescrição ou
   instanciação; isso é resultado legítimo, mas limita o modelo.
9. **Conflito de skill em research:** a skill descreve auditor como owner da matriz e também como
   approver natural. Para evitar aprovação por quem fez trabalho, o programa separa coverage auditor
   de final approver dedicado; o lifecycle/registry precisa aceitar essa forma.
10. **Capacidade de agentes:** o limite de concorrência pode exigir execução serial de grupos sem
    alterar sua independência epistemológica.
11. **Human gate de Robot-Talks:** autorização geral do milestone não substitui aprovação da
    estratégia nem disposição de tensões.
12. **Experimento sem runner governado:** a skill de experiment só governa proposta; runs de
    raciocínio e code têm rotas downstream distintas que ainda precisam ser resolvidas caso o Ramo E
    abra.
13. **Review sem transcript:** a cobertura preservada não reconstitui independência dos attackers;
    é custo aceito pelo contrato atual, não algo a corrigir neste milestone.
14. **Portabilidade:** sem replicação entre domínios, qualquer extração para outro lugar permanece
    hipótese.
15. **Terminologia contaminante:** os próprios rótulos provisórios do inventário podem orientar o que
    explorers enxergam; os contracasos e o skeptic de collapse reduzem, mas não eliminam, esse risco.

## Regra final de declaração

O principal só pode declarar o Milestone 1 alcançado quando todos os dispatches governados estiverem
fechados, as disposições humanas obrigatórias existirem, o bundle canônico localizar os oito
deliverables, o approver independente aceitar o `review.md` e não restar CRITICAL/MAJOR pendente.
A declaração lista paths, `exit_reason` e contagem real de agentes e distingue formalização,
pré-registro e validação experimental.
