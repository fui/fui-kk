mkdir -p ./data/V2016/tex
mkdir -p ./data/V2016/md
cd ./data/V2016/md
find . -iname "*.md" -type f -exec sh -c 'pandoc "${0}" -o "../tex/${0%.md}.tex"' {} \;
