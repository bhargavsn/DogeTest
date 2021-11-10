#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Bhargav
# ---------------------------------------------------------------------------
""" Reads Data from Cryptopanic website, outputs scores for each coin
Coin with most positive or important score can be worth looking into"""

import json
import ssl
import traceback
import urllib.request
import pprint

url: str = "https://cryptopanic.com/api/posts/?auth_token"
auth_token: str = ""  # Replace with your correct token


class CryptoNews:
    def __init__(self, crypto_url, crypto_auth_token):
        self.url = crypto_url
        self.auth_token = crypto_auth_token
        self.full_url = "=".join([self.url, self.auth_token])

    def load_data(self):
        for i in range(0, 10):
            try:
                print("Getting data from cryptopanic")
                context = ssl.SSLContext()
                response_crypto = urllib.request.urlopen(self.full_url, context=context)
            except IOError as e:
                print("Could not get data from cryptopanic.com")
                continue
            break
        try:
            data_crypto = json.loads(response_crypto.read())
        except Exception as e:
            print(traceback.format_exc())

        return data_crypto


def get_crypto_data():
    crypto_obj = CryptoNews(url, auth_token)
    data = crypto_obj.load_data()
    return data


def determine_score(score_info):
    return 1


def analyse_data(data, currency):
    k = {'Currency': currency, 'Score news': 0, 'titles': [], 'mention': 0}
    vote_keys = ['negative', 'positive', 'important', 'liked', 'disliked', 'lol', 'toxic', 'saved', 'comments']
    for key in vote_keys:
        k[key] = 0
    j = 0
    while j < len(data['results']):
        try:
            if 'currencies' in data['results'][j]:
                for x in data['results'][j]['currencies']:
                    if k['Currency'] == x['code']:
                        k['mention'] += 1
                        for key in vote_keys:
                            k[key] += float(data['results'][j]['votes'][key])
                        k['titles'].append(data['results'][j]['title'])

        except (ValueError, Exception):
            pass
        j += 1
    pprint.pprint(k, width=120)


def get_ccy_codes(data):
    ccy_list = []
    j = 0
    while j < len(data['results']):
        try:
            for x in data['results'][j]['currencies']:
                if x['code'] not in ccy_list:
                    ccy_list.append(x['code'])

        except (ValueError, Exception):
            pass
        j += 1
    return ccy_list


# Program Entry point
if __name__ == '__main__':
    crypto_data = get_crypto_data()
    ccy_codes = get_ccy_codes(crypto_data)
    # ccy_codes = ['MC']
    for ccy in ccy_codes:
        analyse_data(crypto_data, ccy)
