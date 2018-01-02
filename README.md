**File:** README.md<br>
**Project:** FUI-KK<br>
**License:** MIT LICENSE

# FUI Course evaluation software (fui-kk)
This piece of software was written by and for students in FUI - the student council at the department of informatics, University of Oslo. FUI evaluates all informatics courses every semester for the department. Students are invited to fill out surveys for their courses. The fui-kk software is used to gather, process and distribute data from these surveys. Summaries and statistics are posted online for other students. Lecturers gain access to all of the data for their course. The department gets a written pdf (LaTeX) report.

**PS:** Documentation includes some Norwegian translations for clarity.
 English readers can ignore these.

## User Documentation
Separate documentation for users of this software is avaliable:
* [Course Evaluation coordinator (Undervisningsansvarlig)](./guide/coordinator.md)
* [Report writers (KK-gruppa)](./guide/writers.md)

The rest of this README is more geared towards those who want to understand
or contribute to the code.

## Demonstration
A Work-In-Progress (WIP) demo can be found on github pages:
http://fui.github.io/fui-kk/

Please note that this is missing the default styling of UiO websites.

## Illustration (Norwegian)
<a href="https://github.com/fui/fui-kk/master/docs/graphics/fui-kk_visuals.pdf">
<img alt="docs/graphics/fui-kk_visuals.png" style="border-width:0" src="https://raw.githubusercontent.com/fui/fui-kk/master/docs/graphics/fui-kk_visuals.png" />
</a><br />.

## Hacking
If you want to test this software, or contribute to the project you can get started like this:
```
git clone git@github.com:fui/fui-kk.git
git submodule update --init --recursive
cd fui-kk
make sample_data
```
You will now have some test data to work with.

## KK Report (pdf)
The makefile is meant as a simple tool to run different parts of the software.

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
https://www-dav.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui/kursevaluering/

#### OSX:
Finder -> Go -> Connect to Server.

#### Windows:
##### WebDrive:
* Open WebDrive
* Click "New"
* Select "Secure WebDAV"
* Copy the above link into the url field
* Use appopriate credentials.
* Done

##### Windows Network drive:
* Open "This PC"
* Rightclick->"Add network location"
* "Choose custom network location"
* Copy the above link
* Use appropriate credentials
* Click next until done.

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

### ./fui_kk
Python package.
Uses underscore to follow python convention.
Also useful to have package name != project name (for searching).

### ./old

`fui_kk/old/` contain old scripts which are no longer in use.

### ./misc

`misc/` and `fui_kk/misc` contain files that can be ignored.

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
