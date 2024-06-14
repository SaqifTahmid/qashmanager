import requests
from flask import Flask, Blueprint, jsonify
import sys
import os
import pandas as pd
import json

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tradingplatform.env.config import IEX_API_TOKEN

highest_traded = Blueprint('top_traded_stocks', __name__)

def fetchtop():
    # Fetch data from the source (e.g., IEX Cloud)
    url = "https://cloud.iexapis.com/stable/stock/market/list/mostactive"
    params = {
        'token': IEX_API_TOKEN,
        'listLimit': 1 # Fetch top 20 most traded stocks
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # top_stocks = response.json()
        top_stocks = []
        for stock in response.json():
            stock_data = {
                'symbol': stock['symbol'],
                'companyName': stock['companyName'],
                'iexVolume': stock['iexVolume'],
                'iexOpen': stock['iexOpen'],
                'iexClose': stock['iexClose'],
                'high': stock['high'],
                'low': stock['low']
            }
            top_stocks.append(stock_data)
        print(top_stocks)
        return top_stocks
    else:
        return None


@highest_traded.route('/top-traded-stocks', methods=['GET'])
def top_traded_stocks():
    top_stocks = fetchtop()

    if top_stocks:
        return jsonify(top_stocks)
    else:
        return jsonify({'error': 'Failed to fetch top traded stocks'}), 500

data= fetchtop()