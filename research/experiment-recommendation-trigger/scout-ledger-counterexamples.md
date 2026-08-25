# Scout — contraexemplos no ledger para recomendação de experimento

## Resposta curta

O ledger pode localizar **candidatos para inspeção**, mas não sustenta sozinho a conclusão
“pesquisou, avançou e não construiu”. No corpus observado, contagem de pesquisas, `resolved`,
`parent_dispatch_id`, pasta compartilhada e ausência de `code`/`experiment` falham como gatilhos
isolados. O uso seguro é uma conjunção em duas etapas:

1. o ledger recupera uma sequência possivelmente relacionada;
2. findings e artefatos ligados demonstram que existe uma incerteza empírica decidível, um próximo
   gate experimental explícito e nenhuma construção ou preparação equivalente já em andamento.

A segunda etapa não é opcional. A maior evidência contrária é Assay: quatro pesquisas `resolved` e
nenhum dispatch `code`/`experiment` relacionado no ledger, mas um primeiro build funcional existe e
está versionado. O caso Schema Service acrescenta outra distinção: um pacote de experimento pode já
estar em preparação sem que exista uma linha `experiment`.

## Escopo e método

- Corpus: somente `C:/Users/victo/cyberalchemy-orchestrator`; sem web e sem leitura dos repositórios
  externos apontados por algumas linhas.
- Ledger: `telemetry/agents/subagents-dispatch.yaml`, lido e unido pelo leitor local
  `implementations/server/ledger.py` (`parse_ledger` + `join_rows`), sem mutação.
- Artefatos: somente famílias ligadas por identificador, objetivo ou `working_folder`: Assay,
  Schema Service, interaction-relations, runtime-v2, irreducible-problems, transferências SWI e
  local-global-continuous-discrete.
- Construção: presença atual de arquivos e, quando possível, histórico Git do caminho. Presença
  sem commit demonstra estado atual, mas não autoria nem momento de criação.

O snapshot observado contém 714 linhas brutas, unidas em 368 dispatches. Destes, 58 são
`research`: 46 `resolved`, 6 `error`, 5 abertos e 1 `user_abort`. Há 11 dispatches `code` e **zero
dispatches `experiment`**. Apenas 7/368 dispatches têm `parent_dispatch_id`; entre pesquisas, apenas
1/58. Oito pesquisas apontam para `working_folder` iniciado por `..`, portanto para construção fora
do corpus local.

Essas contagens descrevem este snapshot, não uma propriedade eterna do sistema.

## Casos delimitados

### C1 — Assay: falso positivo comprovado para “sem `code` = não construiu”

O ledger registra quatro pesquisas relacionadas em 2026-07-23 — `assay-readme-framings`,
`assay-first-approach-probe`, `assay-forward-research` e `assay-discovery` — todas fechadas como
`resolved` (`telemetry/agents/subagents-dispatch.yaml:884-1006`). A busca por `assay` e
`document-information-estimator` no ledger não encontrou dispatch `code` ou `experiment`.

Porém, `internal-tools/document-information-estimator/s0/assay_s0.py` existe, e o README o declara
“First functional build of Assay”, com execução e acceptance test concretos
(`internal-tools/document-information-estimator/s0/README.md:1-38`). O commit
`51008dfc8d5d10dd9cc88aa72016d6c80fedb005`, de 2026-07-24, adicionou o script, seus documentos e os
artefatos de pesquisa. Logo, a ausência de `code` no ledger não demonstra ausência de build.

Ao mesmo tempo, este caso sustenta uma pista semântica melhor: os findings disseram `GO`,
`build-from-owned` e “S0 can ship ... today”, mantendo obrigações empíricas para rungs posteriores
(`internal-tools/document-information-estimator/discovery/research/forward-research/findings.md:9-47`).
Foi o conteúdo do resultado — não o `resolved` — que tornou a construção seguinte defensável.

### C2 — Schema Service: pesquisa avançou e um experimento já está sendo preparado

O ledger contém três pesquisas `resolved` da mesma iniciativa: prior-art, precedentes de famílias de
artefatos e regra de staging experimental
(`telemetry/agents/subagents-dispatch.yaml:6343-6461`). Não há linha `experiment` no ledger.

Os findings dão um próximo movimento empírico preciso: construir dois pacotes de conformidade,
executando primeiro o documental, e proíbem um runtime universal antes das provas
(`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:23-27,115-123`).
Isso é evidência a favor de **oferecer** um experimento.

Mas o estado atual já contém `projects/schema-service/experimentation-plans/artifact-types-v0/`.
O primeiro pacote tem `status: preparing`, manifesto e candidate types; ainda não tem critério,
fixtures, run ou veredito, e nomeia como próxima ação um dispatch `experiment`
(`projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md:1-32`).
Esses arquivos estão atualmente não rastreados pelo Git. Portanto:

- “nenhum `experiment` no ledger” não significa “ninguém começou a preparar o experimento”;
- presença de uma pasta `experiments/` também não significa que o experimento rodou;
- uma recomendação útil teria de reconhecer a preparação existente e sugerir o gate exato ainda
  ausente (`criterion.md`), não repetir genericamente “faça um experimento”.

### C3 — interaction-relations: duas pesquisas resolvidas, mas ainda é uma base candidata

Exploração e síntese aparecem como dois dispatches `research` `resolved`
(`telemetry/agents/subagents-dispatch.yaml:6356-6395`). Os findings têm `status: draft`, dizem
explicitamente que não autorizam implementação e listam áreas ainda não resolvidas
(`docs/features/agents-communication-infra/research/interaction-relations/findings.md:351-372`).
Eles também materializam hipóteses P/N/D para os próximos gates
(`docs/features/agents-communication-infra/research/interaction-relations/findings.md:380-410`).

Este é um candidato plausível para desenho de validação, mas somente porque as hipóteses e os
collapse-tests são explícitos. A mesma sequência numérica sem esses artefatos não sustentaria a
recomendação. O status `draft` e a frase de não autorização devem impedir que `resolved` seja lido
como “pronto para implementar”.

### C4 — runtime-v2: repetição causada por retry; o próximo gate é review, não experimento

Há dois dispatches de pesquisa com o mesmo objetivo e pasta: o primeiro fechou `error` sem agentes;
o retry fechou `resolved` com três agentes (`telemetry/agents/subagents-dispatch.yaml:5288-5317`).
Contar “duas pesquisas” inflaria artificialmente o avanço.

Os findings separam capacidades já implantadas, lacunas e itens `KILL`/`BLOCK`; para o
skill-to-DAG compiler, registram `BLOCK — proposal-only`. A ação prescrita é passar os artefatos pelo
gate canônico de `review` antes de uma discovery de arquitetura
(`docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/findings.md:52-67,91-98`).
Um recomendador baseado só em repetição + `resolved` sugeriria o tipo errado de próximo passo.

### C5 — irreducible-problems: quatro pesquisas não significam quatro avanços

Quatro dispatches compartilham objetivo e pasta: três fecharam `error`; o quarto, `user_abort`
(`telemetry/agents/subagents-dispatch.yaml:5677-5755`). O close do quarto explica que os três scouts
terminaram, mas `close-session` ocorreu antes de persistir/sintetizar tudo. Os artefatos hoje existem,
porém seus findings permanecem `status: exploratory`, não encontraram um único problema fundamental
defensável e exigem síntese e skeptics como próximo estágio
(`research/repository-irreducible-problem-inventory/stages/exploration/findings.md:1-22,45-55`).

Este caso refuta três inferências: número de tentativas não mede avanço; `user_abort` não prova
fracasso epistemológico; e artefato recuperado depois não transforma retroativamente o close em
`resolved`. Também é o único sinal semelhante a uma decisão humana de interrupção encontrado neste
recorte, mas ele registra encerramento da sessão, não recusa de uma sugestão de experimento.

### C6 — transferências SWI: ausência local de construção é desconhecida

Cinco pesquisas `resolved` de transferência apontam para cinco pastas sob
`../subagent-work-infrastructure/` (`telemetry/agents/subagents-dispatch.yaml:5790-5875`). Dentro da
fronteira autorizada não é possível verificar seus outputs nem eventual construção no repositório
alvo. Logo, “não encontrei build neste repo” significa **não observável**, não “não construiu”. Todo
`working_folder` externo deve suspender esse componente do gatilho ou exigir evidência do repo-alvo.

### C7 — local-global: falso negativo para limiar de “várias pesquisas”

Há apenas um dispatch de pesquisa `resolved`
(`telemetry/agents/subagents-dispatch.yaml:6230-6242`), mas os findings nomeiam diretamente o
primeiro experimento prático e seu efeito mensurável
(`research/local-global-continuous-discrete/findings.md:41-55`). Um limiar de duas ou três pesquisas
não o sinalizaria, embora o conteúdo tenha mais prontidão experimental que vários casos repetidos.

### C8 — verdicts mistos não podem virar um único escore de “avanço”

Os findings de precedentes do Schema Service matam quatro alegações de witness completo (`KILL`) e
mantêm uma mecânica como `GO condicionado`
(`projects/schema-service/research/concrete-artifact-family-precedents/findings.md:29-39`). Os
findings de runtime-v2 combinam `GO`, `KILL` e `BLOCK` no mesmo documento. “Findings existe” ou
“contém GO” é insuficiente: o recomendador precisa vincular o experimento a um candidato/veredito
específico, preservando condições e negativos tipados.

## Observabilidade de sugestões recusadas

O ledger não possui, no snapshot examinado, um campo estruturado para `suggestion_offered`,
`accepted`, `declined`, razão da recusa ou snooze. `feedback_prompts` mistura correções de reviewers,
diagnósticos de runtime e decisões do approver; não é um log confiável de resposta do usuário.
Consequentemente, “não repetir uma sugestão já recusada” não é calculável pelo ledger atual. A
ausência de registro não deve ser interpretada como ausência de recusa.

## Tabela orientada a confusão

| proxy | supporting cases | countercases | safe use | unsafe inference |
|---|---|---|---|---|
| `>= 2` pesquisas | Assay; interaction-relations; Schema Service | runtime-v2 e irreducible contam retries/falhas; local-global tem uma pesquisa e experimento explícito | Recuperar famílias candidatas depois de deduplicar retries e provar coerência temática | “Quantidade = avanço” ou “uma pesquisa nunca basta” |
| mesmo `working_folder` | runtime-v2 e irreducible identificam famílias reais | Assay usa caminhos históricos divergentes; Schema Service usa subpastas; SWI aponta para fora do repo | Evidência corroborativa, normalizada e combinada com objetivo/artefatos | Usar igualdade exata como identidade ou tratar caminho externo como inspecionado |
| `parent_dispatch_id` | gapclose de Kahneman e poucos follow-ons têm lineage explícita | só 1/58 pesquisas e 7/368 dispatches têm o campo; Assay e Schema Service não o usam | Sinal forte quando presente | Ausência = trabalhos não relacionados; requisito obrigatório de agrupamento |
| close `resolved` | Assay e Schema Service produziram resultados utilizáveis | runtime-v2 `resolved` pede review; interaction-relations continua draft; o label não contém avanço semântico | Confirmar término operacional antes de ler o resultado | “A hipótese avançou”, “está pronto” ou “o próximo passo é experimento” |
| ausência de `code` | Pode indicar que nenhum build governado foi registrado | Assay tem build funcional versionado sem linha `code`; construção manual pode existir | Pergunta para busca de artefatos e histórico | “Não construiu” |
| ausência de `experiment` | Nenhum caso no snapshot possui linha desse tipo | O ledger inteiro tem zero linhas `experiment`; Schema Service já prepara pacote experimental | Detectar somente que nenhuma execução desse tipo foi registrada neste ledger | Usar como variável discriminante ou negar preparação/run externo |
| findings presentes | Todos os casos aprofundados têm decisão mais rica que o close | irreducible é exploratório; interaction-relations é draft; runtime-v2 manda review | Abrir o artefato e extrair standing, candidato, condição e próximo gate | “Findings = conclusão favorável” |
| `GO` / `build-from-owned` | Assay e parte do Schema Service dão direção acionável | Documentos misturam `GO`, `KILL`, `BLOCK` e condições | Vincular ao candidato exato e carregar suas condições | Colapsar o documento num único sentimento positivo |
| próximo experimento explícito | local-global nomeia probe mensurável; Schema Service nomeia pacote e gate | runtime-v2 exige review; irreducible exige síntese/skeptic | Melhor sinal disponível, desde que haja decisão, falsificador e owner | Inferir experimento apenas de linguagem como “next” ou “build” |
| presença de artefato | Assay prova build; pacote Schema prova preparação | Uma pasta `experiments/` pode estar apenas `preparing`; findings não são implementação | Classificar artefato por conteúdo/status e, se necessário, Git | Contagem de arquivos = construção concluída |
| tempo desde a pesquisa | Pode ajudar a ordenar inspeção | open work, trabalho deliberadamente fundacional e cross-repo tornam idade ambígua | Critério de prioridade depois dos gates semânticos | “Ficou velho = está parado” |

## Limite seguro sugerido por estes casos

Uma recomendação automática só deveria ser **elegível para oferta**, não disparada como conclusão,
quando todas as condições abaixo forem demonstradas:

1. uma família coerente foi reconstruída por evidência positiva — lineage explícita ou combinação de
   objetivo, artefatos e pasta — com retries colapsados;
2. não há pesquisa aberta, erro ainda não recuperado, `user_abort` pendente ou gate anterior exigido;
3. findings identificam um candidato específico com standing favorável/condicionado e uma incerteza
   que só evidência empírica resolve;
4. existe uma hipótese ou critério falsificável, decisão que o resultado muda e próximo gate
   experimental explícito ou reconstruível sem inventar autoridade;
5. uma busca nos artefatos e no histórico não encontra build, run ou pacote equivalente já ativo; e
6. o escopo de construção é observável — ou a recomendação declara honestamente que o repo externo
   não foi verificado.

Mesmo essa conjunção não permite inferir “a pessoa não construiu”; permite apenas dizer: “há uma
incerteza empírica madura e não encontrei, no escopo observado, uma validação equivalente; quer que
eu proponha o menor experimento?”. Para suportar abstinência após recusa, o ledger precisaria de um
evento estruturado separado para oferta, resposta, razão e validade temporal da decisão.
