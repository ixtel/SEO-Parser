# coding: utf-8
from pymongo import MongoClient

from settings import DATABASE
import analyzer
from crawler import Parser


URL = [u'http://kiev.prom.ua/Markizy',
       u'http://prom.ua/Gorizontalnaya-loktevaya-markiza.html',
       u'http://www.ua.all.biz/markizy-bgg1068719',
       'http://kiev.all.biz/markizy-bgg1068719',
       'http://kiev.all.biz/markiza-gorizontalnaya-rivera-30002000mm-g8531599',
       'http://kiev.all.biz/navesy-kozyrki-markizy-markizy-predstavlyayut-g156353',
       'http://markizy.kiev.ua/']

URL2 = ['http://markiza.of.ua/works/corob/',
        'http://kievjaluzi.kiev.ua/markizy-navesy/kovshevye-korobovye',
        'http://markiza.kh.ua/%D0%BA%D0%BE%D0%B2%D1%88%D0%BE%D0%B2%D1%8B%D0%B5-%D0%BA%D0%BE%D1%80%D0%BE%D0%B1%D0%BE%D0%B2%D1%8B%D0%B5-%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D0%B7%D1%8B/',
        'http://skr.com.ua/korobovaya',
        'http://www.artika.lviv.ua/ru/kataloh-tovarivrus/zovnishnirus/markizyrus/kovshovi-markizyrus/',
        'http://markiza-guru.com/component/k2/itemlist/category/7-kovshevye-markizy',
        'http://www.sundesign.com.ua/markizy/korobovaya-markiza/',
        'http://markizy.kiev.ua/korobovye-markizy',
        'http://www.markiza.com.ua/korobovie/',
        'http://www.markiza.ua/catalog/box/',
        'http://www.markiza.ua/catalog/box/14/photos/',
        'http://www.markiza.ua/catalog/box/14/',
        'http://marsol.com.ua/gorizontalnie_markizi.html',
        'http://markiza.ot.ua/korobovye_markizy',
        'http://vdoma-crimea.com/p4191990-markiza-korobovaya-kowsh.html']

# url = URL[0]


def main(url, database=False):

    if not database:
        p = Parser(url)
        p.driver = True
        p.open_url()
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
    t.load_time()
    t.size()
    t.script()

    '''
    print u'H1: {}'.format(t.h1_)
    print u'Title: {}'.format(t.title_)
    print u'KeyWords:'
    for key in t.keys:
        print key, t.keys[key]
    '''
    print u'KeyWords: {}'.format(u' '.join(sorted(t.keys)))
    print '#'*50
    print u'Всего баллов {}'.format(str(t.ball))
    print '#'*50

    # client = MongoClient(DATABASE)
    # db = client.prom_all
    # db.result.insert_one(t.__dict__)

if __name__ == '__main__':
    for url in URL:
        main(url, False)
