# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class CcrentiPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['url'], meta={'name': item['name']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        folder = request.meta['name']
        folder_strip = self.remove_invalid_char(folder)
        # <img src="http://tu.44mvz.com/uploads/img143/img63185021059124.jpg" data-bd-imgshare-binded="1">
        img_name = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, img_name)
        return filename

    def remove_invalid_char(self, path):
        # 把非法字符删掉
        return re.sub(r'[？\\*|“<>:/]', '', str(path)).strip()
