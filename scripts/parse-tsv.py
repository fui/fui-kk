#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parses tsv files and outputs json data for course."""

__authors__    = ["Person1", "Person2"]
__email__      = "person@mail"
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = ["Person1", "Person2", "Person3"]
__version__    = "0.1"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file "LICENSE.txt", which is part of this source code package.

import os
import sys
import csv
import json
import argparse
from bs4 import BeautifulSoup

def get_args():
    argparser = argparse.ArgumentParser(description="Parse tsv file(s) and output json course data")
    argparser.add_argument("--output", "-o", help="Output directory (default='.'')", type=str, default="./json")
    argparser.add_argument("--input", "-i", help="Input directory/file", type=str, default="./tsv")
    argparser.add_argument("--verbose", "-v", help="Verbose", action="store_true")
    args = argparser.parse_args()
    return args

def parse_course_tsv(tsv_filename):
    data = []
    with open(tsv_filename) as tsv_file:
        #for column in zip(*[line for line in csv.reader(tsv_file, delimiter='\t', quoting=csv.QUOTE_NONE)]):
            #print("Column: "+str(column))
        for row in csv.reader(tsv_file, delimiter='\t'):
            #print("Row: "+str(row))
            data.append(row)
    labels = data[0]
    responses_raw = data[1:]
    responses = {}
    for r in range(0, len(responses_raw)):
        responses[r] = {}
        for i in range(0,len(labels)):
            responses[r][labels[i]] = responses_raw[0][i]
    return responses

def main():
    args = get_args()

    if not os.path.exists(args.input):
        sys.exit("Error: invalid input path '{}'".format(args.input))

    input_files = []
    if os.path.isfile(args.input):
        input_files.append(args.input)
    else:
        for (root, dirs, files) in os.walk(args.input):
            for file_x in files:
                if file_x.endswith(".tsv"):
                    input_files.append(root,file_x)
    print(input_files)

    if os.path.exists(args.output):
        if os.path.isfile(args.output):
            sys.exit("Error: Out arg must be directory.")
    else:
        os.mkdir(args.output)

    # Hack
    csv_max = sys.maxsize
    overflow = True
    while overflow:
        overflow = False
        try:
            csv.field_size_limit(csv_max)
        except OverflowError:
            overflow = True
            csv_max = int(maxInt/16)
    courses = {}
    for tsv_filename in input_files:
        coursename = tsv_filename.replace(".tsv","")
        courses[coursename] = parse_course_tsv(tsv_filename)

    print(json.dumps(courses, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
