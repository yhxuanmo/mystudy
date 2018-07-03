### Scrapy组件

#### 引擎(Scrapy)

用来处理整个系统的数据流处理, 触发事务(框架核心)

#### 调度器(Scheduler)

用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 
由它来决定下一个要抓取的网址是什么, 同时去除重复的网址

#### 下载器(Downloader)

用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)

#### 爬虫(Spiders)

爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面

#### 项目管道(Pipeline)

负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，
将被发送到项目管道，并经过几个特定的次序处理数据。

#### 下载器中间件(Downloader Middlewares)

位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。

#### 爬虫中间件(Spider Middlewares)

介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。

#### 调度中间件(Scheduler Middewares)

介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。

### scrapy项目

- 创建虚拟环境
- pip 安装 scrapy，pywin32
- 如果安装scrapy过程中Twisted 安装出错，则需要手动安装Twisted

#### 创建项目

- 需要使用命令来创建项目文件

```
scrapy startproject yourspider
```

![spider_scrapy_project](img\spider_scrapy_project.png)

#### 文件说明

- scrapy.cfg:项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）
- items.py:设置数据存储模板，用于结构化数据，类似于Django的Model
- pipelines:数据处理行为，如：一般结构化的数据持久化
- settings.py:配置文件，如：递归的层数、并发数，延迟下载等
- spiders:爬虫目录，如：创建文件，编写爬虫规则。
- 注意：在spiders文件中创建爬虫的时候，一般以爬取的网站的域名为爬虫的名称 

#### 编写简单的爬虫

- 在spider目录下创建爬虫的py文件，这里以爬取起点中文网的小说分类为例

```python
import scrapy
from scrapy.selector import Selector


class QiDianSpider(scrapy.spiders.Spider):
    # 启动项目指定的name参数
    name = 'qidian'
    # 需要爬取哪些页面
    start_urls = {
        'https://www.qidian.com/',
    }

    def parse(self, response):
        res =Selector(response)
        menu_type_name = res.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        menu_type_href = res.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(menu_type_name, menu_type_href)
        return menu_type_name, menu_type_href
```

- 定义的类需要继承自scrapy.spiders.Spider
- 在类中指定项目启动的name参数
- 指定需要爬取的urls  注意：start_urls 不能写错
- 重构parse函数：在这里写爬取规则；response是服务器返回的响应，其内容可能是网页源码（需要Selector解析），也可能是json格式的字符串（response.text获取）
- 如果是Selector解析解析的网页源码，可以通过.xpath来匹配对应的值

#### 启动项目

- 通过命令来启动项目

```
scrapy crawl qidian
```

- 注意：这里的‘qidian'是定义类中的name的值



- 通过py文件来启动项目，在scrapy.cfg同级目录下创建一个main.py文件用于启动项目

```python
from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'weibo'])
```

- 这种方式启动项目，可以通过debug模式来调试代码
