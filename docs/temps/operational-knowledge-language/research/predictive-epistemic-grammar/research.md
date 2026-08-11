# Retornos integrais da pesquisa

Os quatro retornos abaixo são preservados verbatim. Os títulos de separação pertencem somente a este coletor.

## Manifesto dos retornos-fonte

Escopo de cada SHA-256: bytes UTF-8 do corpo integral do retorno-fonte, incluindo seu LF terminal e
excluindo o título e os separadores acrescentados por este coletor.

| retorno-fonte | função | SHA-256 |
|---|---|---|
| 1 | explorer | `C3C440CB579E2877E889BBA5C23B9551E20ADD55619EA9CE742592088447EAAF` |
| 2 | precedent — fonte reemitida somente com a citação QuickCheck corrigida | `10A8C8A46DBDE240AF50C7C50600D67858959B4CB0E73513B2DA57EB3CE79C0B` |
| 3 | skeptic non-vacuity | `4AA3F273A4B0A829B29854B8183B4AA8A17F86F28151C14F3593B03B347F0D3F` |
| 4 | skeptic definitional-soundness | `E70C221EB30CCF4FEBEE9213902F98027282F9111725B177A0C9526BBB8C61E9` |

A citação QuickCheck do retorno 2 usa uma cópia acadêmica que respondeu GET 200 como
`application/pdf` e conserva o DOI oficial como identificador adicional. O URL Chalmers testado
como primeira preferência respondeu 404 e, por isso, não foi usado.

## Retorno 1 — explorer

# Exploração operacional/prospectiva — candidatos que podem tornar a gramática preditiva

## Regra de classificação

- **Previsão estrutural:** as premissas e regras fixadas excluem antecipadamente certos resultados. Um witness contrário derruba a alegação sob essas premissas.
- **Previsão heurística:** a gramática ordena probes, hipóteses ou intervenções por plausibilidade, custo ou poder discriminante, mas não implica logicamente o resultado.
- **Mera explicação:** o vocabulário apenas organiza um resultado já observado. Não restringe o espaço de resultados antes da observação.

A fonte exige precisamente essa separação e proíbe transformar qualquer falha posterior em “resíduo previsto” ([anexo, linhas 62–116](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)). A base corrente reconhece que ainda não há resultados prospectivos nem vantagem demonstrada sobre alternativas simples ([definições iniciais, linhas 50–86](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/research/predictive-epistemic-grammar/research-initial-definitions.md)).

## Candidato 1 — seleção de probe guiada por perfil residual

**Classe atual:** previsão heurística; poderia tornar-se estrutural sob um teorema de separação.

**Input congelado**

- frame e schema atuais;
- conjunto explícito de hipóteses concorrentes;
- perfil residual tipado antes da escolha;
- conjunto admissível de probes, seus custos e canais;
- métrica de discriminação ou valor decisório.

**Previsão/constraint**

A política que usa o perfil residual selecionará uma probe cuja resposta esperada separa mais hipóteses relevantes, ou reduz mais uma classe residual declarada, que uma política sem acesso ao perfil.

Não conta prever apenas “alguma probe ajudará”. A política precisa nomear a probe ou uma classe estritamente menor de probes antes da resposta.

**Observação discriminante**

Diferença pré-registrada em poder de separação, mudança correta de decisão, redução residual fora da amostra ou custo para atingir a mesma discriminação.

**Baseline mais simples**

- Bayesian experimental design ou active learning com os mesmos candidatos e custos;
- seleção por entropia;
- agente genérico sem perfil residual;
- especialista humano com o mesmo contexto, mas sem a taxonomia da gramática.

**Possível witness**

Duas hipóteses produzem os mesmos readouts atuais; o locus do resíduo implica uma probe de interface, enquanto probes de parâmetro não as separam. A resposta da probe de interface elimina uma hipótese.

**Colapso**

- o perfil não melhora consistentemente nenhum resultado sobre os baselines;
- a vantagem desaparece quando os custos e informações disponíveis são igualados;
- diferentes tipos residuais recomendam as mesmas probes;
- o tipo residual só pode ser atribuído depois de conhecida a resposta.

Este é o teste operacional da ponte ainda ausente `resíduo -> probe -> sinal -> alteração demonstrável do resíduo`, explicitamente identificada no PDF, pp. 30–35, e no anexo ([linhas 184–207](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)).

## Candidato 2 — previsão de uma distinção escondida por compressão

**Classe atual:** heurística. Torna-se estrutural apenas quando a lente futura ou a obrigação de preservação pode ser especificada independentemente do resultado.

**Input congelado**

- representação `R: X -> S`;
- pares ou fibras atualmente identificados;
- tarefa, risco, horizonte e população;
- mecanismos candidatos ou obrigações não avaliadas;
- conjunto limitado de lentes ou readouts futuros.

**Previsão/constraint**

Nomear antecipadamente qual fibra de `R`, ou qual variável atualmente colapsada, deverá ser dividida por uma lente especificada.

**Observação discriminante**

Encontrar `x, y` previamente nomeados com `R(x) = R(y)` e `L(x) != L(y)` no readout independente previsto.

**Baseline mais simples**

- seleção ordinária de features;
- análise de erro e validação fora da amostra;
- sufficient statistics;
- MDL ou regularização;
- busca aleatória por distinções adicionais.

**Possível witness**

Uma representação trata dois casos como equivalentes, mas uma obrigação de segurança previamente declarada prevê respostas diferentes sob uma probe de estresse específica.

**Colapso**

- a distinção só é formulada depois de `L(x) != L(y)` ser observado;
- qualquer diferença candidata pode ser justificada pela gramática;
- busca ordinária de features encontra a distinção com custo igual ou menor;
- a representação não declarava preservar o readout usado no teste.

O caderno já fornece o critério de fatoração em `Set`, mas não um método para antecipar qual fibra romperá ([caderno, linhas 303–334](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)). O salto preditivo é justamente escolher a ruptura antes de executá-la.

## Candidato 3 — previsão de ruptura de analogia

**Classe atual:** previsão heurística; estrutural quando o transporte e as leis de preservação são formalizados.

**Input congelado**

- correspondência parcial fonte–alvo;
- relações positivas, negativas e neutras;
- composições que o transporte promete preservar;
- tarefa e região de validade;
- probes adversariais admissíveis.

**Previsão/constraint**

Nomear antecipadamente:

1. a composição ou região em que a analogia deve quebrar;
2. qual obrigação deixará de ser preservada;
3. qual tipo de witness deverá aparecer.

**Observação discriminante**

A correspondência funciona nos casos retidos, mas falha especificamente na composição, escala ou intervenção prevista, com o tipo de ruptura antecipado.

**Baseline mais simples**

- structure-mapping;
- checklist de especialista do domínio;
- teste sistemático de cada correspondência;
- analogia verbal sem aparato categórico.

**Possível witness**

O transporte preserva estrutura estática, mas foi previsto que falharia sob ordem temporal: dois caminhos correspondentes deixam de ser equivalentes quando a sequência de intervenções é invertida.

**Colapso**

- a previsão é apenas “a analogia quebrará em algum lugar”;
- regiões incompatíveis podem ser justificadas com igual facilidade;
- a ruptura observada não envolve a estrutura prometida;
- o baseline de especialista prevê o mesmo ponto sem usar a gramática.

O anexo exige pré-registro do que transporta e onde pode romper ([linhas 209–224](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)); o PDF enfatiza que a analogia só ganha força quando produz consequências confrontáveis, não narrativas retrospectivas, pp. 36–38.

## Candidato 4 — resíduo de composição ou falha de globalização

**Classe atual:** pode produzir previsão estrutural quando partes, interfaces e obrigação global são formalizadas; caso contrário, permanece heurística.

**Input congelado**

- componentes `A` e `B`;
- provas ou testes de adequação local independentes;
- interface tipada;
- operação de composição;
- obrigação global;
- candidato a witness integrado.

**Previsão/constraint**

Antecipar que `A` e `B` passam localmente, mas que sua composição:

- não admite witness global;
- viola uma obrigação específica;
- requer uma estrutura de interface previamente nomeada.

**Observação discriminante**

A tentativa controlada de construir o witness integrado falha exatamente no contrato previsto, embora os testes locais continuem passando.

**Baseline mais simples**

- constraint satisfaction;
- interface-contract checking;
- integração incremental comum;
- análise de dependências ou incompatibilidades.

**Possível witness**

Duas políticas satisfazem separadamente custo e segurança, mas não existe plano dentro do prazo que realize ambas; um certificado de insatisfatibilidade ou contraexemplo operacional localiza a incompatibilidade cruzada.

**Colapso**

- a falha já era interna a `A` ou `B`;
- a interface estava malformada, mas isso não foi previsto;
- o teste de constraints comum prevê a mesma impossibilidade;
- “resíduo composicional” não distingue ausência de interface, conflito real e mudança temporal do objeto.

O caderno exige provar adequação local antes de atribuir emergência à composição ([linhas 487–488](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)); o anexo propõe o mesmo risco prospectivo ([linhas 226–241](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)).

## Candidato 5 — prever qual enriquecimento quebra uma equivalência

**Classe atual:** candidato forte a previsão estrutural.

**Input congelado**

- objetos ou modelos `X` e `Y`;
- lente `L0`;
- witness da equivalência relevante sob `L0`;
- conjunto finito de enriquecimentos candidatos;
- obrigação de preservação de cada enriquecimento.

**Previsão/constraint**

Escolher antecipadamente um enriquecimento `E` tal que:

- `X ~_{L0} Y`, mas `X not~_{L0+E} Y`; ou
- a equivalência sobreviverá a `E`.

A gramática precisa prever qual enriquecimento, não apenas afirmar que uma lente mais fina pode distinguir mais.

**Observação discriminante**

Um witness próprio do enriquecimento — temporal, causal, normativo, probabilístico etc. — separa os objetos, ou uma prova mostra que a equivalência se eleva à estrutura enriquecida.

**Baseline mais simples**

- testar exaustivamente todos os enriquecimentos;
- conhecimento especializado do domínio;
- refinement typing;
- model checking da obrigação enriquecida.

**Possível witness**

Dois modelos são equivalentes como grafos, mas uma previsão anterior identifica causalidade intervencional como enriquecimento discriminante; uma intervenção produz respostas diferentes.

**Colapso**

- a gramática não escolhe entre enriquecimentos;
- qualquer quebra posterior pode ser redescrita como enriquecimento relevante;
- o witness já estava disponível em `L0`;
- a equivalência ou sua quebra depende de estrutura importada e não declarada;
- brute force ou expertise comum obtém o mesmo resultado mais diretamente.

Esta é a forma operacionalmente mais limpa da hipótese de equivalência indexada por lente ([anexo, linhas 269–289](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt); PDF, pp. 30–31).

## Candidato 6 — minimalidade, generatividade e residualidade

**Classe atual:** previsão heurística quantitativa, não lei estrutural.

**Input congelado**

- família ordenada ou parcialmente ordenada de schemas;
- gerador ou amostrador fixo;
- tarefa, população, risco e horizonte;
- métricas independentes de diversidade útil, validade e resíduo;
- custo do schema, decodificador e probes.

**Previsão/constraint**

Antes dos resultados, prever uma região ou mudança de regime:

- estrutura excessiva reduz diversidade útil;
- estrutura insuficiente aumenta resíduos relevantes;
- uma faixa intermediária oferece melhor fronteira de Pareto.

Não é necessário supor curva suave ou optimum único.

**Observação discriminante**

Curvas fora da amostra mostram a mudança prevista e ela se repete em mais de um domínio não usado para criar a hipótese.

**Baseline mais simples**

- MDL;
- regularização e cross-validation;
- bias–variance;
- análise comum de complexidade versus desempenho;
- busca de Pareto sem vocabulário residual.

**Possível witness**

A remoção de uma relação aumenta diversidade sem alterar obrigações; a remoção seguinte cruza uma distinção previamente declarada e aumenta falhas em probes retidas.

**Colapso**

- não existe relação estável entre liberdade e resíduo;
- “diversidade útil” é definida depois dos resultados;
- o efeito é completamente explicado por complexidade de modelo;
- o optimum muda arbitrariamente com pequenas mudanças de métrica;
- generatividade é confundida com simples cardinalidade da fibra.

O próprio caderno restringe a hipótese: multiplicidade em fibras é liberdade latente, não operação generativa, e resíduo também pode ocorrer sem generatividade ([linhas 324–341](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)). O anexo preserva essas possibilidades contrárias ([linhas 384–416](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)).

## Candidato 7 — enriquecimento prospectivo por risco, antes de qualquer resíduo

**Classe atual:** constraint operacional potencialmente estrutural; sua seleção concreta tende a ser heurística.

**Input congelado**

- decisão irreversível ou de alto custo;
- risco e obrigação de segurança;
- mecanismo conhecido omitido;
- linguagem atual e enriquecimentos candidatos;
- ausência registrada de mismatch anterior.

**Previsão/constraint**

A linguagem atual será insuficiente para licenciar uma ação segura; um enriquecimento específico deve entrar antes da intervenção, mesmo sem resíduo observado.

**Observação discriminante**

Casos indistinguíveis no kernel recebem decisões de risco diferentes após o enriquecimento, e essa diferença é confirmada por simulação, teste ou resultado independente.

**Baseline mais simples**

- FMEA;
- hazard analysis;
- causal risk assessment;
- checklist regulatório;
- ordinary systems thinking.

**Possível witness**

Duas ações parecem equivalentes sem tempo, mas uma possui dano retardado irreversível. O enriquecimento temporal separa as ações antes da primeira falha observada.

**Colapso**

- a gramática apenas renomeia uma obrigação já produzida pela análise de risco;
- não indica qual estrutura deve entrar;
- o enriquecimento não altera nenhuma decisão ou teste;
- o mecanismo “omitido” foi escolhido depois do dano.

Este candidato é importante porque impede que a gramática se torne uma catraca puramente reativa. O caderno já declara que risco e normas podem justificar enriquecimento prospectivo ([linhas 343–363 e 426–435](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)).

## Candidato 8 — diagnóstico residual que seleciona a classe de reparo

**Classe atual:** previsão heurística.

**Input congelado**

- mismatch e perfil residual;
- hipóteses causais concorrentes: probe inadequada, ruído, expectativa falsa, fronteira ruim, interface incompatível, linguagem insuficiente ou drift;
- intervenções diagnósticas disponíveis;
- ordem ou custo de teste.

**Previsão/constraint**

O perfil residual deverá reduzir antecipadamente o conjunto de causas e selecionar uma intervenção diagnóstica que resolve ou localiza a falha mais eficientemente que troubleshooting genérico.

**Observação discriminante**

A intervenção prevista altera o mismatch da forma esperada, enquanto intervenções rivais não o fazem.

**Baseline mais simples**

- diagnóstico diferencial;
- root-cause analysis;
- troubleshooting por ablação;
- árvore genérica de falhas.

**Possível witness**

Um resíduo de transformação prediz perda no mapa, não falta de tipo no alvo; testar round-trip localiza a perda sem enriquecer o schema.

**Colapso**

- o mesmo perfil residual é compatível com todas as causas;
- o resíduo não reduz a incerteza sobre a reparação;
- a árvore genérica usa menos informação e obtém desempenho igual;
- qualquer intervenção bem-sucedida é reclassificada depois como a “resposta mínima”.

Isso testa a formulação prudente do caderno: mismatch não seleciona automaticamente seu remédio ([linhas 343–363](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)).

## Candidato 9 — prever o limite do próprio kernel

**Classe atual:** previsão estrutural somente se a expressividade for formalizada; caso contrário, ablação conceitual.

**Input congelado**

- linguagem exata do kernel;
- fenômenos `X` e `Y`;
- enriquecimento candidato `E`;
- critérios de representação e equivalência;
- proibição explícita de importar `E` por codificação indireta.

**Previsão/constraint**

Prever que:

- `X` é representável pelo kernel;
- `Y` não é representável sem `E`;
- `Y` torna-se representável com `E`.

**Observação discriminante**

Uma construção explícita para `X`, uma impossibilidade ou par de modelos indistinguíveis para `Y`, e uma construção separadora após adicionar `E`.

**Baseline mais simples**

- dependency analysis;
- expressiveness comparison;
- model-theoretic definability;
- feature ablation.

**Possível witness**

Sem estado e ordenação, duas trajetórias com o mesmo estado final são indistinguíveis; uma propriedade dependente do caminho não pode ser expressa. O enriquecimento temporal separa as trajetórias.

**Colapso**

- o kernel codifica tempo, agência ou normatividade clandestinamente;
- não há semântica suficientemente precisa para provar não expressibilidade;
- `E` pode ser removido sem perder a distinção;
- os quatro componentes dependem de derivados que deveriam reconstruir.

O anexo propõe diretamente esse ataque ([linhas 446–475](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)); o caderno proíbe chamar o kernel de mínimo ou independente antes da análise de dependências ([linhas 201–238](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)).

## Candidato 10 — limite reflexivo por diagonalização

**Classe atual:** mera explicação ou programa formal, não previsão disponível.

**Input necessário**

- sistema capaz de representar uma família suficientemente rica de transformações;
- mecanismo preciso de autorrepresentação;
- operação de aplicação;
- condições do teorema de ponto fixo pertinente.

**Previsão/constraint possível**

Somente após essas condições, antecipar um fixed point específico ou uma testemunha de limitação pertencente à classe formal declarada.

**Observação discriminante**

Construção formal do fixed point ou da testemunha; não basta observar self-reference ou uma falha genérica.

**Baseline mais simples**

O teorema clássico de Lawvere, Gödel, Turing ou resultado correspondente, sem a gramática proposta.

**Possível witness**

Um morfismo diagonal ou sentença/programa construído pelas hipóteses do teorema e não por analogia verbal.

**Colapso**

- o sistema não satisfaz autorrepresentação e aplicação;
- “diagonalização” nomeia qualquer recursão;
- o resultado vem integralmente do teorema clássico e a gramática não adiciona consequência;
- fixed point é interpretado como “fechamento” ou “zero resíduo” sem lei de interpretação.

A posição mais honesta é mantê-lo fora do ledger empírico inicial. O anexo já restringe diagonalização a um caso especial ([linhas 418–444](C:/Users/victo/.codex/attachments/f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt)); o caderno também exige hipóteses formais precisas ([linhas 336–341](C:/Users/victo/cyberalchemy-orchestrator/docs/temps/operational-knowledge-language/README.md)).

## Separação final por força

### Candidatos a previsão estrutural

- quebra de equivalência sob enriquecimento;
- falha de globalização sob contratos formais;
- limite de expressividade do kernel;
- distinção em fibras, mas somente para lentes e obrigações fixadas independentemente;
- diagonalização, somente depois de satisfeitas as hipóteses formais — hoje ainda não.

### Candidatos heurísticos

- escolha de probe pelo perfil residual;
- localização de distinção escondida;
- antecipação da ruptura de analogia;
- fronteira minimalidade–generatividade–residualidade;
- seleção prospectiva de enriquecimento por risco;
- escolha da classe de reparo após mismatch.

### Formulações que, isoladamente, são mera explicação

- `lente -> probe -> resíduo -> reframing`;
- “o domínio resistiu”;
- “houve compressão excessiva”;
- “a composição produziu emergência”;
- “faltava um enriquecimento”;
- “a falha foi diagonal”.

Cada uma só cruza a fronteira preditiva quando o locus, o mecanismo, o witness e o resultado excluído são congelados antes da observação.

## Cinco previsões com maior risco informativo

1. Um tipo residual pré-registrado melhora a seleção de probes contra baselines fortes.
2. A gramática escolhe corretamente qual enriquecimento quebrará uma equivalência conhecida.
3. Contratos locais permitem prever antecipadamente uma falha específica de globalização.
4. Uma família de schemas apresenta a mudança de regime minimalidade–generatividade prevista fora da amostra.
5. A especificação do kernel antecipa corretamente uma distinção que não pode expressar sem um enriquecimento nomeado.

## Experimento mínimo mais informativo

O primeiro teste deveria ser uma avaliação cega de **seleção de probe guiada por resíduo**, porque ela atravessa a cadeia central `resíduo -> probe -> nova distinção` e permite comparação direta com métodos simples.

Procedimento mínimo:

1. selecionar casos novos, não usados para formular a gramática;
2. congelar hipóteses, readouts atuais, perfis residuais e conjunto de probes;
3. fazer quatro políticas escolherem a próxima probe: gramática, Bayesian/active-learning baseline, agente genérico e especialista;
4. ocultar as respostas durante a seleção;
5. medir separação correta de hipóteses, mudança de decisão, custo e generalização;
6. preservar resultados negativos e impedir reclassificação posterior dos resíduos.

Se a política da gramática não superar ou complementar os baselines, a principal ponte dinâmica permanece terminologia organizadora. Se superar de forma replicável e o ganho desaparecer quando o perfil residual é retirado, haverá a primeira evidência operacional genuinamente prospectiva.

Fonte editorial inspecionada integralmente nas seções relevantes: :codex-file-citation{path="C:/Users/victo/cyberalchemy-orchestrator/output/pdf/entre_sistemas_e_categorias_v0.2.pdf" purpose="source"}.


## Retorno 2 — precedent

## Precedentes, ownership e comparação com alternativas simples

### Escopo e regra de evidência

Foram inspecionados integralmente:

- `research-initial-definitions.md`;
- o anexo `f981a09e-3ab8-4078-a2b8-1b727083c294/pasted-text.txt`;
- o caderno `docs/temps/operational-knowledge-language/README.md`;
- as partes pertinentes de *Entre Sistemas e Categorias* v0.2: equivalência e enriquecimento, lentes e probes, composição, minimalismo/generatividade, diagonalização, kernel e ledger de claims.

Esta foi uma busca de precedentes limitada, não uma revisão sistemática exaustiva. Portanto, nenhum candidato recebe alegação de novidade. `precedent-clean` só seria justificável após uma busca bibliográfica própria por candidato, com termos e bases predefinidos.

### Resultado executivo

Nenhuma das famílias preditivas do anexo está limpa de precedentes em seus componentes essenciais. Isso não enfraquece necessariamente o programa: quase todas são bons casos de `build-from-owned`.

O espaço potencialmente distintivo da gramática não está em inventar compressão, abstração, probes, composição, analogia ou diagonalização. Está em tentar ligá-las por um contrato comum e operacional:

```text
representação task-relative
    -> expectativa de preservação
    -> contato/probe
    -> readout
    -> mismatch tipado
    -> seleção prospectiva de probe, reparo ou enriquecimento
```

Essa integração ainda não demonstrou poder preditivo. Para acrescentar algo além dos donos, ela precisa transformar o tipo de resíduo em variável operacional que melhora prospectivamente a escolha de probes, prevê rupturas ou seleciona enriquecimentos melhor que baselines especializados.

### Vocabulário de ownership

- `already-deployed`: o resultado reconhecível já está implementado e efetivamente utilizado no repositório.
- `build-from-owned`: existe um dono externo reconhecível, mas ele ainda precisa ser adaptado ou conectado à gramática.
- `precedent-clean`: nenhuma propriedade intelectual conceitual anterior foi localizada numa busca adequada. Nenhum candidato abaixo satisfaz esse padrão nesta busca limitada.

## Matriz de candidatos

| Candidato do anexo | Owner reconhecível | Estado no repositório | Baseline mínimo | O que a gramática ainda precisaria acrescentar |
|---|---|---|---|---|
| Prediction ledger e congelamento prévio | preregistration / Registered Reports | `already-deployed` como infraestrutura metodológica; ainda não como ledger executado desta pesquisa | criterion congelado antes do run | Tipar previsões estruturais sem transformar o vocabulário da gramática em liberdade pós-hoc |
| A. Previsão de distinção | abstração/refinamento, CEGAR, information bottleneck | `build-from-owned` | fatoração `L = L̄ ∘ R` + contraexemplo/refinamento | Prever **qual** distinção faltará antes do contraexemplo, com regra derivada da gramática |
| B. Previsão de probe | Bayesian optimal experimental design, active learning, Blackwell comparison | `build-from-owned` | expected information gain ou redução de risco decisório | Demonstrar que o perfil tipado de resíduo escolhe probes melhores que posterior/incerteza/custo isolados |
| C. Ruptura de analogia | structure-mapping e metamorphic testing | `build-from-owned` | correspondência relacional + relações metamórficas | Prever antecipadamente uma região e um tipo de ruptura que o mapeamento estrutural sozinho não prediz |
| D. Resíduo de composição | assume-guarantee reasoning, compositional verification, sheaf obstructions, system dynamics | `build-from-owned` | contrato de interface ou teste local-global | Unificar falhas formais, empíricas e normativas sem perder os critérios específicos de cada domínio |
| E. Minimalismo–generatividade | MDL, rate-distortion, information bottleneck | `build-from-owned` | curva complexidade–perda task-relative | Mostrar que composicionalidade e perfil de resíduos produzem uma fronteira melhor que compressão/relevância convencionais |
| F. Enriquecimento quebra equivalência | reduct/expansion, forgetful structure, invariantes sob mudança de linguagem | `build-from-owned` | tabela explícita de estrutura esquecida + invariant/property tests | Selecionar prospectivamente o enriquecimento discriminante, não apenas observar depois que mais estrutura separa |
| Famílias separadoras de probes | teoria de experimentos, identificabilidade, restricted observational profiles | `build-from-owned` | matriz hipótese × probe e teste de separação | Regras de formação que derivem probes do resíduo sem circularidade |
| Globalização de estruturas locais | sheaf theory e compositional consistency | `build-from-owned` | existência ou obstrução de seção global | Transportar a ideia para casos não formalizados sem chamar qualquer conflito de obstrução |
| Limites reflexivos/diagonalização | Lawvere e esquemas de fixed point | `build-from-owned` | verificar explicitamente as hipóteses de auto-representação e avaliação | Identificar sistemas do projeto que realmente satisfazem essas hipóteses e produzir uma previsão própria |
| Compressão versus distinção como eixo unificador | rate-distortion, information bottleneck, abstração | `build-from-owned` | objetivo explícito de compressão sob distorção/relevância | Encontrar uma consequência que não seja apenas renomeação do trade-off já conhecido |

## Análise por candidato

### 1. Prediction ledger

O ledger não é poder preditivo; é controle contra reconstrução retrospectiva. Seu ownership é claro. Preregistration registra hipóteses, métodos e plano de análise antes da execução, precisamente para reduzir manipulação e relato seletivo, segundo o [Center for Open Science](https://www.cos.io/open-science). Registered Reports submetem protocolo e desenho antes dos resultados, separando qualidade metodológica de resultado favorável.

No repositório, essa disciplina já está implantada:

- `.codex/skills/experiment/SKILL.md:70-79` exige criterion imutável, congelado antes de qualquer run;
- existem protocolos preregistrados em `docs/features/agent-provenance-telemetry/probes/`;
- há experimentos que preservam explicitamente critérios e resultados negativos.

Classificação: `already-deployed` como infraestrutura. Criar outro tipo de ledger paralelo seria duplicação. O passo correto é usar o mecanismo de experimento existente e especializar o conteúdo do criterion para previsões da gramática.

### 2. Previsão de distinção

A versão reativa — começar com abstração grosseira, obter contraexemplo e refinar — é diretamente possuída por CEGAR. O trabalho original começa com uma aproximação, testa a propriedade e usa contraexemplos para eliminar comportamento espúrio da abstração ([Clarke et al., CEGAR](https://web.stanford.edu/class/cs357/cegar.pdf)).

A versão task-relative de “comprimir preservando somente informação relevante” também tem owner forte no information bottleneck: encontrar um código curto de `X` que preserve informação sobre uma variável relevante `Y` ([Tishby, Pereira e Bialek](https://arxiv.org/abs/physics/0004057)).

O modelo em `Set` do caderno,

```text
R suficiente para L  <=>  L = L_bar o R,
```

já oferece um baseline mais simples que a gramática inteira: basta procurar `x,y` tais que `R(x)=R(y)` e `L(x) != L(y)`.

O que ainda seria distintivo é prever, antes de encontrar esse par, **qual fibra será heterogênea sob qual lente**. Para isso, a gramática precisaria fornecer uma política de seleção derivada de estrutura declarada — não apenas dizer depois que a representação colapsou uma diferença.

Classificação: `build-from-owned`.

### 3. Previsão de probe

O owner principal é desenho experimental/active learning. Esses campos já selecionam observações ou experimentos para maximizar melhoria esperada, informação ou redução de incerteza. Krause et al. tratam diretamente o problema de escolher observações caras segundo objetivos de informação e robustez ([JMLR, observation selection](https://jmlr.org/papers/volume9/krause08b/krause08b.pdf)); Bayesian optimal design planeja experimentos usando incerteza posterior ([Seeger, JMLR](https://www.jmlr.org/papers/v9/seeger08a.html)).

Causal models são o baseline obrigatório quando a probe é intervenção. Do-calculus distingue observação de intervenção e especifica quando distribuições intervencionais são identificáveis a partir de dados observacionais ([Shpitser e Pearl](https://ftp.cs.ucla.edu/pub/stat_ser/r329-uai.pdf)).

Portanto, “escolher uma probe discriminante entre hipóteses” já é owned. A hipótese adicional legítima seria:

> condicionado ao mesmo estado de crença, custo e conjunto de probes admissíveis, acrescentar o tipo de resíduo melhora prospectivamente a seleção.

Isso exige ablation:

```text
baseline: hipótese + incerteza + custo
treatment: hipótese + incerteza + custo + perfil de resíduo
```

Se o perfil não melhorar discriminação, decisão ou custo, a gramática não acrescentou poder.

Classificação: `build-from-owned`.

### 4. Previsão de ruptura de analogia

Structure-mapping já possui alinhamento relacional, correspondência um-a-um, conectividade paralela, systematicity e geração de candidate inferences. Gentner formula analogia como transporte de relações, distinguindo-a de semelhança literal e atributos compartilhados ([Gentner 1983](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf)). A implementação SME materializa o alinhamento e a projeção de inferências ([Northwestern QRG](https://www.qrg.northwestern.edu/ideas/smeidea.htm)).

Metamorphic testing possui a parte de testar uma transformação quando não há oracle simples: declarar relações que deveriam ser preservadas e observar violações. O relatório original propõe gerar novos casos a partir de relações metamórficas ([Chen, Cheung e Yiu](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf)).

A gramática pode acrescentar algo se o “perfil de ruptura” for mais que uma lista posterior. Precisa congelar:

- estrutura transportada;
- estrutura deliberadamente não transportada;
- invariantes esperados;
- região prevista de quebra;
- tipo de mismatch esperado.

Depois deve comparar contra SME + testes metamórficos equivalentes. Se a gramática apenas chama violações de “resíduos”, é renomeação.

Classificação: `build-from-owned`.

### 5. Resíduo de composição

Há vários owners, conforme o domínio.

Em software e sistemas formais, assume-guarantee reasoning verifica componentes sob contratos de suposição e garantia e busca tornar verificação composicional ([counterexample-guided assume-guarantee synthesis](https://doi.org/10.1109/TC.2010.94)).

Para falhas local-global, Abramsky e Brandenburger caracterizam contextualidade como obstrução à existência de seções globais; não é apenas a metáfora de “partes funcionam, conjunto falha”, mas uma construção formal com condições explícitas ([paper sheaf-theoretic](https://arxiv.org/abs/1102.0264)).

Para dinâmica, system dynamics já deriva comportamento global de feedbacks, estoques, fluxos e atrasos e usa simulação para política; a própria associação descreve o campo como abordagem computacional para estratégia e policy design ([System Dynamics Society](https://systemdynamics.org/what-is-system-dynamics-old/)). Isso é um baseline melhor que raciocínio categórico nu quando o resultado depende de ganho, atraso ou estado.

A contribuição potencial da gramática é um contrato de interface entre regimes:

- formal: violação de lei/invariante;
- dinâmico: comportamento emergente após acoplamento;
- empírico: divergência de readout;
- normativo: obrigações incompatíveis.

Mas uma taxonomia comum não é ainda previsão. Ela precisa antecipar qual interface falhará e permitir escolher o formalismo proprietário adequado.

Classificação: `build-from-owned`.

### 6. Minimalismo–generatividade

A hipótese de região intermediária entre excesso e insuficiência de estrutura já se sobrepõe fortemente a rate-distortion, MDL e information bottleneck.

MDL seleciona modelos minimizando comprimento de descrição do modelo e dos dados; Rissanen já formula seleção de estrutura e parâmetros por shortest data description ([Rissanen 1978](https://doi.org/10.1016/0005-1098(78)90005-5)). Information bottleneck explicita o trade-off entre compressão de `X` e preservação de informação relevante para `Y` ([Tishby et al.](https://arxiv.org/abs/physics/0004057)).

Portanto, “estrutura demais reduz flexibilidade; estrutura de menos perde distinções relevantes” não é uma contribuição nova. Também não garante uma curva unimodal.

A gramática acrescentaria algo apenas se:

1. complexidade incluísse não só tamanho, mas regras de composição e custo de interfaces;
2. perda fosse um vetor tipado de resíduos, não um escalar escolhido depois;
3. a fronteira prevista generalizasse entre lentes ou tarefas;
4. o resultado superasse MDL/IB ou explicasse uma falha sistemática deles.

Sem isso, o candidato deve ser tratado como releitura de relevant compression.

Classificação: `build-from-owned`.

### 7. Enriquecimento quebra equivalência

A ideia básica é matematicamente padrão: esquecer estrutura pode tornar objetos ou morfismos indistinguíveis; restaurar estrutura pode separá-los. Portanto,

```text
X ~ sob L0
X ≁ sob L1
```

não é por si uma previsão ou resultado novo.

O desafio real é escolher `L1` antes de observar a quebra. Um baseline mínimo é:

1. declarar a estrutura esquecida;
2. declarar os invariantes que dependem dela;
3. gerar casos property-based;
4. testar preservação e violações.

Property-based testing já está efetivamente implantado no repositório: `tools/test-derivation-engine/src/emit/tests.ts:7-11` gera testes seeded para invariantes universalmente quantificados e preserva gaps quando falta oracle. O owner histórico é QuickCheck, que formula propriedades e gera entradas para buscar contraexemplos ([Claessen e Hughes — PDF](https://www.cis.upenn.edu/~bcpierce/courses/552-2008/resources/icfp-quickcheck.pdf); [DOI](https://doi.org/10.1145/351240.351266)).

O resultado interno `EquivalenceCornerInhabited` permanece somente reportado no PDF/caderno. Sem inspeção direta do Lean, ele não pode ser classificado como `already-deployed` para esta investigação.

Classificação: `build-from-owned`; property testing é `already-deployed` como mecanismo de teste, não como validação da tese.

### 8. Consequências formais `resíduo -> probe -> distinção`

Cada subproblema já tem donos parciais:

- famílias de probes separadoras: identificabilidade, desenho de experimentos e comparação de informação;
- extensões parciais impossíveis: constraint satisfaction, graph matching e structure-mapping;
- composição local-global: sheaves e compositional verification;
- equivalência sob enriquecimento: invariantes e forgetful/reduct structure;
- schema task-minimal: sufficient statistics, MDL e information bottleneck.

A oportunidade não é inventar um novo wrapper. É provar uma ponte que nenhum componente isolado oferece, por exemplo:

> sob condições explícitas, um tipo de resíduo restringe uma classe de probes admissíveis e uma probe dessa classe separa uma equivalência relevante com probabilidade/custo limitado.

Esse enunciado teria conteúdo se:

- o tipo de resíduo fosse determinado independentemente;
- a classe de probes fosse menor que a classe genérica;
- a conclusão fosse mais forte que “alguma probe distingue”;
- houvesse baseline e contraexemplo.

Até lá, `resíduo -> probe -> distinção` é programa de pesquisa, não teorema.

Classificação: `build-from-owned`.

### 9. Diagonalização e previsão de limite próprio

Lawvere já fornece a estrutura categórica de diagonalização/fixed points sob hipóteses precisas ([Lawvere 1969](https://doi.org/10.1007/BFb0080769)); Yanofsky mostra como vários paradoxos, teoremas de incompletude e fixed points instanciam um esquema relacionado ([Yanofsky](https://arxiv.org/abs/math/0305282)).

Logo, “self-representation + avaliação + diagonalização pode expor limite” é owned. A gramática não ganha poder por renomear a testemunha como resíduo reflexivo.

A aplicação ao projeto continua aberta porque seria preciso demonstrar:

- objeto de representações;
- mecanismo de avaliação/aplicação;
- capacidade de codificar a família relevante;
- condição de surjetividade/representabilidade apropriada;
- endomorfismo sem fixed point ou outra testemunha requerida.

Sem esses dados, a relação permanece analogia arquitetural.

Classificação: `build-from-owned`.

### 10. Compressão versus distinção como unificação

Como intuição editorial, é fértil. Como teoria preditiva, está perigosamente perto de ser universal demais. Information bottleneck já formula “descartar o irrelevante e preservar o relevante”; rate-distortion já relaciona taxa e perda; CEGAR já alterna abstração e refinamento.

A gramática precisaria apontar um fenômeno que:

- não seja representável apenas por compressão e função de perda;
- dependa essencialmente de composição, contato ou tipo de resíduo;
- produza uma previsão diferente da obtida pelos baselines.

Normatividade, alteração do objeto pela probe e incompatibilidade entre lentes podem ser bons candidatos, mas só se forem formalizados sem embutir a resposta no critério de relevância.

Classificação: `build-from-owned`.

## O que já está implantado versus apenas descrito

### `already-deployed`

- congelamento de criterion antes de execução;
- preservação de resultados e critérios negativos;
- protocolos preregistrados;
- geração property-based de testes de invariantes;
- uso pontual de metamorphic testing no corpus arquitetural.

Esses mecanismos devem ser reutilizados, não duplicados sob nomes epistemológicos.

### `build-from-owned`

- CEGAR para refinamento por contraexemplo;
- Bayesian design/active learning para escolha de probes;
- causal models para intervenções;
- structure-mapping para analogia;
- metamorphic testing para preservação sob transformação;
- assume-guarantee e sheaf obstructions para composição/local-global;
- MDL/IB para minimalismo task-relative;
- Lawvere para diagonalização.

### `precedent-clean`

Nenhum candidato. A integração específica “perfil multiaxial de resíduo como estado intermediário comum que seleciona probe, reparo ou enriquecimento em domínios heterogêneos” não encontrou um owner único nesta busca, mas isso é apenas uma lacuna observada, não certificação de novidade.

## Baseline suite recomendada

A gramática só deve receber crédito incremental sobre este conjunto:

| Família | Baseline |
|---|---|
| distinção/refinamento | fatoração em `Set` + CEGAR |
| probe | Bayesian experimental design/active learning |
| intervenção | causal model com semântica de `do` |
| analogia | structure-mapping + metamorphic tests |
| composição formal | assume-guarantee |
| local-global | teste explícito de seção global/obstrução quando aplicável |
| dinâmica | system dynamics ou modelo de estado |
| minimalismo | MDL ou information bottleneck |
| preservação | invariants + property-based testing |
| disciplina prospectiva | criterion preregistrado do próprio repositório |

Comparar somente com LLM genérico seria um baseline fraco e poderia inflar artificialmente a contribuição.

## Conclusão de ownership

O anexo melhora substancialmente a disciplina da investigação, mas não identifica ainda uma fonte autônoma de poder preditivo. Quase todos os mecanismos candidatos têm owners fortes e alternativas mais simples.

A aposta que sobrevive ao sweep é mais estreita:

> A gramática pode acrescentar valor se uma representação prospectiva e tipada do mismatch conectar, de modo mensurável, famílias hoje separadas — especialmente se o tipo de resíduo melhorar a escolha de probes, antecipar a quebra de uma equivalência sob enriquecimento ou localizar falhas de composição além do que produzem baselines especializados.

Collapse-test: se CEGAR, Bayesian design, structure-mapping/metamorphic testing, compositional verification e MDL/IB produzirem as mesmas previsões com igual ou menor custo, a gramática continua sendo uma linguagem integradora, não uma teoria preditiva adicional.

## Retorno 3 — skeptic `non-vacuity`

# Retorno verbatim — skeptic `non-vacuity`

## Escopo e regra

Avaliei somente se cada candidato possui testemunha operacional ou formal não vazia. Não avaliei ownership, novidade nem colapso definicional. Um witness exige: input congelável, previsão ex ante, baseline forte, observação que possa contrariar a previsão e collapse-test explícito. Um exemplo que apenas instancia o fenômeno, mas empata com o baseline, pode testemunhar não-vacuidade; ele **não** demonstra contribuição preditiva incremental da gramática.

## Veredito executivo

Dos três gates prioritários, dois têm witnesses formais mínimos do fenômeno, mas nenhum demonstra vantagem incremental sobre o baseline especializado. O gate de probe guiada por perfil residual recebe `NO-WITNESS`: sob paridade de informação há um negativo fechado; sem paridade, o ganho pode ser apenas informação adicional embutida no perfil.

| candidato | non-vacuity |
|---|---|
| Seleção de probe guiada por perfil residual | **NO-WITNESS** |
| Discriminador de enriquecimento/limite expressivo | **WITNESSED** — fenômeno estrutural, não vantagem incremental |
| Falha composicional/local–global | **WITNESSED** — fenômeno estrutural, não vantagem incremental |
| Ruptura de analogia | **WITNESSED** — witness de falha de composição |
| Fronteira minimalidade–generatividade–residualidade | **NO-WITNESS** |
| Enriquecimento prospectivo por risco | **WITNESSED** — separação temporal mínima |
| Diagnóstico residual/classe de reparo | **WITNESSED** — perda por transformação mínima |
| Limite reflexivo/diagonalização | **NO-WITNESS** |
| Prediction ledger | **WITNESSED** — apenas como controle metodológico já operacional; não como poder preditivo |

## 1. Seleção de probe guiada por perfil residual — `NO-WITNESS`

**Negativo fechado sob paridade de informação.** Seja `D` o input congelado disponível ao baseline forte: hipóteses, probabilidades ou incertezas, matriz hipótese × probe, custos, canais e utilidade decisória. Seja o perfil residual `ρ(D)` derivável desse mesmo input. Para qualquer política da gramática `π(D,ρ(D))`, existe a política baseline `π′(D)=π(D,ρ(D))`; portanto o perfil não pode melhorar prospectivamente a escolha sob paridade de informação. Se `ρ` contém informação não derivável de `D`, treatment e baseline deixam de receber o mesmo input, e o resultado não isola a gramática.

- **Input congelável:** `D`, função de tipagem `ρ`, probes, custos e regra de score.
- **Previsão ex ante necessária:** uma probe ou classe estritamente menor escolhida por `ρ`, com ganho sobre Bayesian design/active learning sob inputs igualados.
- **Baseline forte:** desenho experimental ótimo sobre `D`.
- **Observação discriminante necessária:** ganho replicável em separação, decisão ou custo que desaparece na ablação de `ρ`, sem retirar informação bruta do baseline.
- **Collapse-test:** se `ρ` é função de `D`, o baseline pode reproduzir a política; se não é, o ganho pode ser informação extra. Os dois ramos zeram o witness incremental.

O corpus oferece somente o esqueleto “duas hipóteses; probe de interface separa, probes de parâmetro não”, mas não fornece uma instância em que o perfil acrescente informação operacional sem violar a paridade. Logo, nesta rodada: `NO-WITNESS`, não uma prova de impossibilidade absoluta. Para reabrir, deve-se congelar uma restrição computacional, representacional ou de amostragem sob a qual `ρ` seja uma compressão útil de `D`, e comparar políticas com a mesma informação e orçamento.

## 2. Discriminador de enriquecimento/limite expressivo — `WITNESSED`

**Menor witness formal.** Congele `L0=U: Pos_fin -> Set`, o esquecimento da ordem. Tome `X` como a cadeia `0<1` e `Y` como a anticadeia sobre `{0,1}`. Sob `L0`, ambos têm o mesmo conjunto subjacente e são indistinguíveis. Congele candidatos `E={ordem, probabilidade}` e a obrigação `φ := existe um único elemento mínimo`.

- **Previsão ex ante:** adicionar `ordem` quebra a equivalência; adicionar uma distribuição uniforme não separa `X` de `Y` quanto a `φ`.
- **Observação discriminante:** `φ(X)=verdadeiro`, `φ(Y)=falso`; sob a estrutura probabilística uniforme, ambos continuam iguais para o readout congelado.
- **Baseline forte:** comparação ordinária de expressividade/definability ou brute force sobre os dois enriquecimentos.
- **Resultado excluído:** equivalência de `X` e `Y` sobreviver à ordem, ou probabilidade ser o primeiro separador da obrigação.
- **Collapse-test:** se a obrigação `φ` ou a estrutura de ordem forem introduzidas somente depois da separação, o witness colapsa; se `L0` já codifica ordem, colapsa; se `E` puder ser removido preservando `φ`, colapsa.

Este witness fecha a não-vacuidade da forma estrutural “esquecer estrutura colapsa, enriquecer separa”. O baseline escolhe o mesmo `E`; portanto ele não testemunha poder incremental da gramática.

## 3. Falha composicional/local–global — `WITNESSED`

**Menor witness formal.** Congele dois componentes locais: `A` admite somente `x_A=0`; `B` admite somente `x_B=1`. Cada componente é localmente satisfatível. Congele a interface `x_A=x_B` e a obrigação global “existe uma atribuição compatível”.

- **Previsão ex ante:** `A` e `B` passam localmente, mas não existe witness global; a obstrução está exatamente na variável compartilhada.
- **Observação discriminante:** o solver retorna `UNSAT` para `x_A=0 ∧ x_B=1 ∧ x_A=x_B`, preservando a satisfatibilidade local dos dois lados.
- **Baseline forte:** SAT/CSP ou interface-contract checking.
- **Resultado excluído:** existência de qualquer atribuição global compatível.
- **Collapse-test:** se `A` ou `B` já forem localmente insatisfatíveis, não há resíduo composicional; se a igualdade de interface não tiver sido congelada, a falha é artefato de interface; se drift temporal mudar os componentes, é outro tipo de falha.

O witness demonstra uma obstrução local–global não vazia e localiza seu locus. O baseline CSP produz exatamente a mesma previsão; não há witness de ganho incremental.

## 4. Ruptura de analogia — `WITNESSED`

Congele no domínio-fonte a lei de composição `b∘a=c`. No alvo, congele `f:{0}->{0,1}` com `f(0)=0`, `g=id_{0,1}` e `h:{0}->{0,1}` com `h(0)=1`, correspondendo respectivamente a `a,b,c`.

- **Previsão ex ante:** a analogia quebra na composição, pois `g∘f ≠ h`.
- **Observação:** em `0`, `(g∘f)(0)=0`, mas `h(0)=1`.
- **Baseline:** structure-mapping + metamorphic/property test da lei preservada.
- **Collapse-test:** se a analogia nunca prometeu preservar `b∘a=c`, a diferença não é resíduo de analogia; se a lei foi escolhida depois, é retrospectiva.

É witness formal mínimo da ruptura antecipável, mas não de superioridade sobre o baseline.

## 5. Fronteira minimalidade–generatividade–residualidade — `NO-WITNESS`

O corpus fornece apenas um padrão desejado: uma família ordenada de schemas, gerador fixo, métricas independentes e uma mudança de regime fora da amostra. Não fornece valores congelados, gerador, tarefas retidas, curvas nem replicação em segundo domínio. Um exemplo fabricado por definição poderia impor a curva pretendida e seria circular.

- **Baseline forte:** MDL/information bottleneck/Pareto com os mesmos custos e métricas.
- **Observação discriminante necessária:** mudança de regime pré-localizada e replicada fora da amostra, excedendo o que o baseline já prevê.
- **Collapse-test:** “diversidade útil” ou resíduo definidos depois; curva explicada integralmente por complexidade; optimum instável à métrica; cardinalidade de fibra confundida com operação generativa.

Sem dados ou construção independente que satisfaça essas obrigações: `NO-WITNESS`.

## 6. Enriquecimento prospectivo por risco — `WITNESSED`

Congele duas ações `a,b`. A lente sem tempo registra somente dano imediato: `L0(a)=L0(b)=0`. O enriquecimento temporal registra traces: `E(a)=(0,0)` e `E(b)=(0,1)`, onde `1` é dano retardado. Congele antes da decisão a obrigação “dano acumulado no horizonte 1 deve ser zero”.

- **Previsão ex ante:** tempo é necessário e separará `a` de `b`; `a` é admissível, `b` não.
- **Observação discriminante:** os traces confirmam a diferença no passo futuro apesar da igualdade imediata.
- **Baseline forte:** FMEA/hazard analysis temporal.
- **Collapse-test:** se o horizonte ou dano retardado forem escolhidos depois, colapsa; se `L0` já contém traces, o enriquecimento é redundante; se a decisão não muda, não há witness operacional.

Há não-vacuidade estrutural, mas o baseline de risco seleciona a mesma estrutura.

## 7. Diagnóstico residual e classe de reparo — `WITNESSED`

Congele `X={a,b}`, schema comprimido `S={*}`, representação `R(a)=R(b)=*` e decoder `D(*)=a`. A probe round-trip é congelada antes do resultado.

- **Previsão ex ante:** o mismatch é de transformação/perda: `(D∘R)(b)=a≠b`; enriquecer apenas o alvo interpretativo sem refinar `R` não recuperará `b`. A classe de reparo é separar a fibra de `R`.
- **Observação discriminante:** round-trip passa em `a` e falha em `b`; com `S′={a,b}` e `R′=id`, passa nos dois.
- **Baseline forte:** troubleshooting por round-trip/ablation.
- **Collapse-test:** se a distinção `a≠b` não era relevante antes, não há falha; se o erro estiver no decoder apesar de `R` ser injetiva, o diagnóstico está errado; se reparo sem refinar a fibra resolver, a classe prevista colapsa.

É witness mínimo de diagnóstico residual não vazio; não supera o baseline.

## 8. Limite reflexivo/diagonalização — `NO-WITNESS`

Não há no corpus um sistema concreto com objeto de autorrepresentações, aplicação/evaluação, codificação da família relevante e hipótese formal de fixed point verificadas. “Self-reference revela limite” não fecha uma testemunha.

- **Baseline forte:** teorema clássico de Lawvere/Gödel/Turing aplicável ao sistema exato.
- **Observação discriminante necessária:** fixed point ou contraexemplo formal construído pelas hipóteses declaradas.
- **Collapse-test:** ausência de autorrepresentação/aplicação; diagonalização usada como nome para recursão; resultado integralmente importado do teorema sem consequência própria.

Logo: `NO-WITNESS` até que as estruturas formais sejam fornecidas.

## 9. Prediction ledger — `WITNESSED` (metodológico somente)

O repositório já possui criterion congelado antes do run, protocolos preregistrados e preservação de resultados negativos, segundo o retorno de precedentes preservado em `research.md`. Isso é uma testemunha operacional de que o ledger pode impedir reconstrução retrospectiva.

- **Input congelável:** claim, previsão, resultado excluído, baseline, métrica e collapse-test.
- **Observação:** comparação posterior entre registro e outcome.
- **Baseline:** narrativa não preregistrada ou criterion mutável.
- **Collapse-test:** criterion alterado após o outcome, resultados negativos descartados ou categorias residuais reclassificadas.

Esse witness valida infraestrutura metodológica, não poder preditivo da gramática. Para a investigação corrente, ainda não existe ledger executado com outcomes.

## Consequência para a matriz

O campo `witnessed?` pode ser preenchido como `yes` para enriquecimento/limite expressivo, composição/local–global, ruptura de analogia, enriquecimento por risco, diagnóstico residual e prediction ledger; como `no` para probe guiada por perfil residual, fronteira minimalidade–generatividade, e limite reflexivo. O writer deve manter inline a qualificação **“witness do fenômeno, não vantagem incremental”** nos cinco primeiros `yes` conceituais. O candidato de probe recebe typed negative: sob inputs e orçamento igualados, ou o perfil é derivável e redundante, ou contém informação adicional e a comparação não isola a gramática.

## Resposta de uma linha ao gate

A gramática tem instâncias formais não vazias para enriquecimento, composição, ruptura, risco e diagnóstico, mas ainda não possui witness de ganho preditivo incremental; seu candidato central de seleção de probes falha o gate atual sob paridade de informação.


## Retorno 4 — skeptic `definitional-soundness`

## Gate `definitional-soundness`

Escopo deste parecer: somente colapso definicional contra os owners já coletados. `SOUND` significa apenas que o candidato formula uma variável ou consequência incremental falsificável; não significa que exista witness, evidência, novidade ou vantagem empírica.

| candidato | resultado | owner/base equivalente | diferença mínima necessária para sobreviver |
|---|---|---|---|
| Seleção de probe guiada por perfil residual | **SOUND** | Bayesian experimental design; active learning; Blackwell comparison | O candidato contém uma hipótese incremental estreita: mantendo iguais hipóteses, informação disponível, custos e probes admissíveis, um perfil residual tipado e fixado antes do resultado muda a escolha e melhora discriminação, decisão ou custo. Para sobreviver empiricamente, o perfil precisa ter regra de formação independente, não ser função ou renomeação do posterior usado pelo baseline, e restringir a política a uma classe própria de probes. Se carregar informação adicional não oferecida ao baseline, ou apenas reexpressar o estado bayesiano, colapsa. |
| Discriminador de enriquecimento e limite expressivo | **TAUTOLOGICAL** | reduct/expansion; forgetful structure; invariantes; definability; feature ablation | Na formulação atual, “escolher `E` que separa o que `L0` identifica” é exatamente restaurar estrutura esquecida e testar um invariante dependente dela. A gramática não fornece regra própria que selecione `E`; apenas exige que alguma seleção aconteça. Para sobreviver, teria de derivar do kernel ou de uma assinatura residual uma classe estritamente menor de enriquecimentos, sem importar clandestinamente a estrutura discriminante, e produzir uma escolha diferente da análise ordinária de dependências/invariantes. |
| Falha composicional/local–global | **TAUTOLOGICAL** | assume-guarantee; compositional verification; constraint solving; sheaf obstruction; system dynamics | “Partes passam localmente, mas a composição viola uma obrigação global” já é o problema definido pelos owners. Chamar o contraexemplo ou obstrução de resíduo não acrescenta regra. Para sobreviver, a gramática teria de fornecer uma transformação comum e tipada que, preservando as semânticas específicas, antecipe qual interface ou obrigação falhará ou selecione corretamente o formalismo aplicável além do diagnóstico produzido pelo owner local. |
| Ruptura de analogia | **TAUTOLOGICAL** | structure-mapping; metamorphic testing | Correspondência relacional mais relações de preservação e teste da região onde elas falham já constitui structure-mapping acompanhado de teste metamórfico. “Resíduo de analogia” é somente o nome da violação. Para sobreviver, um perfil definido independentemente teria de restringir antecipadamente a região e o tipo de ruptura de modo não derivável das correspondências, invariantes e relações metamórficas já declaradas. |
| Fronteira minimalidade–generatividade–residualidade | **TAUTOLOGICAL** | MDL; rate-distortion; information bottleneck; bias–variance/Pareto | “Estrutura demais reduz liberdade; estrutura de menos perde distinções” é o trade-off conhecido entre complexidade e perda/relevância. A formulação corrente não fixa uma quantidade adicional nem uma lei diferente. Para sobreviver, precisaria definir custo composicional/de interface e um vetor residual pré-fixado que induzam uma ordenação ou mudança de regime impossível de reduzir, por escalarização ou mudança da função de perda, a MDL/IB/rate-distortion. |
| Enriquecimento prospectivo por risco | **TAUTOLOGICAL** | FMEA; hazard analysis; causal risk assessment; checklists regulatórios | Introduzir tempo, causalidade ou outra estrutura antes de uma ação arriscada porque um mecanismo relevante foi omitido é precisamente o trabalho da análise de risco. “Enriquecimento” apenas renomeia a estrutura requerida. Para sobreviver, a gramática teria de derivar do kernel e da obrigação de risco uma seleção de estrutura que altere prospectivamente uma decisão e não seja obtida pela análise de risco com as mesmas informações. |
| Diagnóstico residual e classe de reparo | **TAUTOLOGICAL** | diagnóstico diferencial; root-cause analysis; fault trees; ablation/troubleshooting | Um perfil de sintomas usado para reduzir causas e escolher o próximo teste é diagnóstico ordinário. Nenhuma regra própria associa atualmente os eixos residuais a causas ou reparos; por isso, como candidato separado, ele também duplica a seleção de probe. Para sobreviver, precisaria de um mapa pré-declarado e transportável `tipo residual → subconjunto próprio de causas → classe própria de intervenção`, com informação e custos igualados, cuja remoção elimine o ganho. |
| Limite reflexivo/diagonalização | **TAUTOLOGICAL** | Lawvere; esquemas clássicos de ponto fixo, Gödel e Turing | Autorrepresentação, avaliação e diagonalização produzindo um limite já é o conteúdo dos teoremas proprietários. Nomear a testemunha como “resíduo reflexivo” não acrescenta consequência. Para sobreviver, a gramática teria de construir internamente os objetos e mapas exigidos, demonstrar as hipóteses aplicáveis e derivar uma limitação específica do sistema que não seja mera paráfrase ou aplicação não especializada do teorema clássico. |
| Prediction ledger | **TAUTOLOGICAL** | preregistration; Registered Reports; criterion congelado já implantado | O ledger controla liberdade retrospectiva, mas não fornece poder preditivo nem operação própria da gramática. Como candidato teórico, duplica infraestrutura metodológica existente. Ele só pode sobreviver como mecanismo auxiliar, não como contribuição preditiva: poderia acrescentar um schema verificável para registrar tipos residuais, resultados excluídos e regras de seleção, mas a contribuição teria de vir das regras registradas, não do ledger. |

### Veredito do gate

Dos nove candidatos, apenas **seleção de probe guiada por perfil residual** é definicionalmente distinta o bastante para permanecer aberta: ela enuncia uma comparação incremental condicionada e falsificável. Ainda assim, sua identidade desaparece se o perfil residual for somente uma recodificação do estado informacional do baseline.

Os outros oito candidatos, nas definições atuais, são **TAUTOLOGICAL**: descrevem operações já pertencentes aos owners ou nomeiam seus resultados com o vocabulário da gramática, sem acrescentar regra de formação, variável independente ou consequência própria.

A tese sobrevivente deve, portanto, ser reduzida a:

> Condicionadas às mesmas hipóteses, informações, probes e custos, uma tipagem residual formada independentemente restringe a política de probe e produz uma consequência prospectiva diferente daquela produzida pelos baselines especializados.

Se a tipagem não for independente ou não alterar a política sob informação igualada, o último candidato também colapsa.

