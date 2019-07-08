import os
import time
import requests
from shutil import which
from splinter import Browser
import urllib.parse as up
import json

from common import config

class TD(object):

    def __init__(self):
        self.token = self.get_token()
        self.client_id = config.get_secret('td', 'client.id')

    def get_token(self):

        # Configure webdriver, get code from TD Ameritrade
        executable_path = {
            'executable_path': config.get_secret('paths', 'chromedriver.path')
        }

        browser = Browser('chrome', **executable_path, headless=False)

        client_id = config.get_secret('td', 'client.id')
        redirect_url = config.get_secret('td', 'redirect.url')

        method = 'GET'
        url = config.get('auth', 'td.auth').format(up.quote(redirect_url), up.quote(client_id))

        payload = {'response_type': 'code',
                   'redirect_uri': redirect_url,
                   'client_id': client_id}

        p = requests.Request(method, url, params=payload).prepare()

        auth_url = p.url

        browser.visit(auth_url)

        login = {
            'username': config.get_secret('td', 'username'),
            'password': config.get_secret('td', 'password')
        }

        username = browser.find_by_id("username").first.fill(login['username'])
        password = browser.find_by_id("password").first.fill(login['password'])
        submit = browser.find_by_id("accept").first.click()

        browser.find_by_id("accept").first.click()

        redirect_url_response = browser.url

        time.sleep(1)

        parse_url = up.unquote(redirect_url_response.split('code=')[1])

        browser.quit()

        # Get token from TD Ameritrade

        token_url = config.get('auth', 'oauth')

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            'grant_type': 'authorization_code',
            'access_type': 'offline',
            'code': parse_url,
            'client_id': client_id,
            'redirect_uri': redirect_url
        }

        auth_reply = requests.post(token_url, headers=headers, data=payload)
        decoded_content = auth_reply.json()

        access_token = decoded_content['access_token']

        return access_token

    def get_account(self):
        url = config.get('td', 'get.accounts')

        headers = {
            'Authorization': "Bearer {}".format(self.token)
        }

        payload = {
            'apikey': self.client_id
        }

        response = requests.get(url, params=payload, headers=headers)

        return response.content.decode('utf-8')

    def get_movers(self):
        url = config.get('td', 'get.movers')

        headers = {
            'Authorization': "Bearer {}".format(self.token)
        }

        payload = {
            'apikey': self.client_id,
            'direction': 'up',
            'change': 'percent'
        }

        response = requests.get(url, params=payload, headers=headers)

        return json.loads(response.content.decode('utf-8'))

    def get_price_history(self, symbol, period, period_type, frequency, frequency_type, needExtendedHoursData):
        url = config.get('td', 'get.price.history').format(symbol)

        headers = {
            'Authorization': "Bearer {}".format(self.token)
        }

        payload = {
            'apikey': self.client_id,
            'period': period,
            'periodType': period_type,
            'frequency': frequency,
            'frequencyType': frequency_type,
            'needExtendedHoursData': needExtendedHoursData
        }

        response = requests.get(url, params=payload, headers=headers)

        return json.loads(response.content.decode('utf-8'))

    def get_quote(self, symbol):
        url = config.get('td', 'get.quote').format(symbol)

        headers = {
            'Authorization': "Bearer {}".format(self.token)
        }

        payload = {
            'apikey': self.client_id
        }

        response = requests.get(url, params=payload, headers=headers)

        return json.loads(response.content.decode('utf-8'))