"""Fase 1 — o leitor.

Serve, ao vivo, as sheets pendentes (pré-confirm) e o histórico de dispatches
lido dos ledgers append-only de vários repos.

Este servidor é **somente leitura**. O botão "Disparar" é a Fase 2: ele grava um
confirm, e quem executa a cadeia (check-tension → register-dispatch → agentes)
continua sendo o Claude na sessão. Nada aqui escreve no ledger.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import config as config_module
from . import ledger

CFG = config_module.load()
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

# Teto da lista "tudo que está aberto". 200 cabe numa tela rolável; acima disso
# o que o humano precisa não é uma lista mais longa, é um filtro.
OPEN_ALL_CAP = 200

app = FastAPI(title="Dispatch control plane — leitor", version="0.1.0")


def today_utc() -> str:
    """O dia de hoje em UTC — o MESMO referencial de `ledger.iso_date`.

    Se aqui usássemos o dia local e lá o UTC, "hoje" da UI não bateria com o
    bucket `_day` das rows por algumas horas todo dia. Um só referencial.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _sort_key(row: dict[str, Any]) -> str:
    """Ordena por recência tolerando ausência: `created`, senão o dia, senão nada."""
    created = row.get("created")
    if isinstance(created, str):
        return created
    return row.get("_day") or ""


def snapshot() -> dict:
    repos = CFG.resolved_repos()
    return {
        "repos": [ledger.read_repo(r, CFG.limit, CFG.prompt_limit) for r in repos],
        "config": {
            "limit": CFG.limit,
            "poll_seconds": CFG.poll_seconds,
            "repo_count": len(repos),
        },
    }


@app.get("/api/snapshot")
async def api_snapshot() -> dict:
    return snapshot()


@app.get("/api/dispatch/{repo_name}/{dispatch_id}")
async def api_dispatch(repo_name: str, dispatch_id: str) -> dict:
    for repo in CFG.resolved_repos():
        if repo.name == repo_name:
            # O parse é SEMPRE leniente e nunca levanta `LedgerError` — o antigo
            # `except LedgerError` aqui era código morto. Um ledger ilegível vira
            # `.error` (OSError capturado no parse), e `find_dispatch` só olha
            # `ledger_exists`, então sem este teste um erro de leitura se
            # disfarçaria de 404 "dispatch não encontrada". Surface como 500.
            data = ledger.load_repo_rows(repo, copy=False)
            if data.error:
                raise HTTPException(status_code=500, detail=data.error)
            found = ledger.find_dispatch(repo, dispatch_id)
            if found is None:
                raise HTTPException(status_code=404, detail="dispatch não encontrada")
            return found
    raise HTTPException(status_code=404, detail="repo não encontrado")


@app.get("/api/overview")
async def api_overview() -> dict:
    """Painel de topo: agregados de TODOS os repos + o que pede atenção humana.

    Distinto do `/api/snapshot`, que serve a janela recente de cada repo. Aqui
    nada é truncado por `limit` — as contagens são sobre o ledger inteiro.
    """
    today = today_utc()
    repos = CFG.resolved_repos()

    summaries: list[dict[str, Any]] = []
    pending_all: list[dict[str, Any]] = []
    open_all: list[dict[str, Any]] = []
    open_today: list[dict[str, Any]] = []

    totals_by_type: dict[str, int] = {}
    totals = {"total": 0, "open": 0, "closed": 0, "pending": 0}
    today_totals = {"created": 0, "closed": 0}

    for repo in repos:
        # Lê as sheets pendentes UMA vez por repo e reusa: `summarize_repo` só
        # precisa da contagem e a lista de atenção precisa das entries. Antes eram
        # dois `read_pending` por repo por request (um glob de disco cada).
        pending = ledger.read_pending(repo)
        summary = ledger.summarize_repo(repo, today=today, pending=pending)
        summaries.append(summary)

        totals["total"] += summary["total"]
        totals["open"] += summary["open"]
        totals["closed"] += summary["closed"]
        totals["pending"] += summary["pending_count"]
        today_totals["created"] += summary["today"]["created"]
        today_totals["closed"] += summary["today"]["closed"]
        for kind, count in summary["by_type"].items():
            totals_by_type[kind] = totals_by_type.get(kind, 0) + count

        # `_repo` marca a origem: as listas de atenção misturam repos, e sem a
        # etiqueta o cliente não consegue linkar de volta para o drill-down.
        for entry in pending:
            entry["_repo"] = repo.name
            pending_all.append(entry)

        for row in ledger.load_repo_rows(repo, copy=False).rows:
            if row.get("_state") != "open":
                continue
            item = ledger.slim(row)
            item["_repo"] = repo.name
            open_all.append(item)
            if item["_day"] == today:
                open_today.append(item)

    open_all.sort(key=_sort_key, reverse=True)
    open_today.sort(key=_sort_key, reverse=True)

    attention: dict[str, Any] = {
        "pending": pending_all,
        "open_today": open_today,
        "open_all": open_all[:OPEN_ALL_CAP],
    }
    # A flag vive no contêiner `attention`, não na lista: JSON não deixa anotar
    # um array. `_open_all_total` é o número real, para a UI dizer "200 de N".
    if len(open_all) > OPEN_ALL_CAP:
        attention["_capped"] = True
        attention["_open_all_total"] = len(open_all)

    return {
        "repos": summaries,
        "totals": {
            "repos": len(repos),
            **totals,
            "by_type": dict(sorted(totals_by_type.items())),
            "today": today_totals,
        },
        "today": today,
        "attention": attention,
        "config": {
            "limit": CFG.limit,
            "poll_seconds": CFG.poll_seconds,
            "repo_count": len(repos),
        },
    }


@app.get("/api/repo/{repo_name}")
async def api_repo(
    repo_name: str,
    state: str | None = Query(None, pattern="^(open|closed|all)$"),
    type: str | None = Query(None),
) -> dict:
    """Drill-down de um repo: histórico COMPLETO em peso de listagem.

    ASSIMETRIA DELIBERADA: `state` e `type` filtram SÓ `dispatches`. O `summary`
    e a `series` descrevem sempre o repo inteiro, sem filtro. Se o gráfico
    encolhesse junto com a lista, o usuário perderia a referência exatamente
    quando está comparando um recorte contra o todo — e o eixo mudaria de escala
    a cada clique. O gráfico é o pano de fundo; a lista é o recorte.
    """
    repo = next((r for r in CFG.resolved_repos() if r.name == repo_name), None)
    if repo is None:
        raise HTTPException(status_code=404, detail="repo não encontrado")

    data = ledger.load_repo_rows(repo, copy=False)
    today = today_utc()
    pending = ledger.read_pending(repo)  # uma leitura, reusada por summary e pela resposta

    # Normaliza para o default: assim o handler também é chamável direto de
    # dentro do processo (testes), onde os defaults chegariam como objetos
    # `Query` em vez de string e filtrariam a lista inteira fora.
    state = state if isinstance(state, str) else "all"
    kind = type if isinstance(type, str) and type else None

    rows = [ledger.slim(row) for row in reversed(data.rows)]  # mais nova primeiro
    if state != "all":
        rows = [r for r in rows if r["_state"] == state]
    if kind:
        rows = [r for r in rows if (r.get("dispatch_type") or ledger.NO_TYPE) == kind]

    return {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "error": data.error,
        "warnings": list(data.warnings),
        "summary": ledger.summarize_repo(repo, today=today, pending=pending),
        "series": ledger.daily_series(data.rows),
        "pending": pending,
        "dispatches": rows,
    }


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/api/stream")
async def api_stream() -> StreamingResponse:
    """SSE. Emite o snapshot inteiro sempre que o disco muda.

    Diffar não vale a pena aqui: o payload é pequeno (limitado por `limit`) e o
    snapshot inteiro é trivialmente correto — um cliente que conecta no meio já
    chega com o estado certo.
    """

    async def gen():
        last = ledger.signature(CFG.resolved_repos())
        yield _sse("snapshot", snapshot())
        while True:
            await asyncio.sleep(CFG.poll_seconds)
            current = ledger.signature(CFG.resolved_repos())
            if current != last:
                last = current
                yield _sse("snapshot", snapshot())
            else:
                yield ": keepalive\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def main() -> None:
    import uvicorn

    repos = CFG.resolved_repos()
    print(f"observando {len(repos)} repos:")
    for repo in repos:
        print(f"  - {repo}")
    print(f"\n  http://{CFG.host}:{CFG.port}\n")
    uvicorn.run(app, host=CFG.host, port=CFG.port, log_level="warning")


if __name__ == "__main__":
    main()
