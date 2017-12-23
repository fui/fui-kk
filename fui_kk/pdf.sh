#!/usr/bin/env bash
function triplelatex {
    filename=$(basename "$1")
    filename="${filename%.*}"
    mkdir -p ./.latex
    if [ -d "./.latex/_minted-"$filename ]; then
       mv "./.latex/_minted-"$filename ./
    fi
    pdflatex -shell-escape -output-directory "./.latex" "${1/.pdf/.tex}"
    pdflatex -shell-escape -output-directory "./.latex" "${1/.pdf/.tex}"
    pdflatex -shell-escape -output-directory "./.latex" "${1/.pdf/.tex}"
    mv ./.latex/*.pdf ./
    if [ -d "_minted-"$filename ]; then
        mv "_minted-"$filename ./.latex
    fi
}

mkdir -p ./data/$1/outputs/report
cd ./data/$1/outputs/report || exit 1
triplelatex fui-kk_report_$1.tex
