import os
import requests
from datetime import datetime

from common.config import config

class TD(object):

    # Def: Get stock data from alpha vantage
    # In: freq - time frame, symbol - ticker symbol, interval = 1min, 5min, 15min, 30min, or 60min, data_type - json/csv
    # Out: file locatsion of data
    def get_data(self, freq, symbol, interval, data_type='csv'):
        return None