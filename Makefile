default: help

SEMESTER = V2016

install-mac: # mac only :)
	brew install python3
	brew install phantomjs
	brew install rename
	brew install pandoc
	pip3 install requests
	pip3 install selenium
	pip3 install beautifulsoup4

download:
	# python3 scripts/download_reports.py
	python3 scripts/download_reports.py -u fui -f "testskjema"
	python3 scripts/sort_downloads.py -i downloads -o data -e "(INF9)|(testskjema)|(\*\*\*)"

sample_data:
	git submodule init
	git submodule update
	cp -r sample_data data

responses:
	python3 scripts/responses.py -s all

scales:
	python3 scripts/scales.py all

json:
	python3 scripts/course.py data
	python3 scripts/semester.py
	python3 scripts/courses.py

tex:
	rename -v -f -S inf INF ./data/*/inputs/md/*
	sed -i.bak 's/å/å/g' ./data/*/inputs/md/*.md
	find ./data -type f -name *.md.bak -delete
	./scripts/tex.sh $(SEMESTER)
	python3 scripts/participation_summary.py $(SEMESTER)
	python3 scripts/tex_combine.py -s $(SEMESTER)

pdf: tex
	./scripts/pdf.sh $(SEMESTER)

plots:
	python3 scripts/plot_courses.py $(SEMESTER)

all: responses scales json plots tex pdf web

open:
	open data/$(SEMESTER)/outputs/report/fui-kk_report*.pdf

web:
	./scripts/web.sh $(SEMESTER)
	python3 ./scripts/web_reports.py data/$(SEMESTER)

web-preview: web
	@echo "---------------------------------------------"
	@echo " WARNING: Do NOT commit changes to ./docs if"
	@echo " you are working with real data!"
	@echo "---------------------------------------------"
	rm -rf ./docs
	mkdir ./docs
	cp -r ./data/$(SEMESTER)/outputs/web/upload/$(SEMESTER)/* ./docs
	python3 ./scripts/adapt_preview_html.py

score:
	python3 ./scripts/score.py $(SEMESTER)

help:
	@echo "Available targets:"
	@echo "install-mac"
	@echo "download"
	@echo "sample_data"
	@echo "all"
	@echo "scales"
	@echo "json"
	@echo "plots"
	@echo "tex"
	@echo "pdf"
	@echo "web"
	@echo "web-preview"

clean:
	@find ./data -type d -name "outputs" -exec rm -rf {} +

.PHONY: default install-mac download sample_data json tex pdf scales plots all help clean web
