FROM nginx:1.19-alpine
ADD . /web/nginx

RUN apt-get update \
    && apt-get install -y python3-certbot-nginx vim \
    && ln -svf /web/nginx/nginx.conf /etc/nginx/nginx.conf # certbot detection

WORKDIR /web
CMD nginx -c /web/nginx/nginx.conf
