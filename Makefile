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
	python3 scripts/download-reports.py
	python3 scripts/sort-downloads.py --delete

sample_data:
	git submodule init
	git submodule update
	ln -s sample_data data

json:
	python3 scripts/parse-tsv.py -s all
	python3 scripts/course.py data
	python3 scripts/semester.py
	python3 scripts/courses.py

tex:
	rename -v -f -S inf INF ./data/*/md/*
	sed -i.bak 's/å/å/g' ./data/*/md/*.md
	./scripts/tex.sh V2016
	python3 scripts/tex-combine.py -s V2016

pdf: tex
	./scripts/pdf.sh V2016

scales:
	python3 scripts/misc/scales.py

plots:
	python3 scripts/plot-courses.py

all: scales json plots tex pdf

help:
	@echo "Available targets:"
	@echo "download"
	@echo "json"
	@echo "tex"
	@echo "pdf"

clean:
	@find ./data -type f -path "*/tex/*.tex" -delete
	@find ./data -type f -path "*/plots/*.pdf" -delete
	@find ./data -type f -path "*/plots/*.png" -delete
	@find ./data -type d -name "tex" -delete
	@find ./data -type d -name "plots" -delete
	@find ./data -type f -name "courses.json" -delete
	@find ./data -type f -name "semester.json" -delete
	@find ./data -type f -name "*.responses.json" -delete
	@find ./data -type f -name "*.stats.json" -delete
	@find ./data -type d -name "report" -delete


.PHONY: default install-mac download sample_data json tex pdf scales plots all help clean
