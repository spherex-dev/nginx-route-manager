# Nginx Route Manager

## Overview

The nginx route manager provides a simple way to create dynamic routing using a docker container. A nginx server is managed by an exposed enpoint where http puts and gets are used to create new location blocks that are used to dynamically route to different locations. This is useful for services that are dyanically spun up.

This container image is available [here](https://hub.docker.com/r/spherexdev/nginx-route-manager).
Code to create this container is located on [github](https://github.com/spherex-dev/nginx-route-manager).

## How to run this container

This container can be started using the following command: 

```
docker run -p 8000:8000 -p 8080:80 spherexdev/nginx-route-manager:0.1 &
```

Port `8000` provides the following endpoints:

* [POST] /start_nginx
* [POST] /stop_nginx
* [POST] /update_routes
* [GET] /get_routes
* [GET] /nginx_running

## How this works

A nginx configuation file is dynamically generated and the nginx server is restarted to make the new change active. Currently, only a single server block is supported for simplicity and authentication had not been implemented yet (this maybe be done in the future, thus it is recommended that the handling endpoints are only exposed to trusted hosts only).

The following is a configuration that can be posted to the "/update_routes" endpoint:

```
config = {
    "server": [
        ["listen", "80"],
        ["server_name", "_"],
    ],
    "routes": {
        "/r/server1": [
            ["proxy_pass", "http://localhost:8000/"],
        ],
        "/r/server2": [
            ["proxy_pass", "http://localhost:8001/"],
        ],
        "/r/server3": [
            ["proxy_pass", "http://localhost:8003/"],
            ["rewrite", "^/.well-known/host-meta.json /public.php?service=host-meta-json last"]
        ]
}
```

The created nginx configuration would be the following:

```
server {
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
        rewrite ^/.well-known/host-meta.json /public.php?service=host-meta-json last;
    }
}