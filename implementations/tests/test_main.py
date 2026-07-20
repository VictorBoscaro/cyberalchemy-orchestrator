"""Testes da camada de endpoints (FastAPI) — o buraco de cobertura do FIX 7.

`test_ledger.py` nunca importa `main`, então /api/overview, /api/repo, a
ASSIMETRIA deliberada do filtro (state/type filtram só a lista, nunca o summary
nem a série), o OPEN_ALL_CAP e os totais do overview ficavam sem teste. Mutation
testing deixava 9 sobreviventes exatamente nessas regiões.

Este arquivo roda in-process com o TestClient do FastAPI e usa fixtures
ASSIMÉTRICAS (open != closed, > 40 rows) de propósito: um fixture simétrico de 4
rows deixaria os mutantes de contador-trocado e de corte-nos-40 sobreviverem.

    python tests/test_main.py      (a partir de implementations/)
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402
from server import main as main_module  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} {detail}")
        FAILURES.append(name)


# --------------------------------------------------------------------------
# Síntese de ledgers (mesma forma que o appender escreve)
# --------------------------------------------------------------------------

_GROUP = [
    {
        "group_id": "g",
        "agents": [
            {"role": "explorer", "model": "m", "token_budget": 10, "initial_prompt": "p"}
        ],
    }
]
_SPAWNED = {"total": 1, "tree": {"explorer": 1}, "loops_used": 1}


def _dispatch(did: str, dtype: str, created: str) -> str:
    return (
        f"  - dispatch_id: {json.dumps(did)}\n"
        f'    schema_version: "0.6.0"\n'
        f"    created: {json.dumps(created)}\n"
        f"    dispatch_type: {json.dumps(dtype)}\n"
        f"    goal: {json.dumps('goal de ' + did)}\n"
        f"    groups: {json.dumps(_GROUP)}\n"
    )


def _close(did: str, closed: str) -> str:
    return (
        f"  - close_of: {json.dumps(did)}\n"
        f"    closed: {json.dumps(closed)}\n"
        f'    exit_reason: "resolved"\n'
        f"    agents_spawned: {json.dumps(_SPAWNED)}\n"
    )


def _ledger(rows: list[str]) -> str:
    return "dispatches:\n" + "".join(rows)


def _day(i: int) -> str:
    # Espalha por junho/2026 — sempre no passado (hoje é depois), determinístico.
    return f"2026-06-{(i % 27) + 1:02d}"


def _write_repo(root: Path, name: str, text: str) -> None:
    path = root / name / ledger.LEDGER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _client(root: Path) -> TestClient:
    """Aponta o CFG do módulo para um scan root temporário e devolve o client.

    Cada cenário constrói um `Config` NOVO, então o cache (TTL) de `resolved_repos`
    começa vazio — sem contaminação entre cenários.
    """
    cfg = config_module.Config(scan_roots=[root])
    main_module.CFG = cfg
    ledger.clear_cache()
    return TestClient(main_module.app)


# --------------------------------------------------------------------------
# Fixtures assimétricos
# --------------------------------------------------------------------------

def _asym_repo() -> str:
    """60 rows, 45 abertas / 15 fechadas — assimétrico e > 40."""
    rows: list[str] = []
    # 30 research abertas
    for i in range(30):
        rows.append(_dispatch(f"2026-06-01-research-open-{i:02d}", "research", f"{_day(i)}T10:00:00.000Z"))
    # 10 review abertas
    for i in range(10):
        rows.append(_dispatch(f"2026-06-02-review-open-{i:02d}", "review", f"{_day(i)}T11:00:00.000Z"))
    # 5 code (RESERVED) abertas
    for i in range(5):
        rows.append(_dispatch(f"2026-06-03-code-open-{i:02d}", "code", f"{_day(i)}T12:00:00.000Z"))
    # 15 research fechadas (dispatch + close)
    for i in range(15):
        did = f"2026-06-04-research-closed-{i:02d}"
        rows.append(_dispatch(did, "research", f"{_day(i)}T13:00:00.000Z"))
        rows.append(_close(did, f"{_day(i)}T14:00:00.000Z"))
    return _ledger(rows)


def _open_rows(prefix: str, n: int) -> str:
    return _ledger(
        [_dispatch(f"{prefix}-{i:04d}", "research", f"{_day(i)}T09:00:00.000Z") for i in range(n)]
    )


# --------------------------------------------------------------------------
# Testes
# --------------------------------------------------------------------------

def test_repo_filter_asymmetry(root: Path) -> None:
    print("\n/api/repo — assimetria state/type (filtra a lista, NUNCA summary/série)")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)

    full = client.get("/api/repo/alpha").json()
    check("lista completa tem as 60 rows", len(full["dispatches"]) == 60, f"({len(full['dispatches'])})")
    check("summary conta o repo inteiro", full["summary"]["total"] == 60, f"({full['summary']['total']})")
    check("summary assimétrico: 45 abertas", full["summary"]["open"] == 45, f"({full['summary']['open']})")
    check("summary assimétrico: 15 fechadas", full["summary"]["closed"] == 15, f"({full['summary']['closed']})")

    open_only = client.get("/api/repo/alpha", params={"state": "open"}).json()
    closed_only = client.get("/api/repo/alpha", params={"state": "closed"}).json()
    review_only = client.get("/api/repo/alpha", params={"type": "review"}).json()

    # A LISTA encolhe...
    check("state=open encolhe a lista para 45", len(open_only["dispatches"]) == 45, f"({len(open_only['dispatches'])})")
    check("state=closed encolhe a lista para 15", len(closed_only["dispatches"]) == 15, f"({len(closed_only['dispatches'])})")
    check("type=review encolhe a lista para 10", len(review_only["dispatches"]) == 10, f"({len(review_only['dispatches'])})")

    # ...mas summary e série são IDÊNTICOS ao não-filtrado (a assimetria).
    for label, resp in (("state=open", open_only), ("state=closed", closed_only), ("type=review", review_only)):
        check(f"{label}: summary idêntico ao completo", resp["summary"] == full["summary"])
        check(f"{label}: série idêntica ao completo", resp["series"] == full["series"])

    # dobra de segurança: byte-a-byte.
    check(
        "summary/série byte-idênticos sob filtro",
        json.dumps(open_only["summary"], sort_keys=True) == json.dumps(full["summary"], sort_keys=True)
        and json.dumps(open_only["series"], sort_keys=True) == json.dumps(full["series"], sort_keys=True),
    )


def test_repo_errors(root: Path) -> None:
    print("\n/api/repo — 404 repo desconhecido, 422 state inválido")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    check("404 em repo inexistente", client.get("/api/repo/nao-existe").status_code == 404)
    check("422 em state fora do enum", client.get("/api/repo/alpha", params={"state": "bogus"}).status_code == 422)
    check("state=all é aceito", client.get("/api/repo/alpha", params={"state": "all"}).status_code == 200)


def test_dispatch_endpoint(root: Path) -> None:
    print("\n/api/dispatch — 404s e recuperação de uma row")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    check("404 em repo inexistente", client.get("/api/dispatch/nao-existe/x").status_code == 404)
    check("404 em dispatch inexistente", client.get("/api/dispatch/alpha/nao-existe").status_code == 404)
    ok = client.get("/api/dispatch/alpha/2026-06-01-research-open-00")
    check("acha a dispatch", ok.status_code == 200 and ok.json()["dispatch_id"] == "2026-06-01-research-open-00")


def test_overview_totals(root: Path) -> None:
    print("\n/api/overview — totais = soma por repo (sem dupla contagem), open_all casa")
    _write_repo(root, "alpha", _asym_repo())  # 60 total, 45 open
    # repo beta: 20 abertas + 10 fechadas = 30 total, 20 open
    beta_rows: list[str] = []
    for i in range(20):
        beta_rows.append(_dispatch(f"2026-06-05-beta-open-{i:02d}", "experiment", f"{_day(i)}T08:00:00.000Z"))
    for i in range(10):
        did = f"2026-06-06-beta-closed-{i:02d}"
        beta_rows.append(_dispatch(did, "research", f"{_day(i)}T08:00:00.000Z"))
        beta_rows.append(_close(did, f"{_day(i)}T09:00:00.000Z"))
    _write_repo(root, "beta", _ledger(beta_rows))
    client = _client(root)

    ov = client.get("/api/overview").json()
    summaries = ov["repos"]
    totals = ov["totals"]

    sum_total = sum(s["total"] for s in summaries)
    sum_open = sum(s["open"] for s in summaries)
    sum_closed = sum(s["closed"] for s in summaries)
    check("totals.total == soma dos summaries (90)", totals["total"] == sum_total == 90, f"({totals['total']} vs {sum_total})")
    check("totals.open == soma dos summaries (65)", totals["open"] == sum_open == 65, f"({totals['open']} vs {sum_open})")
    check("totals.closed == soma dos summaries (25)", totals["closed"] == sum_closed == 25, f"({totals['closed']} vs {sum_closed})")
    check("totals.repos == 2", totals["repos"] == 2, f"({totals['repos']})")

    # by_type somado sem dupla contagem: research=30(alpha:15open+... )... conferimos a soma.
    bt = totals["by_type"]
    sum_bt: dict[str, int] = {}
    for s in summaries:
        for k, v in s["by_type"].items():
            sum_bt[k] = sum_bt.get(k, 0) + v
    check("by_type do overview == soma dos by_type por repo", bt == sum_bt, f"({bt} vs {sum_bt})")

    # 65 abertas < CAP(200): open_all NÃO é capado e casa com o total aberto.
    check("len(attention.open_all) == total aberto (65)", len(ov["attention"]["open_all"]) == 65, f"({len(ov['attention']['open_all'])})")
    check("não capado abaixo do teto", "_capped" not in ov["attention"])


def test_open_all_cap(root: Path) -> None:
    print("\n/api/overview — OPEN_ALL_CAP e _open_all_total")
    cap = main_module.OPEN_ALL_CAP
    total_open = cap + 95  # 295 com CAP=200
    _write_repo(root, "flood", _open_rows("2026-06-07-flood", total_open))
    client = _client(root)

    ov = client.get("/api/overview").json()
    att = ov["attention"]
    check(f"open_all capado em OPEN_ALL_CAP ({cap})", len(att["open_all"]) == cap, f"({len(att['open_all'])})")
    check("_capped presente quando estoura", att.get("_capped") is True)
    check("_open_all_total é o número real", att.get("_open_all_total") == total_open, f"({att.get('_open_all_total')})")
    check("totals.open reflete o total real", ov["totals"]["open"] == total_open, f"({ov['totals']['open']})")


def test_snapshot_shape(root: Path) -> None:
    print("\n/api/snapshot — forma intacta (nove UIs dependem)")
    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    snap = client.get("/api/snapshot").json()
    check("tem repos e config", "repos" in snap and "config" in snap)
    repo = next(r for r in snap["repos"] if r["name"] == "alpha")
    for key in ("name", "path", "ledger_exists", "total_dispatches", "open_dispatches", "warnings", "error", "pending", "dispatches"):
        check(f"snapshot.repo tem `{key}`", key in repo)
    check("total_dispatches == 60", repo["total_dispatches"] == 60, f"({repo['total_dispatches']})")
    check("dispatches limitado a config.limit (40)", len(repo["dispatches"]) == 40, f"({len(repo['dispatches'])})")


# --------------------------------------------------------------------------
# Verificação de mutantes: confirmo que os testes acima MATAM cada mutante.
# Onde dá, muto o código de produção de verdade (OPEN_ALL_CAP) e checo pela
# LIVE endpoint; onde a mutação viveria inline no handler, fabrico a saída
# mutante e mostro que o predicado do teste a REJEITA.
# --------------------------------------------------------------------------

def _asymmetry_holds(full: dict, filtered: dict) -> bool:
    return (
        full["summary"] == filtered["summary"]
        and full["series"] == filtered["series"]
        and len(full["dispatches"]) != len(filtered["dispatches"])
    )


def _cap_holds(overview: dict, cap: int) -> bool:
    att = overview["attention"]
    total = att.get("_open_all_total", len(att["open_all"]))
    if len(att["open_all"]) > cap:
        return False
    if total > cap and att.get("_capped") is not True:
        return False
    return True


def _totals_consistent(overview: dict) -> bool:
    s = overview["repos"]
    t = overview["totals"]
    return (
        t["total"] == sum(x["total"] for x in s)
        and t["open"] == sum(x["open"] for x in s)
        and t["closed"] == sum(x["closed"] for x in s)
    )


def test_mutants(root: Path) -> list[str]:
    print("\nverificação de mutantes (o teste realmente mata cada um?)")
    killed: list[str] = []

    _write_repo(root, "alpha", _asym_repo())
    client = _client(root)
    full = client.get("/api/repo/alpha").json()
    open_only = client.get("/api/repo/alpha", params={"state": "open"}).json()

    # Sanidade: no código correto os predicados passam.
    check("baseline: assimetria vale", _asymmetry_holds(full, open_only))

    # M1 "state filter é no-op": lista filtrada == completa. Predicado exige
    # comprimentos diferentes -> rejeita -> morto.
    mutant_noop = dict(open_only, dispatches=full["dispatches"])
    m1 = not _asymmetry_holds(full, mutant_noop)
    check("M1 (state filter no-op) é morto", m1)
    if m1:
        killed.append("state-filter-no-op")

    # M2 "state filter também encolhe o summary": summary do filtrado passa a ser
    # o de um recorte. Fabrico um summary diferente; predicado rejeita -> morto.
    shrunk_summary = dict(full["summary"], total=45, open=45, closed=0)
    mutant_shrink = dict(open_only, summary=shrunk_summary)
    m2 = not _asymmetry_holds(full, mutant_shrink)
    check("M2 (state filter encolhe summary) é morto", m2)
    if m2:
        killed.append("state-filter-shrinks-summary")

    # M3 "OPEN_ALL_CAP ignorado": mutação REAL do módulo. Elevo o CAP e confirmo
    # que a saída viva passa a violar o predicado _cap_holds do teste.
    _write_repo(root, "flood", _open_rows("2026-06-07-flood", main_module.OPEN_ALL_CAP + 95))
    client2 = _client(root)
    real_cap = main_module.OPEN_ALL_CAP
    try:
        main_module.OPEN_ALL_CAP = 10 ** 9  # mutante: cap efetivamente desligado
        ov_mut = client2.get("/api/overview").json()
    finally:
        main_module.OPEN_ALL_CAP = real_cap
    ov_real = client2.get("/api/overview").json()
    m3 = _cap_holds(ov_real, real_cap) and not _cap_holds(ov_mut, real_cap)
    check("M3 (OPEN_ALL_CAP ignorado) é morto", m3, f"(mut len={len(ov_mut['attention']['open_all'])})")
    if m3:
        killed.append("open-all-cap-ignored")

    # M4 "totais dupla-contagem": fabrico um overview com total dobrado num repo;
    # predicado de consistência rejeita -> morto.
    good = ov_real
    doubled = json.loads(json.dumps(good))
    doubled["totals"]["total"] += doubled["repos"][0]["total"]  # contou um repo 2x
    m4 = _totals_consistent(good) and not _totals_consistent(doubled)
    check("M4 (totais dupla-contagem) é morto", m4)
    if m4:
        killed.append("totals-double-count")

    print(f"        -> mutantes mortos: {', '.join(killed)}")
    return killed


def main() -> int:
    with tempfile.TemporaryDirectory() as t1:
        test_repo_filter_asymmetry(Path(t1))
    with tempfile.TemporaryDirectory() as t2:
        test_repo_errors(Path(t2))
    with tempfile.TemporaryDirectory() as t3:
        test_dispatch_endpoint(Path(t3))
    with tempfile.TemporaryDirectory() as t4:
        test_overview_totals(Path(t4))
    with tempfile.TemporaryDirectory() as t5:
        test_open_all_cap(Path(t5))
    with tempfile.TemporaryDirectory() as t6:
        test_snapshot_shape(Path(t6))
    with tempfile.TemporaryDirectory() as t7:
        test_mutants(Path(t7))

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FALHA(S): {', '.join(FAILURES)}")
        return 1
    print("todos os testes de main passaram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
