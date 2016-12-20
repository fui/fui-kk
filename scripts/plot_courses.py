#!/usr/bin/env python3
"""This is a module that is used for generating plots that show how a
course has evolved."""

__authors__    = ["Ole Herman Schumacher Elgesem", "Lars Tveito"]
__copyright__  = "Lars Tveito"
__credits__    = ["Lars Tveito"]
__license__    = "MIT"

# The MIT License (MIT)

# Copyright (c) 2016 Lars Tveito

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import multiprocessing, pipes, os, re
import matplotlib.pyplot as plt
import json
import sys
from collections import OrderedDict

from functools import partial

def plot_course(course_name, courses, output, scales, semester):
    course = courses[course_name]

    if(course[semester]["language"] == "NO"):
        scale = scales["kvalitet"]
    else:
        scale = scales["quality"]

    scale_val = []
    scale_text = []
    for (key,val) in scale.items():
        if not val in scale_val:
            scale_val.append(val)
            scale_text.append(key)

    scale = [y for (x,y) in sorted(zip(scale_val, scale_text))]

    semester_codes = list(course.keys())
    if semester in semester_codes:
        semester_codes = semester_codes[0:semester_codes.index(semester)+1]
    else:
        print("Warning: the course {} doesn't have data for {}".format(course_name, semester))
    semesters = list(course.items())

    scores = [course[semester]["general"]["average"] for semester in semester_codes]

    fig = plt.figure(figsize=(10, 5), edgecolor='k')
    plt.title('Generell vurdering fra ' + semester_codes[0])

    semester_nums = range(len(semester_codes))
    plt.plot(semester_nums, scores, marker='o', markersize=5)

    # Some space between between axis lines and points.
    plt.xlim(-0.2, len(semester_nums) - 0.8)

    # Semester codes along the x-axis.
    plt.xticks(semester_nums, semester_codes)

    # Rating descriptions along the y-axis
    plt.ylim(0.5, 6.5)
    plt.yticks(range(1, len(scale) + 1), scale)

    axis = plt.gca()
    axis.yaxis.grid(True)
    plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

    plt.savefig(output+course_name+'.pdf', format='pdf')
    plt.savefig(output+course_name+'.png', format='png')
    plt.close('all')

def generate_plots(courses, scales, semester_name):
    semester = json.load(open("./data/"+semester_name+"/outputs/courses.json"), object_pairs_hook=OrderedDict)
    courses_to_plot = list(semester.keys())
    outdir = "".join(["./data/", semester_name, "/outputs/plots/"])
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for c in courses_to_plot:
        plot_course(c, courses, outdir, scales, semester_name)

def plot_courses(semester):
    semester = sys.argv[1]
    courses = json.load(open("./data/courses.json"), object_pairs_hook=OrderedDict)
    scales = json.load(open("./data/scales.json"), object_pairs_hook=OrderedDict)
    scales = scales["scales"]
    generate_plots(courses, scales, semester)

if __name__ == "__main__":
    plot_courses(sys.argv[1])
