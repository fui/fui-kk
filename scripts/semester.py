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
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def get_course_data(path):
    course = json.load(open(path), object_pairs_hook=OrderedDict)
    course["general"] = course["questions"]["general"]
    del course["general"]["counts"]
    del course["general"]["most_common"]
    del course["questions"]
    return course

def main(semester_dir):
    files = []
    for f in os.listdir(semester_dir+"/json"):
        if f.endswith(".stats.json"):
            files.append(f)
    semester_data = OrderedDict()
    for f in files:
        course_name = f.replace(".stats.json", "")
        semester_data[course_name] = get_course_data(semester_dir+"/json/"+f)
    dump_to_file(semester_data, semester_dir+"/courses.json")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        semesters = []
        for root, subdirs, files in os.walk("./data"):
            semesters = subdirs
            break
        for sem in semesters:
            main("./data/"+sem)
    else:
        main(sys.argv[1])
