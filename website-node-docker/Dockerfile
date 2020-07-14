FROM node:current-alpine3.12 as base
MAINTAINER @antonpolishko
RUN apk --no-cache add git
RUN git clone https://github.com/CoronaWhy/website-node-docker
WORKDIR /website-node-docker
COPY public /web/public
WORKDIR /web
RUN npm i serve
EXPOSE 5000

#CMD ["node_modules/serve/bin/serve.js", "./public"]
