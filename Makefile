default: help

install:
	brew install python
	brew install python3
	brew install phantomjs
	pip install requests
	pip install selenium
	pip3 install bs4

download:
	python scripts/download-reports.py -f "(testskjema)"
	python3 scripts/sort-downloads.py

json:
	python3 scripts/parse-tsv.py -s all
	python3 scripts/course-data.py data
	python3 scripts/semester-data.py

tex:
	@echo "Not yet implemented!"

pdf:
	@echo "Not yet implemented!"

scales:
	python3 scripts/misc/response-scales.py

help:
	@echo "Available targets:"
	@echo "download"
	@echo "json"
	@echo "tex"
	@echo "pdf"

.PHONY: download json tex pdf help install scales
