# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request

from ccrenti.items import CcrentiItem


class RentiSpider(scrapy.Spider):
    name = 'renti'
    allowed_domains = ['ccrenti.net']
    start_urls = ['http://www.ccrenti.net/xxrt/sy/',
					'http://www.ccrenti.net/xxrt/xz/',
					'http://www.ccrenti.net/xxrt/zp/',
					'http://www.ccrenti.net/xxrt/rb/',
					'http://www.ccrenti.net/xxrt/ddrtys/']

    def parse(self, response):
        for href, name in zip(response.xpath(r'//div[@class="list_pic"]/ul//a/@href').extract(),
                              response.xpath(r'//div[@class="list_pic"]/ul//a/@title').extract()):
            yield Request(response.urljoin(href), callback=self.parse_img, meta={'name': name})

        if response.url.endswith('/'):
            # <a href="list_1_15.html">末页</a>
            last_page_url = response.xpath(r'//div[@class="pages"]/a[last()]/@href').extract_first()
            max_page = int(last_page_url.split('_')[-1].split('.')[0])
            for index in range(2, max_page+1):
                # http://www.ccrenti.net/xxrt/sy/list_1_6.html
                url = last_page_url[:last_page_url.rindex('_') + 1] + str(index) + '.html'
                yield Request(response.urljoin(url), callback=self.parse)

    def parse_img(self, response):
        for url in response.xpath(r'//div[@class="main"]/div[3]//img/@src').extract():
            item = CcrentiItem()
            item['name'] = response.meta['name']
            item['url'] = url
            yield item

        if response.url.find('_') == -1:
            try:
                max_page = int(response.xpath(r'//div[@class="main"]/div/a[last()-1]/text()').extract_first())
            except:
                # 有些图集只有一张图片
                pass
            else:
                for index in range(2, max_page):
                    # http://www.ccrenti.net/xxrt/sy/20180525/2051_2.html
                    url = response.url[:response.url.rindex('.')] + '_' + str(index) + '.html'
                    yield Request(url, callback=self.parse_img, meta={'name': response.meta['name']})