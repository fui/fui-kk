#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This is a module that is used for generating plots that show's how a
course has evolved."""

__authors__    = ["Lars Tveito"]
__copyright__  = "Lars Tveito"
__credits__    = ["Lars Tveito"]
__version__    = "1.0"
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

class TwoWayDict(dict):
    """A dictionary where all keys are accosiated with their values and
    viceversa. Can be used for converting between two units."""
    def __init__(self, arg):
        super(TwoWayDict, self).__init__(arg)
        for key, value in arg.items():
            self.__setitem__(key, value)
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)
    def __len__(self):
        return dict.__len__(self) / 2

# A two way dictionary where a descriptive word is associated with a score,
# and a score is associated with a descriptive word.
SCORE_RANKINGS = TwoWayDict({'Lite' : 1, 'Mindre' : 2, 'Greit' : 3,
                               'Bra' : 4, 'Meget' : 5, 'Særdeles' : 6})

# Regexes to identify scores, semester codes and course codes.
SCORE_REGEX = r'Meget|Lite|Greit|Særdeles|Mindre|Bra'
COURSE_CODE_REGEX = r'[\w-]+\d{4}'
SEMESTER_CODE_REGEX = r'[hv]\d{4}'

def find_courses(directory):
    """Searches a directory for evaluation text files, and returns a list of
    course codes."""
    return [re.sub('.txt', '', file_name.lower())
            for file_name in os.listdir(directory)
            if first_match(COURSE_CODE_REGEX, file_name)]

def first_match(regex, string):
    """Given a regex and a string to search, this function simply returns the
    first match, if there is one."""
    match = re.search(regex, string)
    return match.group(0) if match else None

def find_scores(tree):
    """Traverses a directory for score_overview.txt. It returns a dictionary
    where each key is a semester code, and associated the value is path to
    the score_overview file."""
    return {first_match(SEMESTER_CODE_REGEX, root): root + '/' + f
            for root, directory, files in os.walk(tree)
            for f in files if f == 'score_overview.txt'}

def calculate_score(scores):
    """The input parameter is a list of keywords in a TwoWayDict. The return
    value is the average of the scores associated with the term."""
    return sum([SCORE_RANKINGS[score] for score in scores]) / float(len(scores))

def readlines_no_carrige_return(filename):
    """This is a wrapper for reading file content from a file. It reads the file
    associated with given file name, through a pipe that deletes all carrige
    return (\\r) symbols. It returns the result of readlines()."""
    # Pipe input through 'tr' to delete carrige return symbols.
    pipe = pipes.Template()
    pipe.append('tr -d \'\\r\'', '--')

    # Open the file using our pipe.
    f = pipe.open(filename, 'r')
    result = f.readlines()

    f.close()

    return result

def extract_courses(files):
    """The input parameter files is a dictionary where all keys are a semester
    code, and corresponds to a filename. The function returns a
    dictionary. This dictionary contains keys that corresponds to a semester
    dode, and it's value is another dictionary. Each of these dictionarys
    has a key that corresponds to a course code, and the value is a score. A
    special key called 'average_score' is associated with the average score
    of a semester."""
    courses = dict()
    courses['average_score'] = dict()
    for semester_code, filename in files.items():

        lines = readlines_no_carrige_return(filename)

        average_score = 0.0
        numer_of_scores = 0.0
        # Traverses a file, looking for course ratings.
        for line in lines:
            match = first_match(COURSE_CODE_REGEX, line)
            # If a course rating is found we calculate the score.
            if match:
                scores = re.findall(SCORE_REGEX, line)
                if len(scores) == 0:
                    continue;
                # If a new course is found, we give it a dictionary to fill.
                if not courses.get(match):
                    courses[match] = dict()
                # Fill in the score for a given semester.
                courses[match][semester_code] = calculate_score(scores)
                # Update data to generate an average score.
                average_score += courses[match][semester_code]
                numer_of_scores += 1
        # For each semester an average is calculated.
        average_score /= numer_of_scores
        courses['average_score'][semester_code] = average_score

    return courses

def semester_str(semester_code):
    """Returns a string representation of semestercodes. Example: h2009 ->
    høsten 2009, v2013 -> våren 2013"""
    time_of_year = 'våren' if semester_code[0] == 'v' else 'høsten'
    return time_of_year + ' ' + semester_code[1:]

def plot_course(course_name, courses, output):
    """The function generates a plot for a spesific course. Given a course
    name, and a dictionary of courses, we get the course data from the
    dictionary, with the course name as key. A figure with the name of the
    course (and the proper file extension pdf) is written to file."""
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


def tex_add_plot(course_code, path):
    """This function returns a LaTeX snippet which includes a generated plot
    into a LaTeX document."""
    plot = os.path.join(path, course_code)
    string = """\
\\begin{center}
  \\includegraphics[width=\\textwidth]{""" + plot + """.pdf}
\\end{center}
\\end{minipage}"""
    return string


def rebuild_tex(path_to_report, path):
    """Reads a LaTeX file and adds a include for each course."""
    report = readlines_no_carrige_return(path_to_report)
    report_file = open(path_to_report, 'w')

    course_header_regex = r'\\subsection\*\{([\w-]+\d{4}) - [\w ]+'
    rating_regex = r'\\\\\~\\emph\{Generell vurdering'
    minipage = """\
\\begin{minipage}{\\textwidth}
\\vspace{5mm}
"""
    # When a match is found, a plot should be added two lines below.
    write_in_two = -1
    course_code = ''

    for line in report:
        match = re.findall(course_header_regex, line)
        if match:
            course_code = match[0]
            report_file.write(minipage)
        report_file.write(line)
        if first_match(rating_regex, line):
            write_in_two = 2
        if write_in_two is 0:
            report_file.write(tex_add_plot(course_code, path))
        write_in_two -= 1

    report_file.close()


def main():
    """The main function for this program."""
    import sys
    import argparse

    # Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', action='store',
                        dest='output', default='.',
                        help='Sets OUTPUT destination (\'.\' is default)')
    parser.add_argument('-t', action='store',
                        dest='score_tree_path', default='.',
                        help='Traverse SCORE_TREE_PATH for score_overview.txt files')
    parser.add_argument('-d', action='store',
                        dest='filter_path', default=None,
                        help='Searches FILTER_PATH for courses to plot')
    parser.add_argument('-r', action='store',
                        dest='report', default=None,
                        help='rebuilds a REPORT with plots')
    parser.add_argument('-m', action='store_true',
                        dest='multiprocessing', default=None,
                        help='enable multiprocessing')

    # Extract arguments from command line arguments.
    result = parser.parse_args(sys.argv[1:])
    output = result.output
    score_tree = result.score_tree_path
    filter_path = result.filter_path
    rebuild_report = result.report

    # Traverse a directory tree and finds all score files. These are given to
    # extract_courses, and returns a dictionary of courses.
    courses = extract_courses(find_scores(score_tree))
    with open('course-data.js', 'w') as f:
        f.write(str(courses).upper())

    if filter_path:
        courses = {course: val for course, val in courses.items()
                   if course in find_courses(filter_path)
                   or course == 'average_score'}

    # Make it more LaTeX like (serif)
    plt.figure(figsize=(10, 5))
    plt.rc('font', family='serif')

    if result.multiprocessing:
        # Why not multiprocess?
        pool = multiprocessing.Pool(multiprocessing.cpu_count() * 4)

        # Maps over courses keys, using multithreading.
        pool.map(partial(plot_course, courses=courses, output=output), courses)
    else:
        for course in courses:
            plot_course(course, courses, output)

    if rebuild_report:
        rebuild_tex(rebuild_report, output)

if __name__ == "__main__":
    main()
