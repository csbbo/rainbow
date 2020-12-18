#! /bin/bash

command -v docker > /dev/null && echo "docker found" || { echo "docker not found"; exit 1; }
command -v docker-compose > /dev/null && echo "docker-compose found" || { echo "docker-compose not found"; exit 1; }

echo "------------build the web------------"
docker run -it --rm -v `pwd`/web:/web node:15.4.0-stretch bash -c "cd /web && yarn install && yarn versions && yarn build || cat /root/.npm/_logs/*.log" || { echo "web build fail"; exit 1; }

echo "------------copy the dist to nginx------------"
cp -r ./web/dist ./nginx

echo "------------build nginx images------------"
docker build -t rb_nginx ./nginx

echo "------------build server images------------"
docker build -t rb_server ./server

echo "------------export images to deploy------------"
docker save -o ./rainbow.tar rb_nginx:latest rb_server:latest

echo "------------move to deploy------------"
mv ./rainbow.tar ./deploy

echo "------------clean up the packing env------------"
rm -rf ./nginx/dist
docker image rm -f rb_nginx:latest
docker image rm -f rb_server:latest
