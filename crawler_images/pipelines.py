# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient


class MongodbImagesPipeline(object):

    def __init__(self, server, port, db, collection):
        self.server = server
        self.port = port
        self.db = db
        self.col = collection
        client = MongoClient(self.server, self.port)
        db = client[self.db]
        self.collection = db[self.col]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        server = settings.get('MONGODB_SERVER', 'localhost')
        port = settings.get('MONGODB_PORT', 27017)
        db = settings.get('MONGODB_DB', 'wan')
        col = settings.get('MONGODB_COLLECTION', 'images')
        return cls(server, port, db, col)

    def process_item(self, item, spider):
        if item['image_urls'] and item['image_paths']:
            self.collection.insert(dict(item))
        return item


class WanImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('WanImagesItem contains no images.')
        item['image_paths'] = image_paths
        return item


