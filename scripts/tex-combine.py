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
    semester_folder = data_folder(semester)
    path = semester_folder + "semester.json"
    semester_data = json.load(open(path), object_pairs_hook=OrderedDict)

    tex_contents = deque([])

    with open('./tex/header.tex') as f:
        tex_contents.append(f.read())

    for course_code, course_data in semester_data.items():
        path = semester_folder + "/tex/" + course_code + ".tex"
        try:
            with open(path,'r') as f:
                tex_contents.append(f.read())
        except FileNotFoundError: # parent of IOError, OSError *and* WindowsError where available
            print('Could not open '+path+' ! Skipping...')

    with open('./tex/tail.tex') as f:
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
