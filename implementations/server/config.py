"""Configuração do leitor: quais repos observar.

Sem `config.json`, o servidor auto-descobre — varre o diretório pai do repo
atrás de qualquer pasta que já tenha ledger ou sheets pendentes. Isso funciona
sem setup porque os dispatches já vivem espalhados por vários repos.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from .ledger import LEDGER_RELPATH, PENDING_RELPATH

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = REPO_ROOT / "implementations" / "config.json"

# TTL do cache de `resolved_repos`. A varredura (um `iterdir` do diretório pai,
# ex. C:/Users/victo) custa dezenas de ms e roda a CADA request e a cada poll do
# SSE. Cacheamos por um tempo curto em vez de chavear no mtime do pai porque, no
# Windows, um repo que GANHA um ledger dentro de um filho já existente NÃO muda o
# mtime do pai (muda o do `telemetry/` do filho) — mtime-do-pai perderia esse
# caso de auto-descoberta. Um TTL curto re-varre no máximo a cada RESCAN_TTL s;
# com poll_seconds=1.0 um repo novo aparece em um ou dois ciclos de poll.
RESCAN_TTL = 2.0


@dataclass
class Config:
    repos: list[Path] = field(default_factory=list)
    scan_roots: list[Path] = field(default_factory=list)
    port: int = 8765
    host: str = "127.0.0.1"
    poll_seconds: float = 1.0
    limit: int = 40
    prompt_limit: int = 280
    # Cache do scan (FIX 6b). Não entram em igualdade/repr do dataclass.
    _repos_cache: list[Path] | None = field(
        default=None, compare=False, repr=False
    )
    _repos_cache_at: float = field(default=0.0, compare=False, repr=False)

    def resolved_repos(self) -> list[Path]:
        """Repos explícitos + os auto-descobertos, deduplicados e ordenados.

        Memoizado por `RESCAN_TTL` segundos: o scan é caro e roda a cada request/
        poll, mas um repo novo ainda precisa aparecer sem reiniciar o servidor —
        daí o TTL curto em vez de cache permanente.
        """
        now = time.monotonic()
        if self._repos_cache is not None and now - self._repos_cache_at < RESCAN_TTL:
            return self._repos_cache
        result = self._scan_repos()
        self._repos_cache = result
        self._repos_cache_at = now
        return result

    def _scan_repos(self) -> list[Path]:
        found: dict[str, Path] = {}

        for repo in self.repos:
            if repo.is_dir():
                found[str(repo.resolve())] = repo.resolve()

        for root in self.scan_roots:
            if not root.is_dir():
                continue
            for child in sorted(root.iterdir()):
                if not child.is_dir():
                    continue
                if (child / LEDGER_RELPATH).is_file() or (child / PENDING_RELPATH).is_dir():
                    found[str(child.resolve())] = child.resolve()

        return sorted(found.values(), key=lambda p: p.name.lower())


def load() -> Config:
    cfg = Config(scan_roots=[REPO_ROOT.parent])

    if CONFIG_PATH.is_file():
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))
        if "repos" in raw:
            cfg.repos = [Path(p) for p in raw["repos"]]
        if "scan_roots" in raw:
            cfg.scan_roots = [Path(p) for p in raw["scan_roots"]]
        for key in ("port", "host", "poll_seconds", "limit", "prompt_limit"):
            if key in raw:
                setattr(cfg, key, raw[key])

    return cfg
