default: help

install-mac: # mac only :)
	brew install python
	brew install python3
	brew install phantomjs
	brew install rename
	pip install requests
	pip install selenium
	pip3 install requests
	pip3 install selenium
	pip3 install bs4
	brew install pandoc

download:
	python scripts/download-reports.py
	python3 scripts/sort-downloads.py --delete

sample_data:
	tar -xzf "sample_data.tgz"
	rename -s sample_data data sample_data

json:
	python3 scripts/parse-tsv.py -s all
	python3 scripts/course.py data
	python3 scripts/semester.py
	python3 scripts/courses.py

tex:
	./scripts/tex.sh

rename:
	rename -v -f -s inf INF ./data/*

pdf:
	@echo "Not yet implemented!"

scales:
	python3 scripts/misc/scales.py

plots:
	python3 scripts/plot-courses.py

all: scales json plots

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

.PHONY: download json tex pdf help install scales all plots sample_data clean rename
