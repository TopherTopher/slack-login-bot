#!/usr/bin/env python3

import csv
from time import sleep
from datetime import datetime

from api_token import token

import requests
from tqdm import trange


def write_dicts_to_csv(filename, dictionaries):
    field_names = dictionaries[0].keys()
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for dictionary in dictionaries:
            writer.writerow(dictionary)


def get_access_logs():
    all_access_logs = []
    url = 'https://slack.com/api/team.billableInfo'
    params = {'token': token, 'count': 1000}  # 1000 logs per page is maximum

    print(' Downloading pages …')
    for page in trange(1, 101):  # 100 pages is maximum
        params['page'] = page
        res = requests.get(url, params=params)
        res_data = res.json()

        if not res_data['ok']:
            raise ValueError(f'Something went wrong.'
                             'URL: {res.url}'
                             'Error: {res_data["error"]}')

        all_access_logs.extend(res_data['billable_info'])

        sleep(3)  # Limit for Tier 2 is 20 req/min

    return all_access_logs



def main():
    access_logs = get_access_logs()
    write_dicts_to_csv('raw_data1.csv', access_logs)
    #!last_logins = get_last_logins(access_logs)
    #!members = get_all_members()
    #!add_missing_members(last_logins, members)
    #1write_dicts_to_csv('last_logins.csv', last_logins)


if __name__ == '__main__':
   main()
