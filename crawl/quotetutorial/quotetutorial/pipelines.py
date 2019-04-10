# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
class TextPipeline(object):
    def __init__(self):
        self.limit = 50
    def process_item(self, item, spider):
        if(item['text']):
            if(len(item['text']) > self.limit):
                #rstrip(chars)返回删除 string 字符串末尾的指定字符后生成的新字符串，chars -- 指定删除的字符（默认为空格） -- 指定删除的字符（默认为空格）
                item['text'] = item['text'][0 : self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')

import pymongo
class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    #获取数据库信息等配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    #连接数据库操作
    def open_spider(self, spider):
        #连接数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        #指定数据库名称
        self.db = self.client[self.mongo_db]
    #处理信息,插入数据库
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item
    #关闭数据库
    def close_spider(self, spider):
        self.client.close()

