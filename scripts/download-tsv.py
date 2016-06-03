# Downloads TSV files for all of a users forms

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

from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(800, 600)

driver.get('https://nettskjema.uio.no/user/index.html')
form = driver.find_element_by_css_selector('#login-box-form')

userfield = driver.find_element_by_css_selector('#username')
username = raw_input('Username: ')
userfield.send_keys(username)

passfield = driver.find_element_by_css_selector('#password')
password = getpass.getpass()
passfield.send_keys(password)

button = driver.find_element_by_css_selector('#login-box-form .submit')
button.click()

driver.get('https://nettskjema.uio.no/user/form/list.html')

forms = driver.find_elements_by_css_selector('.forms .formName')

formdata = map(lambda form: (form.text, form.get_attribute('href')), forms)

# Need to filter here if downloading all is not desired

session = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

if not os.path.exists('tsv'):
    os.makedirs('tsv')

for (name, url) in formdata:
    download_url = url.replace('preview', 'download') + '&encoding=utf-8'
    response = session.get(download_url)
    filename = 'tsv/' + name + '.tsv'
    with open(filename, 'w') as f:
        f.write(response.content)
