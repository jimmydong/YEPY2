# -*- coding: utf-8 -*-
import requests
import config

if __name__ == '__main__':
    try:
        response = requests.post('http://127.0.0.1:' + str(config.http_port), data={'_a':'qrcode','secuKey':'wxh_V1'})
        print(response.text)
    except requests.exceptions.ConnectionError:
        print('request return nothing')
    