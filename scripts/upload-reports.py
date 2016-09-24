# UPLOADS HTML REPORTS

# Dependencies:
# pip install selenium
# pip install requests
# brew install phantomjs

# Login and forms system requires javascript, so we use selenium to login and
# browse the page.
# PhantomJS is the engine we use for selenium.

import getpass
import os
import sys
import argparse
import json

import requests

from selenium import webdriver

def get_args():
    argparser = argparse.ArgumentParser(description='Upload reports to vortex')
    argparser.add_argument('--input', '-i', help='Input directory (default="./data")', type=str, default='./data')
    argparser.add_argument('--semester', '-s', help='Semester', type=str)
    argparser.add_argument('--username', '-u', help='Username for login', type=str)
    argparser.add_argument('--password', '-p', help='Password for login', type=str)
    args = argparser.parse_args()

    if not args.semester:
        print("Need to specify semester, ex: -s V2016")
        sys.exit(1)
    if len(args.semester) != 4:
        print("Invalid format for semester, ex: -s V2016")
        sys.exit(1)

    if not args.username:
        args.username = raw_input('Username: ')

    if not args.password:
        args.password = getpass.getpass()

    return args

def login(driver, args):
    driver.get('https://www-adm.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui-kk/KURS/?vrtx=admin')

    userfield = driver.find_element_by_css_selector('#username')
    userfield.send_keys(args.username)

    passfield = driver.find_element_by_css_selector('#password')
    passfield.send_keys(args.password)

    button = driver.find_element_by_css_selector('#login-box-form .submit')
    button.click()


def upload_files(driver, args):
    driver.get('https://www-adm.mn.uio.no/ifi/livet-rundt-studiene/organisasjoner/fui-kk/KURS/?vrtx=admin')

    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Upload html reports into correct folders in vortex


def main():
    args = get_args()

    driver = webdriver.PhantomJS()
    driver.set_window_size(800, 600)

    try:
        login(driver, args)
        upload_files(driver, args)
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    main()
