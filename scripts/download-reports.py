# Downloads TSV and HTML reports for a user from nettskjema.uio.no

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
import requests
import os
import sys
import argparse

from selenium import webdriver

argparser = argparse.ArgumentParser(description='Download report data from nettskjema.uio.no')
argparser.add_argument('--out', '-o', help='Output directory (default=".")', type=str, default='.')
argparser.add_argument('--filter', '-f', help='String to filter by', type=str)
argparser.add_argument('--username', '-u', help='Username for login', type=str)
argparser.add_argument('--password', '-p', help='Password for login', type=str)
argparser.add_argument('--tsv', help='Download TSV files', action="store_true")
argparser.add_argument('--html', help='Download HTML reports', action="store_true")
args = argparser.parse_args()

if not args.tsv and not args.html:
    args.tsv = True
    args.html = True

if not args.username:
    args.username = raw_input('Username: ')

if not args.password:
    args.password = getpass.getpass()

driver = webdriver.PhantomJS()
driver.set_window_size(800, 600)

driver.get('https://nettskjema.uio.no/user/index.html')

userfield = driver.find_element_by_css_selector('#username')
userfield.send_keys(args.username)

passfield = driver.find_element_by_css_selector('#password')
passfield.send_keys(args.password)

button = driver.find_element_by_css_selector('#login-box-form .submit')
button.click()

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

if args.tsv and not os.path.exists(tsv_path):
    os.makedirs(tsv_path)

if args.html and not os.path.exists(html_path):
    os.makedirs(html_path)

for (name, url) in formdata:
    print 'Fetching ' + name

    if args.tsv:
        tsv_url = url.replace('preview', 'download') + '&encoding=utf-8'
        response = session.get(tsv_url)
        filename = os.path.join(tsv_path, name) + '.tsv'
        with open(filename, 'w') as f:
            f.write(response.content)

    if args.html:
        html_url = url.replace('preview', 'report/web') + '&include-open=1&remove-profile=1'
        response = session.get(html_url)
        filename = os.path.join(html_path, name) + '.html'
        with open(filename, 'w') as f:
            f.write(response.content)
