---
artifact_kind: milestone-strategy
status: proposed
milestone: 1
topic: lens-composition
last_updated: 2026-08-13
---

# Estratégia composicional para o Milestone 1

## Decisão de rota

O Milestone 1 deve descobrir e formalizar **como lentes já são usadas e compostas no repositório**, sem assumir que todos os usos de “lente” designam o mesmo fenômeno. O corpus inicial já mostra pelo menos três sentidos que podem ou não convergir:

- lente como divisão deliberada de cobertura (`coverage_diversity`, `paired_tension`);
- lente como posição de ataque ou método atribuído a um agente;
- lente como transformação sincronizada sobre uma identidade estável (por exemplo, views diferentes sobre o mesmo Work).

Por isso, a sequência correta é: **inventariar ocorrências → confrontar tensões entre camadas → propor modelos concorrentes → pré-registrar testes discriminantes → executar apenas os pilotos necessários → sintetizar → revisar adversarialmente**. Começar por um vocabulário normativo cristalizaria a linguagem atual antes de sabermos o que ela explica.

## Pergunta operacional do milestone

> Como lentes são representadas, construídas, selecionadas, atribuídas, combinadas, confrontadas, sintetizadas e avaliadas nas práticas reais do repositório; quais dessas operações têm efeitos observáveis; e qual modelo provisório preserva as diferenças que a evidência exige?

O objeto não é provar que “composição de lentes funciona”. É descobrir **qual fenômeno ocorre**, inclusive a possibilidade de que certos casos sejam apenas cobertura, seleção, agregação, coordenação ou rotulagem posterior.

## Hipóteses concorrentes a manter vivas

As hipóteses estão organizadas em três famílias. Elas não são mutuamente exclusivas entre famílias, mas devem competir dentro de cada pergunta.

### O que é uma lente?

- **L1 — descritor declarativo:** lente é uma tupla de concern, angle, role, método/persona, exclusões, fontes e contrato de saída. A execução realiza bem ou mal esse descritor.
- **L2 — operador de transformação:** lente é a transformação que determina o que se torna saliente, admissível ou relacionável no material observado; o prompt é apenas uma possível implementação.
- **L3 — posição relacional:** lente só existe como posição dentro de uma composição — em contraste, complementaridade ou dependência com outras posições. Isoladamente há apenas um enquadramento.
- **L4 — atribuição retrospectiva:** “lente” é frequentemente um rótulo aplicado depois ou uma instrução sem efeito causal distinguível. Se sobreviver, essa hipótese limita reivindicações sobre composição.

### O que é compor lentes?

- **C1 — união de cobertura:** compor é aumentar a cobertura pela união de observações independentes.
- **C2 — diferenciação coordenada:** compor é preservar diferenças tipadas e atribuir-lhes partes complementares do problema.
- **C3 — transformação por confronto:** a composição ocorre quando uma lente altera a posição de outra por crítica, concessão, revisão ou tradução.
- **C4 — síntese construtiva:** a composição está no operador de síntese que produz relações ou decisões não presentes nas contribuições isoladas.
- **C5 — seleção:** o resultado conjunto melhora principalmente porque escolhe o melhor retorno; “síntese” não acrescenta conhecimento.
- **C6 — efeito topológico:** independência, ordem, reveal, feedback e conexão entre agentes são parte causal da composição, não simples transporte.

### Como reconhecer um efeito composicional?

- **E1 — ganho de cobertura:** aparecem itens válidos ausentes de cada lente isolada.
- **E2 — ganho relacional:** aparecem relações, dependências ou contradições justificadas que nenhum retorno isolado contém.
- **E3 — transformação rastreável:** uma contribuição muda por causa identificável de outra lente, preservando o antes, o depois e a razão.
- **E4 — decisão superior:** o conjunto melhora uma decisão segundo critério congelado, mesmo sem novidade conceitual.
- **E5 — não há efeito atribuível:** qualidade dos agentes, extensão do prompt, seleção do melhor retorno ou julgamento do sintetizador explicam o resultado.

## Operações que o inventário precisa distinguir

Não registrar tudo como “composição”. Cada ocorrência deve indicar quais operações são observáveis:

1. **construir** — definir o recorte ou operador;
2. **vincular** — associar lente a objeto, agente, fonte, método e saída;
3. **selecionar** — escolher uma lente ou conjunto para um objetivo;
4. **diversificar** — buscar diferença de cobertura sem exigir oposição;
5. **parear/tensionar** — colocar duas posições sobre o mesmo concern;
6. **isolar/cegar** — impedir influência antes do primeiro julgamento;
7. **ordenar/revelar** — controlar quando uma lente vê contribuições anteriores;
8. **confrontar** — exigir resposta explícita, concessão, refutação ou revisão;
9. **traduzir/alinhar** — relacionar vocabulários ou granularidades sem apagá-los;
10. **agregar** — reunir retornos sem transformação demonstrada;
11. **selecionar resultado** — escolher um retorno vencedor;
12. **sintetizar** — produzir relações ou conclusões sustentadas por múltiplas contribuições;
13. **adjudicar** — aplicar um critério ao resultado conjunto;
14. **preservar resíduo** — manter desacordos, perdas, dependências e contribuições não absorvidas;
15. **ablar/contrafactualizar** — remover ou trocar uma lente/operação para atribuir efeito.

## Grafo de dispatches recomendado

```text
D1 Inventário evidenciado do repositório (research)
    |
    v
D2 Tensões entre representação, dinâmica e avaliação (Robot-Talks)
    |                         \
    v                          v
D3 Modelos e vocabulário      D4 Critérios experimentais
   concorrentes (research)       (experiment: propostas separadas)
    |                          |
    +------------+-------------+
                 v
      D5 Pilotos mínimos, se necessários
         (runs separados + adjudicação)
                 |
                 v
D6 Síntese do modelo observável e backlog (research/writer + auditor)
                 |
                 v
D7 /review final persistido (review)
                 |
                 v
          gate do Milestone 1
```

Cada dispatch abaixo deve ser planejado por um pequeno grupo estratégico distinto antes do lançamento, conforme a decisão do usuário de que todo dispatch receba ajuda de outros subagentes. Esse meta-planejamento não deve produzir conclusões substantivas; deve resolver corpus, concerns, papéis, dependências, critérios e caminhos de preservação.

### D1 — Inventário evidenciado dos usos reais

**Tipo:** `research`, corpus interno e read-only.

**Pergunta:** onde e de que modo o repositório declara ou realiza lentes, e que evidência existe do caminho entre declaração e resultado?

**Decomposição por concerns, não por arquivos:**

- representação: concern, angle, role, persona/método, prompt, exclusões e contratos;
- seleção e atribuição: como conjuntos e assentos são escolhidos para um objetivo;
- dinâmica: independência, connections, ordem, confrontation, feedback e reveal;
- síntese e avaliação: como contribuições entram no resultado, que resíduos são preservados e o que a telemetria permite atribuir.

Os exploradores devem usar um protocolo comum de ocorrência: objetivo, objeto observado, lente declarada, mecanismo efetivo, operações, topologia, entradas vistas, saída, passagem à síntese, evidência de efeito, perdas/resíduo e confiança da classificação. Um writer reúne ocorrências sem normalizá-las; skeptics atacam **não-vacuidade** (“há um caso concreto?”) e **solidez definicional** (“isso é lente ou apenas role/prompt/view?”); um auditor verifica cobertura e citações.

**Saídas preservadas:** corpus de ocorrências, tipologia descritiva inicial, mapa declaração→execução→resultado e lista explícita do que a telemetria não permite saber. Não emitir definição canônica.

**Dependência:** nenhuma além das initial definitions já existentes. Se o `working_folder` específico exigir sua própria precondição, um subagente deve derivar ali uma initial-definition delimitada ao inventário antes do dispatch, sem acrescentar hipóteses.

### D2 — Robot-Talks sobre tensões composicionais

**Tipo:** sessão autônoma de `Robot-Talks`; não embutir em `research` ou `review`.

**Por que aqui:** depois do inventário haverá afirmações de camadas diferentes que precisam se contradizer diretamente. Robot-Talks serve à confrontação de tensions, não à coleta de exemplos nem à escolha de uma teoria.

**Concerns recomendados:**

- **lente declarada versus lente realizada:** quais campos ou instruções realmente delimitam o olhar;
- **independência versus transformação:** quando não-contaminação ajuda e quando impede composição;
- **síntese versus preservação:** como o todo ganha algo sem apagar autoria, perda e dissenso;
- **avaliação versus atribuição causal:** o que pode ser creditado à composição e o que permanece confundido por agente, prompt ou sintetizador.

**Alternativa rejeitada:** dividir por telemetry, skills, prompts e reports. Isso produziria inventários de arquivo e esconderia as contradições que atravessam essas camadas.

**Saídas preservadas:** `dialogue.md`, relatórios independentes e `findings.md` com tensões evidenciadas. A sessão requer seu human gate próprio antes de suas tensões serem tratadas como disposições; autorização geral para o milestone não deve ser reinterpretada como aceitação automática de cada tensão.

### D3 — Pesquisa de modelos candidatos e precedentes

**Tipo:** `research`, após D1 e a exploração de D2.

**Pergunta:** qual combinação mínima de conceitos explica os casos observados e não colapsa nos vizinhos já nomeados?

**Perspectivas:**

- modelagem operacional extraída das ocorrências do repo;
- precedentes formais e científicos relevantes (framing, perspective taking, ensembles, group cognition, dialectic/deliberation, ablation e causal attribution), com proprietário citado;
- modelagem de processo/topologia;
- representação de proveniência, transformação e resíduo.

O writer deve manter L1–L4, C1–C6 e E1–E5 concorrentes. Skeptics separados aplicam precedent, non-vacuity e definitional-soundness; o auditor produz a matriz de verdicts. “Owned” deve virar `build-from-owned`, nunca derrota. O produto é um **vocabulário provisório com fronteiras, testemunhas e contraexemplos**, além de um modelo de ciclo; não uma ontologia ratificada.

**Saídas preservadas:** `research.md`, `findings.md`, matriz candidato→owner→witness→soundness→verdict→use-mode, vocabulário provisório e hipóteses que perderam.

### D4 — Pré-registros experimentais separados

**Tipo:** vários dispatches `experiment` de proposta. Cada um contém uma hipótese única e produz um `criterion.md` congelado; não executar o probe no mesmo dispatch.

**Prioridade dos critérios:**

1. **Ablation de representação:** retirar/trocar concern, angle, persona/método ou exclusões mantendo o restante fixo. Discrimina L1/L2 de L4 e separa componentes ornamentais dos eficazes.
2. **Topologia:** mesmas lentes e corpus em paralelo selado, sequência, confronto e síntese. Discrimina C1/C3/C6 e mede efeitos de ordem/contaminação.
3. **Síntese versus seleção:** comparar best-of, concatenação e síntese cega aos autores sob critério congelado. Discrimina C4 de C5.
4. **Composição versus agente forte:** conjunto de lentes contra um único agente com orçamento e corpus equivalentes. Ataca E5 e o confound “mais tokens”.
5. **Resíduo e transformação:** verificar se uma síntese consegue apontar contribuição, mudança e perda por lente. Discrimina ganho relacional rastreável de resumo plausível.

Cada designer deve pré-registrar categorias, unidade de análise, observáveis, controles de orçamento/modelo/corpus, condição de falsificação, regra mecânica SURVIVED/FALSIFIED/INVALID e o que ambos os resultados ensinariam. Um skeptic diferente ataca confounds, non-discrimination e reproducibility antes do freeze.

### D5 — Runs mínimos e adjudicação

**Tipo:** dispatches downstream separados, consumindo `criterion.md` read-only; só são necessários antes do milestone quando D3 não consegue escolher entre modelos que mudam a formalização.

Não rodar todo o backlog. O grupo estratégico deve escolher o menor conjunto com maior poder discriminante, provavelmente “síntese versus seleção” e uma ablation de representação. Cada run preserva resultado bruto e adjudicação; o adjudicator não pode ser designer, skeptic ou runner. Se os critérios dependem de execução de código, usar um dispatch de code separado — nunca contrabandear execução para a proposta experimental.

### D6 — Síntese do modelo observável

**Tipo:** `research` de síntese sobre D1–D5, com writer e auditor independentes.

**Obrigação:** construir apenas o modelo que a evidência sustenta. A síntese deve conter:

- definição provisória de lente, incluindo casos-limite e não-lentes;
- separação entre concern, angle, role, persona/método, prompt, view e lens;
- ciclo seleção→vinculação→execução→interação→síntese→avaliação→preservação;
- operações e topologias, com condições sob as quais contam como composição;
- matriz hipótese→evidência→falsificador→estado;
- capacidades observacionais existentes e lacunas de telemetria;
- resultados negativos e resíduos;
- backlog de experimentos priorizado por poder discriminante e custo;
- seção de portabilidade: o que parece geral, o que ainda é específico a agentes e o que não deve ser levado para outro lugar.

O auditor deve rejeitar qualquer item que apareça no vocabulário sem testemunha/contraexemplo, qualquer relação causal apoiada só em retrospectiva e qualquer arquitetura de produto apresentada como descoberta.

### D7 — `/review` final do bundle existente

**Tipo:** `review`, persistido. O alvo é o bundle fechado de D6 e seus artefatos de evidência; review não cria uma teoria concorrente.

**Ataques independentes sobre o corpus completo:**

- fidelidade/evidência: claims excedem ocorrências, pesquisas ou runs?
- definitional collapse: lente/composição apenas renomeiam concern, role, prompt, aggregation ou coordination?
- causalidade/experimento: confounds e critérios móveis sobrevivem?
- governança/proveniência: perdas, desacordos e dependências estão preservados?
- operabilidade/portabilidade: o modelo pode ser aplicado sem julgamento secreto e sem universalizar o domínio de agentes?

Usar attackers independentes, writer, verifiers distintos e coverage auditor. Como o parent apenas orquestra mas o bundle é produzido sob sua sessão, o approver final deve ser humano ou agente dedicado que não faça outro trabalho. O único artefato do dispatch é `review.md`; não persistir transcripts de ataque. O milestone passa com `KEEP`, ou com `FIX` apenas depois que change requests CRITICAL/MAJOR forem tratados e o corpus revisado for novamente verificado.

## Critérios de conclusão do Milestone 1

Todos são necessários:

1. Há um inventário citado de ocorrências reais, incluindo casos negativos e ambiguidades, não apenas exemplos exemplares.
2. “Lente” está provisoriamente delimitada de concern, angle, role, persona, método, prompt e view por testes e contraexemplos.
3. O ciclo composicional identifica operações, participantes, entradas vistas, transformações, síntese, avaliação e resíduo.
4. Pelo menos agregação, seleção, cobertura, tensão, transformação e síntese são distinguíveis; onde não forem, a indeterminação está registrada.
5. Cada hipótese relevante tem evidência favorável, evidência contrária ou falsificador explícito; nenhuma é “aceita” por elegância.
6. Toda reivindicação de efeito causal vem de um contrafactual/run ou é rotulada como hipótese não testada.
7. Existe uma matriz hipótese→evidência→falsificador→estado e um backlog experimental ordenado por poder discriminante/custo.
8. A telemetria atual e suas lacunas estão mapeadas até o nível necessário para observar composição, sem já alterar o runtime.
9. Tensões e contribuições não absorvidas continuam recuperáveis; síntese não é tratada como apagamento legítimo.
10. Portabilidade é classificada como demonstrada, candidata ou não sustentada; nenhuma extração de ferramenta é autorizada pelo milestone.
11. O `/review` final apresenta cobertura completa, cita o corpus em cada finding e não mantém finding refutado.
12. Não restam change requests CRITICAL/MAJOR sem disposição antes do gate final.

## Riscos de cristalização prematura

- **Esquema como ontologia:** porque `angle`, `role` e `initial_prompt` existem, concluir que constituem a essência da lente.
- **Nome como mecanismo:** tratar toda ocorrência da palavra “lens” como instância do mesmo fenômeno.
- **Diversidade nominal:** assumir que personas ou angles distintos produzem observações epistemicamente distintas.
- **Telemetria como verdade causal:** inferir efeito de campos registrados sem ablation ou contrafactual.
- **Síntese como composição por definição:** chamar qualquer resumo conjunto de emergência ou ganho relacional.
- **Confronto como padrão universal:** generalizar Robot-Talks para casos em que cobertura independente ou tradução é mais apropriada.
- **Independência como bem absoluto:** ignorar que certas composições exigem transformação mútua; ou, no sentido oposto, permitir contaminação antes de obter posições independentes.
- **Sucesso sem baseline:** comparar composição apenas com fracasso, não com agente único, best-of, concatenação ou orçamento equivalente.
- **Formalismo sedutor:** escolher teoria das categorias, óptica/lenses, ensembles ou deliberação porque fornece vocabulário elegante antes de provar aderência aos casos.
- **Arquitetura prematura:** converter o modelo em schema, UI, control plane ou ferramenta externa antes de estabilizar observáveis e testes.
- **Universalização indevida:** extrapolar do trabalho multiagente para conhecimento, interfaces e maneiras de trabalhar sem evidência transversal.
- **Perda apagada:** permitir que a síntese final substitua os retornos, tensões e negativas que sustentam seus limites.

## Regra de decisão entre modalidades

- Use **Robot-Talks** quando já existem findings de concerns diferentes e o valor está na contradição/confronto antes da ação.
- Use **research** quando o trabalho é coletar ocorrências, encontrar owners/precedentes, comparar modelos e julgar claim≤proof.
- Use **experiment** quando há uma hipótese única que pode perder contra um critério congelado antes do resultado; a proposta e o run são dispatches separados.
- Use **review** somente quando o bundle do milestone já existe e deve receber change requests verificados; não use review para gerar o modelo.

Essa separação é parte da própria investigação: não chamar coleta, confronto, falsificação e ataque final pelo mesmo nome reduz o risco de que “composição” se torne um recipiente vazio.
