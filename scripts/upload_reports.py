#!/usr/bin/env python3
""" Moves reports(raw data) from the local folder to mounted DAV folder. """

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import getpass
import os
import sys
import argparse
import json
from shutil import copyfile

def get_args():
    argparser = argparse.ArgumentParser(description='Upload reports to vortex')
    argparser.add_argument( '--input', '-i',
                            help='Input directory (default="./data")',
                            type=str, default='./data')
    argparser.add_argument( '--output', '-o',
                            help='Output directory (default="/Volumes/kursevaluering/")',
                            type=str, default='/Volumes/KURS/')
    argparser.add_argument( '--semester', '-s', help='Semester', type=str)
    argparser.add_argument( '--verbose', '-v',
                            help='Print moves', action="store_true")
    args = argparser.parse_args()

    # Some error checking, semester must be specified.
    if not args.semester:
        print("Need to specify semester, ex: -s V2016")
        sys.exit(1)
    if len(args.semester) != 5:
        print("Invalid format for semester, ex: -s V2016")
        sys.exit(1)

    return args


def upload_files(args):
    """
    Moves files from args.input(local) to args.output(mounted webDAV)

    Example of html report locations: (args.semester = "V2016")

    args.input = "./data":
    args.output = "/Volumes/KURS/":

    from_path = ./data/V2016/html/INF1000.html
    to_path = /Volumes/KURS/INF1000/V2016/INF1000.html

    This function will create the necessary folders and copy the reports.
    """

    fromdir = args.input+"/"+args.semester+"/html/"
    print(fromdir)
    for report in os.listdir(fromdir):
        course = report[:-5]
        from_path = fromdir+report
        to_folder = args.output + course + "/" + args.semester + "/"
        to_path = to_folder + report
        if args.verbose:
            print(from_path + " -> " + to_path)
        os.makedirs(to_folder, exist_ok=True)
        copyfile(from_path, to_path)

def main():
    args = get_args()
    upload_files(args)

if __name__ == '__main__':
    main()
