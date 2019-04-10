# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
from ..items import ZhiwangFileItem,FileItem
import requests
import os

class ZhiwangSpider(scrapy.Spider):
    name = 'zhiwang'
    #因为page地址和论文地址域名不一样，所有不能加allowed_domains
   # allowed_domains = ['search.cnki.com.cn']
    start_urls = ['http://search.cnki.com.cn/']
    file_query = 'http://search.cnki.com.cn/Search.aspx?q={q}&rank=relevant&cluster=all&val=&p=0'

    def start_requests(self):
        a = input("请输入查询内容:")
        yield Request(self.file_query.format(q = a),callback=self.parse_page)


    def parse_file(self, response):
        item = response.meta['item']
        author = response.xpath('//div[@id="content"]/div/div[3]').xpath('string(.)').extract_first()
        words = response.xpath('//div[@id="content"]/div/div[4]').xpath('string(.)').extract_first()
        item['author'] = author
        item['words'] = words
        yield item

    def parse_page(self,response):
        #response.xpath('//div[@class="articles"]/div[@class="wz_tab"]/div[@class="wz_content"]/h3/a[1]/string(.)').extract_first()在scrapy中这样无法获取内容，会报错.
        #file_url = response.xpath('//div[@class="articles"]/div[@class="wz_tab"]/div[@class="wz_content"]/h3/a[1]')
        #text = file_url.xpath('string(.)').extract_first()
        results = response.xpath('//div[@class="articles"]/div[@class="wz_tab"]')
        for each in results:
            item = ZhiwangFileItem()
            title = each.xpath('div[@class="wz_content"]/h3/a[1]').xpath('string(.)').extract_first()
            file_urls = each.xpath('div[@class="wz_content"]/h3/a[2]/@href').extract_first()
            techology = each.xpath('div[@class="wz_content"]/h3/a[1]/span/span/text()').extract_first()
            arr1 = each.xpath('div[@class="wz_content"]/span/span[1]/text()').extract_first().split('\xa0\xa0')
            column = arr1[0]
            type = arr1[1]
            if len(arr1) == 2:
               create_time = arr1[1]
            else:
               create_time = arr1[2]
            arr2 = each.xpath('div[@class="wz_content"]/span/span[2]/text()').extract_first().split('|')
            redict_counts = arr2[0]
            index = arr2[1]
            href = each.xpath('div[@class="wz_content"]/h3/a[1]/@href').extract_first()
            #words = each.xpath('div[@class="wz_content"]/div').xpath('string(.)').extract_first()
            #author = Request(url = href, callback = self.parse_author)
            #文档来源网站名称
            item['url'] = self.start_urls
            # 文档来源栏目名称(大学)
            item['column'] = column
            # 文档类型(硕士论文)
            item['type'] = type
            # 文档作者或创建者或发布者
            #item[author] = author
            # 文档创建时间
            item['create_time'] = create_time
            # 文档标题
            item['title'] = title
            # 相关链接
            item['href'] = href
            # 文档来源栏目技术方向
            item['techology'] = techology
            # 特征关键词
           # item['words'] = words
            # 文档评论数
            #comment_counts = scrapy.Field()
            # 文档转载数
            item['redict_counts'] = redict_counts
            # 文档点赞数
            #like_counts = scrapy.Field()
            # 文档来源网站技术重要性权重
            item['weight'] = index
            # 文档传播指标
            item['index'] = index
            # 文档下载地址
            item['file_urls'] = [file_urls]
            #下载文件到指定目录
            # r = requests.get(file_urls)
            # file_path = 'F:/file/newfile/scrapyfile/zhiwangfile/' + techology + '/'
            # if not os.path.exists(file_path):
            #     os.makedirs(file_path)
            # if str(file_urls).endswith('pdfdown'):
            #     file_path = file_path + title + '.pdf'
            #     with open(file_path, "wb") as f:
            #       f.write(r.content)
            #     f.close()
            # if str(file_urls).endswith('cajdown'):
            #     file_path = file_path + title + '.caj'
            #     with open(file_path, "wb") as f:
            #             f.write(r.content)
            #             f.close()
            yield scrapy.Request(url=href, meta={'item' : item }, callback=self.parse_file)
        next = response.xpath('//div[@class="articles"]/p[@id="page"]/a[@class="n"]/@href').extract()
        if(len(next) == 1):
            next = next[0]
        else:
            next = next[1]
        next_url = self.start_urls[0] + next
        if next_url:
           yield Request(url=next_url,callback=self.parse_page)






