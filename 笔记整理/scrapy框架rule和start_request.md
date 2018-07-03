### Rule

1.可以爬虫添加爬取规则属性rules，这个属性是一个列表，它可以包含多个Rule,每个Rule描述了那些链接需要抓取，那些不需要。这些rule可以有callback

2.爬虫的通常需要在一个网页里面爬去其他的链接，然后一层一层往下爬，scrapy提供了LinkExtractor类用于对网页链接的提取



#### LinkExtractor常用的参数有：

```
allow：提取满足正则表达式的链接
deny：排除正则表达式匹配的链接（优先级高于allow）
allow_domains：允许的域名（可以是str或list）deny_domains：排除的域名（可以是str或list）
restrict_xpaths：提取满足XPath选择条件的链接（可以是str或list）
restrict_css：提取满足css选择条件的链接（可以是str或list）
tags：提取指定标签下的链接，默认从a和area中提取（可以是str或list）
attrs：提取满足拥有属性的链接，默认为href（类型为list）
unique：链接是否去重（类型为boolean）
process_value：值处理函数（优先级大于allow）
```

#### Rule和LinkExtractor的使用

- 这里以豆瓣电影movie.douban.com/top250页面的爬取为例
- 该页面的分页请求的url为

```
第一页 https://movie.douban.com/top250
第二页开始 https://movie.douban.com/top250?start=25&filter=
```

- 可以看出每个分页就是？后面的参数变化

```
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule, CrawlSpider
from scrapy.selector import Selector

from qidianspider.items import DouBanpiderItem



class DouBanSpider(CrawlSpider):
    name = 'douban'
    start_urls = {
        'https://movie.douban.com/top250'
    }
    # 添加规则，并指定回调函数
    rules = {
        Rule(LinkExtractor(allow=r'https://movie.douban.com/top250.*'), callback='parse_iterm')
    }

    def parse_iterm(self,response):
        res = Selector(response)
        items = DouBanpiderItem()
        # 电影名
        items['name'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()
        # 电影图片
        items['movie_img'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()


        return items
```

- 使用Rule时，定义的类不再继承自scrapy.spiders.Spider，而是继承自**CrawlSpider**
- 添加url规则rules，通过LinkExtractor指定允许的url，指定回调函数
- 定义爬取函数，这里的函数作为Rule的回调函数，**不能**再以parse命名



### start_request

- 有时url结构固定，只是其中的传递的参数有变化，我们可以重scrapy.spiders.Spider中的start_requests，来拼接url并发起请求

```python
import json
import scrapy
from scrapy import Request
from my_scrapy.items import WeiBoUserItem


class DouBanSpider(scrapy.spiders.Spider):
    name = 'weibo'
    user_uids = ['1223178222', '5187664653', '1476938315', '1678105910']
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid=%s&containerid=100505%s'

    def start_requests(self):
        for uid in self.user_uids:
            yield Request(self.user_url %(uid,uid), callback=self.parse)

    def parse(self, response):
        res = json.loads(response.text)
        pass
```

- 定义的类 继承自scrapy.spiders.Spider

- 定义url模板，user_url

- 重写start_requests方法，注意这里是用yield返回请求，Request中可以指定回调函数，也可以不用指定，程序执行时自动调用parse

  