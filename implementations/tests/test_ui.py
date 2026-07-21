"""Playwright test — runs the SAME contract against every UI variant.

Requires the server to be up (`python -m server.main` from implementations/).

    python implementations/tests/test_ui.py            # all
    python implementations/tests/test_ui.py terminal   # just one

Beyond the testids, each variant is checked for things that only show up in the
browser: console errors, JS that failed to render, external dependencies (the page
must work offline), and a live SSE connection. Screenshots go to
`implementations/tests/screenshots/`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765"
ROOT = Path(__file__).resolve().parent.parent
SHOTS = Path(__file__).resolve().parent / "screenshots"

VARIANTS = [
    "terminal",
    "mission-control",
    "brutalist",
    "linear",
    "cyberpunk",
    "blueprint",
    "grimoire",
    "radar",
    "swiss",
    "aurora",
]

REQUIRED_TESTIDS = [
    "app",
    "live-indicator",
    "pending-list",
    "pending-card",
    "dispatch-button",
    "dispatch-list",
    "dispatch-card",
    "repo-section",
    "total-count",
]


class Report:
    def __init__(self, variant: str) -> None:
        self.variant = variant
        self.passed: list[str] = []
        self.failed: list[str] = []

    def check(self, name: str, cond: bool, detail: str = "") -> bool:
        if cond:
            self.passed.append(name)
        else:
            self.failed.append(f"{name} {detail}".strip())
        return cond

    @property
    def ok(self) -> bool:
        return not self.failed


def test_variant(page, variant: str) -> Report:
    rep = Report(variant)
    console_errors: list[str] = []
    failed_requests: list[str] = []

    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("requestfailed", lambda r: failed_requests.append(r.url))

    # A page that only works online fails the self-contained requirement.
    external: list[str] = []
    page.on(
        "request",
        lambda r: external.append(r.url)
        if not r.url.startswith((BASE, "data:", "blob:", "about:"))
        else None,
    )

    url = f"{BASE}/static/ui/{variant}/index.html"
    # Do NOT use `networkidle`: the SSE keeps a request open forever, so the
    # network never goes idle and goto blows the timeout. We wait for the app below.
    response = page.goto(url, wait_until="domcontentloaded", timeout=20000)

    if not rep.check("page loads (HTTP 200)", response is not None and response.status == 200,
                     f"(status {response.status if response else 'n/a'})"):
        return rep

    # The render is async: wait for the app to appear instead of sleeping.
    try:
        page.wait_for_selector('[data-testid="app"]', timeout=10000)
    except Exception:
        rep.check("app renders", False, "(timeout waiting for [data-testid=app])")
        return rep
    rep.check("app renders", True)

    # The shell usually paints before the data (fetch/SSE are async).
    # Waiting for the first card avoids counting too early and blaming the UI for timing.
    try:
        page.wait_for_selector('[data-testid="dispatch-card"]', timeout=10000)
    except Exception:
        pass  # the count check below reports the real problem

    for testid in REQUIRED_TESTIDS:
        count = page.locator(f'[data-testid="{testid}"]').count()
        rep.check(f"testid '{testid}'", count > 0, "(missing)")

    # Did real data reach the screen?
    cards = page.locator('[data-testid="dispatch-card"]').count()
    rep.check("rendered dispatches", cards > 0, f"(got {cards})")

    pending = page.locator('[data-testid="pending-card"]').count()
    rep.check("rendered the pending sheet", pending >= 1, f"(got {pending})")

    repos = page.locator('[data-testid="repo-section"]').count()
    rep.check("rendered repos", repos > 0, f"(got {repos})")

    # The gate button exists and is disabled (Phase 2 does not wire it yet).
    btn = page.locator('[data-testid="dispatch-button"]').first
    if btn.count() > 0:
        rep.check("Dispatch button disabled", btn.is_disabled(), "(it is enabled!)")

    # Per-card attributes required by the contract.
    first = page.locator('[data-testid="dispatch-card"]').first
    rep.check("card has data-dispatch-id", bool(first.get_attribute("data-dispatch-id")))
    state = first.get_attribute("data-state")
    rep.check("card has valid data-state", state in ("open", "closed"), f"(got {state!r})")

    # The total must be a plausible number, not a placeholder.
    total_text = page.locator('[data-testid="total-count"]').first.inner_text()
    has_digit = any(ch.isdigit() for ch in total_text)
    rep.check("total-count shows a number", has_digit, f"(text {total_text!r})")

    # SSE is up. The handshake takes a moment and some variants paint an initial
    # state before that — so we wait instead of reading once.
    # NOTE: "disconnected" CONTAINS "connected". A naive substring check would
    # pass in exactly the case that should fail, so the negative state is
    # excluded explicitly.
    try:
        page.wait_for_function(
            """() => {
                const el = document.querySelector('[data-testid="live-indicator"]');
                if (!el) return false;
                const t = el.innerText.toLowerCase();
                return t.includes('connected') && !t.includes('disconnected');
            }""",
            timeout=8000,
        )
        live_ok = True
    except Exception:
        live_ok = False
    live_text = page.locator('[data-testid="live-indicator"]').first.inner_text().lower()
    rep.check("indicator says connected", live_ok, f"(text {live_text!r})")

    # The assertion above only counts if it can fail: confirm the current text
    # is not the negative state in disguise.
    rep.check(
        "indicator is not in a down state",
        "disconnected" not in live_text and "interrupt" not in live_text,
        f"(text {live_text!r})",
    )

    # Nothing broken in the console, nothing external.
    real_errors = [e for e in console_errors if "favicon" not in e.lower()]
    rep.check("no console error", not real_errors, f"({real_errors[:2]})")
    # The SSE is a request that stays open; it is aborted when the page is
    # closed. That is the normal teardown, not a UI failure.
    real_failures = [u for u in failed_requests if "/api/stream" not in u]
    rep.check("no failed request", not real_failures, f"({real_failures[:2]})")
    rep.check("no external dependency", not external, f"({external[:2]})")

    # The page must have real height (not an empty 0px body).
    height = page.evaluate("document.body.scrollHeight")
    rep.check("page has content", height > 400, f"(height {height}px)")

    SHOTS.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SHOTS / f"{variant}.png"), full_page=False)
    page.set_viewport_size({"width": 1440, "height": 2200})
    page.screenshot(path=str(SHOTS / f"{variant}-full.png"), full_page=True)
    page.set_viewport_size({"width": 1440, "height": 900})

    return rep


def main(only: list[str]) -> int:
    targets = only or VARIANTS
    missing = [v for v in targets if not (ROOT / "static" / "ui" / v / "index.html").is_file()]
    present = [v for v in targets if v not in missing]

    reports: list[Report] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        for variant in present:
            print(f"\n=== {variant} ===")
            # A fresh page per variant: reusing the same one accumulates the
            # console/network listeners, and one variant's failures leaked into the next.
            page = ctx.new_page()
            try:
                rep = test_variant(page, variant)
            finally:
                page.close()
            reports.append(rep)
            for f in rep.failed:
                print(f"  FAIL  {f}")
            print(f"  {len(rep.passed)} passed, {len(rep.failed)} failed")
        browser.close()

    print("\n" + "=" * 58)
    for rep in reports:
        mark = "OK  " if rep.ok else "FAIL "
        print(f"{mark}  {rep.variant:<18} {len(rep.passed)}/{len(rep.passed) + len(rep.failed)}")
    for variant in missing:
        print(f"MISSING  {variant}")

    broken = [r.variant for r in reports if not r.ok]
    if broken or missing:
        print(f"\nbroken: {broken or 'none'} | missing: {missing or 'none'}")
        return 1
    print(f"\nall {len(reports)} variants passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
