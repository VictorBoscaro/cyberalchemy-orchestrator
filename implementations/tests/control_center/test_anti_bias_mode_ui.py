from __future__ import annotations

import functools
import json
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO = Path(__file__).resolve().parents[3]
UI_ROOT = REPO / "implementations/static/ui"


class _QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *args: object) -> None:
        pass


def _agents(count: int, *, with_angles: bool) -> list[dict[str, object]]:
    return [
        {
            "agent_name": f"agent-{index + 1}",
            "role": ("explorer", "skeptic", "auditor")[index],
            "model": "fixture-model",
            "token_budget": 1000,
            "initial_prompt": f"Inspect perspective {index + 1}",
            **({"angle": f"independent angle {index + 1}"} if with_angles else {}),
        }
        for index in range(count)
    ]


def _pairs(count: int) -> list[dict[str, object]]:
    return [
        {
            "left_index": left,
            "right_index": right,
            "question": f"What tension exists between {left + 1} and {right + 1}?",
            "left_position": f"independent angle {left + 1}",
            "right_position": f"independent angle {right + 1}",
            "evidence": f"fixture evidence {left + 1}-{right + 1}",
        }
        for left in range(count)
        for right in range(left + 1, count)
    ]


def _groups(mode: str) -> list[dict[str, object]]:
    enabled = mode == "enabled"
    groups = []
    for count in (1, 2, 3):
        group: dict[str, object] = {
            "group_id": f"group-{count}",
            "strategy": "parallel",
            "agents": _agents(count, with_angles=enabled and count >= 2),
        }
        if enabled and count >= 2:
            group["anti_bias"] = f"tension axis for {count} agent(s)"
            group["anti_bias_pairs"] = _pairs(count)
        groups.append(group)
    return groups


def _pending(mode: str | None) -> dict[str, object]:
    label = mode or "historical"
    sheet: dict[str, object] = {
        "schema_version": "0.6.3" if mode else "0.6.2",
        "dispatch_id": f"fixture-{label}",
        "created": "2026-08-03T12:00:00Z",
        "dispatch_type": "review",
        "goal": f"Render the {label} pending state",
        "context": "Browser-executed pending fixture",
        "invoked_by": "ui-behavior-test",
        "working_folder": "output/ui-behavior-test",
        "max_loops": 1,
        "final_approver": "test-controller",
        "groups": _groups(mode or "historical"),
        "connections": [],
    }
    if mode is not None:
        sheet["anti_bias_mode"] = mode
    if mode == "enabled":
        sheet["anti_bias_global"] = "Compare every pair in each fan-out group"
    return {
        "_file": f"fixture-{label}.yaml",
        "_path": f"telemetry/agents/pending/fixture-{label}.yaml",
        "sheet": sheet,
    }


def _snapshot() -> dict[str, object]:
    return {
        "repos": [
            {
                "name": "ui-fixture",
                "path": str(REPO),
                "ledger_exists": True,
                "error": None,
                "warnings": [],
                "total_dispatches": 0,
                "open_dispatches": 0,
                "dispatches": [],
                "pending": [_pending("enabled"), _pending("disabled"), _pending(None)],
            }
        ],
        "config": {"limit": 50, "poll_seconds": 60, "repo_count": 1},
    }


class AntiBiasModeUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        handler = functools.partial(_QuietStaticHandler, directory=str(UI_ROOT))
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.server_thread.join(timeout=5)

    def test_all_pending_renderers_distinguish_modes_and_pairwise_cardinalities(self) -> None:
        pages = sorted(UI_ROOT.glob("*/index.html"))
        self.assertEqual(len(pages), 10)
        snapshot = _snapshot()

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for html in pages:
                with self.subTest(ui=html.parent.name):
                    page = browser.new_page()
                    page_errors: list[str] = []
                    page.on("pageerror", lambda error: page_errors.append(str(error)))
                    page.route(
                        "**/openapi.json",
                        lambda route: route.fulfill(
                            status=200,
                            content_type="application/json",
                            body=json.dumps({"paths": {}}),
                        ),
                    )
                    page.route(
                        "**/api/snapshot",
                        lambda route: route.fulfill(
                            status=200,
                            content_type="application/json",
                            body=json.dumps(snapshot),
                        ),
                    )
                    page.route("**/api/stream", lambda route: route.abort())

                    response = page.goto(
                        f"{self.base_url}/{html.parent.name}/index.html",
                        wait_until="domcontentloaded",
                    )
                    self.assertIsNotNone(response)
                    self.assertEqual(response.status, 200)
                    page.locator('[data-testid="pending-card"]').first.wait_for()

                    cards = page.locator('[data-testid="pending-card"]')
                    self.assertEqual(cards.count(), 3)
                    by_mode = {
                        mode: page.locator(f'[data-testid="pending-card"][data-anti-bias-mode="{mode}"]')
                        for mode in ("enabled", "disabled", "historical")
                    }
                    for mode, card in by_mode.items():
                        self.assertEqual(card.count(), 1, f"missing unique {mode} pending card")
                        self.assertIn(mode, card.text_content().lower())

                    disabled_text = by_mode["disabled"].text_content().lower()
                    historical_text = by_mode["historical"].text_content().lower()
                    self.assertIn("anti-bias disabled", disabled_text)
                    self.assertIn("historical", historical_text)
                    self.assertNotEqual(disabled_text, historical_text)

                    enabled_pairs = by_mode["enabled"].locator("[data-pairwise-status]")
                    self.assertEqual(enabled_pairs.count(), 3)
                    self.assertEqual(
                        enabled_pairs.evaluate_all("nodes => nodes.map(node => node.dataset.pairwiseStatus)"),
                        ["complete", "complete", "complete"],
                    )
                    pairwise_text = " ".join(enabled_pairs.all_text_contents()).lower()
                    for expected in ("0/0", "1/1", "3/3"):
                        self.assertIn(expected, pairwise_text)
                    self.assertEqual(by_mode["disabled"].locator("[data-pairwise-status]").count(), 0)
                    self.assertEqual(by_mode["historical"].locator("[data-pairwise-status]").count(), 0)
                    self.assertEqual(page_errors, [])
                    page.close()
            browser.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
