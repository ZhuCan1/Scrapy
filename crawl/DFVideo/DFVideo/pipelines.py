# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import log
import pymongo
class DfvideoPipeline(object):
 def __init__(self):
  self.mongodb = pymongo.MongoClient(host='127.0.0.1', port=27017)
  self.db = self.mongodb["DongFang"]
  self.feed_set = self.db["video"]
  # self.comment_set=self.db[comment_set]
  self.feed_set.create_index("video_title", unique=1)
  # self.comment_set.create_index(comment_index,unique=1)
 def process_item(self, item, spider):
  try:
   self.feed_set.update({"video_title": item["video_title"]}, item, upsert=True)
  except:
   log.msg(message="dup key: {}".format(item["video_title"]), level=log.INFO)
  return item
 def on_close(self):
  self.mongodb.close()