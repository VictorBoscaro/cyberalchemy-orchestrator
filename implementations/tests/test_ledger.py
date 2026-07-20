"""Testes do leitor de ledger.

Roda contra fixtures sintéticas (determinístico) e, se existirem, contra os
ledgers reais da máquina (smoke test — nunca falha por conteúdo, só por crash).

    python -m implementations.tests.test_ledger      (a partir do repo root)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import config as config_module  # noqa: E402
from server import ledger  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} {detail}")
        FAILURES.append(name)


LEDGER_OK = """# comentário de header
# segunda linha de comentário
dispatches:
  - dispatch_id: "2026-06-12-alpha"
    schema_version: "0.6.0"
    created: "2026-06-12T18:00:00.000Z"
    dispatch_type: "research"
    goal: "objetivo alpha"
    context: "contexto alpha"
    max_loops: 1
    final_approver: "parent"
    working_folder: "research/alpha/"
    groups: [{"group_id":"explorers","n":2,"anti_bias":"eixo","agents":[{"role":"explorer","model":"m","token_budget":800,"initial_prompt":"AAAAAAAAAA","angle":"a"},{"role":"explorer","model":"m","token_budget":800,"initial_prompt":"B","angle":"b"}]}]
    connections: [{"from":"explorers","to":"explorers","type":"feedback","loop_cap":2}]
  - dispatch_id: "2026-06-13-beta"
    schema_version: "0.6.0"
    dispatch_type: "review"
    goal: "objetivo beta"
    groups: [{"group_id":"g","agents":[{"role":"auditor","model":"m","token_budget":10,"initial_prompt":"p"}]}]
  - close_of: "2026-06-12-alpha"
    closed: "2026-06-12T19:00:00.000Z"
    exit_reason: "resolved"
    agents_spawned: {"total":2,"tree":{"explorer":2},"loops_used":1}
"""

LEGACY = """dispatches:
  - dispatch_id: "2026-01-01-antiga"
    status: "done"
    agents: [{"name":"x"}]
    corpus: "algum"
"""

ORPHAN = """dispatches:
  - close_of: "2026-05-05-fantasma"
    exit_reason: "error"
    agents_spawned: {"total":0,"tree":{},"loops_used":0}
"""


def test_parse_and_join() -> None:
    print("\nparse + join (schema v0.6.0)")
    parsed = ledger.parse_ledger(LEDGER_OK)
    check("3 rows brutas", len(parsed.rows) == 3, f"(veio {len(parsed.rows)})")
    check("ledger limpo não gera aviso", parsed.warnings == [], f"({parsed.warnings})")

    joined = ledger.join_rows(parsed.rows)
    check("2 dispatches após o join", len(joined) == 2, f"(veio {len(joined)})")

    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")
    beta = next(d for d in joined if d["dispatch_id"] == "2026-06-13-beta")

    check("alpha fechada pela close row", alpha["_state"] == "closed")
    check("alpha carrega o exit_reason", alpha["_close"]["exit_reason"] == "resolved")
    check("beta continua aberta", beta["_state"] == "open")
    check("beta sem close", beta["_close"] is None)
    check("groups vem como lista parseada", isinstance(alpha["groups"], list))
    check("connections com edge tipado", alpha["connections"][0]["type"] == "feedback")
    check("loop_cap preservado", alpha["connections"][0]["loop_cap"] == 2)
    check("contagem de agentes", alpha["_agent_count"] == 2)
    check("research é LIVE", alpha["_live"] is True)
    check("v0.6.0 não é legacy", alpha["_legacy"] is False)


def test_truncation() -> None:
    print("\ntruncagem de initial_prompt")
    joined = ledger.join_rows(ledger.parse_ledger(LEDGER_OK).rows)
    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")

    trimmed = ledger.truncate_prompts(alpha, 5)
    prompt = trimmed["groups"][0]["agents"][0]["initial_prompt"]
    check("prompt longo truncado", prompt == "AAAAA…", f"(veio {prompt!r})")
    check("flag de truncagem no agente", trimmed["groups"][0]["agents"][0]["_prompt_truncated"] is True)
    check("flag de truncagem na row", trimmed["_prompts_truncated"] is True)
    check("prompt curto intacto", trimmed["groups"][0]["agents"][1]["initial_prompt"] == "B")
    check("original não mutado", alpha["groups"][0]["agents"][0]["initial_prompt"] == "AAAAAAAAAA")


def test_legacy_and_orphan() -> None:
    print("\ngrandfathering + close órfã")
    legacy = ledger.join_rows(ledger.parse_ledger(LEGACY).rows)
    check("row pré-v0.5.2 é lida", len(legacy) == 1)
    check("marcada como legacy", legacy[0]["_legacy"] is True)
    # Regressão: `status` é chave REAL das rows pré-v0.5.2. Um campo calculado
    # com esse nome apagaria o dado histórico — por isso o prefixo `_`.
    check("chave histórica `status` preservada", legacy[0]["status"] == "done")
    check("estado calculado não colide", legacy[0]["_state"] == "open")
    check("count_agents tolera ausência de groups", legacy[0]["_agent_count"] == 0)

    orphan = ledger.join_rows(ledger.parse_ledger(ORPHAN).rows)
    check("close órfã é exposta", len(orphan) == 1 and orphan[0]["_orphan_close"] is True)


def test_prettified_legacy() -> None:
    """Forma real encontrada no ledger do domainspec: JSON multi-linha + vírgula final."""
    print("\nrows antigas prettificadas (dado real do domainspec)")
    text = (
        "dispatches:\n"
        '  - dispatch_id: "2026-06-12-prettificada"\n'
        '    corpus: "internal_tools/x"\n'
        '    status: "dispatched"\n'
        "    anti_bias:\n"
        "      {\n"
        '        "axis": "lente crítica",\n'
        '        "pairs":\n'
        "          [\n"
        '            "a ⟂ b",\n'
        '            "b ⟂ c",\n'
        "          ],\n"
        "      }\n"
        "    max_loops: 1\n"
    )
    parsed = ledger.parse_ledger(text)
    check("a row sobrevive", len(parsed.rows) == 1, f"(veio {len(parsed.rows)})")
    row = parsed.rows[0]
    check("valor multi-linha remontado", isinstance(row.get("anti_bias"), dict))
    check("vírgula final tolerada", row["anti_bias"]["pairs"] == ["a ⟂ b", "b ⟂ c"])
    check("chave depois do bloco é lida", row.get("max_loops") == 1)
    check("tolerância é avisada", any("vírgula" in w for w in parsed.warnings))


def test_lenient_vs_strict() -> None:
    print("\nleniente pula a row ruim; estrito levanta")
    broken = (
        "dispatches:\n"
        '  - dispatch_id: "boa-1"\n'
        '    goal: "sobrevive"\n'
        "  isto nao e uma row\n"
        '  - dispatch_id: "boa-2"\n'
        '    goal: "tambem sobrevive"\n'
    )
    parsed = ledger.parse_ledger(broken)
    check("rows boas preservadas ao redor do lixo", len(parsed.rows) == 2, f"(veio {len(parsed.rows)})")
    check("o problema vira aviso", len(parsed.warnings) == 1, f"({parsed.warnings})")

    try:
        ledger.parse_ledger(broken, lenient=False)
        check("modo estrito levanta", False, "(não levantou)")
    except ledger.LedgerError:
        check("modo estrito levanta", True)


def test_corruption() -> None:
    print("\ncorrupção estrutural (modo estrito)")
    cases = {
        "forma de linha inválida": "dispatches:\n  isto nao e uma row\n",
        "JSON inválido": 'dispatches:\n  - dispatch_id: {nao json\n',
        "row começando errado": 'dispatches:\n  - goal: "x"\n',
        "continuação sem row": 'dispatches:\n    goal: "x"\n',
    }
    for name, text in cases.items():
        try:
            ledger.parse_ledger(text, lenient=False)
            check(name, False, "(não levantou LedgerError)")
        except ledger.LedgerError:
            check(name, True)


def test_iso_date() -> None:
    print("\niso_date (dia UTC, com fallback pelo dispatch_id)")
    check(
        "created bom manda",
        ledger.iso_date({"created": "2026-06-12T18:00:00.000Z", "dispatch_id": "2020-01-01-x"})
        == "2026-06-12",
    )
    check(
        "sem created cai no prefixo do id",
        ledger.iso_date({"dispatch_id": "2026-07-10-ui11-metatype-review"}) == "2026-07-10",
    )
    check(
        "created malformado cai no id",
        ledger.iso_date({"created": "ontem", "dispatch_id": "2026-07-10-x"}) == "2026-07-10",
    )
    check(
        "created com mês impossível cai no id",
        ledger.iso_date({"created": "2026-13-45T00:00:00Z", "dispatch_id": "2026-07-10-x"})
        == "2026-07-10",
    )
    check("lixo dos dois lados vira None", ledger.iso_date({"created": None, "dispatch_id": "sem-data"}) is None)
    check("row vazia vira None", ledger.iso_date({}) is None)


def test_join_non_hashable_id() -> None:
    print("\njoin_rows tolera id não-hasheável (FIX 2: não levanta TypeError)")
    # Um `dispatch_id`/`close_of` que parseou para lista JSON não é hasheável;
    # usado como chave de dict levantaria TypeError e derrubaria o parse INTEIRO
    # do repo (500 em todo endpoint). O leitor é leniente: pula a row e segue.
    rows = [
        {"dispatch_id": ["2026-06-01", "x"], "goal": "id virou lista"},
        {"dispatch_id": "2026-06-02-boa", "goal": "sobrevive"},
        {"close_of": ["lista"], "exit_reason": "resolved"},
    ]
    try:
        joined = ledger.join_rows(rows)
    except TypeError as exc:
        check("join_rows não levanta em id não-hasheável", False, f"({exc})")
        return
    check("join_rows não levanta em id não-hasheável", True)
    check("a row de id-lista é pulada", len(joined) == 1, f"(veio {len(joined)})")
    check("a row boa sobrevive ao redor", joined[0]["dispatch_id"] == "2026-06-02-boa")


def test_iso_date_close_precedence() -> None:
    print("\niso_date: _close.closed antes do prefixo do id (FIX 3: stamped > convenção)")
    # Close row órfã, id sem prefixo de data, mas `_close.closed` stampado: o dia
    # exato do fechamento estava à mão e antes ficava sem ser lido.
    orphan = {"dispatch_id": "id-sem-data", "_close": {"closed": "2026-07-15T09:00:00.000Z"}}
    check("close órfã resolve pelo dia do close", ledger.iso_date(orphan) == "2026-07-15", f"({ledger.iso_date(orphan)})")
    check(
        "created ainda ganha do close",
        ledger.iso_date({"created": "2026-01-02T00:00:00Z", "_close": {"closed": "2026-07-15T00:00:00Z"}}) == "2026-01-02",
    )
    check(
        "close ilegível cai no prefixo do id",
        ledger.iso_date({"dispatch_id": "2026-03-03-x", "_close": {"closed": "ontem"}}) == "2026-03-03",
    )
    check("sem nada de data continua None", ledger.iso_date({"dispatch_id": "sem-data", "_close": {"closed": "ontem"}}) is None)


def _row(did: str, kind: str | None = "research", **extra) -> dict:
    row = {"dispatch_id": did, "dispatch_type": kind, "_state": "open", "_legacy": False}
    row.update(extra)
    return row


def test_daily_series() -> None:
    print("\ndaily_series (dias contíguos, buracos com zero)")
    rows = [
        _row("2026-06-01-a", "research"),
        _row("2026-06-01-b", "review"),
        _row("2026-06-04-c", "research"),
    ]
    series = ledger.daily_series(rows)
    check(
        "eixo contíguo do primeiro ao último",
        series["days"] == ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04"],
        f"({series['days']})",
    )
    check("tipos presentes e ordenados", series["types"] == ["research", "review"])
    check("buraco vira zero", series["series"]["research"] == [1, 0, 0, 1], f"({series['series']['research']})")
    check("série curta preenchida", series["series"]["review"] == [1, 0, 0, 0])
    check("totais por tipo", series["totals"] == {"research": 2, "review": 1})
    check("max_day é a coluna mais alta", series["max_day"] == 2, f"({series['max_day']})")
    check("nada indatado", series["undated"] == 0)
    check("span não truncado", series["truncated_span"] is False)

    single = ledger.daily_series([_row("2026-06-01-a", "research")])
    check("um dia só gera um bucket", single["days"] == ["2026-06-01"])
    check("um dia só, max_day=1", single["max_day"] == 1)

    empty = ledger.daily_series([_row("sem-data", "research"), _row("outra", None)])
    check("zero rows datadas: eixo vazio", empty["days"] == [])
    check("zero rows datadas: séries vazias", empty["series"] == {} and empty["totals"] == {})
    check("indatadas são reportadas", empty["undated"] == 2, f"({empty['undated']})")
    check("max_day zero", empty["max_day"] == 0)

    no_type = ledger.daily_series([_row("2026-06-01-a", None)])
    check("tipo ausente vira bucket próprio", no_type["types"] == [ledger.NO_TYPE], f"({no_type['types']})")

    # Uma data de 1970 esticaria o eixo para ~20 mil buckets.
    wild = ledger.daily_series([_row("1970-01-01-a"), _row("2026-06-01-b")])
    check("span patológico é capado", wild["truncated_span"] is True)
    check("eixo capado em MAX_SPAN_DAYS", len(wild["days"]) == ledger.MAX_SPAN_DAYS, f"({len(wild['days'])})")
    check("a row fora da janela é reportada", wild["out_of_range"] == 1, f"({wild['out_of_range']})")

    windowed = ledger.daily_series(rows, days=2)
    check("days=N corta para os N últimos", windowed["days"] == ["2026-06-03", "2026-06-04"], f"({windowed['days']})")
    check("days=N reporta o que ficou fora", windowed["out_of_range"] == 2, f"({windowed['out_of_range']})")


def test_daily_series_future_clamp() -> None:
    print("\ndaily_series clampa a borda futura em hoje (FIX 4: typo de 2126 não zera o gráfico)")
    rows = [
        _row("2026-06-01-a", "research"),
        _row("2026-06-02-b", "research"),
        _row("2126-06-01-typo", "research"),  # typo de século: não pode ancorar o eixo
    ]
    series = ledger.daily_series(rows)
    check("as rows reais continuam plotadas", series["totals"].get("research", 0) == 2, f"({series['totals']})")
    check("a row de 2126 é out_of_range, não âncora", series["out_of_range"] == 1, f"({series['out_of_range']})")
    check("o eixo não estourou para milhares de buckets", len(series["days"]) <= ledger.MAX_SPAN_DAYS, f"({len(series['days'])})")
    # A invariante de contabilidade tem que continuar exata.
    plotted = sum(sum(s) for s in series["series"].values())
    check(
        "plotted + out_of_range + undated == len(rows)",
        plotted + series["out_of_range"] + series["undated"] == len(rows),
        f"({plotted}+{series['out_of_range']}+{series['undated']} vs {len(rows)})",
    )


def test_slim() -> None:
    print("\nslim (peso de listagem, sem prompt nenhum)")
    joined = ledger.join_rows(ledger.parse_ledger(LEDGER_OK).rows)
    alpha = next(d for d in joined if d["dispatch_id"] == "2026-06-12-alpha")

    s = ledger.slim(alpha, goal_limit=8)
    blob = json.dumps(s, ensure_ascii=False)
    check("initial_prompt não aparece em lugar nenhum", "initial_prompt" not in blob)
    check("groups não aparece", "groups" not in s)
    check("goal truncado", s["goal"] == "objetivo…", f"({s['goal']!r})")
    check("flag de goal truncado", s["_goal_truncated"] is True)
    check("_day calculado", s["_day"] == "2026-06-12")
    check("contagem de grupos", s["_group_count"] == 1)
    check("papéis contados", s["_roles"] == {"explorer": 2}, f"({s['_roles']})")
    check("tipos de conexão distintos e ordenados", s["_connection_types"] == ["feedback"])
    check("robot_talks ausente vira False", s["_robot_talks"] is False)
    check("_close enxuto só com closed/exit_reason", set(s["_close"]) == {"closed", "exit_reason"}, f"({s['_close']})")
    check("agents_spawned não vaza", "agents_spawned" not in blob)
    check("original não mutado", "initial_prompt" in json.dumps(alpha["groups"]))

    beta = next(d for d in joined if d["dispatch_id"] == "2026-06-13-beta")
    sb = ledger.slim(beta)
    check("goal curto não ganha flag", "_goal_truncated" not in sb)
    check("aberta tem _close None", sb["_close"] is None)

    legacy = ledger.join_rows(ledger.parse_ledger(LEGACY).rows)[0]
    sl = ledger.slim(legacy)
    check("legacy sem groups sobrevive ao slim", sl["_group_count"] == 0 and sl["_roles"] == {})
    check("legacy sem dispatch_type vira None no campo cru", sl["dispatch_type"] is None)


def _write_ledger(root: Path, text: str) -> None:
    path = root / ledger.LEDGER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_summarize_repo(tmp_root: Path) -> None:
    print("\nsummarize_repo (agregado sobre o ledger inteiro)")
    repo = tmp_root / "repo-sumario"
    _write_ledger(repo, LEDGER_OK + LEGACY.split("dispatches:\n", 1)[1] + ORPHAN.split("dispatches:\n", 1)[1])
    ledger.clear_cache()

    s = ledger.summarize_repo(repo, today="2026-06-12")
    check("total inclui a close órfã", s["total"] == 4, f"({s['total']})")
    check("abertas", s["open"] == 2, f"({s['open']})")
    check("fechadas (alpha + órfã)", s["closed"] == 2, f"({s['closed']})")
    check("legacy conta a antiga + a órfã", s["legacy"] == 2, f"({s['legacy']})")
    check(
        "by_type com bucket para tipo ausente",
        s["by_type"] == {"research": 1, "review": 1, ledger.NO_TYPE: 2},
        f"({s['by_type']})",
    )
    check("live = research + review", s["live"] == 2, f"({s['live']})")
    check("reserved exclui legacy", s["reserved"] == 0, f"({s['reserved']})")
    check("hoje: 1 criada", s["today"]["created"] == 1, f"({s['today']})")
    check("hoje: 1 fechada", s["today"]["closed"] == 1, f"({s['today']})")
    check("open_now espelha open", s["open_now"] == s["open"])
    check("primeiro dia", s["first_day"] == "2026-01-01", f"({s['first_day']})")
    check("último dia", s["last_day"] == "2026-06-13", f"({s['last_day']})")
    check("last_created é o ISO cru mais recente", s["last_created"] == "2026-06-12T18:00:00.000Z")
    check("sem erro", s["error"] is None and s["ledger_exists"] is True)

    ausente = ledger.summarize_repo(tmp_root / "repo-inexistente", today="2026-06-12")
    check("repo sem ledger não explode", ausente["total"] == 0 and ausente["ledger_exists"] is False)


def test_legacy_live_double_count(tmp_root: Path) -> None:
    print("\nrow ao mesmo tempo _legacy e _live (FIX 8b: pinar a não-partição)")
    # Uma research row (LIVE) cujo `groups` falha no parse leniente fica SEM
    # `groups` → `_legacy=True` E `_live=True`, contada nas duas somas. Pinamos
    # que `total == live + reserved + legacy` NÃO vale, para o agente de frontend
    # não renderizar as três como partição fechada.
    text = (
        "dispatches:\n"
        '  - dispatch_id: "2026-06-20-broken-groups"\n'
        '    schema_version: "0.6.0"\n'
        '    dispatch_type: "research"\n'
        '    goal: "objetivo"\n'
        "    groups: @@@nao-json\n"
    )
    joined = ledger.join_rows(ledger.parse_ledger(text).rows)
    check("a row sobrevive ao groups ilegível", len(joined) == 1, f"(veio {len(joined)})")
    row = joined[0]
    check("sem groups vira _legacy", row["_legacy"] is True)
    check("research continua _live", row["_live"] is True)

    repo = tmp_root / "repo-double"
    _write_ledger(repo, text)
    ledger.clear_cache()
    s = ledger.summarize_repo(repo, today="2026-06-20")
    check("contada em legacy", s["legacy"] == 1, f"({s['legacy']})")
    check("contada em live", s["live"] == 1, f"({s['live']})")
    check("reserved a exclui (é live)", s["reserved"] == 0, f"({s['reserved']})")
    check(
        "live+reserved+legacy NÃO particiona total (dupla contagem pinada)",
        s["live"] + s["reserved"] + s["legacy"] == 2 and s["total"] == 1,
        f"(l+r+leg={s['live'] + s['reserved'] + s['legacy']}, total={s['total']})",
    )


def test_parse_cache(tmp_root: Path) -> None:
    print("\ncache de parse (fingerprint mtime_ns + tamanho)")
    repo = tmp_root / "repo-cache"
    _write_ledger(repo, LEDGER_OK)
    ledger.clear_cache()

    first = ledger.load_repo_rows(repo)
    check("primeira leitura parseia", ledger.parse_count() == 1, f"({ledger.parse_count()})")
    check("rows vieram", len(first.rows) == 2)

    ledger.load_repo_rows(repo)
    ledger.load_repo_rows(repo)
    check("arquivo intacto não reparseia", ledger.parse_count() == 1, f"({ledger.parse_count()})")

    # read_repo e find_dispatch também passam pelo cache.
    ledger.read_repo(repo, 40, 280)
    ledger.find_dispatch(repo, "2026-06-12-alpha")
    check("read_repo/find_dispatch reaproveitam", ledger.parse_count() == 1, f"({ledger.parse_count()})")

    # O cache não pode ser contaminado por quem recebeu as rows.
    first.rows[0]["_poluicao"] = True
    check("mutação do chamador não entra no cache", "_poluicao" not in ledger.load_repo_rows(repo).rows[0])

    # Mudança de conteúdo (tamanho + mtime) invalida.
    _write_ledger(repo, LEDGER_OK + '  - dispatch_id: "2026-06-14-gama"\n    goal: "nova"\n')
    again = ledger.load_repo_rows(repo)
    check("append invalida o cache", ledger.parse_count() == 2, f"({ledger.parse_count()})")
    check("a row nova aparece", len(again.rows) == 3, f"({len(again.rows)})")

    # Só o mtime, mesmo tamanho: a fingerprint carrega os dois.
    path = repo / ledger.LEDGER_RELPATH
    stat = path.stat()
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000_000))
    ledger.load_repo_rows(repo)
    check("mtime novo com mesmo tamanho invalida", ledger.parse_count() == 3, f"({ledger.parse_count()})")

    ledger.clear_cache()
    check("clear_cache zera o contador", ledger.parse_count() == 0)


def test_real_repos() -> None:
    print("\nsmoke contra os ledgers reais")
    cfg = config_module.load()
    repos = cfg.resolved_repos()
    check("auto-descoberta achou repos", len(repos) > 0, f"(veio {len(repos)})")

    start = time.time()
    total = 0
    for repo in repos:
        try:
            data = ledger.read_repo(repo, cfg.limit, cfg.prompt_limit)
        except Exception as exc:  # noqa: BLE001 — smoke test: qualquer crash é falha
            check(f"{repo.name} lê sem crashar", False, f"({type(exc).__name__}: {exc})")
            continue
        total += data["total_dispatches"]
        status = data["error"] or "ok"
        print(
            f"        {repo.name:<32} total={data['total_dispatches']:<5}"
            f" open={data['open_dispatches']:<4} pending={len(data['pending']):<3}"
            f" avisos={len(data['warnings']):<3} {status}"
        )
        check(f"{repo.name} sem erro fatal", data["error"] is None, f"({data['error']})")
        # Um ledger com rows antigas ainda deve entregar histórico: avisos são
        # aceitáveis, zerar o repo não é.
        if data["ledger_exists"]:
            check(
                f"{repo.name} entrega dispatches",
                data["total_dispatches"] > 0,
                f"(0 dispatches, avisos={len(data['warnings'])})",
            )

    elapsed = time.time() - start
    print(f"        -> {total} dispatches em {elapsed:.2f}s")
    check("parse de todos os repos < 5s", elapsed < 5.0, f"({elapsed:.2f}s)")


def main() -> int:
    test_parse_and_join()
    test_truncation()
    test_legacy_and_orphan()
    test_prettified_legacy()
    test_lenient_vs_strict()
    test_corruption()
    test_join_non_hashable_id()
    test_iso_date()
    test_iso_date_close_precedence()
    test_daily_series()
    test_daily_series_future_clamp()
    test_slim()
    with tempfile.TemporaryDirectory() as tmp:
        test_summarize_repo(Path(tmp))
        test_legacy_live_double_count(Path(tmp))
        test_parse_cache(Path(tmp))
    ledger.clear_cache()
    test_real_repos()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FALHA(S): {', '.join(FAILURES)}")
        return 1
    print("todos os testes passaram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
