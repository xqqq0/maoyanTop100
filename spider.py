# -*- coding:utf-8 -*-
import json
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
        for item in match:
            yield {
                "index": item[0],
                "image": item[1],
                "title": item[2],
                "star": item[3].strip()[3:],
                "release_time": item[4].strip()[5:],
                "score": item[5] + item[6]
            }

    else:
        print ("匹配失败")

def write_to_file(content):
    with open("result.txt","a") as f:
        # 字典转换为json字符串存储到文件
        f.write(json.dumps(content) + "\n")
        f.close()

def main():
    url = "http://maoyan.com/board/4"
    html = get_one_page(url)
    for item in  parse_one_page(html):
        write_to_file(item)

if __name__ == "__main__":
    main()

