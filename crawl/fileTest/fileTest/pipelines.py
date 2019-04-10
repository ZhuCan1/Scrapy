# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FiletestPipeline(object):
    def process_item(self, item, spider):
        return item

#实现文件名的保存
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import os
class MyFilePipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def file_path(self, request, response=None, info=None):
        parse_result = urlparse(request.url)
        #获取路径名
        path = parse_result.path
        #获取文件名:
        basename = os.path.basename(path)
        return basename
