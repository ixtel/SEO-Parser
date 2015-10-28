# coding: utf-8
from pymongo import MongoClient

from settings import DATABASE
import analyzer
from crawler import Parser


URL = ['http://kiev.prom.ua/Markizy',
       'http://prom.ua/Gorizontalnaya-loktevaya-markiza.html',
       'http://www.ua.all.biz/markizy-bgg1068719',
       'http://kiev.all.biz/markizy-bgg1068719',
       'http://kiev.all.biz/markiza-gorizontalnaya-rivera-30002000mm-g8531599',
       'http://kiev.all.biz/navesy-kozyrki-markizy-markizy-predstavlyayut-g156353',
       'http://markizy.kiev.ua/']

# url = URL[0]


def main(url, database=False):

    if not database:
        p = Parser(url)
        p.driver = False
        p.get_html()
        p.get_elements()
        t = analyzer.TextAnalyzer(p.result)
        print u'Url: {} | Загружен за: {} сек'.format(p.result[u'url'], p.result[u'load_time'])
    else:
        client = MongoClient(DATABASE)
        db = client.prom_all
        result = db.urls.find({'url': url})
        result = result[0]
        t = analyzer.TextAnalyzer(result)
        print u'Url: {} | Загружен за: {} сек'.format(result[u'url'], result[u'load_time'])

    '''
    for x in t.__dict__:
        if x != 'page':
            if type(t.__dict__[x]) is dict:
                for y in t.__dict__[x]:
                    print y, t.__dict__[x][y]
            elif type(t.__dict__[x]) is list:
                print x, ' '.join(t.__dict__[x])
            else:
                print x, t.__dict__[x]
    '''

    t.title()
    t.description()
    t.keywords()
    t.canonical()
    t.h1()
    t.h2()
    t.h3()
    t.text()
    t.anchors()

    '''
    print u'H1: {}'.format(t.h1_)
    print u'Title: {}'.format(t.title_)
    print u'KeyWords:'
    for key in t.keys:
        print key, t.keys[key]
    '''
    print u'KeyWords: {}'.format(t.keys.keys())
    print u'Всего баллов {}'.format(str(t.ball))

if __name__ == '__main__':
    for url in URL:
        main(url, False)
