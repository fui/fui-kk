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
	python3 src/download_reports.py -u fui
	python3 src/sort_downloads.py --delete -i downloads -o data -e "(INF9)|(testskjema)|(\*\*\*)"
	@echo "Warning: Please delete the downloads folder once per semester"
	@echo "         after closing the forms, to ensure that up to date"
	@echo "         reports are downloaded. (The download script will not"
	@echo "         redownload forms with ID in downloaded.txt)"

sample_data:
	git submodule init
	git submodule update
	cp -r sample_data data

responses:
	python3 src/responses.py -s all

scales:
	python3 src/scales.py all

json:
	python3 src/course.py data
	python3 src/semester.py
	python3 src/courses.py

tex:
	rename -v -f -S inf INF ./data/*/inputs/md/*
	sed -i.bak 's/å/å/g' ./data/*/inputs/md/*.md
	find ./data -type f -name *.md.bak -delete
	./src/tex.sh $(SEMESTER)
	python3 src/participation_summary.py $(SEMESTER)
	python3 src/tex_combine.py -s $(SEMESTER)

pdf: tex
	./src/pdf.sh $(SEMESTER)

plots:
	python3 src/plot_courses.py $(SEMESTER)

all: responses scales json plots tex pdf web

open:
	open data/$(SEMESTER)/outputs/report/fui-kk_report*.pdf

web:
	./src/web.sh $(SEMESTER)
	python3 ./src/web_reports.py data/$(SEMESTER)

web-preview: web
	@echo "---------------------------------------------"
	@echo " WARNING: Do NOT commit changes to ./docs if"
	@echo " you are working with real data!"
	@echo "---------------------------------------------"
	rm -rf ./docs
	mkdir ./docs
	cp -r ./data/$(SEMESTER)/outputs/web/upload/$(SEMESTER)/* ./docs
	python3 ./src/adapt_preview_html.py

upload_raw:
	@echo "Mount KURS folder to /Volumes/KURS (mac) or similar before running:"
	python3 src/upload_reports.py --input ./data --output /Volumes/KURS/ --semester $(SEMESTER)

score:
	python3 ./src/score.py $(SEMESTER)

clean:
	find ./data -type d -name "outputs" -exec rm -rf {} +
	find ./data -type d -name "downloads" -exec rm -rf {} +
	rm -rf ./downloads

venv:
	python3 -m venv venv
	# Activate virtual environment by running venv/bin/activate in your shell

pip-install:
	pip install -r requirements.txt

pip3-install:
	pip3 install -r requirements.txt

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

.PHONY: default install-mac download sample_data responses scales json tex pdf plots all open web upload_raw score clean help venv pip-install pip3-install
