# coding: utf-8

START_LINK = 'http://kiev.all.biz/'
DOMAIN = 'kiev.all.biz'

COUNT_URLS = 10

TIMEOUT = 20

TREADS = 10

CHECK_OUTLINKS = False

IGNORE_LIST = [".ico", ".gif", ".png", ".jpg", ".jpeg", ".bmp", ".mp4",
               ".webm", ".apk", ".ogv", ".swf", ".svg", ".eot",
               ".ttf", ".woff", "javascript:", "data:",
               "@", ".zip", ".7z", ".rar", ".exe", ".pl", ".pdf",
               ".css", ".js"]

DATABASE = 'mongodb://localhost:27017/'

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
    u'a': u'//a//text()',
    u'b': u'//b//text()',
    u'i': u'//i//text()',
    u'strong': u'//strong//text()',
    u'li': u'//li//text()',
    u'alt': u'//img/@alt',
    u'title2': u'//@title'
    }
