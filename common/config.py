import os
import configparser

def get(section, key):
    config = configparser.ConfigParser()
    config.read("{}/properties/algo-trading.properties".format(os.getcwd()))
    return config.get(section, key)

def get_secret(section, key):
    config = configparser.ConfigParser()
    config.read("{}/properties/secrets.properties".format(os.getcwd()))
    return config.get(section, key)