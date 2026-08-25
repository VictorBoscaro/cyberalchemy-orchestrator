---
artifact_kind: research-findings
status: candidate-for-validation
date: 2026-08-18
subject: experiment-recommendation-trigger
---

# Findings — when to recommend a validation experiment

## Verdict

The current ledger can nominate work that deserves inspection, but it cannot establish the full proposition “related research advanced understanding and nothing was built.” A defensible candidate procedure therefore has two stages: **ledger nomination** followed by **artifact-and-workspace adjudication**. An offer becomes eligible only when the adjudication identifies a live decision, a surviving falsifiable claim, a bounded world-owned observable whose alternative results change the next action, and neither an artifact that already resolves the claim nor an equivalent validation already active in the declared scope. A build that merely supplies the object or apparatus for a future test does not suppress the offer. It remains a contestable offer to preregister the smallest test, never an automatic experiment or a claim that the user intends one.

Evidence: `scout-ledger-observability.md:3-12,123-133` → `implementations/server/ledger.py:163-221,497-525`, `.codex/skills/experiment/SKILL.md:134-159,185-193`; `scout-domainspec-authority.md:30-42,140-152` → `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/experiment/SKILL.md:72-126,131-179`; `scout-superinterviewer-policy.md:29-49` → `docs/game/QUESTION-LANDSCAPE.md:5-29`, `authority/AUTHORITY-MODEL.md:19-21`.

**Claim-chave / collapse-test.** Se um campo vigente e validado do ledger demonstrar conjuntamente lineage temática, avanço por claim, decisão bloqueada e evidência positiva do estado de construção, cai a necessidade da adjudicação externa; nenhum dos scouts encontrou esse campo (`scout-ledger-observability.md:12,31-42,63-70`).

## Matriz de observabilidade dos três predicados

| Predicado | Ledger-observable | Dependente de artefato/estado | Indisponível |
|---|---|---|---|
| **Sequência de pesquisas relacionadas** | Forte somente quando há `parent_dispatch_id`; contagem, timestamps e pasta exata são observáveis. | Sem parent, objetivo, referências entre findings, pastas normalizadas e artefatos podem sustentar uma hipótese de cluster, nunca parentage inventada. Retentativas precisam ser colapsadas. | Identidade temática causal não pode ser provada por similaridade textual, tempo ou pasta sozinhos. |
| **Avanço epistemológico evidenciado** | Não. `resolved` é fechamento operacional e pode coexistir com `KILL`; o close não registra claims, decisão ou próximo gate. | Sim, quando findings atribuíveis e versionados preservam candidato/veredito, claim ceiling, collapse-test, decisão ainda viva e próximo passo. | Sem artefato atribuível ou com pasta sobrescrita/compartilhada, o avanço permanece desconhecido. |
| **Ausência de construção** | Não. Zero rows `code` significa apenas “nenhum dispatch `code` encontrado no recorte”. Até uma row `code` registra intenção prévia, não diff ou resultado posterior. | Uma busca delimitada em artefatos, histórico, receipts, outros repositórios declarados e trabalho em preparação pode sustentar “não encontrei construção equivalente no escopo observado”. | A inexistência global de construção não é demonstrável: trabalho manual, inline, externo ou não registrado permanece fora do ledger. |

Fontes: `scout-ledger-observability.md:74-121,137-152` → `implementations/server/control_center/sources.py:105-160`, `.codex/skills/research/SKILL.md:100,127-137`, `.codex/skills/domainspec-implement/SKILL.md:57-66`; `scout-ledger-counterexamples.md:41-79,95-135` → `internal-tools/document-information-estimator/s0/README.md:1-38`, `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md:1-32`, `research/local-global-continuous-discrete/findings.md:41-55`; `scout-domainspec-cases.md:11-17,115-147,215-243` → `cyberAlchemy-v2/development/iolm-workable-example/README.md:1-30`, `projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/CURRENT-VALIDATION.md:13-37`.

**Claim-chave / collapse-test.** “Nenhuma row `code` = nada construído” já está falsificada por Assay e IOLM; qualquer regra que preserve essa equivalência sofre colapso definicional entre telemetria e estado do mundo (`scout-ledger-counterexamples.md:41-57`; `scout-domainspec-cases.md:115-147`).

## Procedimento candidato de roteamento e inspeção em duas etapas

### Etapa 1 — nomear para inspeção

Nomear uma família candidata quando houver pelo menos um research handoff explícito para teste, **ou** uma sequência reconstruível por parent explícito ou combinação corroborada de objetivo, referências de artefato e pasta. Não exigir `N ≥ 2`: um único findings pode conter um experimento mensurável, enquanto múltiplas rows podem ser retries ou falhas (`scout-ledger-counterexamples.md:95-135,156-168` → `telemetry/agents/subagents-dispatch.yaml:5288-5317,5677-5755,6230-6242`).

Esta etapa só produz `candidate_for_inspection`; não produz “ready”, “stalled” ou “nothing built”.

Nenhum scout encontrou um novo gatilho positivo que sobreviva sozinho à inspeção. A contribuição específica do ledger é reduzir o conjunto de episódios que um adjudicador precisa examinar. Isso deve ser validado contra inspeção direta, medindo custo, latência e casos perdidos; se não houver ganho incremental, a etapa de nomeação deve ser removida.

### Etapa 2 — adjudicar a oferta

Oferecer o desenho/pré-registro de um experimento somente quando todos os itens abaixo tiverem evidência positiva:

1. há uma decisão, alternativa, salvaguarda ou decisão de parar ainda viva;
2. um candidato específico possui standing favorável ou condicionado, e seu claim e collapse-test estão atribuídos a um artefato atual;
3. a incerteza é discriminável por uma hipótese falsificável e por um observable novo; os resultados incompatíveis levam a ações pré-declaradas diferentes;
4. o sinal é world-owned; perguntar, recuperar informação, responder diretamente, reframar, esperar ou parar não resolve a distinção com menor carga ou risco;
5. o probe é pequeno, reversível, proporcional, tem owner humano e admite recusa, emenda, deferimento e resultado inconclusivo;
6. não existe pesquisa aberta, retry/erro não recuperado, review/síntese anterior exigida, owner ausente ou hard gate de especificação/aparato ainda bloqueado;
7. cada build, run, receipt, critério congelado ou pacote encontrado no escopo declarado é classificado como: (a) resolve a claim, (b) validação equivalente ativa, (c) objeto/aparato que habilita o teste, ou (d) irrelevante. Somente (a) e (b) suprimem a oferta; (c) pode satisfazer readiness, (d) não decide o item e escopo externo não inspecionado o mantém `unknown`.

Fontes: `scout-domainspec-authority.md:30-42,58-84,140-152` → `implementation/mars/templates/experiment-candidates-template.md:12-32`, `implementation/mars/definitions/MARS-PIPELINE.md:48-59`; `scout-domainspec-cases.md:19-33,262-326` → `research/high-attention-low-parameter-models/experiment-protocol-research/findings.md:7,86`, `research/high-attention-low-parameter-models/experiment-protocol/SPEC.md:4,136`; `scout-superinterviewer-policy.md:31-49,70-82` → `docs/game/THINKING-THE-GAME.md:19-32`, `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:56-104`; `scout-ledger-counterexamples.md:170-189`.

**Claim-chave / collapse-test.** Se nenhum resultado plausível mudar uma decisão, salvaguarda, próximo passo ou escolha de parar, a proposta não é um experimento decisório pronto; vira produção de informação sem consumidor (`scout-superinterviewer-policy.md:33-40`; `scout-ledger-observability.md:152`).

### Forma segura da oferta

> A pesquisa parece deixar **H** como a distinção que bloqueia **D**. Um teste pequeno e reversível **E** poderia separar **A** de **B**; cada resultado mudaria o próximo passo desta forma: **R→ação**. Não encontrei validação equivalente em **escopo S**, mas **limites L** não foram verificados. Quer que eu proponha o pré-registro? Podemos também perguntar, recuperar evidência, responder diretamente, esperar ou parar.

Essa formulação é uma composição **precedent-clean** dos contratos e casos, não uma política ratificada nem uma alegação de novidade. O tipo LIVE sustenta pré-registro e gate humano; a política de interação do `superinterviewer` é candidata e ainda sem validação empírica (`scout-domainspec-authority.md:17-26,30-42`; `scout-superinterviewer-policy.md:9-27,68`; `scout-superinterviewer-evaluation.md:3-15`).

## Candidatos e vereditos

Aqui, `GO` significa “levar ao protocolo de validação”, não “implantar como trigger”. `KILL` é usado somente quando falta witness ou quando a definição colapsa.

| candidate | owner (citation or precedent-clean) | witnessed? | sound? | verdict GO/KILL | use-mode |
|---|---|---|---|---|---|
| Handoff explícito: decisão viva + claim falsificável + outcomes→ações + inputs admissíveis | Owner do tipo LIVE `experiment`; `scout-domainspec-authority.md:30-42` → `.../skills/experiment/SKILL.md:72-126`; precedente Mint em `scout-domainspec-cases.md:35-75` | Parcial e retrospectivo: Mint e intent-population testemunham componentes, não o conjunto completo antes da oferta | Sim como hipótese condicionada a owner/gates, checagem de estado e witness prospectivo da conjunção | **GO** | Validar elegibilidade para oferta de pré-registro |
| Claim sobrevivente + negativo fechado + decisão ainda não consumida | **precedent-clean**; `scout-domainspec-cases.md:278-289` → `cyberAlchemy-v2/development/mint/experiment-foundry-boundary/criterion.md:62-75`, `.../run/findings.md:16-23` | Sim, em casos de testable fork; não como campo ledger | Sim, após prova de que run/decisão existente não resolveu o fork | **GO** | Adjudicação por artefato |
| Research→spec marcado decision-ready, com todos os pré-requisitos depois satisfeitos | **precedent-clean**; `scout-domainspec-cases.md:77-113,291-302` → `research/high-attention-low-parameter-models/experiment-protocol-research/findings.md:7,86`, `.../experiment-protocol/SPEC.md:4,136` | Parcial: o caso high-attention testemunha o estado bloqueado, não um run admitido | Somente como condição verificável; `blocked/NOT_RUN` suprime | **GO** | Inspecionar readiness, não disparar |
| Sequência explícita com objetivo estável e resíduo convergindo para mecânica de teste | **precedent-clean**; `scout-domainspec-cases.md:304-315` → `telemetry/agents/subagents-dispatch.yaml:1726,3548`, `research/high-attention-low-parameter-models/experiment-protocol-research/findings.md:7-86` | Parcial; lineage frequentemente está nos artefatos | Sim apenas para nomeação, nunca para recomendação | **GO** | Candidate detector |
| `N` pesquisas `resolved` ou `T` dias sem `code` | Sem owner; contra-precedentes em `scout-domainspec-cases.md:245-260,328-333`; `scout-ledger-counterexamples.md:95-135` → `telemetry/agents/subagents-dispatch.yaml:5288-5317,5677-5755,6230-6242` | Não há witness de validade; há contraexemplos | Não; colapsa contagem com avanço e telemetria com construção | **KILL** | Não usar |
| Ausência de row `experiment` significa que nenhum experimento está em preparação | Sem owner; `scout-ledger-counterexamples.md:59-79` → `projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md:1-32` | Não; o corpus inteiro tinha zero rows e já havia pacote `preparing` | Não; colapso definicional | **KILL** | Não usar |

Nenhum candidato é morto por falta de owner. Onde não há owner normativo, ele permanece explicitamente `precedent-clean` e limitado a pesquisa. Nenhuma reivindicação de novidade deve acompanhar a composição sem busca de precedentes adicional.

“Nenhuma construção equivalente encontrada” não é candidato nem veredito `GO/KILL`; é somente uma checagem negativa e escopada de supressão. Os casos IOLM e Schema Service mostram por que ela não pode ser inferida do ledger (`scout-domainspec-cases.md:317-326`; `scout-ledger-counterexamples.md:182-188`). Nenhum episódio do corpus testemunha prospectivamente todos os sete itens da adjudicação antes de uma oferta; cada item deve ser codificado como `true`, `false` ou `unknown`, e somente uma linha integralmente `true` pode contar como positivo no protocolo held-out.

## Condições explícitas de abstinência e supressão

Suprimir a oferta e nomear o próximo gate quando ocorrer qualquer uma destas condições:

- cluster apenas heurístico, retries não deduplicados, pasta compartilhada não atribuível ou repositório externo não inspecionado;
- status `draft/exploratory` exige verificar se o conteúdo já possui decisão, claim, owner e aparato; suprimir somente quando esses elementos faltarem. Pedido explícito de síntese, skeptic ou review, ou erro/user abort ainda não recuperado, nomeia o gate anterior;
- decisão já foi tomada e o follow-on é implementation-shaped; nesse caso, planejar/construir é precedente suportado;
- faltam owner, critério falsificável, outcome desconfirmador, inputs/fixtures, admission gate ou aparato de execução;
- evidência existente pode ser recuperada sem novo teste;
- um artefato encontrado resolve a claim ou demonstra validação equivalente ativa; se ele apenas fornece objeto/aparato, verificar readiness em vez de suprimir; se for irrelevante, não usá-lo como evidência;
- o usuário recusou, deferiu ou pediu outro modo; silêncio não é consentimento;
- custo, risco, privacidade, indução, irreversibilidade ou competência tornam o probe desproporcional;
- movimentos repetidos não alteraram alternativas, constraints, autorização ou próximo passo: isso exige reavaliar modo e carga, mas não constitui limiar automático de supressão. Qualquer janela temporal deve ser validada prospectivamente.

Fontes: `scout-ledger-observability.md:123-133`; `scout-ledger-counterexamples.md:59-127,146-152`; `scout-domainspec-authority.md:100-126` → `cyberAlchemy-v2/development/research/2026-07-02-validators-as-moat/DECISION.md:55-62`, `arcanum/arcana/decision-gate/SKILL.md:179-209`; `scout-superinterviewer-policy.md:42-53,70-82`; `scout-superinterviewer-evaluation.md:138-151`.

**Claim-chave / collapse-test.** A recomendação perde sua legitimidade interacional se uptake aumenta enquanto correção/recusa cai, há pressão relatada ou revisão tardia rejeita a mudança; isso é compatível com compliance/indução, não com aprendizagem (`scout-superinterviewer-evaluation.md:138-151` → `research/foundation-game-framing/lanes/01-auditable-transition.md:124-130`).

## Decisão de timing e intervenção

| Estado imediatamente anterior | Movimento preferido | Evidência exigida | Suprimir quando |
|---|---|---|---|
| A pessoa possui preferência, constraint, interpretação ou autorização ausente | **Perguntar** uma questão decision-changing | decisão viva e resposta capaz de mudar alternativa | pergunta não muda nada, é invasiva ou difícil de recusar |
| O sinal já existe em fonte, cálculo, comparação ou observação | **Recuperar / informar** | fonte atribuível e discriminante | fonte não distingue alternativas ou seu status seria lavado em verdade |
| A representação esconde a distinção relevante | **Reframe contestável** | frame antigo, alternativas e rota de restauração explícitos | risco de substituição do objetivo ou captura |
| Uma resposta concisa basta | **Responder diretamente** | resposta habilita a escolha sem esconder incerteza material | excede competência ou parece autorizar ação não escolhida |
| Evento futuro, permissão ou evidência nomeada domina pesquisa/teste agora | **Esperar / deferir** | reopen trigger e owner quando existirem | dever imediato de segurança/referral |
| Decisão já fechada e próximo passo autorizado | **Avançar para plano/build/review** | decisão, owner, claims e gates suficientes | compromisso apenas inferido ou aparato ainda bloqueado |
| Decisão viva + world-owned observable novo + probe reversível supera baselines | **Oferecer experimento delimitado** | todos os sete itens da adjudicação | qualquer item desconhecido, alternativa simples melhor ou validação equivalente ativa |
| Ambiguidade produtiva, ausência de autoridade, risco dominante ou movimentos sem delta | **Preservar resíduo, branch ou parar** | razão, owner/reopen trigger quando possível | não usar resíduo como depósito infalsificável |

Fonte: `scout-superinterviewer-policy.md:70-86` → `docs/game/QUESTION-LANDSCAPE.md:7-31`, `docs/game/THINKING-THE-GAME.md:19-48`, `authority/AUTHORITY-MODEL.md:15-21`; coerência operacional em `scout-superinterviewer-evaluation.md:17-32`.

## Menor protocolo de validação

O corpus sustenta validar a **capacidade de recomendar**, antes de construir um recomendador ou rodar experimentos reais:

1. Separar um pequeno conjunto de episódios delimitados em calibração e held-out. Incluir positivos aparentes e os negativos já observados: build sem `code` (Assay/IOLM), experimento em preparação (Schema Service), pesquisa ainda produtiva, próximo gate `review`, owner/spec bloqueado, uma única pesquisa pronta para probe, recusa/no-delta e baseline suficiente.
2. Congelar antes do held-out: os três predicados, a regra em duas etapas, categorias de abstenção, campos de episódio, guardrails, thresholds escolhidos pelo owner e a tabela `resultado→ação`. O corpus não sustenta nenhum threshold numérico.
3. Usar pelo menos dois codificadores independentes e cegos ao desfecho desejado. Comparar (A) a regra candidata com (B) transcrição + decision/change log ordinário; medir concordância sobre fronteira, lineage, distinção, movimento, delta e razão do próximo passo, além de carga e efeitos não representados.
4. Onde o estado pré-intervenção for recuperável, fazer replay/Wizard-of-Oz manual e cego com quatro famílias mínimas: recomendar experimento; resposta direta; pergunta/recuperação simples; esperar/parar. Não executar experimentos reais nessa etapa.
5. Outcome primário: decisão/next-step corretamente alterado **ou** incerteza legitimamente preservada, com correção/recusa e restauração de frame. Uptake, velocidade, confiança ou coerência isolados não contam como benefício.
6. Aplicar mecanicamente a tabela congelada: `baseline_sufficient` demove; `no_witness`, `circular` ou fronteira não confiável mata/redefine a claim; compliance, indução, silent reframe ou risk block restringe/abandona; causalidade não identificável permanece inconclusiva.
7. Só se o held-out mostrar valor incremental com guardrails preservados, propor um teste prospectivo independente e limitado. Promoção continua sendo decisão humana.

Fonte: `scout-superinterviewer-evaluation.md:34-60,76-119,153-169,227-239` → `research/research-plan.md:78-90,385-416,497-507`, `research/foundation-game-framing/lanes/01-auditable-transition.md:93-133`; conjunto de contracasos em `scout-ledger-counterexamples.md:39-168`.

**Claim-chave / collapse-test.** Se codificadores só conseguem justificar o timing após ver o desfecho, não concordam sobre fronteira/distinção/movimento/delta, ou um baseline simples recupera decisões equivalentes com menor carga, o trigger não adiciona valor e deve ser simplificado ou abandonado (`scout-superinterviewer-evaluation.md:32,225,239`).

## Mudanças mínimas de schema/instrumentação

Não são necessárias para executar o protocolo retrospectivo: ele pode usar ledger como índice e artefatos como evidência. Elas passam a ser necessárias somente se o produto quiser detectar, suprimir repetição e auditar recomendações de forma confiável.

1. **Vínculo durável de thread/artefato.** Registrar relação explícita de objetivo/thread e manifest de outputs com path, digest, versão e papel do artefato. A baixa cobertura de `parent_dispatch_id`, a rejeição de chaves legadas e pastas compartilhadas provam que hoje não há atribuição durável suficiente (`scout-ledger-observability.md:31-42,74-92,139-148` → `.codex/skills/register-dispatch/append-dispatch.cjs:146-169,665-684`).
2. **Receipt de estado positivo, não um booleano `nothing_built`.** Referenciar diff/commit/receipt/run/criterion/pacote e o escopo inspecionado, inclusive repositórios externos. Assay, IOLM e Schema Service provam que ausência de row não pode preencher esse papel (`scout-ledger-counterexamples.md:41-79,121-127`; `scout-domainspec-cases.md:115-147`).
3. **Evento separado de recomendação.** Registrar `candidate`, evidence refs, decisão/owner, offer time, resposta `accepted|declined|deferred|amended`, razão opcional, validade/reopen trigger e escopo autorizado. O ledger atual não tem evento confiável de oferta/recusa, e `feedback_prompts` mistura fenômenos diferentes (`scout-ledger-counterexamples.md:146-152`; `scout-ledger-observability.md:42`). Não enriquecer silenciosamente o close fixo.

Não adicionar score de “progresso”, limiar de número/tempo nem campo global `not_built`: os casos demonstram que esses campos condensariam estados incompatíveis. Claims, decisões e readiness devem permanecer em artefatos tipados e atribuíveis; o ledger deve guardar identidade e evidência, não inventar semântica.

**Claim-chave / collapse-test.** Se o protocolo mostrar que transcrição + log e inspeção sob demanda resolvem o problema com menor carga, nenhuma mudança de schema se justifica; instrumentação é uma consequência de valor incremental demonstrado, não pré-condição assumida (`scout-superinterviewer-evaluation.md:80-96,225`).

## Disagreements and residue preserved

- O `domainspec-core` fornece owner LIVE para **pré-registro**, mas seus casos históricos incluem runs e builds; a recomendação aqui termina no gate de oferta, não importa autoridade para executar (`scout-domainspec-authority.md:30-42`; `scout-domainspec-cases.md:54-65,149-176`).
- MARS oferece critérios fortes, mas sua autoridade é limitada ao programa MARS; eles entram como precedente, não norma global (`scout-domainspec-authority.md:58-84`).
- O `superinterviewer` fornece uma política candidata coerente, porém não um trigger empiricamente validado; não há pesos ou thresholds defensáveis (`scout-superinterviewer-policy.md:15-27`; `scout-superinterviewer-evaluation.md:3-30,119`).
- Os snapshots locais reportaram 366 e 368 dispatches em leituras próximas; isso é drift observacional, não contradição útil para o trigger. Nenhuma regra depende dessas contagens (`scout-ledger-observability.md:22-25`; `scout-ledger-counterexamples.md:31-37`).
- “Ausência de construção” permanece formulação forte demais. A saída auditável é sempre “não encontrei validação equivalente no escopo S; limites L permanecem desconhecidos”.

## Resposta em uma linha

A pesquisa encontrou um procedimento candidato, não um gatilho já validado para o “momento correto”: o ledger pode nomear episódios para inspeção e a adjudicação de artefatos pode justificar uma oferta contestável, mas o timing e o valor incremental precisam sobreviver ao protocolo held-out antes de qualquer implementação.
