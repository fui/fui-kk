#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch reports (html) from nettskjema results.(NO LONGER WORKS)"""

__authors__    = ["Unknown"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__credits__    = ["FUI"]
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import requests, getpass, re, codecs
from bs4 import BeautifulSoup


# Usage: python fetch-reports.py FOLDER [REGEX]

# try: input = raw_input
# except NameError: pass
# nettskjema_user = 'brukernavn'
# nettskjema_password = 'passord'
nettskjema_user = input("Nettskjema username: ")
nettskjema_password = getpass.getpass()
try:
    out_dir = sys.argv[1]
except IndexError:
    out_dir = "."

# try:
#     os.mkdir(out_dir, 0o700) #User-only access
# except OSError:
#     pass #It's cool, existed already

#Allow user to specify RegEx filter as second (optional) argument
form_filter = None
if len(sys.argv) > 2:
    form_filter = sys.argv[2]

print('Logging in... ',)

session = requests.session()

# Nettskjema changed login/authentication, this needs update
r_front = session.get('https://nettskjema.uio.no/')

login_data = {'j_username': nettskjema_user,
              'j_password': nettskjema_password,
              'login': ''}

r_login = session.post('https://nettskjema.uio.no/j_spring_security_check',
                       data = login_data)

if r_login.url == 'https://nettskjema.uio.no/index.html?authentication-failure=1':
    print('Wrong username/password, authentication failed!')
    sys.exit(1)

print('OK (code %d)!\nGetting form list... ' % r_login.status_code,)

r_list = session.get('https://nettskjema.uio.no/user/form/list.html')

print('Got it (code %d)!\nParsing... ' % r_list.status_code,)

list_soup = BeautifulSoup(r_list.text, "html.parser")

form_links = list_soup.find_all('a', class_='formName')

form_index = {}
matching_forms = 0

print('Scraped out entries about %d forms.' % len(form_links))
print('Downloading form data...')

for link in form_links:
    #Apply filter, if specified

    if form_filter and not re.search(form_filter, link.text):
        continue

    print('\t%s' % link.text)
    matching_forms += 1

    try:
        form_id = re.search(r'id=(\d+)', link['href']).group(1)

        forms_metadata= session.get('https://nettskjema.uio.no/user/form/submission/report.html?id=%s' % form_id)
        forms_data = session.get('https://nettskjema.uio.no/user/form/report/web.html?id=%s&include-open=1' % form_id)

        m = re.match(r'.* ([A-Z-]+[0-9]+)[A-Z-]*\s.*([VH]\d{4})', link.text)

        if m is None:
            print("Unparsable: " + line.text)
            continue

        (course, semester) = m.groups()

        if semester[0] != 'H' and semester[0] != 'V':
            continue

        os.system("mkdir -p %s" % (semester))

        form_out = codecs.open('%s/%s.html' % (semester, course),
                               mode = 'w',
                               encoding = 'utf-8')

        soup_meta = BeautifulSoup(forms_metadata.text, "html.parser")
        title_bar = soup_meta.select("#title-bar")[0]

        soup = BeautifulSoup(forms_data.text, "html.parser")

        head = soup.new_tag("head");
        # """<meta content="text/html; charset=utf-8" http-equiv="Content-Type">"""

        header_content = \
        [soup.new_tag('base', href='https://nettskjema.uio.no/', target='_blank'),
         soup.new_tag('meta', content='text/html; charset=utf-8',
                      **{'http-equiv':'Content-Type'}),
         soup.new_tag('link', href="/profil/uio-app-top-bottom.css?11.5",
                      media="screen, print", rel="stylesheet",
                      **{'type':'text/css'}),
         soup.new_tag('link', href="/css/reset.css?11.5", media="screen, print",
                      rel="stylesheet", **{'type':'text/css'}),
         soup.new_tag('link', href="/css/nettskjema.css?11.5", media="screen, print",
                      rel="stylesheet", **{'type':'text/css'}),
         soup.new_tag('link', href="/css/print.css?11.5", media="print",
                      rel="stylesheet", **{'type':'text/css'})]

        [head.insert(i, tag) for i, tag in enumerate(header_content)];

        space = soup.new_tag('div', **{'class':'bottom-spacing'})

        load  = soup.new_tag('div', id='load-report',
                             style='background: none;',
                             **{'class':'report-content'})

        # soup.head.insert(1, base_url)
        soup.head.replace_with(head)
        soup.body.insert(1, space)

        [tag.insert(1, title_bar) for tag in soup.select("#main-content")];
        [tag.wrap(load) for tag in soup.select("#main-content")];
        [tag.extract()  for tag in soup.select("#app-head-wrapper")];
        [tag.extract()  for tag in soup.select("#tabs")];
        [tag.extract()  for tag in soup.select("#versionInfo")];
        [tag.extract()  for tag in soup.select("#app-footer-wrapper")];
        [tag.extract()  for tag in soup.select("#contact-info")];
        [tag.extract()  for tag in soup.select("#app-responsible")];
        [tag.extract()  for tag in soup.select(".sub-menu")];
        [tag.extract()  for tag in soup.select(".report-title")];
        [tag.extract()  for tag in soup.select(".report-info > h3")];

        form_out.write(soup.prettify())
        form_out.close()

    except AttributeError as e:
        print('WTF, could not parse ID?! Skipping...', e)
        exit()
    except:
        print('Ouch, something bad happened with this form! Skipping...')
        exit()
