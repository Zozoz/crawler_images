# -*- coding: utf-8 -*-

import os

BOT_NAME = 'crawler_images'

SPIDER_MODULES = ['crawler_images.spiders']
NEWSPIDER_MODULE = 'crawler_images.spiders'

DOWNLOAD_DELAY = 0
COOKIES_ENABLED = False

ITEM_PIPELINES = {
        'crawler_images.pipelines.WanImagesPipeline': 600,
        'crawler_images.pipelines.MongodbImagesPipeline': 700,
        }

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'crawler_images.rotate_useragent.RotateUserAgentMiddleware': 400,
        }

IMAGES_STORE = os.path.join(os.getcwd(), 'image')
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
        'small': (50, 50),
        'big': (500, 500),
        }
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'wan'
MONGODB_COLLECTION = 'images'

