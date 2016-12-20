#!/usr/bin/env python3
"""Script to sort downloaded data (html and tsv) into folder structure
automatically based on file names(form titles)."""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__credits__    = ["Erik Vesteraas"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import argparse
import re
from shutil import copyfile


def get_args():
    argparser = argparse.ArgumentParser(description='Download report data from nettskjema.uio.no')
    argparser.add_argument('--input', '-i', help='Output directory (default="./downloads")', type=str, default='./downloads')
    argparser.add_argument('--output', '-o', help='Output directory (default="./data")', type=str, default='./data')
    argparser.add_argument('--verbose', '-v', help='Print moves', action="store_true")
    argparser.add_argument('--delete', '-d', help='Delete moved files', action="store_true")
    argparser.add_argument('--exclude', '-e', default=r'(testskjema)|(\*\*\*)', type=str,
                            help=r'Exclude regex(default="(testskjema)|(\*\*\*)")')
    args = argparser.parse_args()

    return args

def main():
    args = get_args()
    delete = args.delete
    exclude_pattern = re.compile(args.exclude)
    semester_pattern = re.compile(r'(V|H)[0-9]{4}')
    course_code_pattern = re.compile(r'(([A-Z]{2,4}-){0,1}[A-Z]{2,4}[0-9]{4})([A-Z]{2,4}){0,1}')
    for root, subdirs, files in os.walk(args.input):
        for file_x in files:
            path = os.path.join(root, file_x)
            filename, extension = os.path.splitext(path)
            m = exclude_pattern.search(path)
            if m is not None or path[0] == ".":
                print("Excluded: " + path)
                continue
            m = semester_pattern.search(path)
            if m is None:
                print("Skipped - No semester: " + path)
                continue
            semester = m.group(0)
            m = course_code_pattern.search(path)
            if m is None:
                print("Skipped - No course code: " + path)
                continue
            course = m.group(0)

            dir_name = extension[1:]
            if dir_name == "json":
                dir_name = "participation"
            target_folder = os.path.join(args.output, semester, "downloads", dir_name)
            os.makedirs( target_folder, exist_ok=True )
            newpath = os.path.join(target_folder, course + extension )

            if delete:
                os.rename(path, newpath)
            else:
                copyfile(path, newpath)
            if args.verbose:
                print(path)
                print(" -> "+newpath)
                print(root)

    while delete:
        delete = False
        for root, subdirs, files in os.walk(args.input):
            if len(subdirs) == 0 and len(files) == 0:
                os.rmdir(root)
                if args.verbose:
                    print("rm: "+path)
                delete = True

if __name__ == '__main__':
    main()
