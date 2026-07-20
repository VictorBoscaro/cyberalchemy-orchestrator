"""Leitor do ledger append-only de dispatches de subagentes.

Espelha as formas de linha escritas por `register-dispatch/append-dispatch.cjs`:
toda linha não-comentário é `dispatches:`, um início de row `  - key: <json>`,
ou uma continuação `    key: <json>`. Todo valor é JSON.

DOIS PRINCÍPIOS que este módulo segue:

1. **Estrutural apenas.** Rows escritas em schemas pré-v0.5.2 são artefatos
   históricos e nunca são revalidadas semanticamente — elas carregam chaves
   antigas (`status`, `agents` no topo, `corpus`, ...) e continuam passando.

2. **Leniente por padrão — ao contrário do appender.** O appender é estrito
   porque *protege* o arquivo: ele recusa escrever num ledger corrompido. O
   leitor tem o trabalho oposto — mostrar o que existe. Ledgers reais contêm
   rows antigas prettificadas (JSON multi-linha, vírgulas finais) que o
   appender rejeitaria; perder o histórico inteiro de um repo por causa de uma
   row assim seria pior do que exibi-la. Em modo leniente, uma row ilegível
   vira um aviso e é pulada; o resto do ledger é servido.

Este módulo NUNCA escreve. O ledger é append-only e pertence ao appender.

CONVENÇÃO (escopada a objetos com FORMA DE ROW): num objeto que compartilha o
namespace de uma row do ledger, todo campo calculado por este leitor leva prefixo
`_`. Isso não é cosmético — a chave `status` existe de verdade nas rows pré-v0.5.2,
então um campo calculado chamado `status` sobrescreveria o dado histórico; o `_`
garante que um calculado nunca colida com uma chave do namespace do próprio ledger.
A regra NÃO se aplica a objetos-contêiner/agregado que não são rows e não têm esse
namespace a proteger (`summarize_repo` devolve `total`, `open`, `by_type`, ... sem
prefixo de propósito — não há chave de ledger para sombrear ali).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Como o appender (append-dispatch.cjs:315), mas com o valor opcional: rows
# antigas prettificadas abrem o valor na linha seguinte (`    agents:`).
ROW_RE = re.compile(r"^(  - |    )([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?$")

LEDGER_RELPATH = Path("telemetry") / "agents" / "subagents-dispatch.yaml"
PENDING_RELPATH = Path("telemetry") / "agents" / "pending"

# Só estes três são dispatcháveis sob v0.6.0; o resto é nome reservado.
LIVE_TYPES = {"research", "review", "experiment"}

# Bucket para dispatches sem `dispatch_type` (rows pré-v0.5.2 não têm o campo).
# Um rótulo explícito em vez de `None` porque a chave vai virar coluna de gráfico
# e legenda na UI — e `null` como nome de série é pior do que uma palavra.
NO_TYPE = "(sem tipo)"

# Um span de dias maior que isto quase certamente vem de data corrompida (uma
# row com `1970-01-01` geraria ~20 mil buckets). Ver `daily_series`.
MAX_SPAN_DAYS = 1000

_MISSING = object()

_ISO_DAY_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")


class LedgerError(Exception):
    """O ledger está estruturalmente corrompido (só levantado em modo estrito)."""


@dataclass
class ParseResult:
    rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _loads(text: str) -> tuple[Any, str | None]:
    """JSON, tolerando vírgula final (legal em YAML flow, ilegal em JSON)."""
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        cleaned = re.sub(r",(\s*[\]}])", r"\1", text)
        if cleaned != text:
            try:
                return json.loads(cleaned), "vírgula final tolerada"
            except json.JSONDecodeError:
                pass
        return _MISSING, str(exc)


def parse_ledger(text: str, *, lenient: bool = True) -> ParseResult:
    """Converte o texto do ledger em rows brutas, em ordem de arquivo.

    Em modo estrito levanta `LedgerError` no primeiro problema (a semântica do
    appender). Em modo leniente acumula avisos e segue.
    """
    result = ParseResult()
    current: dict[str, Any] | None = None
    lines = text.split("\n")
    i = 0

    def problem(lineno: int, why: str) -> None:
        if not lenient:
            raise LedgerError(f"linha {lineno}: {why}")
        result.warnings.append(f"linha {lineno}: {why}")

    while i < len(lines):
        lineno = i + 1
        line = lines[i].rstrip("\r")  # tolera conversão CRLF
        i += 1

        if line == "" or line.startswith("#") or line == "dispatches:":
            continue

        match = ROW_RE.match(line)
        if not match:
            problem(lineno, "forma de linha não reconhecida")
            continue

        indent, key, inline = match.groups()

        # Valor possivelmente multi-linha: acumula até virar JSON válido ou até
        # a próxima linha de row.
        buffer = inline if inline is not None else ""
        value, err = (_MISSING, "valor vazio")
        if buffer.strip():
            value, err = _loads(buffer)
        while value is _MISSING and i < len(lines):
            nxt = lines[i].rstrip("\r")
            if ROW_RE.match(nxt):
                break  # começou outra chave — o valor nunca fechou
            buffer += "\n" + nxt
            i += 1
            if buffer.strip():
                value, err = _loads(buffer)

        if value is _MISSING:
            problem(lineno, f'valor de "{key}" não é JSON válido ({err})')
            continue
        if err:
            result.warnings.append(f'linha {lineno}: "{key}" — {err}')

        if indent == "  - ":
            if key not in ("dispatch_id", "close_of"):
                problem(lineno, f'row deve começar com dispatch_id ou close_of, veio "{key}"')
                current = None
                continue
            current = {key: value}
            result.rows.append(current)
        else:
            if current is None:
                problem(lineno, "continuação antes de qualquer row")
                continue
            current[key] = value

    return result


def join_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Casa cada dispatch row com sua close row (a disciplina dos dois appends).

    Retorna mais antigo primeiro. Uma dispatch sem close row está aberta; uma
    close row órfã (dispatch nunca registrada) é uma quebra da disciplina
    upstream e é exposta como tal em vez de silenciada.
    """
    dispatches: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    closes: dict[str, dict[str, Any]] = {}

    for row in rows:
        if "dispatch_id" in row:
            did = row["dispatch_id"]
            # Um id é contratualmente uma string não-vazia (append-dispatch.cjs:145).
            # Uma row cujo `dispatch_id` parseou para lista/objeto JSON não é
            # hasheável e, usada como chave de dict, levantaria TypeError —
            # derrubando o parse INTEIRO do repo (join_rows roda antes do cache) e
            # dando 500 em todo endpoint. Pular a row honra o Princípio 1 (uma row
            # ilegível vira aviso e é pulada; o resto do ledger é servido).
            if not isinstance(did, str):
                continue
            if did not in dispatches:
                order.append(did)
            dispatches[did] = row
        elif "close_of" in row:
            close_of = row["close_of"]
            if not isinstance(close_of, str):
                continue
            closes[close_of] = row

    joined: list[dict[str, Any]] = []
    for did in order:
        row = dict(dispatches[did])
        close = closes.get(did)
        row["_close"] = close
        row["_state"] = "closed" if close else "open"
        # Rows pré-v0.5.2 não têm `groups`; marcamos em vez de tentar adaptar.
        row["_legacy"] = "groups" not in row
        row["_live"] = row.get("dispatch_type") in LIVE_TYPES
        row["_agent_count"] = count_agents(row)
        joined.append(row)

    for close_of, close in closes.items():
        if close_of not in dispatches:
            joined.append(
                {
                    "dispatch_id": close_of,
                    "goal": "(close row órfã — a dispatch row nunca foi escrita)",
                    "_orphan_close": True,
                    "_close": close,
                    "_state": "closed",
                    "_legacy": True,
                    "_live": False,
                    "_agent_count": 0,
                }
            )

    return joined


def count_agents(row: dict[str, Any]) -> int:
    groups = row.get("groups")
    if not isinstance(groups, list):
        return 0
    return sum(
        len(g["agents"])
        for g in groups
        if isinstance(g, dict) and isinstance(g.get("agents"), list)
    )


# ---------------------------------------------------------------------------
# Cache de parse
# ---------------------------------------------------------------------------


@dataclass
class RepoRows:
    """O ledger de um repo já parseado e joinado, mais o contexto da leitura."""

    rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ledger_exists: bool = False
    error: str | None = None


# path do ledger -> (fingerprint, RepoRows). Memo de processo, sem expiração:
# a chave JÁ é o conteúdo (mtime_ns + tamanho), então uma entrada obsoleta é
# impossível de acertar. O teto de memória é o número de repos observados.
# A chave ASSUME que todo write muda o tamanho do arquivo — verdade para o
# appender append-only, que sempre acrescenta uma row. Uma edição fora-de-banda
# que preservasse o tamanho exato poderia servir stale até o próximo append.
_CACHE: dict[str, tuple[tuple[int, int] | None, RepoRows]] = {}

# Contador de parses de verdade. Existe para o teste conseguir provar que o
# cache pegou — sem ele o "não reparseou" só seria observável por tempo, que é
# métrica frágil.
_parse_count = 0


def clear_cache() -> None:
    """Esvazia o memo. Só testes precisam: em produção a fingerprint basta."""
    global _parse_count
    _CACHE.clear()
    _parse_count = 0


def parse_count() -> int:
    """Quantos parses reais aconteceram desde o último `clear_cache`."""
    return _parse_count


def _fingerprint(path: Path) -> tuple[int, int] | None:
    """A MESMA impressão que `signature` usa — mtime_ns + tamanho, ou None."""
    try:
        stat = path.stat()
    except OSError:
        return None
    return (stat.st_mtime_ns, stat.st_size)


def load_repo_rows(repo: Path, *, copy: bool = True) -> RepoRows:
    """Rows joinadas de um repo, reparseando só quando o arquivo mudou.

    O parse completo do maior ledger real (~1.5 MB) custa centenas de ms, e o
    `/api/stream` bate no disco a cada segundo enquanto as novas agregações
    precisam do ledger INTEIRO (não dá mais para escapar truncando por `limit`).
    Sem memo, o custo por request cresceria com o histórico — que é append-only
    e só cresce.

    `copy=True` devolve os dicts de TOPO copiados, para que quem receber possa
    anotar campos (`_repo`, ...) sem contaminar o cache. A cópia é rasa de
    propósito: os aninhados (`groups`, `connections`) pesam quase tudo, e
    nenhuma função deste módulo os edita in-place — `truncate_prompts` e `slim`
    reconstroem o que tocam. Copiar fundo aqui custaria mais que o parse que o
    cache economiza.

    A garantia REAL de `copy=False`: os VALORES (dicts de topo e aninhados) são
    compartilhados com o cache — seguro pela disciplina copy-on-write de todo
    escritor deste módulo, que reconstrói o que toca em vez de mutar — mas o
    CONTÊINER da lista é privado por chamador (uma cópia rasa `list(rows)`). Sem
    isso, um `data.rows.reverse()`/`.sort()` em qualquer chamador corromperia
    permanentemente a ordem cronológica que o cache serve a `read_repo`,
    `first_day`/`last_day` e `daily_series`. A cópia da lista é O(n) de ponteiros,
    barata perto do parse — fecha o buraco de mutação de contêiner sem tocar nos
    ~1.5 MB de aninhados.
    """
    global _parse_count

    ledger_path = repo / LEDGER_RELPATH
    key = str(ledger_path)
    fingerprint = _fingerprint(ledger_path)

    cached = _CACHE.get(key)
    if cached is not None and cached[0] == fingerprint:
        data = cached[1]
    else:
        data = _read_repo_rows(ledger_path)
        _parse_count += 1
        _CACHE[key] = (fingerprint, data)

    if not copy:
        # Valores compartilhados, contêiner da lista privado por chamador.
        return RepoRows(
            rows=list(data.rows),
            warnings=data.warnings,
            ledger_exists=data.ledger_exists,
            error=data.error,
        )
    return RepoRows(
        rows=[dict(row) for row in data.rows],
        warnings=list(data.warnings),
        ledger_exists=data.ledger_exists,
        error=data.error,
    )


def _read_repo_rows(ledger_path: Path) -> RepoRows:
    """Leitura crua de um ledger. Um ledger ausente não é erro — é um repo novo."""
    if not ledger_path.is_file():
        return RepoRows(ledger_exists=False)
    try:
        text = ledger_path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return RepoRows(ledger_exists=True, error=str(exc))
    parsed = parse_ledger(text)
    return RepoRows(
        rows=join_rows(parsed.rows),
        warnings=parsed.warnings,
        ledger_exists=True,
    )


def truncate_prompts(row: dict[str, Any], limit: int) -> dict[str, Any]:
    """Encolhe os `initial_prompt` para a listagem. O detalhe serve o texto inteiro."""
    groups = row.get("groups")
    if not isinstance(groups, list):
        return row

    trimmed_groups = []
    truncated_any = False
    for group in groups:
        if not isinstance(group, dict):
            trimmed_groups.append(group)
            continue
        group = dict(group)
        agents = []
        for agent in group.get("agents", []) or []:
            if isinstance(agent, dict) and isinstance(agent.get("initial_prompt"), str):
                agent = dict(agent)
                prompt = agent["initial_prompt"]
                if len(prompt) > limit:
                    agent["initial_prompt"] = prompt[:limit] + "…"
                    agent["_prompt_truncated"] = True
                    truncated_any = True
            agents.append(agent)
        group["agents"] = agents
        trimmed_groups.append(group)

    row = dict(row)
    row["groups"] = trimmed_groups
    row["_prompts_truncated"] = truncated_any
    return row


def read_pending(repo: Path) -> list[dict[str, Any]]:
    """Lê as sheets pré-confirm de `telemetry/agents/pending/*.json`.

    Este é o artefato NOVO do control plane: a sheet que o humano revisa antes
    de confirmar. Não faz parte do ledger e é a única superfície editável.
    """
    pending_dir = repo / PENDING_RELPATH
    if not pending_dir.is_dir():
        return []

    sheets: list[dict[str, Any]] = []
    for path in sorted(pending_dir.glob("*.json")):
        entry: dict[str, Any] = {
            "_file": path.name,
            "_path": str(path),
            "_mtime": None,
            "_error": None,
        }
        try:
            # `stat` DENTRO da guarda, junto do read: o dir de pending é a única
            # superfície editável, então uma sheet pode ser apagada/renomeada
            # entre o `glob` acima e o `stat` aqui. Fora da guarda esse OSError
            # subiria como 500 em /api/snapshot, /api/overview E /api/repo, e
            # ainda mataria o gerador do SSE — derrubando toda UI conectada. Uma
            # sheet que some no meio da varredura degrada a uma entry com `_error`.
            entry["_mtime"] = path.stat().st_mtime
            sheet = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            entry["_error"] = f"sheet ilegível: {exc}"
            entry["sheet"] = None
        else:
            entry["sheet"] = sheet
            if isinstance(sheet, dict):
                entry["_agent_count"] = count_agents(sheet)
                entry["_live"] = sheet.get("dispatch_type") in LIVE_TYPES
        sheets.append(entry)
    return sheets


def read_repo(repo: Path, limit: int, prompt_limit: int) -> dict[str, Any]:
    """Estado de um repo: sheets pendentes + as `limit` dispatches mais recentes.

    Passa pelo cache de parse, mas a FORMA do retorno é intocada: dez variantes
    de UI e os testes já consomem exatamente estas chaves.
    """
    data = load_repo_rows(repo)
    result: dict[str, Any] = {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "pending": read_pending(repo),
        "dispatches": [],
        "total_dispatches": 0,
        "open_dispatches": 0,
        "warnings": [],
        "error": data.error,
    }

    if not data.ledger_exists or data.error:
        return result

    joined = data.rows
    result["warnings"] = data.warnings
    result["total_dispatches"] = len(joined)
    result["open_dispatches"] = sum(1 for d in joined if d["_state"] == "open")

    # Mais recentes primeiro; o ledger é cronológico por append.
    result["dispatches"] = [
        truncate_prompts(d, prompt_limit) for d in reversed(joined)
    ][:limit]
    return result


def find_dispatch(repo: Path, dispatch_id: str) -> dict[str, Any] | None:
    """Uma dispatch, sem truncar nada — para a visão de detalhe."""
    data = load_repo_rows(repo)
    if not data.ledger_exists:
        return None
    for row in data.rows:
        if row.get("dispatch_id") == dispatch_id:
            return row
    return None


# ---------------------------------------------------------------------------
# Agregações
# ---------------------------------------------------------------------------


def _iso_day(value: Any) -> str | None:
    """`YYYY-MM-DD` do começo de uma string ISO-8601, se houver."""
    if not isinstance(value, str):
        return None
    match = _ISO_DAY_RE.match(value.strip())
    if not match:
        return None
    year, month, day = (int(g) for g in match.groups())
    try:
        date(year, month, day)
    except ValueError:
        return None  # 2026-13-45 casa o regex mas não é um dia
    return match.group(0)


def iso_date(row: dict[str, Any]) -> str | None:
    """O dia `YYYY-MM-DD` de uma dispatch, com fallback pelo `dispatch_id`.

    O dia é derivado do UTC do `created` (que termina em `Z`), NÃO do fuso do
    usuário. É uma escolha, e a escolha é essa por um motivo: o `dispatch_id` —
    a única fonte de dia que as rows legacy têm — já é escrito com prefixo de
    data, e servidor e cliente precisam concordar sobre em qual coluna do
    gráfico uma dispatch cai. Converter para o local do navegador faria a mesma
    row pular de bucket dependendo de quem olha. Na prática o desvio é de no
    máximo um dia, e só para dispatches perto da virada UTC.

    Precedência: `created` → `_close.closed` → prefixo do `dispatch_id` → None.
    O `_close.closed` vem ANTES do prefixo do id porque é STAMPADO pelo appender
    (append-dispatch.cjs:351) — é autoritativo, enquanto o prefixo `YYYY-MM-DD`
    do id é só convenção não-forçada (o appender não valida o formato do id). Uma
    close row órfã com id malformado ainda tem o timestamp exato do fechamento em
    `_close.closed`; sem essa precedência ela ficaria sem data com o dado à mão.
    O prefixo do id fica por último — é o que recupera o dia das rows pré-v0.5.2
    que não têm `created` nem `_close`.
    """
    day = _iso_day(row.get("created"))
    if day:
        return day
    close = row.get("_close")
    if isinstance(close, dict):
        day = _iso_day(close.get("closed"))
        if day:
            return day
    return _iso_day(row.get("dispatch_id"))


def _type_of(row: dict[str, Any]) -> str:
    """`dispatch_type`, ou o bucket explícito quando ausente/não-string."""
    value = row.get("dispatch_type")
    return value if isinstance(value, str) and value else NO_TYPE


def summarize_repo(
    repo: Path, *, today: str, pending: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Agregados sobre o ledger INTEIRO de um repo (não sobre a janela `limit`).

    Contagens são sempre sobre todas as rows joinadas: um painel que dissesse
    "181 dispatches" mas contasse só as 40 servidas seria uma mentira silenciosa.

    `pending` é opcional só por PERFORMANCE: aqui só se usa `len(pending)` para
    `pending_count`, mas o `/api/overview` já lê as sheets pendentes por repo para
    a lista de atenção. Passá-las evita um segundo `read_pending` (um glob de
    disco) por repo por request. Ausente, lê por conta própria.
    """
    data = load_repo_rows(repo, copy=False)
    rows = data.rows
    if pending is None:
        pending = read_pending(repo)

    by_type: dict[str, int] = {}
    open_count = closed_count = legacy_count = live_count = 0
    created_today = closed_today = 0
    days: list[str] = []
    created_stamps: list[str] = []

    for row in rows:
        by_type[_type_of(row)] = by_type.get(_type_of(row), 0) + 1
        if row.get("_state") == "open":
            open_count += 1
        else:
            closed_count += 1
        if row.get("_legacy"):
            legacy_count += 1
        if row.get("_live"):
            live_count += 1

        day = iso_date(row)
        if day:
            days.append(day)
            if day == today:
                created_today += 1

        close = row.get("_close")
        if isinstance(close, dict) and _iso_day(close.get("closed")) == today:
            closed_today += 1

        created = row.get("created")
        if isinstance(created, str):
            created_stamps.append(created)

    return {
        "name": repo.name,
        "path": str(repo),
        "ledger_exists": data.ledger_exists,
        "error": data.error,
        "warning_count": len(data.warnings),
        "total": len(rows),
        "open": open_count,
        "closed": closed_count,
        "legacy": legacy_count,
        "by_type": dict(sorted(by_type.items())),
        "live": live_count,
        # RESERVED = tipo não-dispatchável sob v0.6.0. Rows legacy ficam de fora
        # dos dois lados: elas são de antes da distinção existir.
        # CAVEAT (não é partição): `total == live + reserved + legacy` NÃO é
        # garantido. Uma research row cujo `groups` falhou no parse leniente fica
        # SEM `groups` → `_legacy=True` E `_live=True` ao mesmo tempo, contada nas
        # duas contagens. A UI NÃO deve renderizar live/reserved/legacy como uma
        # partição fechada de `total`. (Pinado em test_legacy_live_double_count.)
        "reserved": sum(1 for r in rows if not r.get("_live") and not r.get("_legacy")),
        "pending_count": len(pending),
        "today": {"created": created_today, "closed": closed_today},
        # Mesmo número que `open`, com nome próprio: a superfície "em execução"
        # da UI é conceitualmente outra coisa e pode divergir na Fase 2.
        "open_now": open_count,
        "first_day": min(days) if days else None,
        "last_day": max(days) if days else None,
        "last_created": max(created_stamps) if created_stamps else None,
    }


def _group_stats(row: dict[str, Any]) -> dict[str, Any]:
    """Achata `groups`/`connections` em contagens — o suficiente para a listagem."""
    roles: dict[str, int] = {}
    group_count = 0
    robot_talks = False

    groups = row.get("groups")
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, dict):
                continue
            group_count += 1
            if group.get("robot_talks"):
                robot_talks = True
            for agent in group.get("agents") or []:
                if not isinstance(agent, dict):
                    continue
                role = agent.get("role")
                if isinstance(role, str) and role:
                    roles[role] = roles.get(role, 0) + 1

    conn_types: set[str] = set()
    connections = row.get("connections")
    if isinstance(connections, list):
        for conn in connections:
            if isinstance(conn, dict) and isinstance(conn.get("type"), str):
                conn_types.add(conn["type"])

    return {
        "_group_count": group_count,
        "_robot_talks": robot_talks,
        "_roles": dict(sorted(roles.items())),
        "_connection_types": sorted(conn_types),
    }


def slim(row: dict[str, Any], *, goal_limit: int = 240) -> dict[str, Any]:
    """A dispatch em peso de listagem: cabeçalho + contagens, zero prompt.

    As listagens novas percorrem o ledger inteiro (~700 rows), e é o
    `initial_prompt` que carrega quase todo o byte. `truncate_prompts` encolhe
    os prompts mas ainda envia a árvore de `groups`; aqui ela some inteira e
    vira contagem. Quem quiser o texto pede `/api/dispatch/{repo}/{id}`.
    """
    goal = row.get("goal")
    truncated = False
    if isinstance(goal, str) and len(goal) > goal_limit:
        goal = goal[:goal_limit] + "…"
        truncated = True

    close = row.get("_close")
    slim_close = None
    if isinstance(close, dict):
        # Só o que a listagem mostra. `agents_spawned` e `feedback_prompts`
        # ficam para o detalhe — `feedback_prompts` é texto longo.
        slim_close = {
            "closed": close.get("closed"),
            "exit_reason": close.get("exit_reason"),
        }

    out: dict[str, Any] = {
        "dispatch_id": row.get("dispatch_id"),
        "created": row.get("created"),
        "_day": iso_date(row),
        "dispatch_type": row.get("dispatch_type"),
        "goal": goal,
        "invoked_by": row.get("invoked_by"),
        "working_folder": row.get("working_folder"),
        "max_loops": row.get("max_loops"),
        "final_approver": row.get("final_approver"),
        "anti_bias_global": row.get("anti_bias_global"),
        "_state": row.get("_state"),
        "_live": row.get("_live"),
        "_legacy": row.get("_legacy"),
        "_agent_count": row.get("_agent_count"),
        "_close": slim_close,
    }
    if truncated:
        out["_goal_truncated"] = True
    if row.get("_orphan_close"):
        out["_orphan_close"] = True
    out.update(_group_stats(row))
    return out


def daily_series(
    rows: list[dict[str, Any]], *, days: int | None = None
) -> dict[str, Any]:
    """Histograma diário empilhado por `dispatch_type`.

    Os dias são CONTÍGUOS entre o primeiro e o último observado, com zeros nos
    vazios. Pular os dias sem dispatch encolheria o eixo e faria uma cadência
    irregular parecer regular — o gráfico mentiria exatamente sobre o que ele
    existe para mostrar.
    """
    counts: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {}
    undated = 0

    for row in rows:
        day = iso_date(row)
        if not day:
            undated += 1
            continue
        counts.setdefault(day, {})
        kind = _type_of(row)
        counts[day][kind] = counts[day].get(kind, 0) + 1

    if not counts:
        return {
            "days": [],
            "types": [],
            "series": {},
            "totals": {},
            "max_day": 0,
            "undated": undated,
            "out_of_range": 0,
            "truncated_span": False,
        }

    first = date.fromisoformat(min(counts))
    last = date.fromisoformat(max(counts))

    # Clampa a borda SUPERIOR da janela a HOJE (UTC). O passado remoto já é capado
    # por MAX_SPAN_DAYS abaixo, mas o futuro não era: um único typo de século (uma
    # row datada 2126) viraria a âncora `last` e empurraria todas as rows reais
    # para fora do range — o gráfico ficaria vazio por causa de UMA row. Datas
    # além de hoje são out_of_range, não âncora. (Skew de relógio dentro do span é
    # inofensivo — o ponto é o outlier de futuro distante que redefine o eixo.)
    today = datetime.now(timezone.utc).date()
    if last > today:
        last = today
    if first > last:
        first = last
    span = (last - first).days + 1

    # Uma única data corrompida (1970) esticaria o eixo para dezenas de milhares
    # de buckets e derrubaria o cliente. Preferimos os dias mais RECENTES: o
    # passado remoto de um ledger vivo é o que menos interessa.
    truncated_span = span > MAX_SPAN_DAYS
    if truncated_span:
        span = MAX_SPAN_DAYS
        first = last - timedelta(days=span - 1)

    day_list = [(first + timedelta(days=i)).isoformat() for i in range(span)]
    if days is not None and days > 0 and days < len(day_list):
        day_list = day_list[-days:]

    window = set(day_list)
    out_of_range = sum(
        total
        for day, kinds in counts.items()
        if day not in window
        for total in [sum(kinds.values())]
    )

    kinds_present = sorted(
        {kind for day, kinds in counts.items() if day in window for kind in kinds}
    )
    series = {
        kind: [counts.get(day, {}).get(kind, 0) for day in day_list]
        for kind in kinds_present
    }
    for kind in kinds_present:
        totals[kind] = sum(series[kind])

    max_day = max(
        (sum(counts.get(day, {}).values()) for day in day_list), default=0
    )

    return {
        "days": day_list,
        "types": kinds_present,
        "series": series,
        "totals": totals,
        "max_day": max_day,
        "undated": undated,
        # Rows datadas que caíram fora da janela (por cap de span ou por `days`).
        # `totals` conta só o que está plotado, então este número é o que faltaria
        # para fechar com `summarize_repo.total`.
        "out_of_range": out_of_range,
        "truncated_span": truncated_span,
    }


def signature(repos: list[Path]) -> tuple:
    """Impressão barata do estado em disco, para detectar mudança sem reparsear.

    Cobre o ledger e cada sheet pendente (mtime + tamanho). Um append muda o
    tamanho; uma edição de sheet muda o mtime.
    """
    parts: list[tuple] = []
    for repo in repos:
        paths = [repo / LEDGER_RELPATH]
        pending_dir = repo / PENDING_RELPATH
        if pending_dir.is_dir():
            paths.extend(sorted(pending_dir.glob("*.json")))
        for path in paths:
            try:
                stat = path.stat()
                parts.append((str(path), stat.st_mtime_ns, stat.st_size))
            except OSError:
                parts.append((str(path), None, None))
    return tuple(parts)
