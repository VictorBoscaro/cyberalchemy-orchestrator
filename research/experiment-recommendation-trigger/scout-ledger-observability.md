# Scout — observabilidade do ledger para recomendar experimento

## Resposta curta

O ledger atual pode localizar **candidatos para inspeção**, mas não sustenta sozinho uma recomendação de experimento. Ele observa que dispatches de pesquisa foram declarados, quando abriram e fecharam, seu resultado operacional, a pasta de trabalho declarada e, raramente, uma relação parental explícita. Ele não registra o avanço epistemológico, as alegações que sobreviveram, uma decisão ainda aberta, a inexistência de construção nem a prontidão de uma hipótese falsificável.

Portanto, um gatilho responsável precisa de duas etapas:

1. o ledger seleciona uma sequência candidata, com confiança explicitamente limitada;
2. um leitor de artefatos e evidência de construção confirma o estado epistemológico antes de sugerir qualquer experimento.

Collapse-test da conclusão: se houver no schema ou nas APIs correntes um campo tipado e validado que ligue uma sequência de pesquisas a seus resultados epistemológicos, decisão bloqueada e evidência positiva de construção, esta conclusão precisa ser refeita. A inspeção abaixo não encontrou esse campo.

## Escopo e base examinada

Corpus limitado a `cyberalchemy-orchestrator`, sem web e sem mutação de fonte ou ledger. Foram confrontados:

- contrato e mecânica de escrita: `.codex/skills/register-dispatch/SKILL.md`, `.codex/skills/register-dispatch/append-dispatch.cjs`;
- registry vigente: `implementations/contracts/dispatch-type-registry.v1.json`;
- leitor e APIs: `implementations/server/ledger.py`, `implementations/server/main.py`, `implementations/server/control_center/sources.py`;
- convenções de artefato: `.codex/skills/research/SKILL.md`, `.codex/skills/experiment/SKILL.md`, `.codex/skills/domainspec-implement/SKILL.md`;
- ledger real: `telemetry/agents/subagents-dispatch.yaml`, snapshot local lido em 2026-08-18/19 UTC;
- amostra de oito openings: dois dispatches Kahneman–Thaler, quatro tentativas do inventário de problemas irredutíveis e duas etapas de typed-interaction.

No snapshot havia 366 opening rows e 348 close rows: 58 `research`, 11 `code`, 251 `review`, 46 `others` históricos e nenhum `experiment`. Apenas sete openings tinham `parent_dispatch_id`. Esses são fatos do snapshot, não garantias do contrato para outros repositórios ou datas.

## O que é realmente registrado

### Campos brutos

O registry vigente declara schema `0.6.4` e tipos live `research`, `code`, `review` e `experiment` (`implementations/contracts/dispatch-type-registry.v1.json:3`, `:15`, `:25`, `:65`). O appender aceita, em uma opening row:

- identidade e tipo: `dispatch_id`, `schema_version`, `dispatch_type`;
- intenção declarada: `goal`, `context`;
- plano: `max_loops`, `final_approver`, `groups`, `connections` e configuração anti-bias;
- vínculo e destino opcionais: `parent_dispatch_id`, `working_folder`, `output_mode`;
- para `code`, o `code_contract` pré-execução;
- `created` e `invoked_by`, estampados/resolvidos durante o append.

Isso é confirmado pelo conjunto fechado de chaves em `.codex/skills/register-dispatch/append-dispatch.cjs:146-159` e pela serialização efetiva em `:665-684`. `topic_slug` e `session`, que poderiam auxiliar agrupamento, são chaves legadas rejeitadas (`:163-169`).

A close row contém somente `close_of`, `closed`, `invoked_by`, `exit_reason`, `agents_spawned` e, opcionalmente, `feedback_prompts` (`append-dispatch.cjs:499-524`, `:646-654`). Não há campo de resultado epistemológico, artefato entregue, decisão, claim, próxima ação ou diff construído.

### Derivações seguras do leitor

O leitor:

- casa opening e close exclusivamente por igualdade `dispatch_id == close_of`;
- deriva `_state = open|closed`, `_legacy`, `_live` e `_agent_count`;
- mantém orphan closes visíveis;
- deriva o dia por `created`, depois `_close.closed`, depois prefixo do id.

Essas regras estão em `implementations/server/ledger.py:163-221` e `:497-525`. Assim, são computáveis com boa confiança:

- existência de opening/close e estado operacional;
- duração aproximada `closed - created`, quando ambos são timestamps válidos;
- contagens por tipo, dia, papel e topologia declarada;
- parentage apenas quando `parent_dispatch_id` está presente;
- co-localização textual por `working_folder` exato.

Não é seguro converter co-localização, proximidade temporal ou similaridade de `goal/context` em “mesma linha de investigação” sem assumir uma heurística. O próprio Control Center diz que normaliza linhas “without inventing parentage” e só cria uma aresta quando encontra `parent_dispatch_id` (`implementations/server/control_center/sources.py:105-160`).

### O que as APIs expõem

- `/api/dispatch/{repo}/{id}` devolve a linha completa já unida ao close (`implementations/server/main.py:156-171`).
- `/api/snapshot` devolve apenas a janela recente configurada, preservando os campos mas truncando prompts (`main.py:139-153`; `ledger.py:432-463`).
- `/api/repo/{repo}` lista todo o histórico em forma `slim` (`main.py:259-303`). Essa forma inclui tipo, data, pasta, estado e resumo do close, mas omite `context`, `parent_dispatch_id`, `groups`, `connections`, `code_contract`, `output_mode`, `agents_spawned` e `feedback_prompts` (`ledger.py:650-697`).
- o Control Center usa as linhas completas para materializar as poucas arestas parentais explícitas (`control_center/sources.py:139-160`).

Nenhum desses caminhos calcula cluster temático, avanço, decisão pendente, construção ou readiness de experimento.

## O que cada sinal permite afirmar

### Pesquisa repetida e relacionada

“Repetida” é computável por contagem de `dispatch_type: research`. “Relacionada” só é forte com `parent_dispatch_id`; pasta idêntica é evidência de co-localização, não de causalidade. Objetivos semelhantes, ids com `-r2/-r3` e proximidade temporal são classificadores candidatos, não fatos.

A amostra Kahneman–Thaler é o caso forte: a segunda pesquisa declara explicitamente a primeira como parent e reutiliza a pasta (`telemetry/agents/subagents-dispatch.yaml:170-180`). Porém essa relação é excepcional: somente sete de 366 openings no snapshot tinham parent. A sequência typed-interaction é semanticamente clara para um leitor humano — exploração e síntese — mas não contém `parent_dispatch_id` (`subagents-dispatch.yaml:6356-6392`). Um detector ledger-only precisaria inferir o vínculo dos textos, pastas aninhadas e intervalo de dois minutos.

### Avanço epistemológico e claims sobreviventes

Não estão no ledger. `exit_reason: resolved` diz que o dispatch fechou sob a semântica operacional do tipo; não carrega o veredito de pesquisa. O skill de pesquisa inclusive permite fechar `resolved` após um KILL confirmado (`.codex/skills/research/SKILL.md:100`).

O avanço torna-se visível apenas nos artefatos. Em typed-interaction, `findings.md` registra cinco candidatos GO e um KILL (`docs/features/agents-communication-infra/research/interaction-relations/findings.md:268-277`), limita explicitamente o alcance da conclusão (`:354-360`) e preserva hipóteses para gates posteriores (`:380-416`). Nada disso aparece nas rows `resolved` correspondentes (`subagents-dispatch.yaml:6375-6399`).

As convenções ajudam a localizar o conteúdo, mas não o tornam parte do ledger: pesquisa com `n >= 2` deve produzir `research.md` e `findings.md`; com `n = 1`, somente `findings.md` (`.codex/skills/research/SKILL.md:127-137`). Não há digest, manifest ou identidade de artefato na opening/close row de pesquisa.

### Decisões não resolvidas

`_state: open` significa apenas ausência de close; não significa decisão em aberto. `resolved` também não significa que todas as decisões de domínio foram tomadas.

O contraexemplo aparece nos artefatos do inventário de problemas: `findings.md` contém cinco perguntas não resolvidas e exige uma próxima etapa de síntese e ataque cético (`research/repository-irreducible-problem-inventory/stages/exploration/findings.md:45-55`). As quatro rows associadas, entretanto, fecharam como três `error` e um `user_abort` (`subagents-dispatch.yaml:5677-5759`). O ledger não consegue dizer qual tentativa produziu quais bytes, pois todas apontam para a mesma pasta.

### Ausência de construção

O máximo que o ledger pode afirmar é “não encontrei dispatch `code` registrado dentro de um recorte definido”. Isso não equivale a “nada foi construído”.

Mesmo para `code`, o `code_contract` registra readiness e intenção pré-execução — `write_scope` e `validation_commands` — não o diff nem os resultados pós-execução (`append-dispatch.cjs:290-355`). A close row não pode carregar esses resultados. O skill de implementação exige como bundle de sucesso diff, inventário de símbolos, rastreabilidade, comandos/resultados e riscos (`.codex/skills/domainspec-implement/SKILL.md:57-66`), mas o ledger não persiste esse bundle.

Além disso:

- construção manual, inline, em outro repositório ou fora do workflow não gera necessariamente uma row local;
- rows históricas podem obedecer schemas anteriores;
- `working_folder` é obrigatório para pesquisa/experimento, não para `code` (`append-dispatch.cjs:133-137`, `:265-275`);
- a existência de uma pasta não prova que o artefato foi produzido pelo dispatch, está íntegro ou permaneceu imutável.

Na amostra, os dois dispatches Kahneman–Thaler estão `resolved` e apontam para a mesma pasta (`subagents-dispatch.yaml:124-153`, `:170-187`), mas essa pasta não existe hoje no repositório. No sentido oposto, a pasta das quatro tentativas `error/user_abort` contém hoje `research.md` e `findings.md`. Portanto, `resolved`, `working_folder` e existência de arquivo falham separadamente como provas de resultado.

### Readiness para experimento

Não há sinal direto. O tipo `experiment` é live no registry, mas a própria semântica vigente é de **proposta/pré-registro**, não de execução: seu resultado é um `criterion.md` congelado; o run posterior produz `experiment.md` e `findings.md` (`.codex/skills/experiment/SKILL.md:134-159`, `:185-193`). Um `experiment` fechado como `resolved` significaria “critério pronto para rodar”, não “hipótese validada”.

Para recomendar a criação dessa proposta, seria necessário obter fora do ledger pelo menos:

- claim ou decisão específica que precisa ser discriminada;
- hipótese única e observação falsificadora candidata;
- evidência de que pesquisa adicional tem retorno menor que um probe;
- dono da decisão e ação que cada resultado desbloqueia;
- verificação positiva do que já foi construído, em vez de inferência por ausência.

O snapshot local tinha zero rows `experiment`, portanto este ledger também não oferece episódios históricos positivos para calibrar o momento da transição.

## Implicação para um recomendador

O desenho defensável com os dados atuais é um **gerador de candidatos**, não um decisor:

1. selecionar clusters por parent explícito; aceitar pasta exata + texto/tempo somente como hipótese de cluster;
2. abrir e validar os artefatos canônicos, preservando autoria, versão e ambiguidade de pasta compartilhada;
3. extrair apenas claims/vereditos/questões/próxima etapa explicitamente escritos;
4. procurar evidência positiva de construção ou de um dispatch posterior relacionado; nunca provar ausência por contagem zero;
5. só então oferecer ao usuário uma sugestão contestável, incluindo por que agora, qual decisão ela desbloqueia e qual fato suprimiria a sugestão.

Suprimir a recomendação quando faltar artefato, houver apenas repetição operacional, a última etapa pedir mais síntese/review, a pasta for compartilhada entre tentativas não atribuíveis, já existir construção/experimento relacionado ou não houver hipótese falsificável e dono da decisão.

## Matriz final

| signal | source | computable now? | confidence | missing evidence | collapse-test |
|---|---|---:|---|---|---|
| Quantidade de pesquisas em um recorte | `dispatch_type`, `created` | Sim | Alta | Definição do recorte temático | Uma row classificada incorretamente ou fora da janela altera a contagem relevante. |
| Relação explícita entre pesquisas | `parent_dispatch_id` | Sim | Alta quando presente | Cobertura é muito baixa; ausência não significa independência | Encontrar parent ausente no ledger mas vínculo obrigatório em outro contrato invalida tratá-lo como fonte única. |
| Co-localização de pesquisas | `working_folder` exato | Sim | Média-baixa | Identidade de objetivo e autoria dos arquivos | Dois objetivos independentes na mesma pasta colapsam o sinal. |
| Relação por texto/tempo/id | `goal`, `context`, `dispatch_id`, timestamps | Sim, heuristicamente | Baixa | Subject/thread id governado | Um par lexicalmente parecido mas causalmente independente colapsa o cluster. |
| Estado operacional | opening + close unidos por id | Sim | Alta | Semântica epistemológica do fechamento | Um `resolved` com KILL ou sem artefato colapsa “closed = advanced”. |
| Cadência/duração | `created`, `_close.closed` | Sim | Alta para tempo; baixa para significado | Causa da repetição e tempo real de trabalho | Retries de infraestrutura rápidos colapsam “cadência = progresso”. |
| Artefatos esperados de pesquisa | `working_folder` + convenção `research.md`/`findings.md` | Parcial | Média | Manifest, digest, autoria por dispatch, imutabilidade | Pasta ausente após `resolved`, ou pasta compartilhada após erros, colapsa atribuição. |
| Avanço epistemológico | Conteúdo citado de `findings.md` | Não pelo ledger; sim por inspeção | Média-alta quando explícito e versionado | Vínculo durável row→artefato e aceitação do approver | Um arquivo posterior, sobrescrito ou não atribuível colapsa a conclusão. |
| Claims sobreviventes | Matriz GO/KILL e collapse-tests no artefato | Não pelo ledger; sim por inspeção | Alta somente para o que está escrito | Estado tipado por claim e versão | Ausência de verdict explícito ou claim mais forte que a citação colapsa o sinal. |
| Decisão não resolvida | Questões/next stage no artefato | Não pelo ledger | Média | Decision id, owner, opções, status e autoridade | “Open question” sem decisão bloqueada colapsa readiness. |
| Construção registrada | Presença de row `code`; `code_contract` em schema atual | Sim | Alta para intenção registrada, não para resultado | Diff, resultados, commit/artefato e vínculo temático | `code` sem bundle aceito colapsa “row = construção”. |
| Ausência de construção | Ausência de row `code` | Não | Muito baixa | Evidência positiva sobre workspace, commits, outros repos e trabalho inline/manual | Qualquer artefato construído fora de dispatch colapsa imediatamente. |
| Critério de experimento já proposto | `experiment` + `working_folder/criterion.md` | Parcial | Média | Digest/freeze e validade atribuível | Criterion ausente, mutado ou não atribuível colapsa pré-registro. |
| Readiness para recomendar experimento | Nenhuma fonte ledger suficiente | Não | Indisponível | Claim, decisão, falsifier, custo, ação pós-resultado, dono e alternativa | Se qualquer resultado não mudar uma decisão, a recomendação não está pronta. |

## Conclusão

O momento correto não é observável como um único estado do ledger. O ledger pode dizer “há uma sequência que merece exame”; os artefatos precisam dizer “o que sobreviveu e o que continua bloqueado”; evidência de workspace precisa dizer “o que já foi construído”. Só a conjunção pode sustentar “talvez seja hora de propor um experimento”, e ainda como recomendação reversível ao dono da decisão, nunca como promoção automática.
