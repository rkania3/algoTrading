import os
import time
import requests
from shutil import which
from splinter import Browser
import urllib.parse as up

from common import config

class TD(object):

    def __init__(self):
        print('Creating TD Ameritrade Interface Object')

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