###############################
# Sample Script to connect to CoinGecko API
# 1. Get Transaction Data of Volumes
# 2. Get Prices by Crypto
# 3. Get News on Crypto
# @Author: BhargavSN
###############################
from IPython.core.display import HTML
from pycoingecko import CoinGeckoAPI
import pprint
import re
import pandas as pd
from IPython.display import display
from pivottablejs import pivot_ui


def runstub():
    cg = CoinGeckoAPI()
    gecko_list = [
        "bitcoin",
        "ethereum",
        "ripple",  # xrp
        "tether",
        "bitcoin-cash",
        "cardano",
        "bitcoin-cash-sv",
        "litecoin",
        "chainlink",
        "binancecoin",
        "eos",
        "tron",
    ]
    time_period = 300
    data = {}
    for coin in gecko_list:
        try:
            nested_lists = cg.get_coin_market_chart_by_id(
                id=coin, vs_currency="usd", days=time_period
            )["prices"]
            data[coin] = {}
            data[coin]["timestamps"], data[coin]["values"] = zip(*nested_lists)

        except Exception as e:
            print(e)
            print("coin: " + coin)

    frame_list = [
        pd.DataFrame(data[coin]["values"], index=data[coin]["timestamps"], columns=[coin])
        for coin in gecko_list
        if coin in data
    ]
    df_crypto = pd.concat(frame_list, axis=1).sort_index()

    pivot_ui(df_crypto, outfile_path='pivottablejs.html')
    HTML('pivottablejs.html')


# Program Entry point
if __name__ == '__main__':
    runstub()
