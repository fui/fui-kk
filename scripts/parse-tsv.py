#!/usr/bin/env python3
"""Parses tsv files and outputs json data for course."""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = ["Erik Vesteraas"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file "LICENSE.txt", which is part of this source code package.

import os
import sys
import csv
import json
import argparse
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_args():
    argparser = argparse.ArgumentParser(
                description = "Parse tsv file(s) and output json course data")
    argparser.add_argument("--output", "-o", help="Output dir", type=str)
    argparser.add_argument("--input", "-i", help="Input dir/file", type=str)
    argparser.add_argument("--semester", "-s", default="all", help="Semester", type=str)

    args = argparser.parse_args()

    if args.semester:
        if args.semester == "all":
            dirs = next(os.walk('data'))[1]
            for d in dirs:
                if d.replace("/", "") == "all":
                    sys.exit("Error: Recursion check failed - 'all' folder!")
                os.system("python3 scripts/parse-tsv.py -s "+d)
            sys.exit()
        else:
            args.input = os.path.join("data",args.semester,"tsv")
            args.output = os.path.join("data",args.semester,"json")

    if not args.input or not args.output:
        sys.exit("Error: Specify input and output using -i and -o parameters, or semester using -s parameter")
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
    responses = OrderedDict()
    for l in labels:
        responses[l] = []
    for r in range(0, len(responses_raw)):
        for i in range(0,len(labels)):
            responses[labels[i]].append(responses_raw[r][i])
    return responses

def init_csv_reader():
    # Hack
    csv_max = sys.maxsize
    overflow = True
    while overflow:
        overflow = False
        try:
            csv.field_size_limit(csv_max)
        except OverflowError:
            overflow = True
            csv_max = int(csv_max/16)

def dump_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def parse_tsv_files(input_path, output_dir):
    if not os.path.exists(input_path):
        sys.exit("Error: invalid input path '{}'".format(input_path))

    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    else:
        for (root, dirs, files) in os.walk(input_path):
            for file_x in files:
                if file_x.endswith(".tsv"):
                    input_files.append(os.path.join(root,file_x))

    if os.path.exists(output_dir):
        if os.path.isfile(output_dir):
            sys.exit("Error: Out arg must be directory.")
    else:
        os.mkdir(output_dir)

    for tsv_filename in input_files:
        coursename = tsv_filename.replace(".tsv","")
        coursename = coursename.replace(input_path, "")
        coursename = coursename.replace("/", "")
        content = parse_course_tsv(tsv_filename)
        dump_to_file(content, os.path.join(output_dir,coursename)+".responses.json")

def main():
    args = get_args()
    init_csv_reader()
    parse_tsv_files(args.input, args.output)

if __name__ == "__main__":
    main()
