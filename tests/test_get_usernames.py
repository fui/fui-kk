#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from fui_kk.get_usernames import coursename_to_lsng_arg, read_course_names

def test_coursename_to_lsng_arg():
    assert coursename_to_lsng_arg('INF1010') == 'sinf1010'
    assert coursename_to_lsng_arg('INF-BIO5121') == 'sinfbio5121'
    assert coursename_to_lsng_arg('INF5004NSA') == 'sinf5004nsa'

def test_read_course_names():
    assert len(read_course_names('H2016')) > 0
    assert len(read_course_names('V2016')) > 0
