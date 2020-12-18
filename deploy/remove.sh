#! /bin/bash

docker-compose down
docker image rm -f rb_nginx:latest
docker image rm -f rb_server:latest
