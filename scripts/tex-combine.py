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
from collections import OrderedDict, deque

def get_args():
    argparser = argparse.ArgumentParser(description='Combine tex reports into 1 document')
    argparser.add_argument('--semester', '-s', help='Semester(folder name)', type=str, required=True)
    argparser.add_argument('--verbose', '-v', help='Print moves', action="store_true")
    args = argparser.parse_args()

    return args

def data_folder(semester):
    return "./data/"+semester+"/"

def tex_combine(semester, verbose=False):
    path = "./resources/course_names/all.json"
    course_names = json.load(open(path), object_pairs_hook=OrderedDict)

    semester_folder = data_folder(semester)
    path = semester_folder + "semester.json"
    semester_data = json.load(open(path), object_pairs_hook=OrderedDict)

    tex_contents = deque([])

    with open('./resources/tex/header.tex') as f:
        tex_contents.append(f.read())

    for course_code, course_data in semester_data.items():
        path = semester_folder + "json/" + course_code + ".numbers.json"
        participation_string = ""
        try:
            with open(path,'r') as f:
                participation_data = json.load(f)
                invited = int(participation_data["invited"])
                answered = int(participation_data["answered"])
                participation = answered / invited

                participation_string = r'''
                \textbf{Respondents -}
                \textbf{Invited:} INVITED
                \textbf{Answered:} ANSWERED
                \textbf{Participation:} PARTICIPATION
                '''.replace("INVITED", str(invited))\
                .replace("ANSWERED", str(answered))\
                .replace("PARTICIPATION", "{0:.1f}".format(participation*100))
                participation_string += r"\%"
        except FileNotFoundError:
            print('Could not open '+path+' ! Skipping...')
            participation_string = ("\nThe course "+course_code+" numbers.json file is missing!\n")

        path = semester_folder + "tex/" + course_code + ".tex"
        try:
            with open(path,'r') as f:
                tex_contents.append("".join([
                r"\section{",course_code,r" - ",
                                course_names[course_code],r"}"]))
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
