# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PeopletestPipeline(object):
    def process_item(self, item, spider):
        return item

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
        name = 'world'
        self.db[name].insert(dict(item))
        return item
    #关闭数据库
    def close_spider(self, spider):
        self.client.close()


