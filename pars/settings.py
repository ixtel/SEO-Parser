# coding: utf-8
from pymongo import MongoClient
from reppy.cache import RobotsCache


class Settings(object):
    START_LINK = 'http://example.com/'

    def __init__(self):
        self.DOMAIN = Settings.START_LINK.split('/')[2]
        self.ROBOTS_LINK = Settings.START_LINK + 'robots.txt'
        self.COUNT_URLS = 200000
        self.THREADS = 4
        self.RAND_NUM = 5
        self.TIMEOUT = 30
        self.AGENT = ''
        self.DATABASE = 'mongodb://localhost:27017/'
        self.DB_NAME = self.DOMAIN.replace('.', '_')
        self.REGULARS = {
            u'title': u'//title/text()',
            u'description': u'//meta[@name="description"]/@content',
            u'keywords': u'//meta[@name="keywords"]/@content',
            u'robots': u'//meta[@name="robots"]/@content',
            u'canonical': u'//link[@rel="canonical"]/@href',
            u'h1': u'//h1//text()',
            u'h2': u'//h2//text()',
            u'h3': u'//h3//text()',
            u'text': u'''//body//*[not(self::script or self::a or self::h1 or
            self::h2 or self::h3)]/text()[normalize-space()]''',
            u'script': u'//script//text()',
            u'p': u'//p//text()',
            u'anchors': u'//a//text()',
            u'alt': u'//img/@alt',
            u'title2': u'//@title'
            }
        self.robots = RobotsCache()
        self.rules = self.robots.cache(self.ROBOTS_LINK)
        self.client = MongoClient(self.DATABASE)
        self.db = self.client[self.DB_NAME]