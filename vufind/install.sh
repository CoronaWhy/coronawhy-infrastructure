#!/bin/bash

version=6.1.2
mkdir webapp
wget https://github.com/vufind-org/vufind/releases/download/v$version/vufind-$version.tar.gz -O webapp/vufind.tar.gz
cd webapp
gzip -cd vufind.tar.gz|tar xf -
mv vufind-$version vufind
