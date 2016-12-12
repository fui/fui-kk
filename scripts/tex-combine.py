#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Combines all latex files into 1 big latex document"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"

__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import json
import argparse
import re
from collections import OrderedDict, deque

def get_args():
    argparser = argparse.ArgumentParser(description='Combine tex reports into 1 document')
    argparser.add_argument('--semester', '-s', help='Semester(folder name)', type=str, required=True)
    argparser.add_argument('--verbose', '-v', help='Print moves', action="store_true")
    args = argparser.parse_args()

    return args

def data_folder(semester):
    return "./data/"+semester+"/"

def extract_number(course_code):
    m = re.search(r"[0-9]{4}", course_code)
    if m is None:
        return None
    return int(m.group(0))

def latex_label_value(label, value, post=""):
    return r"".join([r"\textbf{",label,r":} ",str(value),post])

def tex_combine(semester, verbose=False):
    path = "./resources/course_names/all.json"
    course_names = json.load(open(path), object_pairs_hook=OrderedDict)

    semester_folder = data_folder(semester)
    path = semester_folder + "courses.json"
    semester_data = json.load(open(path), object_pairs_hook=OrderedDict)

    tex_contents = deque([])

    with open('./resources/tex/header.tex') as f:
        tex_contents.append(f.read())

    for course_code, course_data in semester_data.items():
        if extract_number(course_code) >= 4000:
            labels = ["Respondents","of"]
        else:
            labels = ["Antall besvarelser","av"]

        path = semester_folder + "json/" + course_code + ".numbers.json"
        participation_string = ""
        try:
            with open(path,'r') as f:
                participation_data = json.load(f)
                invited = int(participation_data["invited"])
                answered = int(participation_data["answered"])
                participation = answered / invited
                participation_string = r" ".join([
                r"\textbf{", labels[0], r":}",
                str(answered),
                labels[1],
                str(invited),
                "({0:.1f}\%)".format(participation*100)
                ])
        except FileNotFoundError:
            print('Could not open '+path+' ! Skipping...')
            participation_string = ("\nThe course "+course_code+" numbers.json file is missing!\n")

        path = semester_folder + "tex/" + course_code + ".tex"
        try:
            with open(path,'r') as f:
                tex_contents.append("".join([
                r"\section{",course_code,r" - ",
                                course_names[course_code],r"}"]))
                tex_contents.append(r"\label{course:"+course_code+r"}")
                tex_contents.append(participation_string)
                tex_contents.append(r'''
                \begin{figure}[H]
                \begin{center}
                \includegraphics[width=0.99\textwidth]{../plots/COURSE.pdf}
                \end{center}
                \end{figure}
                '''.replace("COURSE", course_code))
                tex_contents.append(f.read())
                tex_contents.append(r"\newpage")
        except FileNotFoundError:
            print('Could not open '+path+' ! Skipping...')
            tex_contents.append("\nThe course "+course_code+" tex file is missing!\n")

    with open('./resources/tex/tail.tex') as f:
        tex_contents.append(f.read())

    tex_final = "\n\n".join(tex_contents)

    report_folder = semester_folder + "report/"
    os.makedirs(report_folder, exist_ok = True)
    report_name = "fui-kk_report_"+semester+".tex"

    with open(report_folder+report_name, 'w') as f:
        f.write(tex_final)

if __name__ == '__main__':
    args = get_args()
    tex_combine(args.semester, args.verbose)
