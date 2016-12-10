mkdir -p ./data/$1/tex
mkdir -p ./data/$1/md
mkdir -p ./data/$1/report
cp ./resources/fui/fui-kompendium-blue.pdf ./data/$1/report/ifi-kompendium-forside-bm.pdf
cp ./resources/tex/ifikompendium/ifikompendium.tex ./data/$1/report
cp ./resources/tex/ifikompendium/ifikompendiumforside.sty ./data/$1/report

cd ./data/$1/md
find . -iname "*.md" -type f -exec sh -c 'pandoc "${0}" -o "../tex/${0%.md}.tex"' {} \;
