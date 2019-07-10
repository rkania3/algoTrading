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

def set_secret(section, key, content):
    config = configparser.ConfigParser()

    file_path = "{}/properties/secrets.properties".format(os.getcwd())

    config.read(file_path)

    config[section][key] = content

    with open(file_path, 'w') as configfile:
        config.write(configfile)