#!/usr/bin/env python3

import getpass
import os
import sys
import argparse
import json

def get_args():
    argparser = argparse.ArgumentParser(description='Upload reports to vortex')
    argparser.add_argument('--input', '-i', help='Input directory (default="./data")', type=str, default='./data')
    argparser.add_argument('--output', '-o', help='Output directory (default="/Volumes/kursevaluering/")', type=str, default='/Volumes/kursevaluering/')
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
        args.username = input('Username: ')

    if not args.password:
        args.password = getpass.getpass()

    return args

def upload_files(args):
    


def main():
    args = get_args()
    upload_files(args)

if __name__ == '__main__':
    main()
