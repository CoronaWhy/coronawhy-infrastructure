FROM node:current-alpine3.12 as base
MAINTAINER @antonpolishko
RUN apk --no-cache add git
RUN git clone https://github.com/CoronaWhy/website-node-docker /website-node-docker
WORKDIR /web
RUN ln -s /website-node-docker/public ./public
RUN npm i serve
EXPOSE 5000
