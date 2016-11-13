#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Downloads TSV and HTML reports for a user from nettskjema.uio.no"""

__authors__    = ["Erik Vesteraas"]
__copyright__  = "Erik Vesteraas"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

# Dependencies:
# pip install selenium
# pip install requests
# brew install phantomjs

# Login and forms system requires javascript, so we use selenium to login and
# browse the page.
# Downloading files with selenium is not very convenient, so we use requests
# for that particular part.
# PhantomJS is the engine we use for selenium.

import getpass
import os
import sys
import argparse
import json

import requests

from selenium import webdriver

def get_args():
    argparser = argparse.ArgumentParser(description='Download report data from nettskjema.uio.no')
    argparser.add_argument('--out', '-o', help='Output directory (default="./downloads")', type=str, default='./downloads')
    argparser.add_argument('--filter', '-f', help='String to filter by', type=str)
    argparser.add_argument('--username', '-u', help='Username for login', type=str)
    argparser.add_argument('--password', '-p', help='Password for login', type=str)
    argparser.add_argument('--tsv', help='Download TSV files', action="store_true")
    argparser.add_argument('--html', help='Download HTML reports', action="store_true")
    argparser.add_argument('--stats', help='Download answer statistics', action="store_true")
    args = argparser.parse_args()

    if not (args.tsv or args.html or args.stats):
        args.tsv = True
        args.html = True
        args.stats = True

    if not args.username:
        args.username = raw_input('Username: ')

    if not args.password:
        args.password = getpass.getpass()

    return args

def login(driver, args):
    driver.get('https://nettskjema.uio.no/user/index.html')

    userfield = driver.find_element_by_css_selector('#username')
    userfield.send_keys(args.username)

    passfield = driver.find_element_by_css_selector('#password')
    passfield.send_keys(args.password)

    button = driver.find_element_by_css_selector('#login-box-form .submit')
    button.click()

def write_to_file(folder, name, extension, content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, name) + '.' + extension
    filename = filename.replace(' ', '_')
    with open(filename, 'w') as f:
        f.write(content)

def try_to_find_int(driver, selector):
    try:
        return int(driver.find_element_by_css_selector(selector).text)
    except:
        return 0

def render_html(stats, content):
    return '''
    <html>
        <head>
            <meta charset="utf-8" />
        </head>
        <body>
            <p>Delivered replies: {answered}</p>
            <p>Commenced replies: {started}</p>
            <p>Number of sent invitations: {invited}</p>
            <hr />
            {content}
        </body>
    </html>
    '''.format(
        content=content,
        answered=stats['answered'],
        started=stats['started'],
        invited=stats['invited']
    )

def download_files(driver, args):
    driver.get('https://nettskjema.uio.no/user/form/list.html')

    forms = driver.find_elements_by_css_selector('.forms .formName')

    formdata = map(lambda form: (form.text, form.get_attribute('href')), forms)

    if args.filter:
        filtered = filter(lambda x: args.filter in x[0], formdata)
        print 'Filter matched {} of {} forms'.format(len(filtered), len(formdata))
        formdata = filtered

    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    tsv_path = os.path.join(args.out, 'tsv')
    html_path = os.path.join(args.out, 'html')
    stats_path = os.path.join(args.out, 'stats')

    for (name, url) in formdata:
        print 'Fetching ' + name

        results_url = url.replace('preview', 'results')
        driver.get(results_url)
        stats = {
            'answered': try_to_find_int(driver, '.delivered-submissions .number'),
            'started': try_to_find_int(driver, '.saved-submissions .number'),
            'invited': try_to_find_int(driver, '.valid-invitations .number')
        }

        if args.tsv:
            tsv_url = url.replace('preview', 'download') + '&encoding=utf-8'
            response = session.get(tsv_url)
            write_to_file(tsv_path, name, 'tsv', response.content)

        if args.html:
            html_url = url.replace('preview', 'report/web') + '&include-open=1&remove-profile=1'
            response = session.get(html_url)
            write_to_file(html_path, name, 'html', render_html(stats, response.content))

        if args.stats:
            stats_json = json.dumps(stats)
            write_to_file(stats_path, name, 'json', stats_json)

def main():
    args = get_args()

    driver = webdriver.PhantomJS()
    driver.set_window_size(800, 600)

    try:
        login(driver, args)
        download_files(driver, args)
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    main()
