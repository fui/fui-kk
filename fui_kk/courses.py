#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from file_funcs import dump_json, load_json

def get_semester_order(start_year, stop_year):
    start_year = int(start_year)
    stop_year = int(stop_year)
    s_order = []
    for i in range(start_year,stop_year):
        s_order.append("V"+str(i))
        s_order.append("H"+str(i))
    return s_order

def get_semesters(path):
    semester_order = get_semester_order(2000,2030)
    semesters = []
    for root, subdirs, files in os.walk(path):
        semesters = list(filter(lambda x: x != ".git", subdirs))
        break

    indices = [semester_order.index(x) for x in semesters]
    semesters = [x for (y,x) in sorted(zip(indices,semesters))]
    return semesters

if __name__ == '__main__':
    semesters = get_semesters("./data")
    courses = OrderedDict()
    for s in semesters:
        p = "./data/"+s+"/outputs/courses.json"
        semester = load_json(p)
        for course in semester:
            if course not in courses:
                courses[course] = OrderedDict()
            courses[course][s] = semester[course]
    dump_json(courses, "./data/courses.json")
