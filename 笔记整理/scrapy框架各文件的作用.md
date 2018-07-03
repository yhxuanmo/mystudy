### setting.py

- 在该文件中，只要是进行整个项目的配置，如配置USER_AGENT、配置管道、添加项目中用到的常量等

####配置USER_AGENT

- 由于一些网站的限制，我们通过爬虫访问网站时，可以加上USER_AGENT参数，模拟浏览器行为

```python
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
```

- 该参数设置之后，不需要手动引用，项目运行时，自动引用

#### 配置管道的调用

- 如果我们要通过管道pipelines.py来处理数据，那么需要配置该参数

```
ITEM_PIPELINES = {
   'qidianspider.pipelines.DouBanspiderPipeline': 300,
   'qidianspider.pipelines.OtherPipeline': 301,
}
```

- DouBanspiderPipeline和OtherPipeline分别对应pipelines.py文件中的类，类名必须一致
- 每个键对应的值（300,301等），表示对应的权重，数字越小，pipelines.py文件中对应的类就先执行

#### 定义项目常量

- 在spider的各文件中，有时我们需要用到一些常量，可以直接在setting中定义
- 这里定义了mongodb相关的常量

```python
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'douban'
MONGODB_COLLECTIONS = 'movies'
```

- 常量的引用：

  - 通过scrapy.conf引用

  ```python
  from scrapy.conf import settings
  ```

  - 通过这种方式引用的setting是类似于字典格式，可以通过[键]或者get方法取值
  -  
  - 通过导入模块的方法引用

  ```python
  from qidianspider import settings
  ```

  - 通过   .属性名    来获取值

### items.py

- 为了对数据做持久化处理，需要首先设置数据的储存模板

```python
import scrapy


class DouBanpiderItem(scrapy.Item):
    name = scrapy.Field()
    movie_img = scrapy.Field()
    directors = scrapy.Field()
    movie_info = scrapy.Field()
```

- 定义的类继承自scrapy.Item
- 每一个属性（键）都是scrapy.Field()，不用指定数据的类型



### pipelines.py

- 在这里对数据进行处理：数据过滤，数据持久化等

```python
import pymongo
from scrapy.conf import settings

class DouBanspiderPipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collections = db[settings['MONGODB_COLLECTIONS']]

    def process_item(self, item, spider):
        for i in range(len(item['name'])):
            data = {}
            data['name'] = item['name'][i]
            data['movie_img'] = item['movie_img'][i]
            data['directors'] = item['directors'][i]
            data['movie_info'] = item['movie_info'][i]
            self.collections.insert(data)
        return item
```

- 在初始化方法中创建连接mongodb的对象，并指定数据库和集合（表）
- 在process_item()方法中编写数据处理逻辑，process_item是固定写法，函数带有三个参数缺一不可：self, item, spider  ，item为爬虫返回的数据（items.py中类实例化的对象）

### spider中的爬虫

```python
import scrapy

from scrapy.selector import Selector

from qidianspider.items import DouBanpiderItem



class DouBanSpider(scrapy.spiders.Spider):
    name = 'douban'
    start_urls = {
        'https://movie.douban.com/top250'
    }

    def parse(self,response):
        res = Selector(response)
        items = DouBanpiderItem()
        # 电影名
        items['name'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()
        # 电影图片
        items['movie_img'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()
        # 电影导演和演员
        info1 = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').extract()
        # 年份/国家/分类
        info2 = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').extract()

        items['directors'] = [info.strip().replace('\xa0', '') for info in info1]
        items['movie_info'] = [info.strip().replace('\xa0', '') for info in info2]

        return items
```



