# -*- coding:utf-8 -*-
import re
import requests
from requests.exceptions import RequestException

'''
1.获取单页的数据
'''


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        print("errorcode:%d" % response.status_code)
        return None
    except RequestException:
        print ("单页面获取失败")
        return None

'''
2.解析页面数据
'''

#.*?<p.*?star".*?>(.*?)</p>
def parse_one_page(html):
    pattern = re.compile('<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"'
                         + '.*?<p.*?"name".*?<a.*?>(.*?)</a>.*?star".*?>(.*?)</p>'
                         + '.*?<p.*?releasetime".*?>(.*?)</p>.*?<p.*?score".*?>'
                         + '.*?integer".*?>(.*?)</i>.*?fraction".*?>(.*?)</i></p>.*?</dd>', re.S)
    match = re.findall(pattern, html)
    if match:
        print (len(match), match)
    else:
        print ("匹配失败")



def main():
    url = "http://maoyan.com/board/4"
    html = get_one_page(url)
    parse_one_page(html)

if __name__ == "__main__":
    main()

