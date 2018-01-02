#!/usr/bin/env bash
mkdir -p ./data/$1/outputs/web/converted
mkdir -p ./data/$1/outputs/web/upload/$1/stats/

cp -r ./resources/web/copy/ ./data/$1/outputs/web/upload/$1/
cp -r ./resources/d3-charts/dist/ ./data/$1/outputs/web/upload/$1/
cp -r ./data/$1/outputs/stats/ ./data/$1/outputs/web/upload/$1/stats/

cd ./data/$1/inputs/md || exit 1
find . -iname "*.md" -type f -exec sh -c 'pandoc "${0}" -o "../../outputs/web/converted/${0%.md}.html"' {} \;
