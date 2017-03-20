#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Hacky way to make sure imports work'''
import sys
import os
sys.path.insert(0, "./")
if "/src" not in os.getcwd() and os.path.exists("./src/__init__.py"):
    sys.path.insert(0, "./src")
