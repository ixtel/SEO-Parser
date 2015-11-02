# coding: utf-8

START_LINK = 'http://www.bg.all.biz/'
DOMAIN = 'www.bg.all.biz'
ROBOTS_LINK = 'http://www.bg.all.biz/robots.txt'

COUNT_URLS = 200000

RAND_NUM = 5

TIMEOUT = 20

AGENT = ''

IGNORE_LIST = [".ico", ".gif", ".png", ".jpg", ".jpeg", ".bmp", ".mp4",
               ".webm", ".apk", ".ogv", ".swf", ".svg", ".eot",
               ".ttf", ".woff", "javascript:", "data:",
               "@", ".zip", ".7z", ".rar", ".exe", ".pl", ".pdf",
               ".css", ".js"]

IMAGE_LIST = [".ico", ".gif", ".png", ".jpg", ".jpeg", ".bmp", ".mp4",
               ".webm", ".apk", ".ogv", ".swf", ".svg", ".eot",
               ".ttf", ".woff", "javascript:", "data:",
               "@", ".zip", ".7z", ".rar", ".exe", ".pl", ".pdf",
               ".css", ".js"]

DATABASE = 'mongodb://localhost:27017/'
DB_NAME = 'www_bg_all_biz'

REGULARS = {
    u'title': u'//title/text()',
    u'description': u'//meta[@name="description"]/@content',
    u'keywords': u'//meta[@name="keywords"]/@content',
    u'robots': u'//meta[@name="robots"]/@content',
    u'canonical': u'//link[@rel="canonical"]/@href',
    u'h1': u'//h1//text()',
    u'h2': u'//h2//text()',
    u'h3': u'//h3//text()',
    u'h4': u'//h4//text()',
    u'h5': u'//h5//text()',
    u'h6': u'//h6//text()',
    u'text': u'//body//*[not(self::script or self::a)]/text()[normalize-space()]',  # or self::a
    u'script': u'//script//text()',
    u'span': u'//span//text()',
    u'samp': u'//samp//text()',
    u'p': u'//p//text()',
    u'anchors': u'//a//text()',
    u'b': u'//b//text()',
    u'i': u'//i//text()',
    u'strong': u'//strong//text()',
    u'li': u'//li//text()',
    u'alt': u'//img/@alt',
    u'title2': u'//@title'
    }
