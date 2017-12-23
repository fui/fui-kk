#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import path_fix

# Test that all modules can be imported:
from fui_kk.file_funcs import path_join, path_clean

def test_path_join():
    assert path_join("a", "b",   "e") == "a/b/e"
    assert path_join("a", "bcd", "e") == "a/bcd/e"

def test_path_clean():
    assert path_clean("INF****") == "INFXXXX"
    assert path_clean("INF1234 - Being cool") == "INF1234_-_Being_cool"
    assert path_clean("* * * *") == "X_X_X_X"
