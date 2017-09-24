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
from file_funcs import dump_json, load_json

def get_course_data(path):
    course = load_json(path)
    language = course["language"]

    if language == "NO":
        general_questions = ["Hva er ditt generelle intrykk av kurset?",
                             "Hva er ditt generelle inntrykk av kurset?"]
    elif language == "EN":
        general_questions = ["How do you rate the course in general?",
                             "What is your general impression of the course?"]
    else:
        print("Unknown language: " + str(language))
        print("Path:" + str(path))
        print("JSON:")
        print(json.dumps(course, indent=2))
        sys.exit(1)

    for general_question in general_questions:
        if general_question in course["questions"]:
            course[general_question] = course["questions"][general_question]
            break
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
    dump_json(semester_data, semester_dir+"/outputs/courses.json")

if __name__ == '__main__':
    semesters = []
    for root, subdirs, files in os.walk("./data"):
        semesters = filter(lambda x: ".git" not in x, subdirs)
        break
    for sem in semesters:
        main("./data/"+sem)
