# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException


'''
1.获取单页的数据
'''
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return  response.text
        print("errorcode:%d" % response.status_code)
        return None
    except RequestException:
        print ("单页面获取失败")
        return None


