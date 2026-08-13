---
artifact_kind: milestone-evidence-strategy
status: proposed
milestone: 1
last_updated: 2026-08-13
---

# Evidence strategy — Milestone 1: modelo observável da composição de lentes

## Decisão recomendada

Executar o milestone como uma sequência de dispatches dependentes, não como uma única varredura. O
primeiro resultado deve ser um inventário estratificado do que o repositório **declara, planeja,
executa e preserva** como uso de lentes. Só depois esse inventário pode sustentar vocabulário,
modelo do ciclo, hipóteses e experimentos.

Cada dispatch deve começar com assentos independentes que ajudem a decidir a forma do trabalho
downstream. O orquestrador não interpreta o corpus, escreve sínteses, escolhe hipóteses nem arbitra
findings; apenas confirma, lança, encaminha outputs e fecha. A decisão substantiva de cada etapa
fica registrada no output dos próprios subagentes.

O milestone não deve alegar causalidade. O repositório já contém mecanismos desenhados para lentes,
mas, salvo execução preservada com controles, eles são precedentes operacionais ou prescrições, não
prova de que a composição melhorou um resultado.

## Âncoras e limites já confirmados

- O laboratório existe para tornar composição observável e investigável, sem escolher uma teoria ou
  arquitetura prematuramente (`internal-tools/composition-lab/README.md`).
- As definições iniciais exigidas pela skill de pesquisa existem, e registram como lacuna a ausência
  de vocabulário observacional e de base empírica para atribuir resultados à composição
  (`internal-tools/composition-lab/research/research-initial-definitions.md`).
- O ledger é append-only e guarda, entre outros campos, `groups`, `connections`, `role`, `angle`,
  `initial_prompt` e ocorrências de `robot_talks` (`telemetry/agents/subagents-dispatch.yaml:1-4`).
  Esses campos evidenciam desenho declarado, não necessariamente comportamento ou efeito.
- Robot-Talks manda decompor por concerns, com perguntas não sobrepostas, e requer evidência nos
  relatórios (`.agents/skills/robot-talks/SKILL.md:42-55`).
- Review manda atacantes lerem o corpus inteiro, diferenciados por uma lente cada
  (`.agents/skills/review/SKILL.md:66-76`). Isso é diferente de particionar o corpus.
- O Reference Scout descreve um mecanismo mais forte: grupos independentes produzem `v1`, recebem a
  lente alheia e produzem `v2` com delta preservado
  (`docs/features/agent-provenance-telemetry/probes/reference-scout-tool.md:113-127`). É uma
  especificação/proposta até que haja evidência de execução correspondente.
- APT-P007 preregistra uma lente projetada sobre emissões seladas e compara organizações com
  informação equivalente (`docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md`).
  Isso fornece um precedente experimental, não prova de que toda composição de agentes funciona da
  mesma forma.

## Unidade de evidência

Não contar a palavra “lens/lente” como ocorrência. Uma **ocorrência candidata de composição de
lentes** exige:

1. um alvo ou pergunta comum identificável;
2. duas ou mais perspectivas distinguíveis;
3. a diferença pretendida entre elas registrada antes ou durante o trabalho;
4. uma operação que relacione as contribuições — síntese, confronto, revelação, reavaliação,
   verificação, projeção ou seleção;
5. algum traço preservado do resultado da operação.

Se 1–3 existem sem 4–5, classificar como **pluralidade de lentes declarada**, não composição
observada. Se só existe linguagem de lente, classificar como **menção**. Se há agentes em paralelo
divididos apenas por arquivos ou territórios sem perspectiva comum, classificar como **partição de
trabalho** até aparecer evidência contrária.

Para cada ocorrência, registrar quatro níveis separadamente:

| nível | pergunta | evidência aceitável |
|---|---|---|
| prescrição | o mecanismo é recomendado? | skill, spec, proposal |
| instanciação | ele foi configurado para este caso? | dispatch/proposal/prompt/connections congelados |
| execução | as etapas realmente aconteceram? | relatórios, handoffs, versões, receipts, close record |
| efeito | o que mudou por causa da relação entre lentes? | delta atribuível, controle/contrafactual, avaliação independente |

Uma claim nunca sobe de nível por inferência. `close: resolved` demonstra encerramento do dispatch,
não utilidade da composição.

## Corpus e amostragem

### Censo estrutural

Fazer censo de todas as linhas de abertura e fechamento em
`telemetry/agents/subagents-dispatch.yaml`, extraindo sem interpretação: tipo, grupos, agentes,
`role`, `angle`, `initial_prompt`, `anti_bias`, `robot_talks`, connections, loops, approver,
working folder, close state e outputs referenciados. Registrar contagens reproduzíveis e o commit ou
digest do corpus. Não usar contagens como medida de eficácia.

Complementar o censo com índices de:

- sessões Robot-Talks (`**/robot-talks/**/{dialogue,findings,reports}*`);
- propostas/manifests de dispatch (`.codex/workflow-inputs/**`, `.codex/dispatch-proposals/**`);
- skills que prescrevem lenses/concerns/topologias (`.agents/skills/**/SKILL.md` e equivalentes
  ativos);
- resultados e contratos de observação em `docs/features/agent-provenance-telemetry/**`;
- reviews persistidos em `**/review.md`.

Congelar a lista de paths e hashes usada em cada dispatch. Arquivos históricos e duplicatas
`.claude`/`.codex` não devem ser contados como ocorrências independentes sem provar proveniência
distinta.

### Estratos para inspeção profunda

1. **Mesmo alvo, ataque por lentes distintas** — review.
2. **Concerns distintos, síntese de tensões** — Robot-Talks.
3. **Independência, revelação e reavaliação** — `v1 → lens reveal → v2`.
4. **Explorers diferenciados por perspectiva + síntese/gates** — research.
5. **Lente observacional declarada/versionada** — Probe/APT.
6. **Perspectivas inscritas apenas em `angle`, role ou prompt** — dispatches legados.

Inspecionar todos os casos raros dos estratos 3 e 5. Nos estratos numerosos, usar amostra
determinística de máxima variação: no mínimo três casos por estrato, distribuídos por data, tipo de
dispatch, topologia e estado de fechamento, mais todo outlier que contradiga a tipologia. Aumentar a
amostra até que duas inclusões consecutivas não criem nova operação nem novo modo de falha; chamar
isso de **saturação do vocabulário desta amostra**, nunca saturação do repositório ou do fenômeno.

### Controles negativos obrigatórios

- dois agentes divididos apenas por arquivos/fontes;
- duas instruções nominalmente diferentes que pedem o mesmo julgamento;
- um único agente usando “lens” em prosa;
- múltiplos retornos agregados sem síntese, confronto ou delta preservado;
- uma proposta nunca executada;
- uma execução fechada sem outputs capazes de mostrar interação.

Os controles servem para impedir que “multiagente”, “diversidade” ou “síntese” virem sinônimos
automáticos de composição de lentes.

## Sequência de dispatches

Cada dispatch abaixo tem uma primeira camada de exploradores/estrategistas independentes. O writer
downstream decide a forma final a partir deles; o parent não substitui essa decisão. Para pesquisa
com `n >= 2`, preservar retornos em `research.md` e síntese citada em `findings.md`, conforme a skill
`research`.

### D1 — Corpus protocol e inventário reproduzível

**Pergunta:** onde o repositório instancia perspectivas distinguíveis e que evidência existe de sua
relação?

**Forma:** três explorers independentes: (a) ledger/manifests, (b) artifacts/outputs preservados,
(c) normas e contratos; um writer cruza os três; skeptics separados aplicam
definitional-soundness e non-vacuity; um auditor verifica cobertura e hashes.

**Outputs:**

- `research/milestone-1/01-inventory/research.md`
- `research/milestone-1/01-inventory/findings.md`
- dentro de `findings.md`: protocolo, manifest do corpus, tabela de ocorrências, controles negativos,
  limites e lacunas.

**Passa quando:** toda linha da tabela aponta para evidência; prescrição/instanciação/execução/efeito
estão separados; amostragem é reproduzível; cada estrato tem caso e contracaso; zero claim de efeito
se apoia apenas em configuração.

### D2 — Vocabulário provisório e fronteiras

**Entrada congelada:** D1.

**Pergunta:** quais distinções são necessárias para descrever os casos sem renomear `concern`,
`angle`, `role`, persona, prompt, partição ou agregação?

**Forma:** explorers propõem vocabulários concorrentes a partir do mesmo inventário; writer produz
uma tabela de termos; skeptics separados testam non-vacuity, definitional-soundness e precedent
interno. Um termo só sobrevive com dois testemunhos positivos de estratos diferentes e um
contraexemplo discriminante. “Precedente encontrado” vira `build-from-owned` ou
`already-deployed`, não KILL.

**Outputs:** `research/milestone-1/02-vocabulary/{research.md,findings.md}`.

**Passa quando:** cada termo tem definição operacional, não-exemplo, evidência, vizinho conceitual,
teste de colapso e status (`provisional`, `alias`, `rejected`, `unknown`). Nenhuma definição depende
de “melhor resultado” ainda não medido.

### D3 — Ciclo e operações composicionais

**Entrada congelada:** D1–D2.

**Pergunta:** que operações realmente conectam lentes, e o que se perde ou transforma em cada uma?

**Forma:** Robot-Talks porque a questão atravessa representação, dinâmica e preservação. Concerns
não sobrepostos: (1) formação/atribuição da lente; (2) topologia e ordem de interação; (3)
transformação/delta; (4) síntese, resíduo e decisão. A sessão deve preservar `dialogue.md`, reports e
`findings.md` sob `robot-talks/2026-08-13-lens-composition-cycle/`. Um sintetizador posterior, em
dispatch de research, converte apenas tensões validadas e casos evidenciados em modelo provisório.

**Passa quando:** o ciclo mapeia pelo menos três estratos, explicita estados/entradas/saídas e modos
de falha, preserva divergência e perdas, e marca quais arestas são apenas prescritas. O Human Gate
dispõe cada tensão antes de ela entrar no modelo.

### D4 — Hipóteses concorrentes e matriz de falsificação

**Entrada congelada:** D1–D3.

**Pergunta:** quais explicações concorrentes cabem nos casos e que observação as separaria?

**Forma:** explorers formulam hipóteses concorrentes, nunca um modelo único; writer produz matriz;
skeptics distintos atacam precedente, não-vacuidade e solidez definicional. Cada hipótese carrega
seu collapse-test na mesma linha.

Hipóteses mínimas a admitir como concorrentes, sem presumir que sobrevivam:

- o ganho vem da cobertura independente, não da composição;
- o ganho vem da operação relacional (reveal/confronto/síntese), não só das partes;
- o sintetizador seleciona a melhor contribuição, sem produzir efeito composicional;
- diversidade nominal de prompts não produz diferença epistemicamente material;
- ordem e informação disponível mudam o resultado;
- preservar resíduo/divergência aumenta auditabilidade, não necessariamente qualidade da decisão.

**Outputs:** `research/milestone-1/04-hypotheses/{research.md,findings.md}`, incluindo matriz
`hipótese → suporte → contraevidência → falsificador → medida → status`.

**Passa quando:** toda hipótese pode perder; explicações rivais compartilham pelo menos um teste
discriminante; “não há evidência” permanece `unknown`, não vira refutação.

### D5 — Backlog de experimentos discriminantes

**Entrada congelada:** matriz D4.

**Pergunta:** qual menor conjunto de experimentos reduz mais incerteza sobre as hipóteses?

**Forma:** dois designers experimentais independentes propõem controles; um terceiro estima riscos
de contaminação/custo; writer prioriza por ganho de informação, viabilidade e reversibilidade;
skeptic tenta construir falso positivo em cada protocolo. Este dispatch desenha, não executa, os
experimentos.

Backlog mínimo a avaliar:

1. ablação: mesmas partes com e sem operação de composição;
2. complementaridade: lenses distintas versus duplicadas/parafraseadas;
3. ordem: isolamento, compartilhamento precoce e reveal tardio `v1→v2`;
4. síntese: agregação, seleção e síntese com proveniência/resíduo;
5. atribuição: leave-one-lens-out e troca cega de labels/personas;
6. portabilidade: repetir protocolo em tarefas de pesquisa, review e design;
7. custo: qualidade verificável por token, tempo e número de falsos positivos.

Cada protocolo deve congelar tarefa, corpus, modelo/configuração, repetições, randomização, avaliador
cego, baseline de informação equivalente, invalidações e regra de decisão. Métricas candidatas:
findings únicos verificados, cobertura, contradições descobertas, falsos positivos, delta `v1→v2`,
retenção de proveniência/resíduo, qualidade cega da decisão e custo. Métrica sem rubric e unidade de
análise é rejeitada.

**Outputs:** `research/milestone-1/05-experiment-backlog/{research.md,findings.md}`.

**Passa quando:** cada experimento discrimina hipóteses nomeadas, tem baseline equivalente,
falsificador, invalidações e menor versão executável; a prioridade não depende de preferência
arquitetural.

### D6 — Síntese do milestone

**Entrada congelada:** todos os outputs aceitos de D1–D5 e a disposição humana de D3.

**Forma:** dois leitores independentes propõem o que sobrevive e o que deve ser demovido; um writer
produz a síntese; skeptics verificam cada claim load-bearing contra os outputs; auditor constrói a
matriz de rastreabilidade.

**Outputs:** `research/milestone-1/06-synthesis/{research.md,findings.md}`. `findings.md` deve conter:
inventário resumido, vocabulário, ciclo, operações/topologias, matriz de hipóteses, backlog
priorizado, desconhecidos, claims rejeitadas e condições para o Milestone 2.

**Passa quando:** cada claim aponta para evidência anterior; fatos, inferências e hipóteses estão
rotulados; nenhuma frequência amostral é generalizada para eficácia; propostas são separadas de
execuções; portabilidade é uma hipótese, não conclusão.

### D7 — `/review` final e loop de correção

Executar review somente depois de D6 existir. O corpus-alvo completo é D1–D6, manifestado por
path/hash. Quatro attackers independentes leem o corpus inteiro, cada qual por uma lente:

1. fidelidade/proveniência — claims versus evidência citada;
2. solidez definicional — colapsos, circularidade e fronteiras falsas;
3. validade causal/experimental — baselines, confundidores e falsificadores;
4. operabilidade/gaming — se o protocolo pode ser cumprido na letra sem produzir evidência útil.

Um writer sintetiza; pelo menos dois verifiers refutam findings contra os artefatos; um coverage
auditor confirma alvo × lente e dispara o zero-findings red flag; um agente separado, sem outro
trabalho, é `final_approver`. Não usar o parent como approver efetivo, pois ele coordenou a cadeia e
não deve autocertificá-la.

Persistir somente
`research/milestone-1/07-review/review.md`, conforme o contrato excepcional da skill `review`.
Findings refutados não entram. Cada finding sobrevivente cita e quota o artefato atacado.

Se houver CRITICAL ou MAJOR, o verdict é FIX: lançar dispatch de correção por subagentes, preservar
as versões anteriores, e repetir o review sobre o corpus revisado. Limite inicial: duas rodadas de
correção; não declarar o milestone completo por exaustão do limite. Se continuar FIX, registrar
milestone não atingido e a lacuna exata.

## Critério global de passagem

O Milestone 1 está atingido somente quando:

1. D1–D6 passam seus gates e têm corpus/hash/linhagem preservados;
2. o inventário distingue menção, pluralidade, instanciação, execução e efeito;
3. o vocabulário possui contraexemplos e testes de colapso;
4. ciclo e operações cobrem casos reais sem alegar mecanismo universal;
5. toda hipótese possui falsificador e status epistêmico;
6. o backlog contém experimentos controlados e priorizados;
7. o `/review` final é aceito sem CRITICAL/MAJOR sobrevivente;
8. a síntese diz explicitamente o que sobreviveu, morreu e permanece desconhecido.

## Prevenção de overclaim

- “Usado no repo” exige instanciação; “executado” exige output/receipt; “funcionou” exige critério e
  resultado; “causou” exige contrafactual ou desenho equivalente.
- Frequência de `angle`, `robot_talks` ou `zig-zag` mede prevalência declarada, não valor.
- Relatório de síntese não prova que as lentes interagiram; procurar delta, desafio/resposta ou
  atribuição explícita.
- Discordância não é automaticamente diversidade útil; consenso não é automaticamente cobertura.
- Persona, role, concern, angle e prompt podem coincidir em um caso, mas não devem ser definidos como
  sinônimos sem teste.
- “Emergente” fica restrito à definição e ao protocolo do artefato que o usa; não generalizar APT-P007
  para equipes ou conhecimento.
- Ausência no corpus congelado é “não observado neste corpus”, nunca “não existe”.
- Portabilidade para outro lugar só é claim depois de replicação entre domínios; neste milestone ela
  pode aparecer apenas como hipótese e requisito experimental.

## Riscos de execução a vigiar

- **Viés de sobrevivência:** outputs persistidos tendem a mostrar casos bem cuidados; incluir closes
  incompletos, propostas não executadas e controles negativos.
- **Dupla contagem:** proposal, workflow manifest, ledger e report podem representar a mesma
  ocorrência.
- **Drift histórico:** schema e skills mudaram; datar cada mecanismo e não aplicar regra atual
  retroativamente.
- **Vazamento entre lenses:** agentes que veem retornos alheios antes de `v1` não demonstram
  independência.
- **Autoria do sintetizador:** resultado conjunto pode ser criação do writer; preservar contribuições,
  deltas e resíduos para testar isso.
- **Reviewer circular:** atacante nunca verifica a própria finding; approver dedicado não acumula
  outro papel.
- **Expansão prematura:** pesquisa externa ampla antes do inventário tende a impor taxonomia alheia.
  Fazer precedent externo apenas depois de D2, em dispatch separado, se uma hipótese específica
  precisar de owner fora do repo.

## Próxima decisão de orquestração

Lançar D1. Não lançar D2–D7 em paralelo: cada um deve receber outputs congelados do anterior, e os
assentos iniciais de cada dispatch devem recomendar, com evidência, o recorte downstream. A única
paralelização segura é interna a cada grupo independente.
