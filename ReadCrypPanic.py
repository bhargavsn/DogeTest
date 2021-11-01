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
    auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Replace with your correct token
    crypto_obj = CryptoNews(url, auth_token)
    data = crypto_obj.load_data()
    return data


# Program Entry point
if __name__ == '__main__':
    crypto_data = get_crypto_data()
    print(crypto_data)
