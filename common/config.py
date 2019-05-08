import configparser

config = configparser.ConfigParser()
config.read("../properties/algo-trading.properties")

def get(self, section, key):
    return config[section].get(key, '')