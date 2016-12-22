#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation string"""

__authors__    = ["Person1", "Person2"]
__email__      = "person@mail"
__copyright__  = "Ole Herman Schumacher Elgesem"
__credits__    = ["Person1", "Person2", "Person3"]
__version__    = "0.1"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import json
import argparse
from collections import OrderedDict
from file_funcs import dump_json, load_json

def participation_summary(input_path, output_path):
    semester = load_json(input_path)
    #if not os.path.exists(output_path):
    with open(output_path, "w") as f:
        f.write("\n".join([
            r"\begin{table}[H]",
            r"\centering",
            r"\begin{tabular}{|l|c|c|c|}"
        ])+"\n")
        f.write("\n".join([r"\hline",r"Kurs & Respondenter & Inviterte & Prosent\\ \hline", ""]))
        for course_code, content in semester.items():
            answered = int(content["respondents"]["answered"])
            invited = int(content["respondents"]["invited"])
            if invited < 100:
                continue
            participation = "{0:.1f}\%".format(100*answered/invited)
            f.write("    "+" & ".join([
                course_code,
                str(answered),
                str(invited),
                participation
            ]))
            f.write(r" \\ \hline" + "\n")
        f.write("\n".join([
            r"\end{tabular}",
            r"\end{table}"
        ]))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Usage: participation_summary semester")
        sys.exit(0)
    semester_folder = "./data/"+sys.argv[1]+"/"
    participation_summary(semester_folder+"/outputs/courses.json", semester_folder+"/outputs/participation.tex")
