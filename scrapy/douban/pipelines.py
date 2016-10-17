# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
import time


class DoubanPipeline(object):

    def process_item(self, item, spider):
        file_name1 = 'doubanmovie'
        file_name2 = item['img_url'][0].split('/')[-1].split('.')[0]
        file_name = file_name1 + '/' + file_name2
        if not os.path.exists(file_name):
            os.makedirs(file_name)

        desc_name = '%s/%s.txt' % (file_name, file_name2)
        with open(desc_name, 'wb') as f:
            _desc = item['desc'].encode('utf-8')
            _desc_title = item['title'].encode('utf-8')
            _url = item['img_url'][0].encode('utf-8')
            f.write(_desc_title + '\n' + _desc + '\n' + _url)
            f.close()
        return item



class MyImgPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for img_url in item['img_url']:
            yield scrapy.Request(img_url)

    def file_path(self, request, response=None, info=None):
        name = request.url.split('/')[-1]
        file_name2 = name.split('.')[0]
        return 'doubanmovie/%s/%s.jpg' % (file_name2, file_name2)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
