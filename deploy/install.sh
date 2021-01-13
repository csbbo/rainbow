#! /bin/bash

docker load -i rainbow.tar
docker-compose -p rainbow -f docker-compose.yml up -d