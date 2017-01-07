**File:** README.md<br>
**Project:** FUI-KK<br>
**Date:** 2016-12-26<br>
**License:** MIT LICENSE

# FUI Course evaluation software
A collection of scripts and tools for gathering, processing and exporting
course evaluation survey results.

## Hacking
If you want to test this software, or contribute to the project you can get started like this:
```
git clone git@github.com:fui/fui-kk.git
cd fui-kk
make sample_data
```
You will now have some test data to work with.

## KK Report (pdf)
The makefile is meant as a simple tool to run all the scripts.

If you need to download reports from nettskjema:
```
make download
```
(Not needed if you're using sample_data)

Generate statistics and plots:
```
make json
make plots
```

Insert markdown files into `./data/<semester>/md`.
Then convert them to latex and put everything together using:
```
make tex
make pdf
```

## Web reports
```
make json
make web
```

## Publish raw data:

### Mount DAV
https://www-dav.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui-kk/kursevaluering/

Finder -> Go -> Connect to Server.

Use script `upload-reports.py` to move html reports to the mounted folder structure.

## Folder structure

### ./data

Reports and survey answers are downloaded to `download/` and sorted into `data/`.
This folder contains *everything*, html reports, json statistics, plots etc. for all semesters.
Note that `downloads` and `data` folders are in `.gitignore` so git doesn't track changes.
This means you can work on the real data in the same project folder as you do development,
you will *not* push confidential content to github.

This is a mirror of the data folder used by FUI, without file contents:

https://github.com/fui/fui-kk-data-structure

### ./scripts
Python and bash scripts. See Makefile for example usage.

### ./old

`scripts/old/` contain old scripts which are no longer in use.

### ./misc

`misc/` and `scripts/misc` contain files that can be ignored.

## Contributors
Thank you to everyone who has been involved with this project over the years, including:
 * [Lars Tveito](https://github.com/larstvei)
 * [Kenneth Klette Jonassen](https://github.com/knneth)
 * [Bendik Rønning Opstad](https://github.com/bendikro)
 * [Helga Nyrud](https://github.com/helgany)
 * [Ole Herman Schumacher Elgesem](https://github.com/olehermanse)
 * [Erik Vesteraas](https://github.com/evestera)

## MIT License

Copyright (c) 2016 Fagutvalget ved Institutt for Informatikk - IFI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
<br>
