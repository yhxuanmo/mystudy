# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.conf import settings
import pymongo

from my_scrapy.items import WeiBoUserItem, UserRelationItem


class UserCreateTimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiBoUserItem):
            item['create_time'] = datetime.now()
        return item


class MyScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveToMongoPipeline(object):
    def __init__(self):
        self.MONGODB_HOST = settings['MONGODB_HOST']
        self.MONGODB_PORT = settings['MONGODB_PORT']
        self.MONGODB_DB = settings['MONGODB_DB']
        conn = pymongo.MongoClient(host=self.MONGODB_HOST, port=self.MONGODB_PORT)
        db = conn[self.MONGODB_DB]
        self.collections = db[WeiBoUserItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, WeiBoUserItem):
            self.collections.update({'id':item['id']}, {'$set':item}, True)
        if isinstance(item,UserRelationItem):
            self.collections.update({'id':item['id']},
                                        {'$addToSet':{
                                            'fans':{'$each': item['fans']},
                                            'followers':{'$each':item['followers']}
                                            }
                                        }
                                    )
        return item
