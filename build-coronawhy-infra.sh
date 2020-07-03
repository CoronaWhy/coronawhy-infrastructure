#!/bin/bash

echo "Download CoronaWhy jupyter notebooks..."
mkdir ./data/repo
cd ./data/repo
git clone https://github.com/CoronaWhy/SpanishFlu
git clone https://github.com/CoronaWhy/bel4corona
git clone https://github.com/CoronaWhy/task-ts
git clone https://github.com/CoronaWhy/task-ties
git clone https://github.com/CoronaWhy/task-risk
git clone https://github.com/CoronaWhy/task-geo
git clone https://github.com/CoronaWhy/dataverse-integrations
git clone https://github.com/CoronaWhy/ai-annotations

