#!/usr/bin/env python3
"""Gets the usernames of students taking courses this semester"""

__authors__    = ["Erik Vesteraas"]
__copyright__  = "Erik Vesteraas"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import paramiko
import getpass
import argparse
import sys
import os
from datetime import date, timedelta
from file_funcs import load_json

def get_args():
    argparser = argparse.ArgumentParser(description='Get usernames of students taking courses this semester')
    argparser.add_argument('--username', '-u', help='Username for login', type=str)
    argparser.add_argument('--password', '-p', help='Password for login', type=str)
    argparser.add_argument('--prev', help='Read data for the previous semester', action='store_true')
    args = argparser.parse_args()

    if not args.username:
        args.username = input('Username: ')

    if not args.password:
        args.password = getpass.getpass()

    if args.prev:
        args.semester = semester_string(date.today() - timedelta(days=182))
    else:
        args.semester = semester_string(date.today())

    return args

def semester_string(today):
    if today.month <= 7:
        return 'V' + str(today.year)
    else:
        return 'H' + str(today.year)

def coursename_to_lsng_arg(coursename):
    return 's' + coursename.lower().replace('-', '')

def read_course_names(semester):
    if semester.startswith('V'):
        filename = 'spring.json'
    elif semester.startswith('H'):
        filename = 'fall.json'
    else:
        print('Error: Invalid semester value, ' + semester)
        sys.exit()
    json_names = load_json('./resources/course_names/' + filename)
    return list(json_names.keys())

def main(args):
    print('Getting students for all courses in', args.semester)
    course_names = read_course_names(args.semester)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect('vor.ifi.uio.no', username=args.username, password=args.password, look_for_keys=False)

    outdir = './data/' + args.semester + '/outputs/usernames/'
    os.makedirs(outdir, exist_ok=True)

    try:
        for (i, course) in enumerate(course_names):
            print('Getting students for', course, '({}/{})'.format(i + 1, len(course_names)))
            lsng_arg = coursename_to_lsng_arg(course)
            stdin, stdout, stderr = client.exec_command('lsng ' + lsng_arg)
            usernames = stdout.read()
            file_path = outdir + course + '.txt'
            with open(file_path, 'w') as f:
                f.write(usernames.decode('utf-8'))
    finally:
        client.close()

if __name__ == '__main__':
    main(get_args())
