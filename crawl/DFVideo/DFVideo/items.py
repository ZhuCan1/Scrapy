# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DfvideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_url = scrapy.Field()  # 视频源url
    video_title = scrapy.Field()  # 视频标题
    video_local_path = scrapy.Field()  # 视频本地存储路径
