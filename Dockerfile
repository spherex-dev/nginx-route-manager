FROM python:3.10.5-alpine3.16
RUN apk update && apk add nginx build-base
RUN mkdir /nginx-router
COPY ./nginx_config.py /nginx-router
COPY ./route_manager.py /nginx-router
COPY ./requirements.txt /nginx-router
RUN pip3 install -r /nginx-router/requirements.txt
