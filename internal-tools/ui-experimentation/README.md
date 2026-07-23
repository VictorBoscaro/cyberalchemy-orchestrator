# UI Experimentation — 10 visualizadores de dispatch

Dez telas standalone (HTML puro, sem servidor obrigatorio) para **ver os dispatches que
tem estrutura de grafo, escolher um, clicar e ver os agentes e seus dados de forma bonita**.

Cada variante e um arquivo unico (CSS + JS inline). Todas compartilham o **mesmo
comportamento** (governado pela Frontend Constitution, `CONST-FE`), mas cada uma tem uma
**linguagem visual distinta** e uma **geometria de grafo distinta**. Esse e o eixo do
experimento: *diversidade estetica ⊥ consistencia de comportamento*.

## O que cada tela faz

1. **Lista so os dispatches com estrutura real** — grupos cujos agentes formam um grafo
   (2+ agentes, e/ou um papel revisor/cetico/auditor, e/ou `connections`). Dispatches
   triviais (1 agente sem arestas) sao filtrados fora na extracao.
2. **Clicar num dispatch → renderiza o grafo** — nos de agentes agrupados por grupo,
   revisores/ceticos/auditores marcados, e as arestas tipadas (`connections`) ligando os
   grupos (quem revisa o que).
3. **Clicar num no de agente → painel** com os dados do agente: papel, modelo,
   `token_budget`, `agent_name`, `angle`/tensao e o `initial_prompt` **completo**
   (colapsado por padrao, revelado sob demanda).

## CONST-FE honrado por todas as variantes

- **FE-1** densidade opt-in: o `initial_prompt` nunca aparece no grafo; abre no painel e o
  texto completo so aparece ao clicar em "Revelar prompt inicial completo".
- **FE-2** um unico sistema de tooltip (`#tt` + `data-tip`): tipo de aresta, eixo
  anti-vies e metadados ficam no hover, nao em rotulos permanentes.
- **FE-3** dispensa instantanea: `Esc` e clique-fora fecham o painel sem delay (sem
  `setTimeout` de fechamento).
- **FE-5** tres estados: carregando, erro (com "Tentar novamente"), vazio (mensagem em
  pt-BR). Nunca uma superficie em branco.
- **FE-6** um foco por vez: abrir um agente fecha o anterior; trocar de dispatch fecha o
  painel.
- **FE-9** marcador discreto de auto-explicacao: o `?` no canto liga o *modo explicacao*;
  nele, o hover num no revela "o que e + por que importa" em vez do tooltip padrao.

## As 10 variantes

| # | Arquivo | Linguagem visual | Geometria do grafo |
|---|---------|------------------|--------------------|
| 01 | `variants/blueprint.html` | planta tecnica ciano sobre azul-marinho, grade milimetrada | colunas |
| 02 | `variants/editorial.html` | jornal impresso serifado, tinta sobre creme, fios/capitulares | faixas |
| 03 | `variants/terminal.html` | CRT fosforo verde, monospace, scanlines | linha do tempo |
| 04 | `variants/brutalist.html` | neo-brutalista, bordas pretas grossas, sombras duras | disperso |
| 05 | `variants/glass.html` | glassmorphism, paineis foscos sobre gradiente aurora | radial |
| 06 | `variants/orbital.html` | sistema orbital, espaco profundo, aneis concentricos | orbital |
| 07 | `variants/swiss.html` | estilo suico, Helvetica, vermelho-preto-branco, grade rigida | faixas |
| 08 | `variants/mission.html` | console de operacoes escuro, ambar + teal, telemetria | radial |
| 09 | `variants/sketch.html` | caderno desenhado a mao, papel quadriculado, bordas irregulares | disperso |
| 10 | `variants/mono.html` | monocromatico minimo, linhas finas, muito espaco | colunas |

(Variantes que compartilham geometria tem CSS, tipografia e forma-de-no completamente
diferentes — a linguagem visual e distinta em todas as 10.)

## Estrutura da pasta

```
ui-experimentation/
├── index.html            # galeria com link para as 10 variantes
├── README.md             # este arquivo
├── extract.py            # le o ledger YAML → data/dispatches.json (+ .js)
├── build_variants.py     # gera variants/*.html a partir de um motor compartilhado
├── review_audit.py       # auditoria CONST-FE (o passo de revisao)
├── data/
│   ├── dispatches.json    # corpus extraido (fonte canonica que o HTML consome)
│   └── dispatches.js      # mesmo payload como window.__DISPATCHES__ (fallback file://)
└── variants/             # os 10 visualizadores standalone
```

## Como ver

- **Servido** (recomendado): `python -m http.server` na raiz desta pasta e abrir
  `index.html`. Cada variante faz `fetch('../data/dispatches.json')`.
- **Duplo-clique** (`file://`): navegadores bloqueiam `fetch` de arquivo local; por isso
  cada HTML tambem carrega `data/dispatches.js`, que popula `window.__DISPATCHES__` como
  fallback. Funciona sem servidor.

## Dados

`data/dispatches.json` e extraido de `telemetry/agents/subagents-dispatch.yaml` por
`extract.py`. Dos **46** dispatches estruturados encontrados, os **8 mais ricos**
(por numero de agentes, arestas, revisores e volume de prompt/angle) formam o corpus. O
`initial_prompt` e o `angle` sao preservados **na integra** — sao eles o payoff clicado.

Para regenerar tudo:

```bash
python extract.py         # ledger → data/
python build_variants.py  # data/ → variants/ + index.html
python review_audit.py    # auditoria CONST-FE
```
