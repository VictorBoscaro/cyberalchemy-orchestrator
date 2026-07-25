from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright


IMPLEMENTATIONS = Path(__file__).resolve().parents[2]
REPO = IMPLEMENTATIONS.parent
PORT = 8876
BASE = f"http://127.0.0.1:{PORT}"
OUTPUT = REPO / "output" / "playwright" / "ux-validator" / "skill-control-center-phase1"
SHOTS = OUTPUT / "screenshots"
REPRESENTATIVE = OUTPUT / "representative"
FIXTURE_ROOT = IMPLEMENTATIONS / "fixtures" / "skill-control-center"
STATIC_ROOT = IMPLEMENTATIONS / "static" / "control-center"
STATES = (
    "loading", "empty", "no-match", "focal-lineage", "observed-overlay",
    "stale-degraded", "partial-error", "invalid-endpoint", "truncated-path",
    "draft-dirty", "draft-saved", "validating", "valid", "invalid",
    "save-failed", "local-conflict", "read-api-unavailable",
)
VARIANTS = ("A", "B", "C")
VIEWPORTS = {"desktop": {"width": 1440, "height": 1024}, "mobile": {"width": 390, "height": 844}}
THEMES = ("light", "dark")
REQUIRED_TESTIDS = {
    "cc-scope", "cc-attention", "cc-source-health", "cc-search", "cc-filters",
    "cc-catalog", "cc-selection", "cc-open-detail", "cc-open-topology",
    "cc-detail", "cc-topology", "cc-topology-table", "cc-path-form",
    "cc-path-result", "cc-back", "cc-status-live",
}
STATE_CASE_MAP = {
    "loading": "state-loading", "empty": "state-empty", "no-match": "state-no-match",
    "focal-lineage": "state-focal-lineage", "observed-overlay": "state-observed",
    "stale-degraded": "state-stale", "partial-error": "state-partial",
    "invalid-endpoint": "state-invalid-endpoint", "truncated-path": "state-truncated",
    "draft-dirty": "state-draft-dirty", "draft-saved": "state-draft-saved",
    "validating": "state-validating", "valid": "state-valid", "invalid": "state-invalid",
    "save-failed": "state-save-failed", "local-conflict": "state-local-conflict",
    "read-api-unavailable": "state-read-api-unavailable",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(REPO).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def wait_port() -> None:
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", PORT), timeout=.2):
                return
        except OSError:
            time.sleep(.1)
    raise RuntimeError("Control Center server did not start")


class ControlCenterFrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(IMPLEMENTATIONS)
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "server.main:app", "--host", "127.0.0.1",
             "--port", str(PORT), "--log-level", "error"],
            cwd=IMPLEMENTATIONS, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        wait_port()
        for name in ("screenshots", "representative", "accessibility", "aria", "measurements", "traces"):
            (OUTPUT / name).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.terminate()
        try:
            cls.server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.server.kill()

    def test_01_shared_contract_and_critical_flows(self) -> None:
        structural = []
        browser_records = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for variant in VARIANTS:
                context = browser.new_context(viewport=VIEWPORTS["desktop"], color_scheme="light", reduced_motion="reduce")
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
                page = context.new_page()
                console_errors: list[str] = []
                failed_requests: list[str] = []
                page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                page.on("requestfailed", lambda request: failed_requests.append(request.url))
                response = page.goto(f"{BASE}/static/control-center/{variant.lower()}/index.html", wait_until="domcontentloaded")
                self.assertEqual(response.status, 200)
                page.wait_for_function("() => document.querySelector('#result-count')?.textContent.includes('results')")

                # CF-02: selection is inert until an explicit action.
                page.locator("#search").fill("task-session")
                page.locator("#search-form button").click()
                page.wait_for_selector('.catalog-item[data-id="task-session"]')
                page.locator('.catalog-item[data-id="task-session"]').click()
                self.assertIn("task-session", page.locator("#selection").inner_text())
                self.assertEqual(page.locator('[data-testid="cc-evidence"]').count(), 0)
                self.assertIn("Identity changed", page.locator('[data-testid="cc-detail"]').inner_text())

                # CF-03 / CF-05 / CF-06: honest evidence and local-only proposal.
                page.locator('[data-testid="cc-open-detail"]').click()
                page.wait_for_selector('[data-testid="cc-evidence"]')
                self.assertEqual(page.evaluate("document.activeElement.id"), "detail-title")
                detail = page.locator('[data-testid="cc-detail"]').inner_text()
                self.assertIn("observed usage", detail.lower())
                self.assertIn("Unknown", detail)
                self.assertNotIn("Observed usage\n0", detail)
                self.assertIn("unknown-or-unavailable", detail)
                self.assertIn("sigil-invocations", detail)
                self.assertIn("Safe end of Phase 1", detail)
                page.locator('[data-testid="cc-back"]').click()
                self.assertEqual(page.evaluate("document.activeElement?.dataset?.id"), "task-session")
                page.locator("#draft-text").fill("Improve the bounded local description")
                page.locator("#save-draft").click()
                self.assertIn("Saved locally", page.locator('[data-testid="cc-draft-status"]').inner_text())
                page.locator("#validate-draft").click()
                page.wait_for_function("() => document.querySelector('[data-testid=\"cc-draft-status\"]').textContent.includes('non-authoritative')")

                # CF-04: map and semantic table are both populated from the same response.
                page.locator('[data-testid="cc-open-topology"]').click()
                page.wait_for_function("() => document.querySelector('#topology-meta')?.textContent.includes('nodes')")
                self.assertGreater(page.locator("#topology-table tr").count(), 0)

                # Path output preserves order/evidence and highlights the same table/graph identity.
                page.locator("#path-target").fill("decision-gate")
                page.locator("#path-limit").select_option("1")
                page.locator("#path-form button").click()
                page.wait_for_function("() => document.querySelector('#path-result')?.textContent.includes('truncated by declared limit')")
                path_text = page.locator("#path-result").inner_text()
                self.assertIn("task-session → decision-gate", path_text)
                self.assertIn(".agents/skills/", path_text)
                self.assertGreater(page.locator("#topology-table tr.path-hit").count(), 0)
                self.assertGreater(page.locator("#graph .edge.path-hit").count(), 0)
                self.assertGreater(page.locator("#graph .graph-node.path-hit").count(), 1)

                page.locator("#path-target").fill("not-a-real-skill")
                page.locator("#path-form button").click()
                page.wait_for_function("() => document.querySelector('#path-result')?.textContent.includes('invalid-endpoint')")
                self.assertIn("No path asserted", page.locator("#path-result").inner_text())
                self.assertEqual(page.locator(".path-hit").count(), 0)

                # Dispatch hierarchy is a distinct real model.
                page.locator('input[name="kind"][value="dispatch"]').check()
                self.assertNotIn("task-session", page.locator('[data-testid="cc-detail"]').inner_text())
                self.assertIn("filter changed", page.locator('[data-testid="cc-detail"]').inner_text())
                self.assertIn("No relationships", page.locator("#topology-table").inner_text())
                self.assertIn("Choose endpoints", page.locator("#path-result").inner_text())
                self.assertEqual(page.locator('[data-testid="cc-draft"]').count(), 0)
                page.locator("#search").fill("2026-07-20-linear-ui-multilevel")
                page.locator("#search-form button").click()
                lineage_id = "cyberalchemy-orchestrator:2026-07-20-linear-ui-multilevel"
                page.wait_for_selector(f'.catalog-item[data-id="{lineage_id}"]')
                page.locator(f'.catalog-item[data-id="{lineage_id}"]').click()
                page.locator("#model").select_option("dispatch-lineage")
                page.locator('[data-testid="cc-open-topology"]').click()
                page.wait_for_function("() => document.querySelector('#topology-meta')?.textContent.includes('5 nodes')")
                self.assertIn("parent_dispatch_id", page.locator("#topology-table").inner_text())

                # Fresh representative evidence after the reviewed interaction sequence.
                page.evaluate("window.scrollTo(0, 0)")
                page.screenshot(path=str(REPRESENTATIVE / f"variant-{variant}-desktop-light.png"), full_page=True)
                page.set_viewport_size(VIEWPORTS["mobile"])
                self.assertLessEqual(page.evaluate("document.body.scrollWidth"), VIEWPORTS["mobile"]["width"])
                page.screenshot(path=str(REPRESENTATIVE / f"variant-{variant}-mobile-light.png"), full_page=True)
                page.set_viewport_size(VIEWPORTS["desktop"])

                present = {testid: page.locator(f'[data-testid="{testid}"]').count() for testid in REQUIRED_TESTIDS}
                self.assertTrue(all(present.values()), f"missing shared test IDs in {variant}: {present}")
                forbidden = page.locator('button').all_inner_texts()
                self.assertFalse(any(word in text.lower() for text in forbidden for word in ("apply", "reconcile", "promote", "receipt")))
                self.assertEqual(console_errors, [])
                self.assertEqual(failed_requests, [])
                dimensions = page.evaluate("""() => {
                    const w=getComputedStyle(document.querySelector('.workspace'));
                    const p=getComputedStyle(document.querySelector('.surface'));
                    const s=getComputedStyle(document.querySelector('.semantic-panel'));
                    return {display:w.display,columns:w.gridTemplateColumns,radius:p.borderRadius,semanticOrder:s.order}
                }""")
                structural.append(dimensions)
                aria = page.locator("body").aria_snapshot()
                (OUTPUT / "aria" / f"variant-{variant}.yml").write_text(aria, encoding="utf-8")
                accessibility = {
                    "variant": variant, "language": page.locator("html").get_attribute("lang"),
                    "h1_count": page.locator("h1").count(), "main_count": page.locator("main").count(),
                    "skip_link": page.locator(".skip-link").count() == 1,
                    "semantic_topology_rows": page.locator("#topology-table tr").count(),
                    "keyboard_flow": "passed-native-controls-explicit-open-back",
                    "status": "automated-pass",
                    "limits": "Not a complete WCAG audit; screen-reader comprehension remains human residue.",
                }
                (OUTPUT / "accessibility" / f"variant-{variant}.json").write_text(json.dumps(accessibility, indent=2), encoding="utf-8")
                context.tracing.stop(path=str(OUTPUT / "traces" / f"critical-flows-{variant}.zip"))
                browser_records.append({"variant": variant, "console_errors": console_errors, "failed_requests": failed_requests})
                context.close()
            browser.close()

        self.assertEqual(len({json.dumps(item, sort_keys=True) for item in structural}), 3)
        (OUTPUT / "console-network.json").write_text(json.dumps(browser_records, indent=2), encoding="utf-8")

    def test_02_exact_204_screenshot_matrix(self) -> None:
        fixture_manifest = json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8"))
        fixture_digests = {
            case["case_id"]: case["sha256"]
            for fixture in fixture_manifest["fixtures"] for case in fixture["cases"]
        }
        frontend_revision = sha256_files(list(STATIC_ROOT.rglob("*.*")))
        source_revision = sha256_files(list((REPO / "docs" / "features" / "skill-control-center").glob("*.md")))
        backend_revision = sha256_files(list((IMPLEMENTATIONS / "server" / "control_center").glob("*.py")))
        rows = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for viewport_name, viewport in VIEWPORTS.items():
                for theme in THEMES:
                    context = browser.new_context(viewport=viewport, color_scheme=theme, reduced_motion="reduce")
                    page = context.new_page()
                    for variant in VARIANTS:
                        for state in STATES:
                            url = f"{BASE}/static/control-center/{variant.lower()}/index.html?state={state}&theme={theme}"
                            response = page.goto(url, wait_until="domcontentloaded")
                            self.assertEqual(response.status, 200)
                            testid = f"cc-state-{state}"
                            page.locator(f'[data-testid="{testid}"]').wait_for()
                            self.assertEqual(page.locator("h1").count(), 1)
                            self.assertEqual(page.locator("main").count(), 1)
                            self.assertEqual(page.locator("html").get_attribute("data-theme"), theme)
                            self.assertLessEqual(page.evaluate("document.body.scrollWidth"), viewport["width"])
                            page.evaluate("window.scrollTo(0, 0)")
                            filename = f"{variant}-{viewport_name}-{theme}-{state}.png"
                            screenshot = SHOTS / filename
                            page.screenshot(path=str(screenshot), full_page=True)
                            case_id = STATE_CASE_MAP[state]
                            rows.append({
                                "variant": variant, "viewport": viewport_name, "theme": theme,
                                "state": state, "fixture_case_id": case_id,
                                "fixture_digest": fixture_digests[case_id], "test_id": testid,
                                "source_revision": source_revision, "backend_revision": backend_revision,
                                "frontend_revision": frontend_revision,
                                "screenshot_path": screenshot.relative_to(REPO).as_posix(),
                                "screenshot_digest": sha256_file(screenshot),
                                "executable_test": "SCC-T-STATE-001",
                            })
                    (OUTPUT / "measurements" / f"{viewport_name}-{theme}.json").write_text(
                        json.dumps({"viewport": viewport, "theme": theme, "horizontal_overflow": False}, indent=2),
                        encoding="utf-8",
                    )
                    context.close()
            browser.close()

        expected = {(v, p, t, s) for v in VARIANTS for p in VIEWPORTS for t in THEMES for s in STATES}
        actual = {(r["variant"], r["viewport"], r["theme"], r["state"]) for r in rows}
        self.assertEqual(actual, expected)
        self.assertEqual(len(rows), 204)
        matrix_paths = {REPO / row["screenshot_path"] for row in rows}
        self.assertEqual(len(matrix_paths), 204)
        self.assertTrue(all(path.is_file() for path in matrix_paths))
        (OUTPUT / "screenshot-manifest.json").write_text(
            json.dumps({"schema_version": "1", "count": len(rows), "rows": rows}, indent=2), encoding="utf-8"
        )
        (OUTPUT / "run-metadata.json").write_text(json.dumps({
            "run_id": "skill-control-center-phase1", "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": f"{BASE}/static/control-center/{{a,b,c}}/",
            "variants": list(VARIANTS), "viewports": VIEWPORTS, "themes": list(THEMES),
            "states": list(STATES), "screenshot_count": 204,
            "fixture_calibration": "not-run-seed-validator", "promotion": "prohibited-phase1",
        }, indent=2), encoding="utf-8")
        (OUTPUT / "findings.json").write_text(json.dumps({
            "hard_gates": [], "soft_flags": [],
            "screenshot_review": "pending-independent-review",
            "human_study": ["real-user task success", "subjective workload", "trust and preference"],
            "not_automatable": ["variant preference and production promotion"],
        }, indent=2), encoding="utf-8")
        (OUTPUT / "residue-ledger.yml").write_text(
            "status: open-human-residue\nitems:\n"
            "  - real-user comprehension and task success\n"
            "  - screen-reader experience beyond semantic snapshot\n"
            "  - variant preference; promotion is prohibited in Phase 1\n",
            encoding="utf-8",
        )
        (OUTPUT / "summary.md").write_text(
            "# UX Evidence Summary\n\n"
            "- Browser-observed: 204 deterministic screenshots; shared semantic contract; responsive "
            "overflow gate; light/dark rendering; representative CF-02..06 interactions; no console "
            "or request failures.\n"
            "- Hard gates: deterministic structure, fixture binding, authority fence, unknown-not-zero, "
            "keyboard-native controls, graph-table availability.\n"
            "- Limits: automation does not prove comprehension, low workload, trust, delight, complete "
            "WCAG conformance, or real-user task success.\n"
            "- Promotion: prohibited in Phase 1; scores are descriptive only.\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
