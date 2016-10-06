#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Divides course evaluation results among fui-members."""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__email__      = "olehelg@uio.no"
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
from collections import OrderedDict
import json

def course_divide(semester, num):
    p = "./data/"+semester+"/semester.json"
    semester = json.load(open(p), object_pairs_hook=OrderedDict)
    courses = []
    for name, data in semester.items():
        answers = data["respondents"]["answered"]
        courses.append((name, answers))
    courses = sorted(courses, reverse=True, key= lambda x: x[1])
    people = []
    for i in range(num):
        people.append( OrderedDict() )
        people[-1]["name"] = "Unknown"
        people[-1]["answers"] = 0
        people[-1]["courses"] = []
    for course in courses:
        victim = people[0]
        for person in people:
            if person["answers"] < victim["answers"]:
                victim = person
        victim["answers"] += course[1]
        victim["courses"].append(course[0])
    print(json.dumps(people, indent=1))

def main():
    if(len(sys.argv) < 2):
        print("Usage: ./course_divide.py num semester")
        exit()
    semester = sys.argv[2]
    num = int(sys.argv[1])
    course_divide(semester, num)

if __name__ == "__main__":
    main()
