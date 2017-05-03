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
                            help='Output directory (default="/Volumes/KURS/")',
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

def copy_file(src, dst, verbose=False):
    if verbose:
        print(src + " -> " + dst)
    if not os.path.exists(src):
        print("Warning: cannot copy file {} - does not exist.".format(src))
        return
    copyfile(src, dst)

def upload_files(src_dir, dest_dir, semester, verbose=False):
    """
    Moves files from args.input(local) to args.output(mounted webDAV)

    Example of html report locations:

    semester = "V2016"
    src_dir  = "./data":
    dest_dir = "/Volumes/KURS/":

    from_path = ./data/V2016/downloads/html/INF1000.html
    to_path   = /Volumes/KURS/INF1000/V2016/INF1000.html

    This function will create the necessary folders and copy the reports.
    """

    src_dir_html = src_dir+"/"+semester+"/downloads/html/"
    src_dir_tsv = src_dir+"/"+semester+"/downloads/tsv/"
    src_dir_json = src_dir+"/"+semester+"/outputs/stats/"
    src_dir_pdf = src_dir+"/"+semester+"/outputs/plots/"

    for report in os.listdir(src_dir_html):
        course = report[:-5]
        to_folder = dest_dir + course + "/" + semester + "/"
        os.makedirs(to_folder, exist_ok=True)

        from_html = src_dir_html + report
        from_tsv  = src_dir_tsv + course + ".tsv"
        from_json = src_dir_json + course + ".json"
        from_pdf  = src_dir_pdf + course + ".pdf"

        to_html = to_folder + report
        to_tsv  = to_folder + course + ".tsv"
        to_json = to_folder + course + ".json"
        to_pdf  = to_folder + course + ".pdf"

        copy_file(from_html, to_html, verbose)
        copy_file(from_tsv,  to_tsv, verbose)
        copy_file(from_json, to_json, verbose)
        copy_file(from_pdf,  to_pdf, verbose)

if __name__ == '__main__':
    args = get_args()
    upload_files(args.input, args.output, args.semester, args.verbose)
