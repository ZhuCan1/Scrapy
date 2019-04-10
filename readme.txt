1.scrapy的安装:百度
2.常用指令:
#创建一个项目
scrapy startproject quoteproject （+ 路径）;
cd quoteproject;

#创建一个spider

scrapy genspider quotes quotes.toscrape.com

#启动爬虫

scrapy crawl quotes

#进入交互模式(网址要用""不是'')

scrapy shell "网址"

#启动爬虫并设置保存结果格式
scrapy crawl quotes -o quotes.csv
scrapy crawl quotes -o quotes.json
scrapy crawl quotes -o quotes.xml
3.xpath和css的使用:
Xpath获取文本内容

response.xpath('//div/text()');//获取div文本(不包含div子标签中的文本)
response.xpath('//div').xpath('string(.)')这种方式获取所有文本 并且拼接
注意：在scrapy中使用string(.)必须单独使用:
     例如:response.xpath('//div/string(.)') 使用错误

Xpath获取属性内容

response.xpath('//a/@href')

Xpath按照属性选择

response.xpath('//div[@id="images"]/a/text()').get()

获取孩子中第二个超链接a[2]
response.xpath('//div[@class="articles"]/div[@class="wz_tab"]/div[@class="wz_content"]/h3/a[2]/@href')

response.xpath('//a[contains(@href, "image")]/@href')

response.css('a[href*=image]::attr(href)')

response.xpath('//a[contains(@href, "image")]/img/@src')

response.css('a[href*=image] img::attr(src)')

css获取文本内容
response.css('span::text')

css获取属性内容
response.css('base::attr(href)')

最后用extract(),extract_first(),get(),getall()提取值,css选择器不支持//查找


4.实例分析
   4.1  爬取http://quotes.toscrape.com/上所有的名人名言：
1.创建scrapy项目:
     scrapy startproject quoteturial
     cd quoteturial
     scrapy genspider quotes quotes.toscrape.com
        
2.用编译软件打开该项目:
        # -*- coding: utf-8 -*-
import scrapy
from quotetutorial import items

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        # 必须使用.extract()才能提取最终的数据
        for quote in quotes:
            item = items.QuotetutorialItem()
            text =   quote.xpath('span[@class="text"]/text()').extract_first()
            author = quote.xpath('span/small[@class="author"]/text()').extract_first()
            tags = quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
          #获取下一页的地址链接 
          next = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        url = response.urljoin(next);
        yield scrapy.Request(url=url, callback=self.parse)
        
 3.保存在数据库
   setting.xml中配置
     #配置mongo环境
     MONGO_URI='localhost'
     MONGO_DB='quotes'
     
     ITEM_PIPELINES = {
     'quotetutorial.pipelines.TextPipeline': 300,
     'quotetutorial.pipelines.MongoPipeline': 400,
  }
4.自定义Items
     import scrapy
     class QuotetutorialItem(scrapy.Item):
       text = scrapy.Field()
       author = scrapy.Field()
       tags = scrapy.Field()
       
5.pipelines.py
TextPipeline
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

MongoPipeline
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
   
4.2.爬取https://twistedmatrix.com/documents/current/core/ex    amples/上所有的文件
使用scrapy自带的FilesPipeline进行爬取:
1.开启FilesPipeline
  ITEM_PIPELINES = {
      'scrapy.pipelines.files.FilesPipeline': 1,
}
#定义存储路径
FILES_STORE = 'F:/file/newfile/scrapyfile'

2.自定FileItem,必须包含下面两个属性:
class FileItem(scrapy.Item):
    file_urls = scrapy.Field()  #指定文件下载的链接
    files = scrapy.Field()   #文件下载完成后会在里面写相关信息
    
3.spider
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['twistedmatrix.com']
    start_urls =   ['https://twistedmatrix.com/documents/current/core/examples/']

    def parse(self, response):
        urls = response.css('a.reference.download.internal::attr(href)').extract()
        for url in urls:
           item = FileItem()
           #注意设置file_urls时必须用[url]，不能直接用url字符串
           item['file_urls'] = [response.urljoin(url)]
           yield item
           
4.修改保存文件默认名称:
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
ITEM_PIPELINES = {
    'fileTest.pipelines.MyFilePipeline': 1,
}


FilesPipeline的工作流如下：
  1.在spider中爬取要下载的文件链接，将其放置于item中的file_urls
  2. spider将其返回并传送至pipeline链
  3.当FilesPipeline处理时，它会检测是否有file_urls字段，如果有的话，会将url传送给scarpy调 度器和下载器。
  4.下载完成之后，会将结果写入item的另一字段files，files包含了文件现在的本地路径（相对于配置FILE_STORE的路径）、文件校验和checksum、文件的url.
 从上面的过程可以看出使用FilesPipeline的几个必须项：
  1. Item要包含file_urls和files两个字段；
  2.打开FilesPipeline配置；
  3.配置文件下载目录FILE_STORE。

4.3  爬取image.so.com上的图片
使用scrapy自带的FilesPipeline进行爬取:
1.开启FilesPipeline
  ITEM_PIPELINES = {
      'scrapy.pipelines.images.ImagesPipeline': 1,
}
#定义存储路径
IMAGES_STORE = 'F:/file/newfile/scrapypicture'
#开启这个功能后，下载一张图片时，本地会出现3张图片，1张原图片，2张缩略图
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
#检查图片的宽度和高度，过滤掉尺寸小的图片
IMAGES_MIN_WIDTH = 110  # 最小宽度
IMAGES_MIN_HEIGHT = 110  # 最小高度

2.自定BeautyItem,必须包含下面两个属性:
class BeautyItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field() #指定图片下载的链接
    images = scrapy.Field()#图片下载完成后会在里面写相关信息

    
3.spider
class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.so.com']
    url_pattern = 'http://image.so.com/zj?ch=beauty&sn={offset}&listtype=new&temp=1'

    #    start_urls = ['http://image.so.com/']
    def start_requests(self):
        step = 30
        for page in range(0, 1):
            url = self.url_pattern.format(offset=page * step)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        ret = json.loads(response.body)
        for row in ret['list']:
          yield BeautyItem(image_urls=[row['qhimg_url']], name=row['group_title'])




4.4  爬取知网的论文:
http://search.cnki.com.cn/Search.aspx?q={q}&rank=relevant&cluster=all&val=&p=0
class ZhiwangFileItem(scrapy.Item):
    #文档来源网站名称(知网)
    url = scrapy.Field()
    #文档来源栏目名称(机器学习)
    column = scrapy.Field()
    # 文档类型(硕士论文)
    type = scrapy.Field()
    # 文档作者或创建者或发布者
    author = scrapy.Field()
    # 文档创建时间
    create_time = scrapy.Field()
    # 文档标题
    title = scrapy.Field()
    # 相关链接
    href = scrapy.Field()
    # 文档来源栏目技术方向
    techology =scrapy.Field()
    # 特征关键词
    words = scrapy.Field()
    # 文档评论数
    comment_counts = scrapy.Field()
    # 文档转载数
    redict_counts = scrapy.Field()
    # 文档点赞数
    like_counts = scrapy.Field()
    # 文档来源网站技术重要性权重
    weight = scrapy.Field()
    # 文档传播指标
    index = scrapy.Field()
    #文档下载地址
    file_urls = scrapy.Field()
    #文档相关信息
    files = scrapy.Field()

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

MONGO_URI='localhost'
MONGO_DB='zhiwang'
    
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
            r = requests.get(file_urls)
            file_path = 'F:/file/newfile/scrapyfile/zhiwangfile/' + techology + '/'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            if str(file_urls).endswith('pdfdown'):
                file_path = file_path + title + '.pdf'
                with open(file_path, "wb") as f:
                  f.write(r.content)
                f.close()
            if str(file_urls).endswith('cajdown'):
                file_path = file_path + title + '.caj'
                with open(file_path, "wb") as f:
                        f.write(r.content)
                        f.close()
            yield scrapy.Request(url=href, meta={'item' : item }, callback=self.parse_file)
        next = response.xpath('//div[@class="articles"]/p[@id="page"]/a[@class="n"]/@href').extract()
        if(len(next) == 1):
            next = next[0]
        else:
            next = next[1]
        next_url = self.start_urls[0] + next
        if next_url:
           yield Request(url=next_url,callback=self.parse_page)



4.4.5python下载文件
import requests
import os
url = 'http://search.cnki.net/down/default.aspx?filename=SZTJ201801088&dbcode=CJFD&year=2018&dflag=pdfdown'
r = requests.get(url)
file_path = 'f:/file/newfile/zc/pdf/'
if not os.path.exists(file_path):
        os.makedirs(file_path)
if str(url).endswith('pdfdown'):
    file_path = file_path + 'zc.pdf'
with open(file_path, "wb") as f:
     f.write(r.content)
f.close()
4.5 链接提取器的使用(正则表达式)
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import PeopleItem
from scrapy import Request
class PeopleSpider(scrapy.Spider):
    name = 'people'
    #allowed_domains = ['word.people.com.cn']
    query_urls = 'http://{type}.people.com.cn/'
    def start_requests(self):
        type = input('请输入新闻类别:(politics,world,tw(台湾),military,leaders,legal,society):')
        yield Request(self.query_urls.format(type=type),callback=self.parse)

    def parse(self, response):
        pattern = 'n1/[^\s]*html'
        link = LinkExtractor(allow=pattern)
        links = link.extract_links(response)
        if links:
            for link_one in links:
                yield Request(url=link_one.url,callback=self.parse_url)

    def parse_url(self, response):
        item = PeopleItem()
        column = response.xpath('//div[@class="box01"]/div[@class="fl"]/a/text()').extract_first()
        type = response.xpath('//div[@class="clearfix w1000_320 path path2 pos_re_search"]/div[@class="fl"]/span[@id="rwb_navpath"]').xpath('string(.)').extract_first()
        author = response.xpath('//div[@class="clearfix w1000_320 text_con"]/div[@class="fl text_con_left"]/div[@class="box_con"]/div[@class="edit clearfix"]/text()').extract_first()
        #记者
        journalist = response.xpath('//div[@class="clearfix w1000_320 text_title"]/p[@class="author"]').xpath('string(.)').extract_first()
        create_time = response.xpath('//div[@class="clearfix w1000_320 text_title"]/div[@class="box01"]/div[@class="fl"]/text()').extract_first()
        if len(create_time.split('\xa0\xa0')):
            create_time = create_time.split('\xa0\xa0')[0]
        title = response.xpath('//div[@class="clearfix w1000_320 text_title"]/h1/text()').extract_first()
        content = response.xpath('//div[@class="clearfix w1000_320 text_con"]/div[@class="fl text_con_left"]/div[@class="box_con"]').xpath('string(.)').extract_first()
         #来源
        item['url'] = response.url
        # 文档来源栏目名称('人民网－人民日报')
        item['column'] = column
        # 文档类型(人民网>>时政>>高层动态)
        item['type'] = type
        # 文档作者或创建者或发布者
        item['author'] = author
        # 文档创建时间
        item['create_time'] = create_time
        # 文档标题
        item['title'] = title
        # 文档链接
        item['file_urls'] = response.url
        # 新闻内容
        item['content'] = content
        yield item


参考网址:
https://www.jianshu.com/p/0775a4df1fe4
https://www.cnblogs.com/lei0213/p/8097515.html









