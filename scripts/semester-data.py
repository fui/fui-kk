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

def get_course_data(path):
    course = json.load(open(path))
    print(course)

def main(semester_dir):
    files = []
    for f in os.listdir(semester_dir+"/json"):
        if f.endswith(".stats.json"):
            files.append(f)
    semester_data = OrderedDict()
    for f in files:
        semester_data[course_name] = get_course_data(f)


if __name__ == '__main__':
    main(sys.argv[1])
