import json
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from my_scrapy.items import WeiBoUserItem, UserRelationItem


class DouBanSpider(scrapy.spiders.Spider):
    name = 'weibo'
    # 用户
    # user_uids = ['1223178222', '5187664653', '1476938315', '1678105910']
    user_uids = ['1223178222']

    user_url = 'https://m.weibo.cn/api/container/getIndex?uid=%s&containerid=100505%s'

    # 关注
    followers_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'

    # 粉丝
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'

    # start_urls = {
    #     'https://m.weibo.cn/api/container/getIndex?uid=1223178222&containerid=1005051223178222',
    # }

    def start_requests(self):
        for uid in self.user_uids:
            yield Request(self.user_url %(uid,uid), callback=self.parse)

    def parse(self, response):
        res = json.loads(response.text)
        if res.get('ok'):
            user_info = res.get('data').get('userInfo')
            user_item = WeiBoUserItem()
            user_params = {
                'id':'id', 'screen_name': 'screen_name', 'profile_image_url': 'profile_image_url',
                'profile_url': 'profile_url', 'verified_reason': 'verified_reason', 'close_blue_v':'close_blue_v',
                'description': 'description', 'gender': 'gender', 'followers_count': 'followers_count',
                'follow_count': 'follow_count', 'cover_image_phone': 'cover_image_phone','avatar_hd': 'avatar_hd'
            }
            for k, v in user_params.items():
                user_item[k] = user_info.get(v)

            yield user_item

            yield Request(self.followers_url.format(uid=user_item['id'], page=1),
                          callback=self.followser_parse,
                          meta={'uid': user_item.get('id'), 'page': 1}
                          )

            yield Request(self.fans_url.format(uid=user_item['id'], page=1),
                          callback=self.fans_parse,
                          meta={'uid': user_item.get('id'), 'page': 1})



    def followser_parse(self,response):
        # 解析关注用户的信息
        res = json.loads(response.text)
        if res['ok']:
            card_group = res['data']['cards'][-1]['card_group']
            for card_info in card_group:
                user_info = card_info.get('user')
                uid = user_info.get('id')
                yield Request(self.user_url %(uid, uid), callback=self.parse)

            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1

            user_relation = UserRelationItem()
            followers = []
            for c_info in card_group:
                followers.append([{'id':c_info.get('user').get('id'), 'name':c_info.get('user').get('screen_name')}])
            user_relation['id'] = uid
            user_relation['fans'] = []
            user_relation['followers'] = followers
            yield user_relation


            yield Request(self.followers_url.format(uid=uid,page=page), callback=self.followser_parse, meta={'uid':uid, 'page':page})


    def fans_parse(self,response):
        # 解析粉丝信息
        res = json.loads(response.text)
        if res['ok']:
            fans_info = res.get('data').get('cards')[-1].get('card_group')
            for fen in fans_info:
                uid = fans_info.get('user').get('id')
                yield Request(self.user_url % (uid, uid), callback=self.parse)

            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1

            user_relation = UserRelationItem()
            fans = []
            for fen in fans_info:
                fans.append([{'id':fen.get('user').get('id'), 'name':fen.get('user').get('screen_name')}])
            user_relation['id'] = uid
            user_relation['fans'] = fans
            user_relation['followers'] = []
            yield user_relation

            yield Request(self.fans_url.format(uid=uid,page=page), callback=self.fans_parse, meta={'uid':uid, 'page':page})
