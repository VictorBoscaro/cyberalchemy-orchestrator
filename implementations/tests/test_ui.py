"""Teste Playwright — roda o MESMO contrato contra todas as variantes de UI.

Exige o servidor no ar (`python -m server.main` a partir de implementations/).

    python implementations/tests/test_ui.py            # todas
    python implementations/tests/test_ui.py terminal   # só uma

Além dos testids, cada variante é checada em coisas que só aparecem no browser:
erro de console, JS que não renderizou, dependência externa (a página tem que
funcionar offline), e conexão SSE viva. Screenshots vão para
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

    # Uma página que só funciona online falha o requisito de autocontida.
    external: list[str] = []
    page.on(
        "request",
        lambda r: external.append(r.url)
        if not r.url.startswith((BASE, "data:", "blob:", "about:"))
        else None,
    )

    url = f"{BASE}/static/ui/{variant}/index.html"
    # NÃO usar `networkidle`: o SSE mantém uma requisição aberta para sempre, então
    # a rede nunca fica ociosa e o goto estoura o timeout. Esperamos o app abaixo.
    response = page.goto(url, wait_until="domcontentloaded", timeout=20000)

    if not rep.check("página carrega (HTTP 200)", response is not None and response.status == 200,
                     f"(status {response.status if response else 'n/a'})"):
        return rep

    # O render é assíncrono: espera o app aparecer em vez de dormir.
    try:
        page.wait_for_selector('[data-testid="app"]', timeout=10000)
    except Exception:
        rep.check("app renderiza", False, "(timeout esperando [data-testid=app])")
        return rep
    rep.check("app renderiza", True)

    # O shell costuma pintar antes dos dados (fetch/SSE são assíncronos).
    # Esperar o primeiro card evita contar cedo demais e culpar a UI por timing.
    try:
        page.wait_for_selector('[data-testid="dispatch-card"]', timeout=10000)
    except Exception:
        pass  # a checagem de contagem abaixo reporta o problema de verdade

    for testid in REQUIRED_TESTIDS:
        count = page.locator(f'[data-testid="{testid}"]').count()
        rep.check(f"testid '{testid}'", count > 0, "(ausente)")

    # Dados reais chegaram na tela?
    cards = page.locator('[data-testid="dispatch-card"]').count()
    rep.check("renderizou dispatches", cards > 0, f"(veio {cards})")

    pending = page.locator('[data-testid="pending-card"]').count()
    rep.check("renderizou a sheet pendente", pending >= 1, f"(veio {pending})")

    repos = page.locator('[data-testid="repo-section"]').count()
    rep.check("renderizou repos", repos > 0, f"(veio {repos})")

    # O botão do gate existe e está desabilitado (Fase 2 ainda não liga).
    btn = page.locator('[data-testid="dispatch-button"]').first
    if btn.count() > 0:
        rep.check("botão Disparar desabilitado", btn.is_disabled(), "(está habilitado!)")

    # Atributos por card exigidos pelo contrato.
    first = page.locator('[data-testid="dispatch-card"]').first
    rep.check("card tem data-dispatch-id", bool(first.get_attribute("data-dispatch-id")))
    state = first.get_attribute("data-state")
    rep.check("card tem data-state válido", state in ("open", "closed"), f"(veio {state!r})")

    # O total tem que ser um número plausível, não placeholder.
    total_text = page.locator('[data-testid="total-count"]').first.inner_text()
    has_digit = any(ch.isdigit() for ch in total_text)
    rep.check("total-count mostra número", has_digit, f"(texto {total_text!r})")

    # SSE ligado. O handshake leva um instante e algumas variantes pintam um
    # estado inicial antes disso — então esperamos em vez de ler uma vez só.
    # ATENÇÃO: "desconectado" CONTÉM "conectado". Uma checagem ingênua de
    # substring passa justamente no caso que deveria reprovar, então o estado
    # negativo é excluído explicitamente.
    try:
        page.wait_for_function(
            """() => {
                const el = document.querySelector('[data-testid="live-indicator"]');
                if (!el) return false;
                const t = el.innerText.toLowerCase();
                return t.includes('conectado') && !t.includes('desconectado');
            }""",
            timeout=8000,
        )
        live_ok = True
    except Exception:
        live_ok = False
    live_text = page.locator('[data-testid="live-indicator"]').first.inner_text().lower()
    rep.check("indicador diz conectado", live_ok, f"(texto {live_text!r})")

    # A asserção acima só vale se souber reprovar: confirma que o texto atual
    # não é o estado negativo disfarçado.
    rep.check(
        "indicador não está em estado de queda",
        "desconectado" not in live_text and "interrompid" not in live_text,
        f"(texto {live_text!r})",
    )

    # Nada quebrado no console, nada externo.
    real_errors = [e for e in console_errors if "favicon" not in e.lower()]
    rep.check("sem erro de console", not real_errors, f"({real_errors[:2]})")
    # O SSE é uma requisição que fica aberta; ela é abortada quando a página é
    # fechada. Isso é o encerramento normal, não uma falha da UI.
    real_failures = [u for u in failed_requests if "/api/stream" not in u]
    rep.check("sem requisição falha", not real_failures, f"({real_failures[:2]})")
    rep.check("sem dependência externa", not external, f"({external[:2]})")

    # A página tem que ter altura real (não um corpo vazio de 0px).
    height = page.evaluate("document.body.scrollHeight")
    rep.check("página tem conteúdo", height > 400, f"(altura {height}px)")

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
            # Uma página nova por variante: reusar a mesma acumula os listeners
            # de console/rede, e as falhas de uma variante vazavam para a seguinte.
            page = ctx.new_page()
            try:
                rep = test_variant(page, variant)
            finally:
                page.close()
            reports.append(rep)
            for f in rep.failed:
                print(f"  FAIL  {f}")
            print(f"  {len(rep.passed)} passaram, {len(rep.failed)} falharam")
        browser.close()

    print("\n" + "=" * 58)
    for rep in reports:
        mark = "OK  " if rep.ok else "FALHA"
        print(f"{mark}  {rep.variant:<18} {len(rep.passed)}/{len(rep.passed) + len(rep.failed)}")
    for variant in missing:
        print(f"AUSENTE  {variant}")

    broken = [r.variant for r in reports if not r.ok]
    if broken or missing:
        print(f"\nquebradas: {broken or 'nenhuma'} | ausentes: {missing or 'nenhuma'}")
        return 1
    print(f"\ntodas as {len(reports)} variantes passaram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
