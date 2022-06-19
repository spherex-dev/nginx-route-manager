###############################################################################
# Copyright (C) 2022, created on June 19, 2022
# Written by Justin Ho
#
# This source code is proprietary and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

import unittest
from nginx_config import render_server, start_nginx, stop_nginx, reload_nginx

server = [
    ("listen", "80"),
    ("server_name", "_"),

]

routes = {
    "/r/server1": {
        "proxy_pass": "http://localhost:8000/"
    },
    "/r/server2": {
        "proxy_pass": "http://localhost:8001/"
    },
    "/r/server3": {
        "proxy_pass": "http://localhost:8003/",
        "ssl_certificate": "/etc/letsencrypt/live/www.test.com/fullchain.pem"

    }
}


nginx_expected = """server {
    listen 80;
    server_name _;

  location /r/server1 {
        proxy_pass http://localhost:8000/;
    }
  location /r/server2 {
        proxy_pass http://localhost:8001/;
    }
  location /r/server3 {
        proxy_pass http://localhost:8003/;
        ssl_certificate /etc/letsencrypt/live/www.test.com/fullchain.pem;
    }
}"""


class TestNginxConfig(unittest.TestCase):
    """Testing nginx config and process management"""

    def setUp(self) -> None:
        stop_nginx()

    def test_render_server(self):
        """Testing config rendering"""
        self.assertEqual(render_server(server, routes), nginx_expected)

    def test_control_nginx(self):
        """Testing config rendering"""

        self.assertFalse(reload_nginx())
        self.assertTrue(start_nginx())
        self.assertFalse(start_nginx())
        self.assertTrue(reload_nginx())
        self.assertTrue(stop_nginx())
        self.assertFalse(stop_nginx())


if __name__ == "__main__":
    unittest.main()
