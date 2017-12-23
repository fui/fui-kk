#!/usr/bin/env/bash
mkdir -p ./data/$1/outputs/tex
mkdir -p ./data/$1/inputs/md
mkdir -p ./data/$1/outputs/report

if [ ! -d ./data/$1/resources ]; then
  cp -r ./resources ./data/$1/resources
fi

cp ./data/$1/resources/fui/fui-kompendium-blue.pdf ./data/$1/outputs/report/ifi-kompendium-forside-bm.pdf
cp ./data/$1/resources/ifikompendium/ifikompendium.tex ./data/$1/outputs/report
cp ./data/$1/resources/ifikompendium/ifikompendiumforside.sty ./data/$1/outputs/report

mkdir -p ./data/$1/inputs/tex
if [ ! -f ./data/$1/inputs/tex/header.tex ]; then
  cp ./templates/header.tex ./data/$1/inputs/tex/header.tex
fi

if [ ! -f ./data/$1/inputs/tex/tail.tex ]; then
  cp ./templates/tail.tex ./data/$1/inputs/tex/tail.tex
fi

cd ./data/$1/inputs/md || exit 1
find . -iname "*.md" -type f -exec sh -c 'pandoc "${0}" -o "../../outputs/tex/${0%.md}.tex"' {} \;
