import os
import requests
from datetime import datetime

from common.config import config

class Alpha(object):

    # Def: Get intraday data from alpha vantage
    # In: freq - time frame, symbol - ticker symbol, interval = 1min, 5min, 15min, 30min, or 60min, data_type - json/csv
    # Out: file location of data
    def get_data(self, freq, symbol, interval, data_type='csv'):
        # Get AlphaVantage API Key
        key = config.get('alpha-vantage', 'api.key')

        # Format URL
        url = config.get('alpha-vantage', 'intraday.data')

        url = url.format(freq, symbol, interval, key, data_type)

        print("Getting data from: {}".format(url))

        # Grab Data
        try:
            response = requests.get(url)

        except Exception as e:
            raise e

        # Save data
        workspace = os.getcwd()
        time = datetime.now().date()

        data_loc = '{}/data/'.format(workspace)

        file_name = '{}_{}_{}.{}'.format(freq, symbol, interval, time, data_type)

        with open(data_loc + file_name, 'w+') as file:
            file.write(response.content.decode("utf-8") )

        return data_loc + file_name

    # Helper function for possible inputs
    # In: None
    # Out; String of options
    def get_data_help(self):
        return """
        freq options:                       interval options:       data_type options:
            TIME_SERIES_INTRADAY                1min                    csv
            TIME_SERIES_DAILY                   5min                    json
            TIME_SERIES_DAILY_ADJUSTED          15min
            TIME_SERIES_WEEKLY                  30min
            TIME_SERIES_WEEKLY_ADJUSTED         60min
            TIME_SERIES_MONTHLY
            TIME_SERIES_MONTHLY_ADJUSTED
        """