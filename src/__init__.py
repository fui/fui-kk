#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

# All modules are all .py files in src folder without __ in filename
files = os.listdir(os.path.dirname(__file__))
__all__ = [x[:-3] for x in files if "__" not in x and x.endswith(".py")]
