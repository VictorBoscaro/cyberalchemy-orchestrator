# implementations — dispatch control plane

**Fase 1: o leitor.** Um servidor FastAPI que lê, ao vivo, as sheets pendentes
(pré-confirm) e o histórico de dispatches dos ledgers append-only espalhados
pelos repos. Dez variantes de UI sobre a mesma API.

> **Somente leitura.** Nada aqui escreve no ledger — ele pertence ao appender da
> skill `register-dispatch`. O botão "Disparar" existe em todas as UIs, mas está
> `disabled`: ligá-lo é a Fase 2.

## Rodar

```sh
pip install -r requirements.txt
cd implementations
python -m server.main
# http://127.0.0.1:8765
```

A raiz serve o hub de seleção das dez variantes.

## Por que existe

O ledger só é escrito **depois** do confirm humano (a skill `register-dispatch`
é explícita: *"Only after the human's explicit confirm of the sheet"*). Logo uma
UI que lê apenas o ledger **sempre chega tarde** — ela mostra o que já foi
disparado e nunca pode *ser* o gate.

A peça que faltava é um artefato **pré-confirm**. Daí
`telemetry/agents/pending/<dispatch_id>.json`: a sheet que o humano revisa antes
de confirmar. Ela é a única superfície editável; o ledger continua append-only e
intocado.

## Estrutura

| Caminho | O quê |
|---|---|
| `server/ledger.py` | Leitor do ledger. Parse estrutural, leniente, nunca escreve. |
| `server/config.py` | Quais repos observar (auto-descoberta por padrão). |
| `server/main.py` | FastAPI: `/api/snapshot`, `/api/stream` (SSE), `/api/dispatch/{repo}/{id}`, `/api/overview` (agregados de todos os repos + filas de atenção), `/api/repo/{name}` (drill-down: histórico completo `slim` + `summary` + `series`, com filtros `?state=`/`?type=`). Formas completas em `UI-CONTRACT.md`. |
| `static/index.html` | Hub de seleção das variantes. |
| `static/ui/<slug>/` | Uma variante de UI, autocontida num arquivo. |
| `UI-CONTRACT.md` | Contrato normativo das UIs: API, forma dos dados, testids. |
| `tests/test_ledger.py` | Testes do parser + smoke contra os ledgers reais. |
| `tests/test_ui.py` | Playwright: o mesmo contrato contra as dez variantes. |

## Configuração

Sem `config.json`, o servidor **auto-descobre**: varre o diretório pai do repo
atrás de qualquer pasta com `telemetry/agents/`. Para fixar a lista, copie
`config.example.json` para `config.json`.

## Duas decisões que os dados reais forçaram

**1. O leitor é leniente; o appender é estrito.** O appender recusa escrever num
ledger corrompido — ele *protege* o arquivo. O leitor tem o trabalho oposto:
mostrar o que existe. O ledger do `domainspec` contém rows antigas prettificadas
(JSON multi-linha, vírgulas finais) que o appender rejeitaria; em modo estrito o
leitor devolvia **0** dispatches para aquele repo. Lenientemente, devolve 55 e
acumula avisos. Perder o histórico inteiro por causa de uma row antiga seria pior
do que exibi-la.

**2. Campos calculados levam prefixo `_` — em objetos com FORMA DE ROW.** Não é
cosmético: `status` é uma chave **real** das rows pré-v0.5.2, e num objeto que
compartilha o namespace de uma row do ledger um campo calculado com esse nome
sobrescrevia o dado histórico — bug que o teste `chave histórica 'status'
preservada` trava. A regra é escopada a rows/sheets: objetos-agregado que não são
rows (`summary`, `series`, `totals`) não têm namespace de ledger a proteger e
devolvem chaves sem prefixo de propósito (`total`, `open`, `by_type`, ...).

## Testes

```sh
python implementations/tests/test_ledger.py      # parser + smoke nos ledgers reais
python implementations/tests/test_ui.py          # Playwright nas dez variantes
python implementations/tests/test_ui.py terminal # só uma
```

Screenshots caem em `tests/screenshots/`.

## Fixture

`telemetry/agents/pending/2026-07-19-exemplo-ui-control-plane.json` é uma sheet
de **demonstração** (marcada com `"_example": true`), não uma dispatch real.
Existe para as UIs terem o que renderizar. Apagar quando o fluxo real estiver de pé.

## Próximas fases

- **Fase 2 — o botão.** `POST /confirm` grava o confirm; o Claude, esperando via
  `Monitor`, segue a cadeia normal (`check-tension` → `register-dispatch` →
  agentes → close row). Quem dispara continua sendo o Claude na sessão, o que
  preserva contexto e a cadeia de skills.
- **Fase 3 — edição** da sheet pendente antes do confirm.
