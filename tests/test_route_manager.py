###############################################################################
# Copyright (C) 2022, created on June 19, 2022
# Written by Justin Ho
#
# This source code is proprietary and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

import unittest
from route_manager import app
from nginx_config import stop_nginx

server = [
    ["listen", "80"],
    ["server_name", "_"],

]

routes = {
    "/r/server1": [
        ("proxy_pass", "http://localhost:8000/"),
    ],
    "/r/server2": [
        ("proxy_pass", "http://localhost:8001/"),
    ],
    "/r/server3": [
        ("proxy_pass", "http://localhost:8003/"),
        ("rewrite", "^/.well-known/host-meta.json /public.php?service=host-meta-json last")
    ]
}


server_kwargs = {"motd": False}


class TestRouteManager(unittest.TestCase):

    def setUp(self) -> None:
        stop_nginx()

    def test_routes(self):
        _, response = app.test_client.post("/start_nginx", server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])
        _, response = app.test_client.post(
            "/update_routes", json={"server": server, "routes": routes}, server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])
        _, response = app.test_client.get("/get_routes", server_kwargs=server_kwargs)
        self.assertEqual(response.json, {"server": server, "routes": routes})
        _, response = app.test_client.post("/stop_nginx", server_kwargs=server_kwargs)
        self.assertTrue(response.json["ok"])


if __name__ == "__main__":
    unittest.main()
