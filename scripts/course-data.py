#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create relevant statistics from individual responses"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = []
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

def dump_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def count_answers(course):
    stats = OrderedDict()
    responses = course["responses"]
    stats["respondents"] = len(responses["NR"])
    stats["invited"] = "Unknown"
    questions = OrderedDict()

    scales = json.load(open("data/response-scales.json"))
    for question in course["responses"]:
        if question in scales["questions"]:
            questions[question] = OrderedDict()
            responses = course["responses"][question]
            scale_key = scales["questions"][question]
            scale = scales["scales"][scale_key]

            counts = {}
            total = 0;
            ctr = 0;
            for response in responses:
                if response not in scales["invalid"]:
                    ctr += 1
                    total += scale[response]
                if response in counts:
                    counts[response] += 1
                else:
                    counts[response] = 1
            average = total/ctr
            delta = 1000
            average_text = ""
            for grade in scale:
                d = abs(average - scale[grade])
                if d < delta:
                    delta = d
                    average_text = grade
            questions[question]["counts"] = counts
            questions[question]["average"] = average
            questions[question]["average-text"] = average_text


    stats["questions"] = questions
    course["stats"] = stats

def main(path):
    course = json.load(open(path), object_pairs_hook=OrderedDict)

    count_answers(course)
    course.move_to_end("responses")
    dump_to_file(course, path)


if __name__ == '__main__':
    if(len(sys.argv) == 1):
        sys.exit("Must specify file path (overwrites file)")
    path = sys.argv[1]
    input_files = []
    if os.path.isfile(path):
        input_files.append(path)
    else:
        for (root, dirs, files) in os.walk(path):
            for file_x in files:
                if file_x.endswith(".json") and file_x.startswith("INF"):
                    input_files.append(os.path.join(root, file_x))
    for f in input_files:
        main(f)
