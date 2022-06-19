FROM python:3.10.5-alpine3.16
RUN apk update && apk add --no-cache nginx build-base linux-headers sudo
RUN mkdir /nginx-route-manager
COPY ./nginx_config.py /nginx-route-manager
COPY ./route_manager.py /nginx-route-manager
COPY ./requirements.txt /nginx-route-manager
COPY ./entrypoint.sh /nginx-route-manager
RUN pip3 install -r /nginx-route-manager/requirements.txt
RUN apk del libgcc libstdc++ binutils libmagic file libgomp libatomic gmp isl22 mpfr4 mpc1 gcc musl-dev libc-dev g++ make fortify-headers patch build-base linux-headers
ENTRYPOINT /nginx-route-manager/entrypoint.sh