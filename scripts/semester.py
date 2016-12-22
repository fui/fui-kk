#!/usr/bin/env python3
"""Combines all data for the semester into a shared json"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

def dump_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def get_course_data(path):
    course = json.load(open(path), object_pairs_hook=OrderedDict)
    language = course["language"]

    if language == "NO":
        general_question = "Hva er ditt generelle intrykk av kurset?"
    elif language == "EN":
        general_question = "How do you rate the course in general?"
    else:
        print("Unknown language: "+language)
        sys.exit(1)

    course[general_question] = course["questions"][general_question]
    del course["questions"]
    return course

def main(semester_dir):
    files = []
    for f in os.listdir(semester_dir+"/outputs/stats"):
        if f.endswith(".json"):
            files.append(f)
    semester_data = OrderedDict()
    for f in files:
        course_name = f.replace(".json", "")
        semester_data[course_name] = get_course_data(semester_dir+"/outputs/stats/"+f)
    dump_to_file(semester_data, semester_dir+"/outputs/courses.json")

if __name__ == '__main__':
    semesters = []
    for root, subdirs, files in os.walk("./data"):
        semesters = filter(lambda x: ".git" not in x, subdirs)
        break
    for sem in semesters:
        main("./data/"+sem)
