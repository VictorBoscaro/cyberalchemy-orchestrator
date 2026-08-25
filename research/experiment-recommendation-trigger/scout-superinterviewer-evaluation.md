# Scout — avaliação do momento de recomendar um experimento

## Escopo e força da evidência

**Conclusão:** o `superinterviewer` contém um desenho interno coerente para avaliar a recomendação, mas não contém validação empírica de que ele funciona. O desenho mais forte combina: (1) uma unidade de episódio auditável, (2) seleção prospectiva entre movimentos concorrentes, (3) comparação com baselines simples, (4) guardrails de agência e carga e (5) uma tabela pré-declarada de `resultado → ação`.

O status importa:

- `research/research-plan.md` é **proposed** e possui apenas autoridade sobre sequência, expectativas de evidência, gates e condições de parada; não possui resultados nem verdade de produto (`research/research-plan.md:1-6, 11-26`; `authority/AUTHORITY-MODEL.md:5-13`).
- `research/foundation-game-framing/research.md` é **internal synthesis with residue**; declara que não examinou literatura externa nem corpus independente (`research/foundation-game-framing/research.md:1-3`).
- `docs/game/THINKING-THE-GAME.md` e `docs/game/QUESTION-LANDSCAPE.md` são **propostas**, não scripts nem políticas validadas (`docs/game/THINKING-THE-GAME.md:1-3`; `docs/game/QUESTION-LANDSCAPE.md:1-3`).
- A lane do episódio auditável terminou `completed_with_residue` e mantém não validadas a confiabilidade entre avaliadores e o valor comparativo (`research/foundation-game-framing/lanes/01-auditable-transition.md:8-21`).
- Promoção para autoridade de produto exige decisão humana explícita; assentimento, execução ou ausência de objeção não bastam (`authority/AUTHORITY-MODEL.md:15-22`).

Portanto, a formulação defensável é: **há um protocolo candidato pronto para um primeiro teste de baixa vinculação; não há ainda uma regra comprovada para recomendar experimentos no momento correto.**

## O que “momento correto” pode significar neste corpus

O corpus não sustenta “várias pesquisas sem construção” como gatilho. Contagem de pesquisas, duração e ausência aparente de artefato não demonstram bloqueio, necessidade de teste nem benefício esperado. O plano diz explicitamente que número de documentos, agentes, turnos, probes ou dispatches não é progresso (`research/research-plan.md:520-529`).

O candidato mais forte é um gate prospectivo e local:

1. Há uma decisão, alternativa, salvaguarda ou escolha de parada viva que continua bloqueada.
2. A incerteza bloqueadora é discriminável: resultados incompatíveis levariam a ações diferentes.
3. O sinal necessário está principalmente no mundo e pode ser obtido por um passo pequeno, recuperável e proporcional. Se a pessoa possui o sinal, perguntar compete melhor; se falta informação, buscar/informar compete; se o frame é o gargalo, reframe contestável compete; esperar, resposta direta e parar continuam admissíveis.
4. Pelo menos um resultado plausível do experimento mudaria uma alternativa, próximo passo, salvaguarda ou decisão de parar.
5. A recomendação expõe que é uma proposta, suas premissas, reversibilidade, permissão necessária, riscos e o que ocorrerá se o resultado for inconclusivo.
6. Entre movimentos elegíveis, ela tem maior valor discriminante esperado a carga, custo, privacidade, indução e irreversibilidade aceitáveis.

Esses critérios derivam dos gates de elegibilidade, fonte, agência e comparação da proposta (`docs/game/THINKING-THE-GAME.md:18-31`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:97-106`) e da família “reversibilidade e probe” (`docs/game/QUESTION-LANDSCAPE.md:13-29`). Eles não fornecem pesos nem um score validado; a comparação é deliberadamente ordinal e contextual.

**Collapse-test do timing:** se avaliadores não conseguem prever, a partir do estado anterior à intervenção, por que recomendar um experimento supera perguntar, informar, responder diretamente, esperar ou parar, “momento correto” vira justificativa retrospectiva. Nesse caso, não há trigger avaliável.

## Requisitos para episódios históricos

O episódio deve ser limitado por um antes/depois e anotado sem preencher lacunas com a teoria desejada. O núcleo explicitamente proposto na lane é (`research/foundation-game-framing/lanes/01-auditable-transition.md:93-107`):

1. identidade e fronteiras do episódio;
2. estado anterior, separando declaração da pessoa e inferência do sistema;
3. distinção possivelmente ausente e sua proveniência (`prospective`, `emergent` ou `retrospective`);
4. intervenção observável, intenção declarada e eventual bundle de movimentos;
5. sinal observável, mantendo separada a interpretação do sistema;
6. delta antes/depois e seu alvo;
7. evento de contestabilidade — aceitar, emendar, rejeitar, adiar ou retirar;
8. consequência: próximo passo habilitado/corrigido **ou** resíduo tipado;
9. explicação causal alternativa.

Para avaliar especificamente uma recomendação de experimento, o protocolo precisa ainda tornar explícitos, antes da recomendação:

- possibilidade/decisão bloqueada e alternativas vivas;
- incerteza que o experimento pretende discriminar;
- movimentos concorrentes considerados e a razão local para escolher `suggestion`;
- descrição do experimento, resultados possíveis, reversibilidade, custo, autorização e stop rule;
- resultado esperado de cada alternativa e sua consequência decisória;
- carga e riscos previstos;
- sinal posterior de aprendizado, correção, não mudança ou dano, idealmente com follow-up suficiente para detectar retirada ou rejeição tardia.

Os quatro últimos itens são uma **especialização proposta** a partir do admission contract do plano, que exige decisão consumidora, alternativas, baseline, evidência discriminante, tabela `resultado → ação`, falsificador, limites e stop condition (`research/research-plan.md:78-90`). Não são campos já ratificados de produto.

Casos negativos devem permanecer no conjunto: `no delta`, delta contestado, delta confundido e efeito apenas global (`research/foundation-game-framing/lanes/01-auditable-transition.md:115-120`). Rejeição, não mudança, indução danosa, vitória do baseline e ambiguidade preservada são observações válidas, não dados a descartar (`research/foundation-game-framing/lanes/01-auditable-transition.md:107`).

## O que conta como aprendizagem útil

Aceitação ou execução do experimento não basta. O episódio precisa mostrar uma mudança observável e relevante, por exemplo:

- uma alternativa foi eliminada, revisada ou mantida por uma razão observável;
- um próximo passo foi corrigido, habilitado, deliberadamente adiado ou abandonado;
- uma salvaguarda ou stop decision mudou;
- a incerteza foi preservada porque o resultado foi inconclusivo;
- a pessoa corrigiu ou recusou a proposta e essa contestação evitou uma mudança não autorizada.

O aprendizado deve ser distinguido de confiança, fluência, velocidade, coerência narrativa, satisfação, cumprimento ou mera articulação. O corpus proíbe promovê-los silenciosamente a benefício ou autonomia (`research/foundation-game-framing/lanes/03-agency-governance.md:170-189`). Gate B1 requer uma distinção relevante alterada e um próximo passo habilitado/corrigido, com contraste plausível contra baseline simples (`research/research-plan.md:360-370`).

**Collapse-test de utilidade:** se a recomendação apenas aumenta aceitação, confiança, coerência ou movimento, sem alterar uma decisão relevante melhor que o baseline, a alegação de aprendizagem útil colapsa.

## Baselines necessários

Há dois níveis que não devem ser misturados:

### Baseline da representação

Comparar a gramática de transição com **transcrição + decision/change log ordinário**. Medir confiabilidade entre codificadores, detecção de reframe silencioso, recuperação da razão do próximo passo, carga de representação e efeitos relevantes não representados. Casos históricos podem gerar e calibrar a gramática; validação requer conjunto independente/held-out (`research/foundation-game-framing/lanes/01-auditable-transition.md:122-133`).

### Baselines da intervenção

No mesmo estado pré-intervenção, comparar a recomendação de experimento com:

- resposta direta concisa;
- mais uma pergunta ou entrevista fixa;
- informação/recuperação de evidência;
- conversa genérica competente;
- espera, preservação de ambiguidade ou stop quando cabíveis.

Replay, codificação cega, Wizard-of-Oz, comparação manual e mockups não executáveis são os métodos de menor compromisso preferidos antes de prototipar (`research/research-plan.md:385-395`). A lane recomenda ao menos resposta direta, sequência fixa e conversa genérica competente (`research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:141-148`).

**Collapse-test dos baselines:** se uma alternativa simples obtém aprendizado/decisão equivalente ou melhor, com menor carga ou risco, a recomendação especializada é `baseline_sufficient` e deve ser demovida; não pode reivindicar valor incremental (`research/research-plan.md:497-507`).

## Probes discriminantes de baixa vinculação

Em ordem de compromisso crescente:

1. **Codificação retrospectiva cega:** dois ou mais codificadores aplicam, sem conhecer o desfecho desejado, a gramática candidata e o baseline de transcrição + log a episódios delimitados.
2. **Replay contrafactual:** congelar o estado imediatamente anterior à recomendação e pedir a avaliadores ou facilitadores cegos que escolham entre recomendar experimento, perguntar, informar, responder, esperar ou parar, registrando a razão e a previsão.
3. **Wizard-of-Oz/manual pareado:** apresentar variantes do mesmo episódio com movimentos concorrentes, congelando outcomes e guardrails antes da comparação.
4. **Follow-up de contestabilidade:** oferecer rota barata de rejeitar, corrigir ou restaurar o frame anterior e observar se a mudança persiste após a pressão imediata da interação.

Os três primeiros métodos são diretamente previstos pelo plano e pelas lanes. O quarto é uma **inferência operacional mínima** exigida pelas ameaças de compliance, indução e retirada tardia; o corpus diz que aceitação momentânea não prova durabilidade, autonomia, benefício ou causalidade (`research/foundation-game-framing/lanes/01-auditable-transition.md:62-70`).

Resultados primários candidatos:

- concordância sobre fronteira, movimento, distinção e delta;
- proporção de episódios nos quais a recomendação muda corretamente uma decisão/next step ou preserva uma incerteza relevante;
- recuperação da razão do próximo passo;
- correção/recusa e restauração de frame;
- detecção de reframe silencioso;
- carga cognitiva, tempo, abandono e custo de anotação/interação;
- efeitos não representados e sinais posteriores de retirada ou contradição.

Nenhum threshold numérico é suportado pelo corpus; ele precisa ser pré-declarado no protocolo, não escolhido após os resultados.

## Explicações causais alternativas obrigatórias

O campo mínimo já propõe `multiple interventions`, `external event`, `mere articulation`, `compliance` e `unknown` (`research/foundation-game-framing/lanes/01-auditable-transition.md:97-105`). Para esta pergunta, registrar também:

- fadiga ou desejo de encerrar;
- deferência ao sistema/efeito de autoridade;
- demand characteristics e pressão social;
- sugestão/anchoring ou preferência induzida;
- ordem dos movimentos e path dependence;
- informação obtida fora da interação;
- maturação temporal ou trabalho já em andamento;
- seleção retrospectiva de episódios favoráveis;
- atribuição indevida ao movimento mais próximo quando houve bundle;
- narrativa mais coerente sem decisão melhor.

O resíduo causal já tem owner proposto: `WS4`, via experimento discriminante com baseline simples e casos independentes (`research/foundation-game-framing/lanes/03-agency-governance.md:155-168`).

## Carga, agência e segurança

Guardrails mínimos:

- propósito da sugestão visível e permissão distinta de autorização para executar;
- recusa, correção, deferimento, branch, resposta direta e stop sem penalidade;
- reversibilidade e rota de volta ao frame anterior;
- não registrar mais dados do que o necessário para contestabilidade;
- não recomendar quando custo, privacidade, manipulação, dependência ou irreversibilidade superam o valor decisório esperado;
- em contextos médicos, legais, financeiros, de saúde mental ou segurança interpessoal, preservar referral, ajuda qualificada, resposta direta ou ausência de deliberação como alternativas superiores possíveis (`research/foundation-game-framing/lanes/03-agency-governance.md:91-104`).

**Collapse-test de agência:** se uptake sobe enquanto correção/recusa cai, há relato de pressão, ou revisões path-dependent são depois rejeitadas, o resultado é compatível com compliance/indução, não com governança bem-sucedida (`research/foundation-game-framing/lanes/01-auditable-transition.md:124-130`; `research/foundation-game-framing/lanes/02-cooperative-investigation-game.md:118-128`).

**Collapse-test de carga:** se a seleção/explicação/registro custa tanto quanto o benefício decisório, ou se um baseline simples tem resultado equivalente com menor custo/risco, interromper ou demover o mecanismo.

## Tabela mínima `resultado → ação`

Esta tabela é uma proposta derivada do gate do plano; deve ser congelada antes do teste.

| Resultado observado | Classificação | Ação permitida |
|---|---|---|
| A recomendação supera baseline pré-declarado em aprendizado/next-step e respeita guardrails | sinal positivo limitado | avançar para teste independente/held-out; não promover ainda a política |
| Resultado equivalente ao baseline com maior carga/risco | `baseline_sufficient` | demover a recomendação especializada e usar o baseline |
| Uptake/assentimento sem mudança decisória posterior | `no_witness` ou `mere_articulation` | não alegar benefício; revisar ou parar |
| Mais aceitação com menos recusa/correção, pressão ou rejeição tardia | `compliance` / `harmful_induction` | restringir ou abandonar o trigger; preservar contestação |
| Reframe/objetivo muda sem delta visível ou rota de restauração | `silent_reframe` | invalidar o episódio como sucesso e corrigir o protocolo antes de novo teste |
| Vários movimentos/evento externo impedem atribuição | `causal_attribution_unresolved` | resultado inconclusivo; redesenhar comparação, não creditar a recomendação |
| Codificadores não concordam ou campos só são preenchíveis retrospectivamente | `boundary_unreliable` / `circular` | simplificar/redefinir a unidade; não medir timing com ela |
| Outcome indeterminado, mas guardrails intactos | `inconclusive` | preservar incerteza, nomear owner/reopen trigger e escolher evidência seguinte ou stop |
| Guardrail de segurança/privacidade falha | `risk_block` | parar; referral ou decisão humana conforme o contexto |

Gate B4a exige identidade congelada do protocolo, comparação observada, thresholds/guardrails, aplicação da tabela pré-declarada, resultado inconclusivo tipado e proposta explícita de atualização da claim (`research/research-plan.md:397-401`). Só decisão humana posterior pode aceitar, restringir, reframar ou abandonar a claim (`research/research-plan.md:408-416`).

## Resíduo preservado

O corpus ainda não resolve: thresholds, população/contexto, horizonte de follow-up, peso entre benefício e carga, quando uma incerteza está madura para teste, nem quais direitos de agência são universais. Também não demonstra que um ledger contém os campos necessários para observar o gate. Essas lacunas pertencem respectivamente a WS2/WS4, decisão humana de WS5 e investigação separada de observabilidade; não podem ser fechadas por este relatório.

## Esquema mínimo de episódio avaliável

**Owner/status:** candidato de pesquisa pertencente a WS0/WS2/WS3/WS4; a gramática-base é síntese interna com resíduo e a especialização abaixo é **proposta deste scout**, sem autoridade de produto.

```yaml
episode_id: string
boundary: {before_ref: string, after_ref: string}
prior_state:
  declared_intention: string | absent
  system_inference: string | absent
  blocked_possibility_or_decision: string
  live_alternatives: [string]
missing_distinction:
  statement: string
  provenance: prospective | emergent | retrospective
candidate_moves:
  considered: [ask, inform, suggest_experiment, reframe, direct_answer, wait, stop]
  chosen: string
  stated_local_reason: string
experiment_candidate:
  discriminating_uncertainty: string
  possible_results: [{result: string, decision_consequence: string}]
  reversibility: string
  burden_and_risk: string
  permission_required: string
  inconclusive_consequence: string
observed_intervention:
  content_ref: string
  bundled_moves: [string]
signal:
  observable: string
  system_interpretation: string | absent
delta:
  before_after_proposition: string | no_delta
  target: intention | goal | value | constraint | belief | option | commitment | uncertainty
  status: proposed | accepted | amended | contested | deferred | withdrawn | unresolved
contestability:
  authorized_owner: string | unknown
  low_cost_refusal_or_restore_path: string
consequence:
  next_step_or_residue: string
  later_follow_up: string | unavailable
alternatives_and_guardrails:
  baseline_observation: string
  burden: string
  safety_privacy_result: string
causal_alternatives: [string]
coder_confidence: string
```

**Collapse-test:** se os campos de timing só puderem ser preenchidos após conhecer o desfecho, se codificadores não concordarem sobre fronteira/distinção/movimento/delta, ou se transcrição + decision log recuperar as mesmas decisões com menor carga, o esquema não adiciona valor avaliativo e deve ser simplificado ou abandonado.

## Menor protocolo de validação crível

**Owner/status:** desenho de `WS4 — Evaluation, causal attribution, and discriminating experiments`, sob o plano **proposed**; requer adjudicação humana e não autoriza implementação.

1. Separar um conjunto pequeno de episódios históricos em **calibração** e **held-out**. Incluir positivos aparentes, não construção deliberada, pesquisa ainda produtiva, no-delta, recusa, confusão causal e baseline suficiente.
2. Congelar o esquema, as categorias, os thresholds qualitativos/quantitativos, guardrails e a tabela `resultado → ação` antes de ver o held-out.
3. Fazer codificação cega independente com (A) esquema acima e (B) transcrição + decision log. Testar confiabilidade, detecção de reframe silencioso, recuperação da razão do próximo passo, carga e efeitos não representados.
4. Nos episódios em que o estado anterior é recuperável, executar replay/manual Wizard-of-Oz cego com pelo menos quatro opções: recomendar experimento, resposta direta, movimento informacional/interrogativo simples e esperar/parar. Não executar experimentos reais nesta etapa.
5. Comparar decisão/next-step ou incerteza preservada, correção/recusa, restauração de frame, carga, risco e explicações causais. Uptake isolado não é outcome.
6. Aplicar mecanicamente a tabela `resultado → ação`; registrar inconclusivo e owner/reopen trigger quando causalidade ou timing não forem identificáveis.
7. Somente se o held-out mostrar valor incremental e guardrails preservados, propor um próximo teste independente e limitado. Promoção da regra continua sendo decisão humana explícita.

**Collapse-test:** o protocolo falha se usa os mesmos episódios para gerar e validar a regra, se o evaluator conhece a condição desejada, se não compara uma alternativa simples, se muda outcomes após observar os resultados, se aceitação substitui aprendizagem, ou se não admite resultado inconclusivo/negativo. O mecanismo deve ser demovido se a recomendação não superar o baseline a carga e risco aceitáveis, e abandonado/restrito se produzir compliance, reframe silencioso ou dano.
