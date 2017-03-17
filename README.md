# maoyanTop100
抓取猫眼电影top100的数据

> 这是我关于爬虫得第二篇文字，其实应该放在第一篇，我看的三套视频顺序有点问题，本篇应该是算是最基础最简单的。

# 前言
> 本篇博客主要记录猫眼视频Too100的榜单的数据，每条榜单的数据由以下6部分组成，这五部分主要是集中一个<dd></dd>标签中，故通过正则匹配可以获取其中的数据

* 索引
* 封面
* 标题
* 主演
* 上映时间
* 评分

#分析页面
![单条榜单页面结构图](http://upload-images.jianshu.io/upload_images/954728-5f358335238a2580.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 索引是在i标签中
* 封面是在img标签的链接中
* 标题在a便签
* 主演是在p标签
* 上映时间在p标签
* 评分是在两个i标签中，拼起来的

# 具体爬取
> 这次爬取的代码大致分为4部分，页面获取，单条榜单的获取，页面所有榜单，最后保存到文件

### 页面获取
> 有了前面的爬取的基础，这里就很简单， 主要就是通过一个url下载页面，本次依旧采用requests框架进行数据的下载

```
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
```

### 单条榜单的获取
> 这一节是重头戏，通过正则匹配，将页面中6类有用的信息逐条拆解出来

##### 索引
* 源码
![索引源码](http://upload-images.jianshu.io/upload_images/954728-bc4a46699b8699b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 分析：
  * 根据崔老师教程中提到，要提取的数据所以在标签的正则表达式要是标签闭合，比如索引是在i标签中，故开头`<i`结尾要用`</i>`
  * 首先要dd开头，这是区分每一条单独的榜单，然后i标签，最好将css的样式匹配一部分，但是后边的`board-index-2`经过观察是不一样的，所以仅保留前半部分，然后分组(\d+)获取索引数据，最后i标签结束`<dd>.*?<i.*?board-index.*?>(.*?)</i>`

##### 图片
* 源码
![图片源码](http://upload-images.jianshu.io/upload_images/954728-58c30cd4883ce132.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 注意：
  * 在分析之前，提出一点注意，当页面元素很多的时候，我们分不清到底哪个才是我们想要的资源的时候，可以通过浏览器的开发工具自带一个选择器（一般类似箭头的标识）去选中元素，这时候就会自定的定位到相应的页面元素
  *  是还要记得和页面的源码对比一下，有时候会不一样，以页面源码为主，选择器当做一个参考
* 分析：封面主要是在img标签的src属性中，难度不大
`<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"`

#### 标题
* 源码
![标题源码](http://upload-images.jianshu.io/upload_images/954728-977806646d3ed712.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 分析： 标题主要是a标签，如何唯一确定呢，可以通过其父标签p的属性来唯一标识
`<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"`
`.*?<p.*?"name".*?<a.*?>(.*?)</a></p>`

####  主演
* 源码
![主演源码](http://upload-images.jianshu.io/upload_images/954728-5a5429a09779086b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 分析：主要就是存在p标签中，通过star来唯一确定
`<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"`
`.*?<p.*?"name".*?<a.*?>(.*?)</a>.*?star".*?>(.*?)</p>`

#### 上映时间
* 源码
![上映时间源码](http://upload-images.jianshu.io/upload_images/954728-ca9b53314e45e1ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 分析：同上，不再赘述
`<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"`
`.*?<p.*?"name".*?<a.*?>(.*?)</a>.*?star".*?>(.*?)</p>`
`.*?<p.*?releasetime".*?>(.*?)</p>`

#### 评分
* 源码
![评分源码](http://upload-images.jianshu.io/upload_images/954728-78e4b92a038738b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
* 分析：评分分两部分，在一个p标签之下，然后两个i标签，通过class加以区分
`<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)"`
`.*?<p.*?"name".*?<a.*?>(.*?)</a>.*?star".*?>(.*?)</p>`
`.*?<p.*?releasetime".*?>(.*?)</p>.*?<p.*?score".*?>`
`.*?integer".*?>(.*?)</i>.*?fraction".*?>(.*?)</i></p>.*?</dd>`

# 将数据转换为字典
* 设计好正则的pattern之后，利用正则的findall方法，将网页所有的表单进行过滤，此方法返回一个list，然后遍历list，将每条表单抽离成一个字典
![解析榜单](http://upload-images.jianshu.io/upload_images/954728-986d068f6af17e65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 将字典存储到本地文件
> 属于Python基础知识，不过多赘述，请看代码

```
'''
3，将获取到的数据转换为json格式存储到本地文件
'''
def write_to_file(content):
    with open("result.txt","a") as f:
        # 字典转换为json字符串存储到文件
        f.write(json.dumps(content) + "\n")
        f.close()

'''
4.项目总调度
'''
def main():
    # 主页面url
    url = "http://maoyan.com/board/4"
    # 获取页面
    html = get_one_page(url)
    # 遍历页面进行正则匹配
    for item in  parse_one_page(html):
        # 写入文件
        write_to_file(item)

if __name__ == "__main__":
    main()
```
# 数据转码
> 参看本地的txt文件，发现数据为Unicode编码，不易读取，根据视频中修改方式，报错，有可能是Python版本问题，我使用的是2.7的版本，但是视频中是3.x的版本

* 原视频是修改方式
![3.x修改方式](http://upload-images.jianshu.io/upload_images/954728-20a2f020ee5e388b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 报错信息
open函数在2.7版本，没有这个encoding的参数，所以不能使用，所以删掉
![报错信息](http://upload-images.jianshu.io/upload_images/954728-d6b50b9007208f16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 
* 继续报错
  当时想放弃探索，但是又不甘心谷歌了一把，虽然没有明白为什么这修改，但是还是起作用了
![继续报错](http://upload-images.jianshu.io/upload_images/954728-e706ab3f56c99324.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 修改
 头文件导入
```
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

# 总结
> 像前言中写道的，本文应该放在第一篇，算是爬虫里比较初级的，网页结构也较为简单，考查的知识点也主要是正则的匹配，除去这几点，还有几点自己感觉重要的罗列一下：

* 正则匹配的时候，如果正则的pattern过长，建议写一段就测试一下看能不能正常匹配，如果等所有的都写完在测试，不容易发现错误点
* 对于便签内取值的别不<i>(.*?)</i>,这样的一定要注意闭合标签
* 通过浏览器的开发者工具只能大致看下代码结果，但是细节有时候不可信，前端可能会对页面源代码进行处理，所以匹配的时候要查看源代码进行匹配

[源码地址](https://github.com/xqqq0/maoyanTop100)