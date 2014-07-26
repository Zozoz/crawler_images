#!/usr/bin/env python
# encoding: utf-8
# Author: zozoz

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from crawler_images.items import WanImagesItem

class WanSpider(Spider):
    name = "wan"
    allowed_domains = ["92wan.org"]
    start_urls = [
            "http://www.92wan.org/meitui",
            "http://www.92wan.org/xinggan",
            "http://www.92wan.org/rbmm",
            "http://www.92wan.org/xrtt",
            "http://www.92wan.org/jiepaimeinv",
            "http://www.92wan.org/meitu",
            ]
    base_url = "http://www.92wan.org"

    def parse(self, response):
        first_page_rep = response.xpath('//div[@class="pages"]/a/@href').extract()
        for a in first_page_rep:
            if a:
                tt = response.url.split('/')
                length = len(tt)
                if length == 5 and tt[-1] == '':
                    next_url = response.url + a
                    yield Request(url=next_url, callback=self.parse)
                elif length == 4:
                    next_url = response.url + '/' + a
                    yield Request(url=next_url, callback=self.parse)

        first_page_rep = response.xpath('//ul[@id="need"]/li')
        item = WanImagesItem()
        for li in first_page_rep:
            next_url = self.base_url + li.xpath('./a/@href').extract()[0]
            yield Request(url=next_url, callback=self.parse)

        download_page_rep = response.xpath('//div[@class="fengmian"]/img/@src').extract()
        if download_page_rep:
            image_url = self.base_url + download_page_rep[0].replace("-lp", "")
            item['image_urls'] = [image_url]
            yield item

        next_download_page_rep = response.xpath('//div[@class="pic_list"]')
        for page in next_download_page_rep:
            next_url = page.xpath('.//a/@href').extract()[1]
            tt = response.url.split('/')
            tt[-1] = next_url
            next_url = '/'.join(tt)
            yield Request(url=next_url, callback=self.parse)

            image_url = page.xpath('.//img/@src').extract()[0]
            image_url = self.base_url + image_url
            item['image_urls'] = [image_url]
            yield item



