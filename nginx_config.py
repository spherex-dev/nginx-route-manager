###############################################################################
# Copyright (C) 2022, created on June 19, 2022
# Written by Justin Ho
#
# This source code is proprietary and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

from tempfile import NamedTemporaryFile
import subprocess
import psutil
import time

server = [
    ("listen", "80"),
    ("server_name", "_"),

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


def render_server(server_settings, routes):
    rendered_routes = "\n".join([render_route(route, config) for route, config in routes.items()])
    settings = "\n".join(["    " + f"{k} {_render_param(v)};" for k, v in server_settings])

    template = """server {
%s

%s
}"""
    return template % (settings, rendered_routes)


def _render_param(param):
    if isinstance(param, str):
        return param
    if isinstance(param, list):
        return " ".join(param)
    if isinstance(param, tuple):
        return " ".join(param)


def render_route(route: str, config: list):
    template = """  location %s {
%s
    }"""
    settings = "\n".join(["    " * 2 + f"{k} {_render_param(v)};" for k, v in config])
    return template % (route, settings)


def nginx_running():
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == "nginx":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def update_routes(server, routes):

    with NamedTemporaryFile('w') as f:
        f.write(render_server(server, routes))
        subprocess.run(["sudo", "cp", f.name, "/etc/nginx/sites-available/default"])
        subprocess.run(["sudo", "chown", "root:root", "/etc/nginx/sites-available/default"])
        return reload_nginx()


def start_nginx():
    if not nginx_running():
        subprocess.run(["sudo", "nginx"])
        return True
    return False


def stop_nginx():
    if nginx_running():
        subprocess.run(["sudo", "nginx", "-s", "stop"])
        while nginx_running():
            time.sleep(0.01)
        return True
    return False


def reload_nginx():
    if nginx_running():
        subprocess.run(["sudo", "nginx", "-s", "reload"])
        return True
    return False


if __name__ == "__main__":
    # print(render_server(server, routes))

    # start_nginx()
    # stop_nginx()
    print(nginx_running())
