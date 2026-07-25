from __future__ import annotations

import unittest
from dataclasses import replace

from fastapi import FastAPI

from server import config, main


class InterfaceBindingTest(unittest.TestCase):
    def test_each_missing_if_i5_member_unpublishes_all_six_routes(self):
        for field in (
            "control_center_host_id",
            "control_center_auth_contract_id",
            "control_center_route_owner_id",
        ):
            with self.subTest(field=field):
                cfg = replace(config.Config(), **{field: None})
                app = FastAPI()
                state = main.bind_control_center_routes(
                    app, cfg, lambda: object()
                )
                self.assertEqual(state["interface_state"], "unavailable")
                self.assertEqual(state["published_routes"], [])
                paths = {
                    route.path
                    for route in app.routes
                    if route.path.startswith("/v1/control-center")
                }
                self.assertEqual(paths, set())

    def test_complete_binding_publishes_exactly_six_routes(self):
        app = FastAPI()
        state = main.bind_control_center_routes(
            app, config.Config(), lambda: object()
        )
        self.assertEqual(state["interface_state"], "available")
        paths = {
            path
            for path in app.openapi()["paths"]
            if path.startswith("/v1/control-center")
        }
        self.assertEqual(len(paths), 6)


if __name__ == "__main__":
    unittest.main()
