# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from zhihuuser.items import UserItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'

   #用户信息页面
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

   #用户关注人的信息
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit=20'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #用户粉丝信息
    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit=20'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # url = 'https://www.zhihu.com/api/v4/members/gong-sun-qi-65?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        # url ='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=60&limit=20'
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0),callback=self.parse_follows)
        yield Request(self.follower_query.format(user=self.start_user,include=self.follower_query_query,offset=0),callback=self.parse_followers)

    def parse_user(self, response):
        results = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item
        #获取用户后接着输出用户关注的对象
        yield Request(self.follows_url.format(user=results.get('url_token'),include=self.follows_query,offset=0),callback=self.parse_follows)
        # 获取用户后接着输出用户粉丝的对象
        yield Request(self.follower_url.format(user=results.get('url_token'), include=self.follower_query, offset=0),
                      callback=self.parse_followers)
    #int offset = 20
    def parse_follows(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            #获取每一个关注者的信息，根据url_token获得关注者的url
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)

        #依次遍历后面几页的关注人
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            #获得的next_page
            #https://www.zhihu.com/members/excited-vczh/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadg
            #e%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=20
            urlresult = results.get('paging').get('next')
            urlresult2 = results.get('paging').get('next')
            #实际next_page
            #https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=
            # data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%
            # 2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20
            urlresult =  urlresult.split('&')[2].split('=')[1]
            urlresult2 = urlresult2.split('/')[4]
            yield Request(self.follows_url.format(user=urlresult2,include=self.follows_query,offset=urlresult),callback=self.parse_follows)




    def parse_followers(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            #获取每一个关注者的信息，根据url_token获得关注者的url
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)

        #依次遍历后面几页的关注人
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            urlresult = results.get('paging').get('next')
            urlresult2 = results.get('paging').get('next')
            urlresult =  urlresult.split('&')[2].split('=')[1]
            urlresult2 = urlresult2.split('/')[4]
            yield Request(self.follower_url.format(user=urlresult2,include=self.follows_query,offset=urlresult),callback=self.parse_followers)

