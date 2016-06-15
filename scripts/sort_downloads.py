#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to sort downloaded data (html and tsv) into folder structure
automatically based on file names(form titles)."""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = ["Ole Herman Schumacher Elgesem", "Erik Vesteraas"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import argparse
import re


def get_args():
    argparser = argparse.ArgumentParser(description='Download report data from nettskjema.uio.no')
    argparser.add_argument('--input', '-i', help='Output directory (default="./downloads")', type=str, default='./downloads')
    argparser.add_argument('--output', '-o', help='Output directory (default="./data")', type=str, default='./data')
    argparser.add_argument('--verbose', '-v', help='Print moves', action="store_true")
    args = argparser.parse_args()

    return args

def main():
    args = get_args()

    for root, subdirs, files in os.walk(args.input):
        for file_x in files:
            path = os.path.join(root, file_x)
            if(file_x == ".DS_Store"):
                os.remove(path)
                if args.verbose:
                    print("rm: "+path)
                break
            filename, extension = os.path.splitext(path)
            m = re.search('(V|H)[0-9]{4}',path)
            if m is None:
                break
            semester = m.group(0)
            m = re.search('INF[0-9]{4}',path)
            if m is None:
                break
            course = m.group(0)
            target_folder = os.path.join(args.output, semester, extension[1:])
            os.makedirs( target_folder, exist_ok=True )
            newpath = os.path.join(target_folder, course + extension )
            os.rename(path, newpath)
            if args.verbose:
                print(path)
                print(" -> "+newpath)

    deleting = True
    while deleting:
        deleting = False
        for root, subdirs, files in os.walk(args.input):
            if len(subdirs) == 0 and len(files) == 0:
                os.rmdir(root)
                if args.verbose:
                    print("rm: "+path)
                deleting = True

if __name__ == '__main__':
    main()
