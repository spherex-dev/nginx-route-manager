from nginx_config import start_nginx as start_nginx_
from nginx_config import stop_nginx as stop_nginx_
from nginx_config import update_routes as update_routes_
from nginx_config import nginx_running as nginx_running_
from sanic import Sanic
from sanic.response import text, json
from sanic.request import Request

app = Sanic("route_manager")
settings = {"server": [], "routes": {}}


@app.route('/')
@app.route('/<path:path>')
async def catch_all(request, path=''):
    print("the path was", path)
    return text('You want path: %s' % path)


@app.route("/start_nginx", methods=["POST"])
async def start_nginx(request: Request):
    return json({"ok": start_nginx_()})


@app.route("/stop_nginx", methods=["POST"])
async def stop_nginx(request: Request):
    return json({"ok": stop_nginx_()})


@app.route("/update_routes", methods=["POST"])
async def update_routes(request: Request):
    server = request.json["server"]
    routes = request.json["routes"]
    settings.update(request.json)
    return json({"ok": update_routes_(server, routes)})


@app.route("/get_routes")
async def get_routes(request: Request):
    return json(settings)


@app.route("/nginx_running")
async def nginx_running(request: Request):
    return json({"running": nginx_running_()})

if __name__ == '__main__':
    app.run()
