# -*- coding: utf-8 -*-
# python 2.7.11  scrapy 1.1.0  selenium 2.53.6

# 一个问题，为什么先执行MyImgPipeline，再执行process_item，process_item不会被执行完，整个程序就结束了
# 除了selenium，豆瓣电影的内容可以通过以下链接获得，比较原始网址和获取图片链接地址的区别
# 图片获取网址：https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0
# 原始链接：https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0



import scrapy
from scrapy import Selector
from douban.items import DoubanItem
from selenium import webdriver

driver = webdriver.Ie()


class DoubanMovieSpider(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["douban.com"]
    # start_urls = (
    #     'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0',
    # )

    def start_requests(self):
        item = DoubanItem()
        url = 'https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
        driver.get(url)
        source = str(driver.page_source.encode('utf-8'))
        with open('driver.html', 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
        sel = Selector(text=source)
        a_s = sel.xpath('//*[@id="gaia"]/div[4]/div/a')
        for a in a_s:
            movie_url = a.xpath('./@href').extract()[0]
            item['movie_url'] = movie_url
            yield scrapy.Request(url=item['movie_url'], meta={'item': item}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        item['desc'] = response.xpath('//*[@id="link-report"]/span[1]/text()').extract()[0]
        img_url = response.xpath('//*[@id="mainpic"]/a/img/@src').extract()
        item['img_url'] = img_url
        yield item











