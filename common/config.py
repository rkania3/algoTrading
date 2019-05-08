import os
import configparser

config = configparser.ConfigParser()
config.read("{}/properties/algo-trading.properties".format(os.getcwd()))

def get(section, key):
    return config.get(section, key)