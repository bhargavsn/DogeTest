###############################
# Sample Script to connect to CryptoPanic API
# 1. Get Transaction Data of Volumes
# 2. Get Prices by Crypto
# 3. Get News on Crypto
# @Author: BhargavSN
###############################
import json
import ssl
import traceback
import urllib.request


class CryptoNews:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
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
    url = "https://cryptopanic.com/api/posts/?auth_token"
    auth_token = "xxxxxx"  # Replace with your correct token
    crypto_obj = CryptoNews(url, auth_token)
    data = crypto_obj.load_data()
    return data


def analyse_data(data, currency):
    k = {'Currency': currency, 'Score news': 0}
    j = 0
    while j < len(data['results']):
        # print("Scanning the news...")
        # print(data['results'][j])
        try:
            for x in data['results'][j]['currencies']:
                # print(x['code'])
                if k['Currency'] == x['code']:
                    important_votes = float(data['results'][j]['votes']['important'])
                    if important_votes == 0:
                        important_votes = 1

                    negative_votes = float(data['results'][j]['votes']['negative'])
                    if negative_votes == 0:
                        negative_votes = 1

                    positive_votes = float(data['results'][j]['votes']['positive'])
                    if positive_votes == 0:
                        positive_votes = 1

                    liked_votes = float(data['results'][j]['votes']['liked'])
                    if liked_votes == 0:
                        liked_votes = 1

                    disliked_votes = float(data['results'][j]['votes']['disliked'])
                    if disliked_votes == 0:
                        disliked_votes = 1

                    toxic_votes = float(data['results'][j]['votes']['toxic'])
                    if toxic_votes == 0:
                        toxic_votes = 1

                    # print("Found news on " + k['Currency'] + " calculating news score...")
                    k[
                        'Score news'] += important_votes / negative_votes * positive_votes * liked_votes / disliked_votes / toxic_votes

        except Exception as e:
            print("")
        j += 1
    print(k)


def print_ccy_codes(data):
    ccy_list = []
    j = 0
    while j < len(data['results']):
        try:
            for x in data['results'][j]['currencies']:
                if x['code'] not in ccy_list:
                    ccy_list.append(x['code'])

        except Exception as e:
            print("")
        j += 1
    print(ccy_list)


# Program Entry point
if __name__ == '__main__':
    crypto_data = get_crypto_data()
    print_ccy_codes(crypto_data)
    analyse_data(crypto_data, "DOGE")
    analyse_data(crypto_data, "BTC")
