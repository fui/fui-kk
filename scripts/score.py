#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate the average score for a semester"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE.txt'

import os
import sys
import json
import argparse
from collections import OrderedDict
import numpy

def find_all(dictionary, search_key):
    hits = []
    for key,value in dictionary.items():
        if type(value) is dict:
            hits.extend(find_all(value, search_key))
        elif key == search_key:
            hits.append(dictionary[key])
    return hits

def calculate_average(semester):
    with open("./data/"+semester+"/outputs/courses.json", "r") as f:
        courses = json.load(f)
    averages = find_all(courses, "average")
    average = numpy.mean(averages)
    average = round(average, 2)
    return average

if __name__ == '__main__':
    a = calculate_average(sys.argv[1])
    print("Semester average for {} is {}( or {} in scale used by vurdering.js)".format(sys.argv[1], a, a+1))
