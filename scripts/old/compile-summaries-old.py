#!/snacks/bin/python3
# -*- coding: utf-8 -*-
"""Compiles tex files for the course evaluation report"""

__authors__    = ["Bendik Rønning Opstad"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__credits__    = ["Bendik Rønning Opstad", "josek"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import re
import sys
import pprint
import codecs
import string
import json

# Encoding of input files
ENCODING = "utf-8"

with open("../course-data.js") as f:
    scores = eval(f.read())

print(scores["INF2810"])

course_regex = '.*Kurs:\s?(.+)'
participants_regex = 'Antall besvarelser:(.+)'
files_and_scores = {}
course_regex = ".*=== (Kurs|Kurskode)\s?:\s*(?P<kode>.*)"
#kursregex = ".*=== (Kurs|Kurskode)\s?:\s*(?P<kode>[A-Za-z0-9\-]*)"
tmpl = None
tmpl_eng = None

with open('template.html') as tmpl_file:
    tmpl = string.Template(tmpl_file.read())

with open('template-eng.html') as tmpl_file:
    tmpl_eng = string.Template(tmpl_file.read())

if tmpl == None or tmpl_eng == None:
    print("template error")
    sys.exit(-1)


def extract_block(paragraph, fileContent):

    blocks = re.findall(r'=== ' + str(paragraph) + '\).*^=== ' + str(paragraph+1) + '\)', fileContent, flags=re.DOTALL|re.MULTILINE)

    if blocks == None or len(blocks[0]) < 2:
        return ""

    block = blocks[0]
    block = "<p>" + " ".join(re.sub('\n?===.*\n?', '', block).split("\n")) + "</p>"
    return block


def makeLatex(course_file, fileContent):
    """
    Creates the latex code for one course.
    """
    print("Parsing: " + str(course_file))

    data  = {"semester": "Høst 2015",
             "semester_eng": "Autumn 2015",
             "emneniva": "",
             "undervisning": "",
             "kommentar": "",
             "obligeksamen": ""}
    match = re.search(course_regex, fileContent)

    if match == None:
        raise ValueError("Could not find course name in file:" + course_file)

    groups = match.groups()
    data["course_name"] = match.group('kode')
    data["course_code"] = data["course_name"].split("- ")[0].strip()
    english = int(data["course_code"][-4]) >= 4

    match = re.search(participants_regex, fileContent)
    if match == None:
        raise ValueError("Particiapants not found")

    participants = match.group(1).strip()
    percent = getPercent(participants)
    percent = " (" + percent + "%" + ")"
    data["participants"] = participants + percent

    # Remove every line starting with "==="
    ###fileContent = re.sub("(\n)?===.*", '', fileContent)
    fileContent = re.sub("(\n)+", "\n", fileContent)

    # A line containing one or more hash characters is replaced with a newline (paragrach)
    fileContent = re.sub("\n#+\n", "</p><p>", fileContent)

    # Format *string* as emphesized
    #fileContent = re.sub("\*(.+?)\*", "\emph{\g<1>}", fileContent, flags=re.MULTILINE|re.DOTALL)
    fileContent = re.sub("\*\*(.+?)\*\*", "<strong>\g<1></strong>", fileContent)
    fileContent = re.sub("\*(.+?)\*", "<em>\g<1></em>", fileContent)

    #block  = re.findall(r'=== \d\)(.*)=== \d\)', fileContent, re.M)

    data['emneniva'] = extract_block(3, fileContent)
    data['undervisning'] = extract_block(4, fileContent)
    data['obligeksamen'] = extract_block(6, fileContent)
    #data['kommentar']
    kommentar = extract_block(7, fileContent)

    if len(kommentar) > 7:
        if english:
            data['kommentar'] = "<h2>Comment</h2>\n" + kommentar
        else:
            data['kommentar'] = "<h2>Kommentar</h2>\n" + kommentar

    # Handles score
    data["course_score"] = parse_score(files_and_scores, course_file, fileContent)
    #fileContent = re.sub("Generell vurdering: }(\s|\n)+", "Generell vurdering: }", fileContent)

    if data["course_code"] in scores:
        a = scores[data["course_code"]]
        b = [[k, a[k]] for k in a.keys()]
        c = sorted(b, key=lambda s: s[0][1:] + ('1' if s[0][0] == "V" else '2'))
        data["course_scores"] = c
    else:
        data["course_scores"] = {}

    data["course_scores"] = json.dumps(data["course_scores"])

    # Replace "" with «».
    fileContent, data["sitat"] = fix_quotes(fileContent)

#    print(data)

    if english:
        tmpl_html = tmpl_eng.substitute(data)
    else:
        tmpl_html = tmpl.substitute(data)

    return tmpl_html


def parse_score(files_and_scores, course_file, fileContent):
    """
    Handles the score rating
    """
    score_test = True

    ################
    # Remove the empty scores (not selected)
    #################
    while score_test:
        match = re.search('(\(\s+?\)\s.+)', fileContent)
        if match == None:
            break
        groups = match.groups()
        if groups == None:
            break
        if len(groups) == 0:
            score_test = False
        for m in groups:
            fileContent2 = fileContent.replace(m, '')
            fileContent = fileContent2

    # Fixes the score
    course_score = ""
    evalCount = 0

    # Notat lagt inn av josek, 20. mars 2011, redigert 25. apr 2011:
    # Rekkefølgen av valgene for generell karakter for kursene i mal.txt
    # bør snus om slik at det stemmer med rekkefølgen på skjemaene,
    # Det venter vi med til neste semester (høst 2011) bl.a. fordi flere
    # i kk-gruppen ikke bruker nyeste mal.  Jeg byttet tilbake til
    # gammel rekkefølge på alle kursrapportene ("Svært bra" nederst) slik
    # at alt skal komme ut riktig.  Neste gang bør vi sende selve filen
    # mal.txt på mail til alle som skal skrive kursevalueringer og si fra
    # at de skal bruke den nye; og endre dette skriptet slik at det bytter
    # om rekkefølgen under behandling (slik at det blir "Bra til meget bra"
    # og ikke "Meget bra til bra").

    fileContent = re.sub("===[^\n]+", '', fileContent)

    while score_test:
        match = re.search('(\([X|x]\)(\s.+))', fileContent)
        if match == None:
            break
        groups = match.groups()
        if groups == None or len(groups) == 0:
            break
        # Safety
        if evalCount == 10:
            print("Evalcount == 10")
            break
        replace = ""

        if evalCount > 0:
            course_score = "<em>" + groups[1].strip() + "</em>" + " til " + course_score
        else:
            course_score += "<em>" + groups[1].strip() + "</em>"

        evalCount =+ 1

        fileContent2 = fileContent.replace(groups[0], replace)
        fileContent = fileContent2

    files_and_scores[course_file] = course_score

    return course_score

def fix_quotes(content):
    """Fixing quotes in the string 'content'"""

    quotes = ""

    while True:
        match = re.search('^"([^"]+)"', content, re.MULTILINE | re.DOTALL)

        if match == None:
            return (content, quotes)

        groups = match.groups()
        for mat in groups:
            mat_orig = mat
            mat2 = "<blockquote>" + mat + "</blockquote>"

            quotes += mat2 + '\n'
            content = content.replace('\"'+mat_orig+'\"', "")

    return (content, quotes)

def unit_test():

    print("Running unit test")

    course_list = courses.splitlines()

    for i in range(len(course_list)):
        course_list[i] = course_list[i].strip()

    #print "Course list:\n", course_list

    # uses own defined sort function
    course_list.sort(kursevalueringssortering)

    #print "Course list soirted:\n", course_list

    for course in course_list:
        print(course)

# Sorting the files alphabetically .
# INFPS, INF-MAT, INF-GEO, HUMIT og TOOL is placed at the end.

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function
    cmp was removed from Python 3 and replaced by key which
    is crippled in comparison. Hence this class.
    """
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def cmp(x, y):
    if x == y:
        return 0
    elif x < y:
        return -1
    else:
        return 1

def kurs_cmp(x, y):
    regex = "(humit|inf-mat|inf-geo|infps|tool)"
    y_matched = re.search(regex, y.lower()) != None
    x_matched = re.search(regex, x.lower()) != None
    if y_matched == x_matched:
        return cmp(x, y)
    if x_matched:
        return 1
    else:
        return -1

def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return [adict[key] for key in keys]


def sortedDictValues3(adict):
    adict.sort(sortfuncdict)

def sortfuncdict(x,y):
    return cmp(x[1],y[1])


def printStuff():

    #print "\n\n\nUnsorted:\n"

    keys = files_and_scores.items()

    #for key in keys:
    #    print key

    #print "\n\nSORTED:\n"
    #tuples.sort(lambda (k1,v1),(k2,v2):cmp(v1,v2))

    vk=[(v,k) for v, k in  files_and_scores.items()]
    #vk.sort(lambda (k1,v1),(k2,v2):cmp(v1,v2))
    vk.sort(lambda arg : cmp(arg[0][1], arg[1][1]))

    #pprint.pprint(vk)

    #for value, key in vk:

    sortedDict = sortedDictValues(files_and_scores)

    #print "\n\n\nSorted:\n"
    #pprint.pprint(vk)

    #for elem in sortedDict:
     #   print elem

def getPercent(participants):
    match = re.search("(\d+).+?(\d+)", participants)
    if match == None:
        raise ValueError("Participants not on correct format: %s" % participants)
    groups = match.groups()
    if len(groups) != 2:
        return ""
    percent = int( float(groups[0]) / float(groups[1]) * 100)
    return str(percent)

import sys

def write_score_overview():
    score_overview = codecs.open('score_overview.txt', 'w', encoding=ENCODING)
    score_values = files_and_scores.values()
    score_sum = {}
    for key in score_values:
        if not key in score_sum:
            score_sum[key] = 1
        else:
            score_sum[key] += 1
    for key in score_sum.keys():
        #value = key + ":" + unicode(score_sum[key])
        value = key + ":" + str(score_sum[key])
        score_overview.write(value + "\n")
        print(value)

    score_overview.write("Alle kurs:\n")
    for key in files_and_scores.keys():
        score_overview.write(str(key) + ":" + files_and_scores[key] + "\n")
    score_overview.close()

if __name__ == '__main__':

    stuffPrint = False;

    if len(sys.argv) > 1:
        option = sys.argv[1]

        # Runs unit test
        if option == "unit":
            unit_test()
            print("Unit test done")
            sys.exit(0)
        elif option == "print":
            stuffPrint = True

    startDir = "../"

    directories = [startDir]
    fileDic = {}

    while len(directories)>0:
        directory = directories.pop()
        for fname in os.listdir(directory):
            fullpath = os.path.join(directory, fname)
            if os.path.isfile(fullpath):
                if re.search(".+\d{4}.*?\.txt$", fname) != None:
                    #if fileDic.has_key(fname.lower()):
                    if fname.lower() in fileDic:
                        print("Two files with the same name exists. No good!!")
                        sys.exit(1)
                    fileDic[fname.lower()] = fullpath
            elif os.path.isdir(fullpath):
                directories.append(fullpath)

    fileList = list(fileDic.keys())
    print("fileList type:", type(fileList))

    print("Course file read.")

    # uses own defined sort function
    #print("kursevalueringssortering:", kursevalueringssortering)
    fileList.sort(key=cmp_to_key(kurs_cmp))

    for fname in fileList:
        emnekode = fname.split('.')[0].upper()
        os.system("mkdir -p kurs/" + emnekode)
        reportFile = codecs.open("kurs/" + emnekode + "/index.html", 'wb', encoding=ENCODING)
        f = codecs.open(fileDic[fname], encoding=ENCODING)
        fileContent = None

        try:
            fileContent = f.read()
        except UnicodeDecodeError:
            print("ERROR reading non-UTF-8 encoded file:")
            print("fileDic[fname]:", fileDic[fname])
            print("fname:", fname)
            sys.exit(1)

        f.close()

        if fileContent == None:
            print("fileContent:" + fileContent.encode(ENCODING))
            sys.exit(0)

        try:
            latexstr = makeLatex(fname, fileContent)
        except(ValueError, e):
            print("ERROR: %s: %s" % (fname, e), file=sys.stderr)
            sys.exit(1)

        if latexstr != None:
            reportFile.write(latexstr)

        reportFile.close()

    if stuffPrint == True:
        printStuff()

    write_score_overview()

    sys.exit(0)
