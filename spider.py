# -*- coding:utf-8 -*-
import requests


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
    except RequestException:
        print

    pass