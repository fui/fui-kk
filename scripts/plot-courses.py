#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is a module that is used for generating plots that show how a
course has evolved."""

__authors__    = ["Lars Tveito"]
__copyright__  = "Lars Tveito"
__credits__    = ["Lars Tveito"]
__license__    = "MIT"

# The MIT License (MIT)

# Copyright (c) 2013 Lars Tveito

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

from functools import partial

def plot_course(course_name, courses, output):
    course = courses[course_name]
    scale = ['Lite bra', 'Mindre bra', 'Greit',
             'Bra', 'Meget bra', u'Særdeles bra']

    # A function that returns turns v12 -> 12, h12 -> 12.5 ...
    semester_value = lambda x: float(x[1:]) + (0.5 if x[0] == 'h' else 0)
    # We sort the courses in chronological order.
    semester_codes = sorted(course.keys(), key=semester_value)

    scores = [course[semester] for semester in semester_codes]

    # Enable horizontal grid lines.
    axis = plt.gca()
    axis.yaxis.grid(True)

    plt.title('Generell vurdering fra %s' % semester_str(semester_codes[0]))
    # A numeric representation of semesters
    semesters = range(len(semester_codes))

    plt.plot(semesters, scores, marker='o', markersize=5)

    # Some space between between axis lines and points.
    plt.xlim(-0.2, len(semesters) - 0.8)

    # Semester codes along the x-axis.
    plt.xticks(semesters, semester_codes)
    # Rating descriptions along the y-axis
    plt.ylim(0.5, 6.5)
    plt.yticks(range(1, len(scale) + 1), scale)

    # Figure for inf1010 --> INF1010.pdf
    if first_match(COURSE_CODE_REGEX, course_name):
        course_name = course_name.upper()
    plt.savefig(os.path.join(output, course_name) + '.pdf', format='pdf')
    plt.savefig(os.path.join(output, course_name) + '.png', format='png')
    plt.cla()


if __name__ == "__main__":
    main()
