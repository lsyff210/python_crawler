# -*- coding: utf-8 -*-
# python 2.7.11  scrapy 1.1.0  selenium 2.53.6

import scrapy
from lanren.items import LanrenItem


class LanrenimgSpider(scrapy.Spider):
    name = "lanrenimg"
    allowed_domains = ["lanrentuku.com"]
    start_urls = (
        'http://www.lanrentuku.com/tupian/beijingtupian/',
    )

    def parse(self, response):
        dl = response.xpath('//div[@class="list-pic"]/dl/dd/a')
        for a in dl:
            item = LanrenItem()
            item['title'] = a.xpath('./img/@alt').extract()[0]
            item['img_urls'] = a.xpath('./img/@src').extract()
            yield item