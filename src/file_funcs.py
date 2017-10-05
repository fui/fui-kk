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
from collections import OrderedDict
import io

def path_join(*args):
    return "/".join(args)

def path_clean(p):
    return p.replace("*", "X").replace(" ", "_")

def filename_clean(p):
    return path_clean(p).replace("/", "_").replace("\\", "_")

def print_json(data):
    print(json.dumps(data, indent=2))

def dump_json(data, path):
    path = path_clean(path)
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(path, 'w', encoding="utf-8") as out_file:
        json.dump(data, out_file, indent=2, ensure_ascii=False)

def load_json(path):
    path = path_clean(path)
    try:
        with open(path, 'r', encoding="utf-8") as in_file:
            return json.load(in_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        print("ERROR: Could not open '{}' for read, file doesn't exist.".format(path))
        sys.exit(1)
    except json.decoder.JSONDecodeError as err:
        print("ERROR: The file '{}' contains invalid json syntax: {}".format(path,err))
        sys.exit(1)
