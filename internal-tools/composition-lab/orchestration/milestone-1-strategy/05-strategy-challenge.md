---
artifact_kind: strategy-challenge
status: proposed
date: 2026-08-13
milestone: "Milestone 1 — Modelo observável da composição de lentes"
scope:
  - 01-evidence-strategy.md
  - 02-composition-strategy.md
  - 03-governance-strategy.md
---

# Challenge independente — estratégias do Milestone 1

## Parecer

As três estratégias têm material aproveitável, mas nenhuma deve ser executada integralmente. A
base mais segura é a disciplina de evidência de `01`, a ordem inventário → Robot-Talks e a pesquisa
externa de `02`, e as fronteiras contratuais/owners de `03`. O programa deve ser reduzido a três
ondas substantivas — inventário interno, precedentes externos e síntese — mais Robot-Talks entre as
duas primeiras e `/review` ao final. Pré-registros e runs experimentais ficam para o Milestone 2.

## Objeções e correções mínimas

### 1. Robot-Talks antes do inventário mistura coleta com confronto — MAJOR

**Parecer atacado:** `03-governance-strategy.md`, “Onda 1 — Robot-Talks sobre tensões do uso real”,
vem antes da “Onda 2 — research: inventário evidenciado”. `01-evidence-strategy.md` e
`02-composition-strategy.md` fazem o contrário; `02`, em “Regra de decisão entre modalidades”, diz
que Robot-Talks é apropriada quando já existem findings de concerns diferentes.

Sem um inventário congelado, os investigadores da Robot-Talks precisam simultaneamente descobrir
casos e alegar contradições entre eles. Isso torna a amostra dependente da lente de cada assento e
permite que a sessão transforme ausência de busca em tensão. O contrato de Robot-Talks não exige
inventário anterior, mas exige tensões evidenciadas; portanto, a ordem de `03` é possível, porém
epistemicamente mais fraca para esta pergunta.

**Correção mínima:** mover o inventário para a primeira onda substantiva. Depois dele, apresentar
ao usuário uma estratégia Robot-Talks derivada dos findings, com pergunta, assumptions, concerns,
exclusions e decomposição rejeitada. A autorização geral do milestone não substitui essa aprovação
específica. A sessão continua autônoma, fora do ledger, e preserva somente `dialogue.md`,
`findings.md` e `reports/` (mais `ring/` se necessário).

### 2. O inventário já chega contaminado por uma teoria de composição — MAJOR

**Pareceres atacados:** `01-evidence-strategy.md`, “Unidade de evidência”, define antes do censo que
uma ocorrência exige duas perspectivas, uma operação relacional e um traço; `02-composition-strategy.md`,
“Hipóteses concorrentes” e “Operações que o inventário precisa distinguir”, fornece L1–L4,
C1–C6, E1–E5 e quinze operações antes de D1. Ambos correm o risco de só encontrar o que seus
próprios codebooks permitem nomear.

O problema não é ter hipóteses concorrentes; é usá-las como filtro de inclusão na primeira leitura.
Casos em que uma lente é temporal, material, coletiva, implícita ou não relacional podem desaparecer
antes de serem classificados como contraexemplos.

**Correção mínima:** tornar D1 bifásico e preservar as duas camadas:

1. extração descritiva sem classificação: alvo, campos literais, agentes, entradas vistas, ordem,
   conexões, outputs, versões e paths/hashes;
2. classificação posterior: menção, pluralidade, partição, operação candidata, execução e efeito,
   sempre mantendo `unclassified` e a justificativa.

Os explorers de extração não recebem L/C/E nem a lista de quinze operações em seus prompts. Dois
classificadores aplicam o codebook posteriormente e o auditor publica concordâncias e divergências;
nenhuma divergência é resolvida apagando a linha bruta.

### 3. Há dispatches demais para o deliverable acordado — MAJOR

**Pareceres atacados:** `01-evidence-strategy.md` propõe D1–D7; `02-composition-strategy.md` adiciona
“vários dispatches `experiment`”, runs e adjudicação; `03-governance-strategy.md` cria cinco ondas,
decision packets para cada uma e helpers recursivos. O milestone pedido termina em inventário,
formalização, hipóteses e backlog de experimentos; ele não exige pré-registrar nem executar probes.

A cerimônia aumenta custo, superfícies de failure/binding e drift entre pastas sem aumentar
necessariamente a independência. Em particular, separar vocabulário, hipóteses e backlog em três
researches repete writer, skeptics, auditor e approver sobre o mesmo corpus.

**Correção mínima:** quatro dispatches governados, no máximo:

- R1 — inventário interno reproduzível;
- R2 — precedentes externos orientados pelas lacunas de R1 + Robot-Talks;
- R3 — modelos concorrentes, vocabulário, ciclo, matriz de hipóteses e backlog;
- R4 — `/review` persistido do bundle fechado.

Robot-Talks permanece uma sessão autônoma entre R1 e R2. Cada onda deixa no próprio `findings.md`
uma recomendação auditável para a forma da próxima; dois advisers podem contestá-la antes da
abertura, sem criar um novo dispatch só para meta-planejamento. Experimentos são backlog, não
dispatches do Milestone 1.

### 4. As precondições de `research` não estão satisfeitas de modo uniforme — CRITICAL

**Pareceres atacados:** `01-evidence-strategy.md`, “Âncoras”, aponta para
`internal-tools/composition-lab/research/research-initial-definitions.md`, mas seus dispatches usam
subpastas diferentes sem initial-definitions locais. `02-composition-strategy.md`, D1, trata a
precondição como condicional: “Se o `working_folder` específico exigir...”. Não é condicional.
`03-governance-strategy.md`, “Fronteiras contratuais” e árvore de artefatos, é o único parecer que
a aplica corretamente.

O contrato de `research` exige `<research-folder>/research-initial-definitions.md` antes de
selecionar roles ou propor o dispatch e exige sua leitura completa.

**Correção mínima:** cada R1–R3 recebe seu próprio `research-initial-definitions.md`, produzido e
lido antes do desenho do dispatch. O arquivo geral pode ser fonte, nunca substituto. Ele registra
contexto, pergunta refinável, baseline e lacunas; não contém hipóteses, método, roles, topologia,
budgets ou findings esperados.

### 5. O plano experimental de `02` excede o milestone e deixa contratos incompletos — MAJOR

**Parecer atacado:** `02-composition-strategy.md`, D4–D5, prescreve vários pré-registros e runs. A
separação proposal/run está correta, mas não há paths nem `experiment-initial-definitions.md` por
working folder; a execução downstream também depende de uma rota de run que a própria skill declara
reservada, e código exige dispatch separado.

**Correção mínima:** não abrir `experiment` neste milestone. R3 entrega apenas protocolos candidatos
com hipótese única, falsificador, controles, unidade de análise, regra de decisão e menor versão
executável, explicitamente rotulados `not preregistered / not run`. O Milestone 2 decide quais
merecem `experiment-initial-definitions.md` e `criterion.md` congelado.

### 6. A pesquisa externa não pode ser opcional — MAJOR

**Parecer atacado:** `01-evidence-strategy.md`, “Expansão prematura”, recomenda precedente externo
“apenas depois de D2” e somente “se uma hipótese específica precisar”. `02` e `03` incluem
precedentes externos, mas `02` mistura o sweep com modelagem e `03` o separa corretamente.

A pergunta é deliberadamente difícil e o usuário pediu pesquisa. Formalizar apenas a linguagem do
repo corre o risco de rebatizar framing, perspective taking, ensembles, group cognition,
deliberação, integração de informação ou efeitos de interação. Precedent-first também é regra da
skill `research` para qualquer claim de novidade.

**Correção mínima:** executar R2 externa depois de R1 e do Human Gate da Robot-Talks, limitada às
lacunas observadas. Cada conceito importado mantém owner, fonte primária, job que pode cumprir,
limites de transferência e use-mode (`build-from-owned`, `already-deployed` ou `novel-attempt`).
Não usar pesquisa externa para recodificar retrospectivamente as linhas brutas de R1.

### 7. Vários critérios de passagem verificam presença, não qualidade — MAJOR

**Pareceres atacados:** `01-evidence-strategy.md` aceita o ciclo quando cobre “pelo menos três
estratos”; `03-governance-strategy.md` aceita R3 quando “os sete conteúdos existem”; os critérios
globais das três estratégias incluem aprovação e ausência de MAJOR/CRITICAL, mas não definem uma
checagem mecânica suficiente da formalização.

Três estratos é um número arbitrário; sete headings podem existir vazios; aprovação é uma decisão,
não evidência de que o modelo discrimina composição de agregação.

**Correção mínima:** o auditor de R3 deve validar uma matriz observável:

- cada termo tem definição operacional, ao menos dois witnesses de famílias distintas, um
  contraexemplo e um collapse-test;
- cada operação/ciclo aponta para occurrence IDs de R1 e informa `prescribed`, `instantiated`,
  `executed`, `effect-observed` ou `unknown`;
- cada hipótese tem suporte, contraevidência, falsificador, medida/unidade e status;
- cada experimento do backlog discrimina ao menos duas hipóteses nomeadas e possui baseline,
  confounds, invalidações e versão mínima;
- toda claim load-bearing liga-se por IDs a uma linha bruta, tensão disposta ou precedente com
  owner;
- desacordos de classificação e resíduos permanecem localizáveis.

O milestone passa quando essa matriz é completa e o `/review` não mantém CRITICAL/MAJOR, não quando
um número predeterminado de categorias aparece.

### 8. Decision packets e arquivos agregados têm ownership ambíguo — MAJOR

**Parecer atacado:** `03-governance-strategy.md` declara “um único owner de cada escrita”, mas a
árvore atribui alguns decision packets a “writer/auditor da onda anterior” e a Onda 1 diz que
“sintetizador e um crítico independente produzem” o packet. No review, writer e coverage auditor
precisam contribuir para o único `review.md`; sem sequência explícita, dois agentes podem editar o
mesmo arquivo compartilhado. `01` e `02` tampouco nomeiam owners por path.

**Correção mínima:** cada path recebe exatamente um filesystem owner no decision packet anterior.
Advisers, skeptics, verifiers e auditor retornam material pelo canal; não editam o arquivo agregado.
Para `review.md`, o coverage auditor é autor semântico da seção Coverage, mas retorna seu payload ao
writer, único editor do arquivo, que o incorpora sem alteração; o approver verifica essa
incorporação. Relatórios paralelos mantêm paths distintos. Rework escreve `-v2`, nunca altera o
corpus congelado.

### 9. O corpus final de review está ora inflado, ora insuficientemente definido — MINOR

**Pareceres atacados:** `01-evidence-strategy.md` manda atacar D1–D6 inteiros; isso pode obrigar cada
attacker a reler retornos verbatim volumosos. `03-governance-strategy.md` define um corpus principal
mais estreito, mas deixa `research.md` e reports apenas como “evidência de apoio”, sem manifestar
quando são load-bearing. `02` lista cinco lentes de ataque, enquanto o contrato canônico limita o
grupo a 2–4 attackers, uma lente por agente.

**Correção mínima:** congelar como target corpus o `README`, os initial-definitions, os
`findings.md` de R1–R3 e o `findings.md` da Robot-Talks após Human Gate. Congelar separadamente um
evidence manifest com todos os returns e fontes citados; verifiers abrem esse material ao checar
claims. Usar quatro attackers sobre o corpus completo: fidelidade/proveniência, colapso
definicional, validade causal/experimental e operabilidade/gaming. Persistir somente `review.md`.

## Sequência recomendada

1. **Integração enxuta da estratégia.** Um único integrador, aconselhado por um challenger, fixa
   paths, owners, gates e o decision packet de R1. Não cria conclusões sobre lentes.
2. **R1 — inventário interno bifásico (`research`).** Initial-definitions local; extração bruta;
   classificação separada; controles negativos; manifest path/hash; divergências preservadas.
3. **Robot-Talks — tensões evidenciadas.** A estratégia deriva de R1 e volta ao usuário para a
   aprovação específica exigida pela skill. Human Gate dispõe cada tensão.
4. **R2 — precedentes externos (`research`).** Busca limitada às lacunas de R1 + tensões dispostas;
   owners e limites de transferência obrigatórios.
5. **R3 — formalização concorrente (`research`).** Constrói vocabulário, ciclo, operações,
   hipóteses e backlog a partir dos artefatos congelados; um auditor aplica a matriz observável.
6. **R4 — `/review` persistido.** Quatro attackers, writer, verifiers, coverage auditor e approver
   dedicado; somente `review.md`. CRITICAL/MAJOR gera R3 `-v2` e nova review; duas reincidências no
   mesmo fundamento levam a gate humano.

Essa sequência satisfaz a exigência de que o agente principal apenas orquestre: a recomendação da
próxima onda vem de subagentes e recebe contestação independente, enquanto a quantidade de
dispatches permanece proporcional ao que o Milestone 1 realmente promete entregar.
