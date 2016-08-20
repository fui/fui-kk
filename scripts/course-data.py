#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create relevant statistics from individual responses"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = []
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

def dump_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def main(path):
    course = json.load(open(path), object_pairs_hook=OrderedDict)

    stats = OrderedDict()
    responses = course["responses"]
    stats["answers"] = len(responses["NR"])

    course["stats"] = stats
    course.move_to_end("responses")
    dump_to_file(course, path)


if __name__ == '__main__':
    if(len(sys.argv) == 1):
        sys.exit("Must specify file path (overwrites file)")
    path = sys.argv[1]
    main(path)
