# Skill control center UX research — collected returns

## Seat: `task_first_researcher`

### Integridade e escopo

- Canonicalização confirmada: `sort_keys=True`, `separators=(",", ":")`, UTF-8, `ensure_ascii=False`.
- SHA-256 obtido: `7cf476d3d6e6ca7bd90c0252f05bd31b4672377ecd969aebc886dc129769402e` — confere com o proposal.
- Todos os nove hashes de `local_source_manifest` conferem, incluindo os seis documentos deste seat.
- Pesquisa somente leitura; nenhum arquivo alterado, agente lançado ou mensagem externa enviada.

### Veredito

Abrir em um espaço de trabalho orientado a tarefa: lista de atenção e histórico filtrável como
superfície principal; árvore expansível apenas onde a ancestralidade for relevante; grafo como
explicação secundária, acionada por uma pergunta explícita de relação/caminho. Isso atende ao objeto
prioritário já definido localmente — o gate humano e as dispatches pendentes — sem negar que
relações e dependências devem ser inspecionáveis.

Não alego que listas são universalmente superiores a grafos. A conclusão é uma inferência
contextual, falsificável por teste de tarefas: se usuários encontrarem, compararem ou configurarem
objetos conhecidos mais rápida e corretamente a partir do grafo inicial, o default deve ser revisto.

### Perguntas que devem ser respondidas no primeiro paint

1. Há alguma proposta/dispatch pendente de confirmação humana? Qual requer atenção primeiro?
2. Qual é o estado operacional agora: aberto, fechado, erro, inconclusivo, parcial ou indisponível?
3. Que recorte estou vendo: repositório, período UTC, filtros, contagem carregada e possíveis exclusões?
4. Qual é a proveniência e o frescor: fonte, snapshot/manifesto, última observação e limite de frescor?
5. Esta relação ou métrica é declarada, observada, inferida, desconhecida/indisponível ou stale?
6. Quem/que configuração declarou a rota, e qual é a tensão de papéis, grupos e ângulos?
7. Onde está o próximo caminho seguro: abrir detalhe, comparar, rastrear caminho ou pedir confirmação — sem sugerir que a projeção possui autoridade?

### Modelo de interação recomendado

- **Default:** lista ordenada por atenção operacional, com filtros por repositório, estado, tipo,
  papel, evidência e recência. Pendências primeiro, depois abertos/alertas e então histórico.
- **Árvore:** dentro do detalhe quando a pergunta for “de que dispatch/pai/etapa isto deriva?”.
  Preferir disclosure semântico; usar `role=tree` somente quando necessário.
- **Grafo:** ação explícita “Explicar caminho/relações”, aberta com o item atual selecionado e retorno
  visível à lista. Destacar somente o caminho solicitado.
- Não mudar de visualização automaticamente. Seleção e filtros permanecem ao trocar de vista.

O grafo existente demonstra busca, filtros, seleção e relações declaradas, mas é evidência do limite
atual, não referência visual. Ele mistura relações explícitas e menções, usa interação pointer-first
no canvas e persiste rascunhos no navegador.

### Busca, filtros e destaque de caminhos

- Busca textual retorna lista e identifica o campo pesquisado.
- Filtros cumulativos visíveis: `repo`, estado, tipo, papel, `evidence_state`, período UTC e atenção.
- A seleção aponta para o mesmo objeto estável em todas as vistas.
- No grafo, caminho declarado, observado e inferido recebe linha e legenda próprias; nunca somente cor.
- “Sem resultados” informa o recorte e não pode ser interpretado como “não houve uso”.

### Limite seguro de configuração e recibos

A versão atual deve continuar leitora. Pode exibir configuração declarada, política, snapshot e
diff proposto, mas não salvar drafts como configuração oficial. Alteração/confirmação precisa sair
da projeção e passar pela autoridade apropriada. O recibo mínimo contém identidade do alvo, ator,
autorização, valores efetivos, versão, manifesto/hash, timestamp, resultado, evento/journal e frescor.
“Aceito” significa fato registrado; “enviado” e “rascunho” não significam confirmação.

### Estados de evidência

| Estado | Significado e apresentação obrigatória |
|---|---|
| `declared` | Fonte declarativa identificável; não prova execução. |
| `observed` | Journal/telemetria aceito; mostrar janela, fonte e cobertura. |
| `inferred` | Regra/fórmula, entradas e versão visíveis; nunca fato primário. |
| `unknown-or-unavailable` | Não retornado, não autorizado, não implementado ou sem cobertura; nunca zero/falso. |
| `stale` | Fora da SLA ou snapshot antigo; mostrar idade, limiar e último valor. |

Uma relação pode ser simultaneamente declarada e observada. Ausência de telemetria nunca é ausência
de uso.

### Frequência, recência, estados operacionais

Resumo por objeto: estado atual, contagem observada na janela, última observação UTC, frescor e
cobertura. Mini-séries exigem escala e período. `0 observed` somente com cobertura conhecida.
Loading, empty, error, degraded, profile-blocked e live-update devem preservar identidade, recorte,
último snapshot e impacto, sem expor prompts/logs brutos ou roubar foco.

### Cartões de alegação

| ID | Alegação | Classe | Fonte direta; tipo | Força e limite |
|---|---|---|---|---|
| C1 | Pendências humanas precedem histórico. | `repository-fact` | `implementations/UI-CONTRACT.md` | Forte para a Fase 1; revisável por novo contrato. |
| C2 | Projeções não mutam, reparam ou inferem fatos ausentes. | `repository-fact` | `docs/features/agent-provenance-telemetry/UI-SPEC.md` | Forte como fronteira; APT UI ainda deferred. |
| C3 | Primeiro paint preserva contexto essencial; detalhe é progressivo. | `repository-fact` | `research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md` | Restrição local forte; não decide layout. |
| C4 | Lista/busca/filtros são precedente para catálogos grandes. | `implemented-precedent` | [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/) | Média; precedente, não causalidade. |
| C5 | Busca deve declarar campos, filtros e paginação. | `implemented-precedent` | [Backstage Catalog API](https://backstage.io/docs/features/software-catalog/software-catalog-api/) | Média; depende do backend local. |
| C6 | Grafo é útil para execução selecionada e debug, não prova landing page. | `implemented-precedent` | [GitHub Actions — Monitor workflows](https://docs.github.com/en/actions/how-tos/monitor-workflows?tool=webui) | Média; domínio diferente. |
| C7 | Separar por quê, como e o quê melhora a especificação de tarefas. | `causal-usability` rebaixada a orientação | [Brehmer & Munzner, 2013](https://www.cs.ubc.ca/labs/imager/tr/2013/MultiLevelTaskTypology/) | Média; tipologia, não prova lista > grafo. |
| C8 | Overview, filtro, seleção, conexão e detalhe são complementares. | `causal-usability` rebaixada a taxonomia | [Heer & Shneiderman, 2012](https://doi.org/10.1145/2133806.2133821) | Média; não estabelece threshold. |
| C9 | Foco, nome/papel/valor e status determinável são requisitos. | `normative` | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Forte; não determina IA. |
| C10 | Árvore interativa exige semântica e teclado completos. | `normative` | [WAI-ARIA APG Tree View](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/) | Média-alta; APG é prática, não WCAG independente. |
| C11 | Propósito claro, tarefas encontráveis, busca, prevenção e feedback favorecem task-first. | `normative` | [W3C COGA Design Guide](https://www.w3.org/TR/coga-usable/design_guide.html) | Média; suplementar. |
| C12 | Proveniência e indisponibilidade devem ser explícitas. | `repository-fact` | `maestro-trama/.../dashboard-contracts-constitution.md` | Média; referência adjacente não autoritativa. |
| C13 | Task-first com grafo contextual é a síntese recomendada. | `inference` | C1, C3–C11 | Média; falsificada por benchmark local favorável ao grafo inicial. |

### Rubrica de aceitação

| Critério | Checks observáveis | Limiar proposto |
|---|---|---|
| Clareza | Identificar pendência, estado, recorte, proveniência/frescor e evidência. | 9/10 respostas corretas em até 30 s; cinco campos no first paint; zero inferência apresentada como fato. |
| Usabilidade | Buscar, filtrar, abrir detalhe, voltar, expandir ancestry e abrir caminho por teclado. | 100% dos fluxos críticos sem pointer; zero violações WCAG críticas. |
| Consistência visual | Mesmos estados, semântica, dados, ações e test IDs nas três variantes. | 100% do contrato funcional idêntico; distinção apenas visual. |
| Eficiência operacional | Localizar pendência/dispatch, filtrar erro, verificar observação e rastrear caminho. | Até 3 ações para pendência/objeto; até 5 para caminho/proveniência; medir fixture de ~700 dispatches. |

Confiança, compreensão profunda, carga cognitiva e prazer estético exigem avaliação humana.

### URL ledger

Aceitas:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C COGA Design Guide](https://www.w3.org/TR/coga-usable/design_guide.html)
- [WAI-ARIA APG Tree View](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)
- [Brehmer & Munzner, 2013](https://www.cs.ubc.ca/labs/imager/tr/2013/MultiLevelTaskTypology/)
- [Heer & Shneiderman, 2012](https://doi.org/10.1145/2133806.2133821)
- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Backstage Catalog API](https://backstage.io/docs/features/software-catalog/software-catalog-api/)
- [GitHub Actions — Monitor workflows](https://docs.github.com/en/actions/how-tos/monitor-workflows?tool=webui)

Rejeitadas: o viewer local como inspiração visual; agregadores `colab.ws` e DBLP quando havia fonte
primária.

## Seat: `topology_first_researcher`

### Integridade

- SHA-256 do proposal: `7cf476d3d6e6ca7bd90c0252f05bd31b4672377ecd969aebc886dc129769402e` — confere.
- Os nove hashes do manifesto conferem.
- Pesquisa procedimentalmente read-only, sem escrita, agentes ou mensagens externas.

### Veredito

Abrir em uma **topologia focal**, não lista nem hairball global: grafo declarado como estrutura
estável, seleção inicial explícita, vizinhança limitada e caminhos upstream/downstream legíveis.
Lista/grid é a superfície de busca e comparação; árvore somente para relação hierárquica, acíclica e
de pai único.

O objeto local é relacional: 70 skills, 262 arestas tipadas e 256 pares inclusivos. A lista localiza,
mas esconde dependentes, dependências, centralidade e caminhos. O grafo deve ter filtros, path
highlighting, painel de detalhes e alternativa integral por teclado. A topologia atual prova somente
relações declaradas: uso observado precisa de journal/telemetria separado.

### Registro de claims

| ID | Alegação | Classe | Fonte direta; tipo | Força e limite |
|---|---|---|---|---|
| C1 | O corpus possui 70 nós, 262 arestas tipadas e 256 pares inclusivos. | `repository-fact` | `experiments/skill-relationship-graph/graph.json` | Alta; extração textual, não execução. |
| C2 | UI deve separar ledger de campos derivados. | `repository-fact` | `implementations/UI-CONTRACT.md` | Alta; contrato da UI atual. |
| C3 | Catálogos separam fonte editável de relações/status processados. | `implemented-precedent` | [Backstage Catalog](https://backstage.io/docs/features/software-catalog/), [descriptor format](https://github.com/backstage/backstage/blob/master/docs/features/software-catalog/descriptor-format.md) | Alta como precedente, não UX causal. |
| C4 | Lineage graph pode ligar catálogo, filtros, materialização e detalhes. | `implemented-precedent` | [Dagster UI](https://master.dagster.dagster-docs.io/concepts/webserver/ui) | Alta como precedente; domínio diferente. |
| C5 | Seleção relacional pode expressar ancestrais, descendentes e profundidade. | `implemented-precedent` | [Dagster asset selection](https://master.dagster.dagster-docs.io/concepts/assets/asset-selection-syntax) | Alta; sintaxe pode ser especializada demais. |
| C6 | “Show paths” e relação direta/transitiva são operações de primeira classe. | `implemented-precedent` | [GitHub — Exploring dependencies](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/explore-dependencies) | Alta como precedente; página é list-led. |
| C7 | Grafos precisam de limite, stats, detalhes e troca de layout. | `implemented-precedent` | [Grafana Node graph](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/node-graph/) | Alta; 200 nós não garantem legibilidade de 262 arestas. |
| C8 | Interações devem seguir intenção: select, explore, reconfigure, elaborate, filter, connect. | `causal-usability` rebaixada a taxonomia | [Yi et al., 2007](https://doi.org/10.1109/TVCG.2007.70515) | Moderada; não prova graph-first. |
| C9 | Grafo customizado exige teclado, foco e estado programático. | `normative` | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Alta; não prescreve layout. |
| C10 | Eventos observados carregam identidade, tempo, produtor e contexto. | `implemented-precedent` | [OpenLineage facets](https://openlineage.io/docs/spec/facets/) | Alta como envelope precedente; não autoridade local. |
| C11 | Topologia focal com lista/grid simétrica é a recomendação. | `inference` | C1–C10 | Moderada-alta; falsificável por benchmark task-first. |

### Respostas às perguntas compartilhadas

1. First paint: skills existentes/seleção; dependências; caminhos; estado da evidência; uso realmente
   observado; cobertura/frescor; mudança pendente e autoridade necessária.
2. Default: grafo focal direcionado, 1 hop em cada direção. Grid para localizar/ordenar/comparar;
   tree somente para relação de pai único; vista global sempre explícita.
3. Busca por nome, descrição, path e tags; filtros por direção, relação, profundidade,
   source/sink/isolated, evidência, janela, status e frescor; ação “Mostrar caminhos” entre A e B.
4. Preferências pessoais reversíveis não requerem autoridade; alteração declarativa usa draft,
   revision/hash, diff e validações; alteração executável requer capability, confirmação e
   append-before-ack.
5. Evidência não é enum exclusiva: uma relação pode ser `declared` e `observed`; `stale` qualifica
   frescor. Ausência de telemetria é `unknown-or-unavailable`.
6. Geometria declarada fica estável; frequência observada usa espessura/arc com escala; recência usa
   `last seen` e série; status usa ícone/forma/texto. Toggle separa estrutura, uso e comparação.
7. Loading/empty/error/degraded preservam último snapshot e saúde por fonte; falha de métricas não
   derruba estrutura; SSE down não pode fingir live.

### Rubrica de aceitação

| Critério | Checks | Threshold proposto |
|---|---|---|
| Clareza | Seleção, upstream/downstream, estados, frescor/cobertura. | ≥90% corretas; lineage ≤20 s mediana. |
| Usabilidade | Localizar, path A→B, trocar vista, recuperar filtro, teclado. | ≥90% completion; busca→seleção ≤15 s P75; zero keyboard traps. |
| Consistência visual | Mesma semântica/legenda/estados nas três variantes. | 100% dos estados; zero divergência semântica; contraste aplicável AA. |
| Eficiência operacional | Fixture 70/262, busca, filtro, path e degradação. | first meaningful paint ≤1,5 s P95; filtro/seleção ≤100 ms P95; path ≤250 ms P95; zero long task >200 ms. |

Benchmark: localizar objeto, explicar dependências, encontrar caminho, comparar uso, diagnosticar
stale e revisar diff. Topology-first é aceito se perder menos de 10 p.p. em localização e ganhar
≥25% no tempo mediano de lineage/path sem reduzir correção.

### Candidatas de direção visual — não decisões

1. Atlas estratificado: topologia em faixas e path como rota.
2. Tear de sinais: skills em colunas funcionais e relações como fios.
3. Constelação operacional: nós focais, anéis declarados/observados e ledger inferior.

As três preservam API, fixtures, test IDs, estados e thresholds; não podem reutilizar composição,
CSS ou linguagem visual das variantes existentes.

### URL ledger

Aceitas:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Yi et al., 2007](https://doi.org/10.1109/TVCG.2007.70515)
- [Grafana Node graph](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/node-graph/)
- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Backstage descriptor format](https://github.com/backstage/backstage/blob/master/docs/features/software-catalog/descriptor-format.md)
- [Dagster UI](https://master.dagster.dagster-docs.io/concepts/webserver/ui)
- [Dagster asset selection](https://master.dagster.dagster-docs.io/concepts/assets/asset-selection-syntax)
- [GitHub Exploring dependencies](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/explore-dependencies)
- [OpenLineage facets](https://openlineage.io/docs/spec/facets/)

Rejeitadas: páginas comerciais quando existia documentação operacional; marketplace de terceiros;
agregadores; Wikipedia; Reddit; issues exploratórias; documentação legacy quando havia fonte oficial
corrente.
