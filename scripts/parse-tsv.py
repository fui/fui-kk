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
import getpass
import argparse
from bs4 import BeautifulSoup

def get_args():
    argparser = argparse.ArgumentParser(description="Parse tsv file(s) and output json course data")
    argparser.add_argument("--out", "-o", help="Output directory (default=".")", type=str, default="./tsv")
    argparser.add_argument("--in", "-i", help="Input directory/file", type=str, default="./json")
    argparser.add_argument("--verbose", "-v", help="Verbose", action="store_true")
    args = argparser.parse_args()
    return args

def main():
    args = get_args()

if __name__ == "__main__":
    main()
