import os
import requests
from datetime import datetime

from common.config import config

class Utils(object):

    # Def: Get intraday data from alpha vantage
    # In: symbol - ticker symbol, interval = 1min, 5min, 15min, 30min, or 60min, data_type - json/csv
    # Out: file location of data
    def get_intraday_data(self, symbol, interval, data_type='csv'):
        # Get AlphaVantage API Key
        key = config.get('alpha-vantage', 'api.key')

        # Format URL
        url = config.get('alpha-vantage', 'intraday.data')

        url.format(symbol, interval, key, data_type)

        # Grab Data
        response = requests.get(url)

        # Save data
        workspace = os.getcwd()
        time = datetime.now().date()

        data_loc = '{}/algoTrading/data/'.format(workspace)

        file_name = '{}_{}_{}.{}'.format(symbol, interval, time, data_type)

        with open(data_loc + file_name, 'w+') as file:
            file.write(response.content)

        return data_loc + file_name
