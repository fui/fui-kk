#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Combines all data for the semester into a shared json"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = []
__version__    = "0.1"
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

def main(dir):
    pass

if __name__ == '__main__':
    semesters = []
    for root, subdirs, files in os.walk("./data"):
        semesters = subdirs
        break

    courses = {}
    for s in semesters:
        p = "./data/"+s+"/semester-data.json"
        semester = json.load(open(p), object_pairs_hook=OrderedDict)
        for course in semester:
            if course not in courses:
                courses[course] = {}
            courses[course][s] = semester[course]
    dump_to_file(courses, "./data/courses.json")
