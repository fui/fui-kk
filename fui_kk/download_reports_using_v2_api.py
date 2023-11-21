#!/usr/bin/env python3

""" Downloads reports from Nettskjema's v2 API using token authentication.

API documentation: https://utv.uio.no/docs/nettskjema/api

The required authorization token is acquired in the following steps:
1. Create an API user at https://nettskjema.no/user/api/index.html
2. Grant the API user the `READ_FORMS` and `READ_SUBMISSIONS` roles
3. Add your IP address to the `Permitted IP addresses` (all of UiO = 129.240.0.0/16)
4. Grant the API user access to edit each form under `Permissions`

The v2 API lack a method to iterate all avalible forms. Get form IDs:
a. either manually when you add the API user's permissions,
b. or scrape https://nettskjema.no/user/form/all-my-forms.json
"""

from csv import reader as csv_reader
from datetime import date, datetime
from dateutil.parser import parse as date_parse
from json import dumps as json_dumps
from requests import get as requests_get

api_url = 'https://nettskjema.no/api/v2'


def read_form_ids(filename):
    '''Reads the form IDs of a given text file.'''
    with open(filename, 'r') as file:
        lines = list(csv_reader(file))
        return [item for sublist in lines for item in sublist] # dirty fix


def create_headers(token):
    '''Create the request headers needed for API requests.'''
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    return headers


def get_token_expiration_date(headers):
    '''Get the token's expiration date as a `datetime` object.'''
    query_url = '{}/users/admin/tokens/expire-date'.format(api_url)
    response = requests_get(query_url, headers=headers)
    if response.status_code == 200:
        expiration_date = date_parse(response.json()['expireDate']).date()
        if expiration_date > date.today(): # fails for tokens expiring later today
            return expiration_date
        else:
            raise Exception('Token has expired (expiration date {})'.format(expiration_date))
    else:
        raise Exception('API error (HTTP code {})'.format(response.status_code))


def list_form_submissions(headers, form_id):
    '''List all submissions for a form.'''
    query_url = '{}/forms/{}/submissions'.format(api_url, form_id)
    response = requests_get(query_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('API error (HTTP code {})'.format(response.status_code))


if __name__ == '__main__':
    token = input('Enter your API user\'s authentication token: ')
    headers = create_headers(token)
    try:
        expiration_date = get_token_expiration_date(headers)
    except Exception as error:
        print(error)
        exit(1)
    print('The provided token seems to be valid (expires {})'.format(expiration_date))

    form_ids_file = input('Enter name of file with form IDs: ')
    form_ids = read_form_ids(form_ids_file)
    # TODO get output path from user
    for form_id in form_ids:
        submissions_ids = list_form_submissions(headers, form_id)
        print(json_dumps(submissions_ids, sort_keys=True, indent=4))
        # TODO: convert JSON to either TSV or CSV
        # TODO: store the output in a file
