**File:** README.md<br>
**Project:** FUI-KK<br>
**Date:** 2016-06-03<br>
**License:** MIT LICENSE

# FUI Course evaluation software
A collection of scripts and tools for gathering, processing and exporting
course evaluation survey results.

## Makefile
The makefile is meant as a simple tool to run all the scripts. Example:
```
make download
make json
make plots
make tex
make pdf
```

## Scripts
### download-reports.py
Downloads reports from nettskjema.uio.no, requires login.
```
python scripts/download-reports.py -f V2016 -u "username"
Password: *
```
### sort-downloads.py
Sorts downloaded files (tsv and html) into folder structure(data/).
```
python3 scripts/sort-downloads.py
```
### parse-tsv.py
Parses tsv files, "converting" them to json.
```
python3 scripts/parse-tsv.py -s all
```
### course-data.py
Updates the json files with useful statistics, by counting how many answered
each option, calculating averages, etc.
```
python3 scripts/course.py data/V2015
```

### semester.py
Not yet implemented.
### plot-courses.py
Not yet up to date.

## Mount DAV
https://www-dav.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui-kk/kursevaluering/

Finder -> Go -> Connect to Server

<!-- **List of stuff**<br>
0. [Title 0](./path0/)<br>
1. [Title 1](./path1/)<br> -->

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
