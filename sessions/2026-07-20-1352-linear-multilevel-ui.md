---
tags: [agents, orchestration, control-plane, ledger, ui]
node_type: spec
is_session: true
layer: architecture
nature: technical
status: active
created: 2026-07-20
timestamp: 2026-07-20T13:52:00-03:00
expires: 2026-09-18
conversation_id: 56e14c26-9c5b-434b-861f-6aee74e58eaa
decisions_made: true
contradictions_found: true
specs_updated: [implementations/UI-CONTRACT.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Entregou a superfície de feature que o humano precisa para avaliar (IA de 3 níveis + diagrama de topologia) e fechou defeitos reais de confiabilidade/segurança, mas o keystone da Fase 2 (produtor de sheet pendente / POST /confirm) segue intocado, então o control plane ainda não age como o gate humano que deveria ser."
---

# UI linear multinível + endpoints de agregação

## Summary

A sessão começou como um pedido para tirar a "desajeitice" da UI linear plana
dando-lhe níveis de exibição, e cresceu para uma reconstrução multinível mais a
agregação de backend que os níveis exigiam. Decidiu-se uma arquitetura de informação
em três níveis roteada por `location.hash`: um painel (sheets pendentes primeiro,
faixa "hoje", grade de repos com contagem por `dispatch_type`), um drill-down por repo
(plot SVG empilhado por dia/tipo, filtros, lista completa) e uma visão por dispatch
cujo centro é um diagrama de topologia (grupos, agentes por role, `robot_talks` como
interconexão intra-grupo, arestas tipadas `sequential`/`zig-zag`/`feedback` com
`loop_cap`, objetivo e eixos de anti-viés). Dois endpoints somente-leitura foram
adicionados — `/api/overview` e `/api/repo/{name}` — com um cache de parse chaveado em
`(st_mtime_ns, st_size)`, enquanto `/api/snapshot`, `/api/stream` e `/api/dispatch`
foram mantidos byte-idênticos para não quebrar as outras nove variantes de UI nem o
contrato Playwright compartilhado. O referencial de dia foi decidido como **UTC** (para
servidor e todo cliente concordarem em qual barra uma row cai) e, como o usuário é
UTC-3, declarado na tela em vez de implícito. Cada build foi revisado por pares de
subagentes opostos por **fonte de autoridade** (contrato escrito vs comportamento
executado), e as revisões acharam defeitos reais. Corrigidos: o `stat()` de
`read_pending` ficava fora do `try` e podia dar 500 em todos os endpoints de leitura e
matar o gerador SSE; `join_rows` quebrava em id não-hashável contra o próprio princípio
leniente do módulo; a camada `main.py` inteira não tinha teste (novo `tests/test_main.py`);
UTC não era declarado; e o contrato desatualizado já tinha feito o fallback da UI
reimplementar as agregações com semântica divergente (dia local vs UTC, `reserved`
incluindo legacy), agora reconciliada. Path traversal em `/api/repo/{name}` foi atacado
(60 vetores) e está fechado; o revisor empírico não reproduziu o ganho de cache de ~35x
alegado (real ~6x; latência morna dominada por varreduras de diretório não-cacheadas,
desde então de-duplicadas). Dois follow-ups pontuais entraram: os nós de agente no
diagrama agora abrem por clique/teclado o `initial_prompt` inteiro num modal com foco
gerenciado, e `robot_talks`/`zig-zag`/`feedback` ficaram descobríveis via badges no
nível 1 e um filtro (o "não vejo" do usuário era ausência nos dispatches amostrados, não
bug de render — os dados reais têm 117/161/88). Uma regressão de doc introduzida nesta
sessão foi pega e corrigida: agentes de revisão leram errado `append-dispatch.cjs` e
tiraram `synthesizer` do enum de role no `UI-CONTRACT.md`, sendo que o appender de fato
aceita `explorer|synthesizer|skeptic|writer|auditor`. O store de sheets pendentes segue
ligado ponta-a-ponta mas **sem produtor**, então a superfície do gate humano ainda
observa só o fixture de demonstração até a Fase 2.

## Contradictions

- contradicts `.claude/skills/register-dispatch/SKILL.md` — esta sessão registrou seis
  dispatches todos de `dispatch_type: "code"` (tipo RESERVED), cada um puxando o aviso
  "RESERVED ... recording anyway" do appender, enquanto a skill diz que registrar um
  tipo RESERVED "signals an upstream violation". Mas o hook PreToolUse instalado exige
  registro a cada dispatch de Agent e nenhum tipo LIVE cobre trabalho de tooling/UI —
  então a regra escrita e a prática imposta se refutam a cada dispatch do projeto. Reforça
  a mesma aresta da sessão anterior com contagem de primeira mão.

## Open questions

- O referencial UTC é o certo, ou o dia deveria ser o **local** (UTC-3) do usuário com o
  servidor carregando um tz explícito — isto é, "concordância entre observadores" é a
  invariante certa quando há efetivamente um observador só? A sessão declarou UTC e o
  tornou honesto na tela, mas não decidiu se é a escolha certa.
- A distinção `zig-zag` vs `feedback` aguenta sem cor? O implementador sinalizou (palpite)
  que em arestas muito curtas a diferença de forma fica sutil; não foi decidido se precisa
  de rótulo de tipo sempre-visível no meio de cada aresta.

## Next steps

1. Construir o **produtor de sheet pendente** (escrever `telemetry/agents/pending/<id>.json`
   pré-confirm) + `POST /confirm`, para o gate observar sheets reais e não só o fixture;
   então apagar o fixture de demonstração.
2. Reconciliar o `buildSeries` do fallback ao `daily_series` do servidor (clampar o eixo
   ao hoje-UTC, computar `out_of_range`/`truncated_span`), para o caminho degradado não
   escalar errado — hoje um gap menor sobre a janela de 40 rows do snapshot.
3. Escolher a variante de UI e remover as outras nove (herdado da sessão anterior; o
   trabalho de três níveis entrou só na `linear`).

## Recommendation

O keystone é o passo 1, o produtor de pendentes — a UI do gate agora existe em três
níveis mas observa um store vazio, então toda a sua razão de ser fica não-realizada até
uma sheet poder ser escrita pré-confirm. O fato que licencia isso é de primeira mão: esta
sessão renderizou o painel do gate e ele mostrou só o fixture `_example`. Mas o passo 1
não deve preceder a resolução da aresta de Contradictions acima: ela mostra que o projeto
já escreve no ledger dispatches que a regra escrita diz não deverem existir, e um produtor
que grava um artefato pré-confirm herdaria exatamente essa frouxidão de disciplina de
escrita. Resolver a aresta antes de construir o produtor, não depois.

## Files touched

- implementations/server/ledger.py
- implementations/server/main.py
- implementations/server/config.py
- implementations/tests/test_ledger.py
- implementations/tests/test_main.py
- implementations/static/ui/linear/index.html
- implementations/UI-CONTRACT.md
- implementations/README.md
- telemetry/agents/subagents-dispatch.yaml
