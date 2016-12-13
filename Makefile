default: help

install-mac: # mac only :)
	brew install python3
	brew install phantomjs
	brew install rename
	brew install pandoc
	pip3 install requests
	pip3 install selenium
	pip3 install beautifulsoup4

download:
	python3 scripts/download_reports.py
	python3 scripts/sort_downloads.py -i downloads -o data

sample_data:
	git submodule init
	git submodule update
	ln -s sample_data data

json:
	python3 scripts/parse_tsv.py -s all
	python3 scripts/course.py data
	python3 scripts/semester.py
	python3 scripts/courses.py

tex:
	rename -v -f -S inf INF ./data/*/md/*
	sed -i.bak 's/å/å/g' ./data/*/md/*.md
	find ./data -type f -name *.md.bak -delete
	./scripts/tex.sh V2016
	python3 scripts/participation_summary.py V2016
	python3 scripts/tex_combine.py -s V2016

pdf: tex
	./scripts/pdf.sh V2016

scales:
	python3 scripts/misc/scales.py

plots:
	python3 scripts/plot_courses.py

all: scales json plots tex pdf

open:
	open data/V2016/report/fui-kk_report*.pdf

help:
	@echo "Available targets:"
	@echo "download"
	@echo "sample_data"
	@echo "all"
	@echo "json"
	@echo "tex"
	@echo "pdf"

clean:
	@find ./data -type f -path "*/tex/*.tex" -delete
	@find ./data -type f -path "*/plots/*.pdf" -delete
	@find ./data -type f -path "*/plots/*.png" -delete
	@find ./data -type f -name "semester.json" -delete
	@find ./data -type f -name "courses.json" -delete
	@find ./data -type f -name "*.responses.json" -delete
	@find ./data -type f -name "*.stats.json" -delete
	@find ./data -type d -name "tex" -exec rm -rf {} +
	@find ./data -type d -name "plots" -exec rm -rf {} +
	@find ./data -type d -name "report" -exec rm -rf {} +


.PHONY: default install-mac download sample_data json tex pdf scales plots all help clean
