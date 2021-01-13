#! /bin/bash

docker-compose -p rainbow -f docker-compose.yml down
docker image rm -f rb_nginx:latest
docker image rm -f rb_server:latest
