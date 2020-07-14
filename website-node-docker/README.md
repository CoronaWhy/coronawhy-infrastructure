# Description

- `/public` is a simple code export from `webflow.com` for `coronawhy.org` website (July 13th, 2020)

- `Dockerfile` packages the website into very slim alpine based docker image, via node and [serve](https://www.npmjs.com/package/serve). 

- build container exposes 5000 port


## TODO

- repackage into webserver backend more suitable for production like `nginx` instead of `serve` (will need extra configuring on top of nginx image)


### Issues

The dynamic features of webflow platform don't work and need reimplementing

### Repository

https://github.com/CoronaWhy/website-node-docker
