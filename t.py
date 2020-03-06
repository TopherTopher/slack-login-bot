import csv
from time import sleep
from datetime import datetime

from api_token import token # Store API token in app_token.py

import requests
from tqdm import trange

api_url = 'https://slack.com/api/'


def write_dicts_to_csv(filename, dictionaries):
    field_names = dictionaries[0].keys()
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for dictionary in dictionaries:
            writer.writerow(dictionary)



def get_users():
    concat_url = api_url + 'users.list' # Create API URL with endpoint
    params = {'token': token}
    print(' Downloading users ...')
    res = requests.get(concat_url, params=params)
    res_data = res.json()

    if not res_data['ok']:
        raise ValueError(f'Something went wrong.'
                            'URL: {res.url}'
                            'Error: {res_data["error"]}')

    return res_data['members']

    sleep(3)  # Limit for Tier 2 is 20 req/min


def main():
    user_list = get_users()
    write_dicts_to_csv('list_users.csv', user_list)

if __name__ == '__main__':
   main()
