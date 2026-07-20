# Contrato de UI — Fase 1 (leitor)

Todas as variantes consomem a mesma API e obedecem os mesmos `data-testid`, para
que um único teste Playwright rode contra as dez. **Só a estética varia.**

## Onde o arquivo mora

`implementations/static/ui/<slug>/index.html` — **um único arquivo autocontido**.
CSS e JS inline. **Zero dependência externa** (sem CDN, sem fonte remota, sem
build): a página tem que abrir offline. Use apenas fontes do sistema
(`ui-monospace`, `Georgia`, `system-ui`, etc.).

## API

| Endpoint | O que devolve |
|---|---|
| `GET /api/snapshot` | O estado inteiro, janela recente por repo (ver forma abaixo). |
| `GET /api/stream` | SSE. Emite `event: snapshot` com o mesmo payload sempre que o disco muda. Conecte com `EventSource` e re-renderize. |
| `GET /api/dispatch/{repo_name}/{dispatch_id}` | Uma dispatch sem truncar os prompts (para um painel de detalhe). 404 se o repo/id não existe; 500 se o ledger existe mas não pôde ser lido. |
| `GET /api/overview` | Painel de topo: agregados de TODOS os repos + o que pede atenção humana (ver forma abaixo). Nada é truncado por `limit`. |
| `GET /api/repo/{repo_name}` | Drill-down de um repo: histórico COMPLETO em peso de listagem (rows `slim`), mais `summary` e `series`. Filtros opcionais `?state=open\|closed\|all` e `?type=<dispatch_type>` (ver a ASSIMETRIA abaixo). 404 se o repo não existe; 422 se `state` está fora do enum. |

**Convenção do prefixo `_` (escopada a objetos com FORMA DE ROW):** num objeto que
compartilha o namespace de uma row do ledger (uma dispatch, uma sheet), todo campo
com prefixo `_` é calculado pelo leitor e os demais vêm literalmente do ledger — o
`_` existe para um campo calculado nunca sombrear uma chave real do ledger (ex.:
`status` nas rows pré-v0.5.2). A regra NÃO vale para objetos-contêiner/agregado que
não são rows (`summary`, `series`, `totals`, `attention`): eles não têm namespace de
ledger a proteger e por isso devolvem chaves sem prefixo de propósito (`total`,
`open`, `by_type`, ...).

### Referencial de DIA — UTC

`today`, o `_day` de cada dispatch e os buckets de `series["days"]` são **dias de
calendário em UTC**, não no fuso do navegador. É deliberado: servidor e todos os
clientes precisam concordar em qual barra do gráfico uma row cai. Se um cliente
usasse o dia LOCAL, a mesma row pularia de bucket dependendo de quem olha, e "hoje"
da UI divergiria do `_day` das rows por algumas horas todo dia. Derive o dia do
campo `_day`/`today` que a API já dá — **não** recompute a partir de `created` com
`new Date()` no fuso local.

### Forma do `/api/snapshot`

```jsonc
{
  "repos": [
    {
      "name": "domainspec-lean-formalization",
      "path": "C:\\Users\\victo\\...",
      "ledger_exists": true,
      "total_dispatches": 334,      // total no ledger
      "open_dispatches": 23,        // sem close row
      "warnings": ["linha 13: ..."],// rows antigas ilegíveis (não-fatal)
      "error": null,                // falha fatal de leitura
      "pending": [ /* sheets pré-confirm — ver abaixo */ ],
      "dispatches": [ /* as N mais recentes, mais nova primeiro */ ]
    }
  ],
  "config": { "limit": 40, "poll_seconds": 1.0, "repo_count": 11 }
}
```

### Uma dispatch

```jsonc
{
  "dispatch_id": "2026-06-12-residue-precedent-sweep",
  "schema_version": "0.6.0",
  "created": "2026-06-12T18:00:00.000Z",
  "invoked_by": "victorboscaro@gmail.com",
  "dispatch_type": "research",        // research|code|review|plan|suggestion|experiment
  "goal": "…",
  "context": "…",
  "max_loops": 1,
  "final_approver": "parent",
  "anti_bias_global": "otimismo de novidade vs ceticismo de precedente",
  "working_folder": "research/…/",
  "groups": [
    {
      "group_id": "explorers",
      "n": 2,
      "anti_bias": "corpus de origem (literatura formal vs blogs de prática)",
      "robot_talks": false,            // opcional
      "layers": 1,                     // opcional
      "agents": [
        {
          "agent_name": "Abramsky, Samson",   // pode ser null
          "role": "explorer",                 // explorer|synthesizer|skeptic|writer|auditor (enum do appender)
          "model": "claude-sonnet-5",
          "token_budget": 800,
          "angle": "fica com o lado da literatura formal",
          "initial_prompt": "…",
          "_prompt_truncated": true           // presente só se cortado
        }
      ]
    }
  ],
  "connections": [
    { "from": "explorers", "to": "synthesizer", "type": "sequential" },
    { "from": "skeptic", "to": "synthesizer", "type": "feedback", "loop_cap": 2 }
  ],

  // calculados pelo leitor:
  "_state": "open",        // "open" | "closed"
  "_live": true,           // dispatch_type é LIVE (research/review/experiment)
  "_legacy": false,        // row pré-v0.5.2, sem `groups`
  "_agent_count": 3,
  "_orphan_close": true,   // presente só em close row sem dispatch row
  "_close": {              // null enquanto aberta
    "close_of": "…",
    "closed": "2026-06-12T19:00:00.000Z",
    "exit_reason": "resolved",  // resolved|loop_ceiling_reached|dissent_irreconcilable|user_abort|error
    "agents_spawned": { "total": 3, "tree": {"explorer": 2}, "loops_used": 1 },
    "feedback_prompts": ["…"]
  }
}
```

### Uma sheet pendente

```jsonc
{
  "_file": "2026-07-19-exemplo.json",
  "_path": "C:\\…\\telemetry\\agents\\pending\\2026-07-19-exemplo.json",
  "_mtime": 1752900000.0,
  "_error": null,
  "_agent_count": 4,
  "_live": true,
  "sheet": { /* mesma forma da dispatch, SEM os campos `_` nem `_close` */ }
}
```

> `_mtime` é `null` (em vez de um float epoch) quando `_error` está setado — a
> sheet sumiu/ficou ilegível entre a varredura e a leitura.

### Forma do `/api/overview`

Agregados de TODOS os repos + as filas de atenção humana. Nada truncado por `limit`.

```jsonc
{
  "repos": [ /* um objeto `summary` por repo — ver forma abaixo */ ],
  "totals": {
    "repos": 11,
    "total": 703, "open": 43, "closed": 660, "pending": 1,
    "by_type": { "research": 500, "review": 140, "(sem tipo)": 55 },  // soma por repo
    "today": { "created": 3, "closed": 1 }                            // dia UTC
  },
  "today": "2026-07-20",           // dia de HOJE em UTC
  "attention": {
    "pending": [ /* sheet pendente + "_repo": "<nome>" */ ],
    "open_today": [ /* dispatch `slim` + "_repo", aberta e com _day == today */ ],
    "open_all":  [ /* dispatch `slim` + "_repo", toda aberta; no MÁX. 200 */ ],
    "_capped": true,               // presente SÓ quando open_all passou de 200
    "_open_all_total": 253         // presente SÓ quando capado — o total real
  },
  "config": { "limit": 40, "poll_seconds": 1.0, "repo_count": 11 }
}
```

Cada objeto em `repos` (e o `summary` de `/api/repo`) — o agregado de um repo:

```jsonc
{
  "name": "domainspec-core", "path": "C:\\…", "ledger_exists": true, "error": null,
  "warning_count": 0,             // quantas rows antigas geraram aviso
  "total": 181,                   // todas as rows joinadas (não a janela `limit`)
  "open": 5, "closed": 176,
  "legacy": 12,                   // rows pré-v0.5.2 (sem `groups`)
  "by_type": { "research": 150, "review": 20, "(sem tipo)": 11 },
  "live": 170,                    // dispatch_type LIVE (research/review/experiment)
  "reserved": 4,                  // tipo não-LIVE e não-legacy
  "pending_count": 0,
  "today": { "created": 0, "closed": 0 },
  "open_now": 5,                  // == open (nome próprio; pode divergir na Fase 2)
  "first_day": "2026-01-01", "last_day": "2026-07-19",  // dias UTC
  "last_created": "2026-07-19T20:00:00.000Z"            // ISO cru mais recente
}
```

> **Não é partição:** `total == live + reserved + legacy` **não** é garantido. Uma
> research row cujo `groups` falhou no parse leniente fica sem `groups` e conta em
> `live` E em `legacy` ao mesmo tempo. Não renderize os três como fatias de um todo.

### Forma do `/api/repo/{repo_name}`

```jsonc
{
  "name": "domainspec-core", "path": "C:\\…", "ledger_exists": true, "error": null,
  "warnings": [ "linha 13: …" ],
  "summary": { /* mesma forma do objeto de `repos` acima — SEMPRE o repo inteiro */ },
  "series": { /* histograma diário — ver abaixo */ },
  "pending": [ /* sheets pendentes deste repo */ ],
  "dispatches": [ /* rows `slim`, mais nova primeiro; ESTA lista é filtrada */ ]
}
```

**ASSIMETRIA deliberada:** `?state=` e `?type=` filtram **só** `dispatches`. O
`summary` e a `series` descrevem sempre o repo inteiro — o gráfico é o pano de
fundo estável, a lista é o recorte. Se a série encolhesse junto, o eixo mudaria de
escala a cada clique.

A lista `dispatches` é **`slim`** (contagens em vez de prompts, e `_close`
enxuto): é lossy para as chaves antigas das rows legacy. Para a row inteira (todos
os campos, prompts sem corte), peça `GET /api/dispatch/{repo}/{dispatch_id}`.

Uma row `slim`:

```jsonc
{
  "dispatch_id": "…", "created": "…Z", "_day": "2026-06-12",  // _day é UTC
  "dispatch_type": "research", "goal": "… (cortado em ~240 chars)",
  "invoked_by": "…", "working_folder": "…", "max_loops": 1,
  "final_approver": "parent", "anti_bias_global": "…",
  "_state": "open", "_live": true, "_legacy": false, "_agent_count": 3,
  "_close": { "closed": "…Z", "exit_reason": "resolved" },  // null enquanto aberta
  "_goal_truncated": true,        // só se o goal foi cortado
  "_orphan_close": true,          // só em close row órfã
  "_group_count": 2, "_robot_talks": false,
  "_roles": { "explorer": 2, "writer": 1 },
  "_connection_types": [ "feedback", "sequential" ]
}
```

O histograma `series` (de `daily_series`):

```jsonc
{
  "days": [ "2026-06-01", "2026-06-02", … ],  // contíguos, UTC; borda superior = hoje
  "types": [ "research", "review" ],          // ordenado
  "series": { "research": [1,0,2,…], "review": [0,1,0,…] },  // alinhado a `days`
  "totals": { "research": 42, "review": 8 },  // só o que está PLOTADO
  "max_day": 5,                               // a coluna empilhada mais alta
  "undated": 3,                               // rows sem dia legível
  "out_of_range": 1,                          // rows datadas fora da janela…
  "truncated_span": false                     // …(cap de 1000 dias, futuro, ou days=N)
}
```

> Invariante: `sum(totals) + out_of_range + undated == total de rows`. Uma data no
> futuro distante (typo de século) não ancora o eixo — vira `out_of_range`.

## O que a tela precisa comunicar

Em ordem de importância — a UI existe para o **gate humano**:

1. **Sheets pendentes em primeiro lugar, com destaque forte.** É a proposta
   aguardando confirmação: o objeto mais importante da tela. Se houver zero,
   diga isso explicitamente em vez de deixar vazio.
2. **Botão "Disparar" em cada sheet pendente — `disabled`**, com o rótulo
   deixando claro que é Fase 2 (ex.: título "confirmar dispara na Fase 2").
   Ele marca o lugar do gate; ainda não funciona.
3. **Aberta vs fechada.** Uma dispatch sem close row está viva. Ao fechar,
   mostre o `exit_reason` (`resolved` é bom; `error` e
   `dissent_irreconcilable` merecem cor de alerta).
4. **Grupos e agentes**: papel, modelo, orçamento de tokens, `agent_name`, e o
   **`angle`** de cada agente contra o **`anti_bias`** do grupo. O eixo de
   tensão é conteúdo de primeira classe, não decoração.
5. **`connections` como arestas tipadas**: `sequential`, `zig-zag`, `feedback`
   precisam ser visualmente distintos; mostre `loop_cap` quando houver.
6. **LIVE vs RESERVED.** Só `research`, `review` e `experiment` são LIVE.
   `code`, `plan`, `suggestion` são reservados — marque-os visivelmente.
7. **Rows legacy** (`_legacy: true`, sem `groups`) e **`_orphan_close`** devem
   aparecer como o que são, não sumir.
8. **Avisos e erros por repo** acessíveis (podem ficar recolhidos).
9. **Indicador de conexão ao vivo** (SSE conectado / caído).
10. Filtro ou agrupamento por repo — são 11 repos e ~700 dispatches.

## `data-testid` obrigatórios

O teste Playwright é o mesmo para as dez. Sem estes atributos, a variante falha.

| testid | Onde |
|---|---|
| `app` | Elemento raiz, depois do primeiro render. |
| `live-indicator` | Estado do SSE. Deve conter o texto `conectado` quando ligado. |
| `pending-list` | Contêiner das sheets pendentes (existe mesmo com zero). |
| `pending-card` | Um por sheet pendente. |
| `dispatch-button` | Um por sheet pendente, `disabled`. |
| `dispatch-list` | Contêiner do histórico. |
| `dispatch-card` | Um por dispatch renderizada. |
| `repo-section` | Um por repo exibido (ou por grupo de repo). |
| `total-count` | Elemento cujo texto contém o total de dispatches. |

Além disso, cada `dispatch-card` deve carregar
`data-dispatch-id="<dispatch_id>"` e `data-state="open|closed"`.

## Regras

- Português nos rótulos.
- Tem que aguentar `null`/ausente em quase tudo: rows antigas não têm `groups`,
  `agent_name` pode ser `null`, `connections` pode não existir.
- ~700 dispatches no total — não trave a página; a API já limita a 40 por repo.
- Nada de escrever: é um leitor.
