#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads course codes and names"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__license__    = "MIT"

import os
import sys
import argparse
import json
import requests
from collections import OrderedDict
from bs4 import BeautifulSoup

from file_funcs import dump_json, load_json

def get_args():
    argparser = argparse.ArgumentParser(description='Download report data from nettskjema.uio.no')
    argparser.add_argument('--url', '-u', help='URL', type=str)
    argparser.add_argument('--output', '-o', help='Output file', type=str)
    argparser.add_argument('--filter', '-f', help='File with course codes to exclude', type=str)
    args = argparser.parse_args()
    return args

def write_page(content, path):
    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    with open(path+".html", 'wb') as f:
        f.write(content)

def course_dict(html):
    courses = OrderedDict()
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all("td", class_="vrtx-course-description-name"):
        l = td.text.split(" ")
        course_code = l[0]
        course_name = " ".join(l[2:-2])
        courses[course_code] = course_name
    return courses

def course_filter(courses, filters):
    if (filters is None) or (len(filters) == 0):
        return courses
    for course_code in list(courses):
        for substring in filters:
            if substring in course_code:
                del courses[course_code]
                break
    return courses

def course_list(url, path, filters_path):
    filters = []
    if filters_path != None:
        with open(filters_path) as f:
            filters = f.read().splitlines()

    page = requests.get(args.url)
    # write_page(page.content, path)

    html = page.content.decode("utf-8")
    courses = course_filter(course_dict(html), filters)
    dump_json(courses, path)

if __name__ == '__main__':
    args = get_args()
    course_list(args.url, args.output, args.filter)
