"""Reader configuration: which repos to observe.

Without a `config.json`, the server auto-discovers — it scans the repo's parent
directory for any folder that already has a ledger or pending sheets. This works
with no setup because the dispatches already live spread across several repos.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from .ledger import LEDGER_RELPATH, PENDING_RELPATH

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = REPO_ROOT / "implementations" / "config.json"

# TTL of the `resolved_repos` cache. The scan (an `iterdir` of the parent
# directory, e.g. C:/Users/victo) costs tens of ms and runs on EVERY request and
# every SSE poll. We cache for a short time rather than key on the parent's mtime
# because, on Windows, a repo that GAINS a ledger inside an already-existing child
# does NOT change the parent's mtime (it changes the child's `telemetry/` mtime) —
# parent-mtime would miss that auto-discovery case. A short TTL re-scans at most
# every RESCAN_TTL s; with poll_seconds=1.0 a new repo shows up in one or two poll
# cycles.
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
    # Scan cache (FIX 6b). Excluded from the dataclass's equality/repr.
    _repos_cache: list[Path] | None = field(
        default=None, compare=False, repr=False
    )
    _repos_cache_at: float = field(default=0.0, compare=False, repr=False)

    def resolved_repos(self) -> list[Path]:
        """Explicit repos + the auto-discovered ones, deduplicated and sorted.

        Memoized for `RESCAN_TTL` seconds: the scan is expensive and runs on every
        request/poll, but a new repo still needs to appear without restarting the
        server — hence the short TTL rather than a permanent cache.
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
