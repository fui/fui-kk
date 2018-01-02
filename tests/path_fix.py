#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Hacky way to make sure imports work'''
import sys
import os
sys.path.insert(0, "./")
if "fui_kk" not in os.getcwd() and os.path.exists("./fui_kk/__init__.py"):
    sys.path.insert(0, "./fui_kk")
