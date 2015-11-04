# coding: utf-8
from analyzer import TextAnalyzer
from crawler import Parser


URL = [u'http://kiev.prom.ua/Markizy',
       u'http://prom.ua/Gorizontalnaya-loktevaya-markiza.html',
       u'http://www.ua.all.biz/markizy-bgg1068719',
       u'http://kiev.all.biz/markizy-bgg1068719',
       u'http://kiev.all.biz/markiza-gorizontalnaya-rivera-30002000mm-g8531599',
       u'http://kiev.all.biz/navesy-kozyrki-markizy-markizy-predstavlyayut-g156353',
       u'http://markizy.kiev.ua/']


class Worker(Parser, TextAnalyzer):

    def __init__(self, url, database=False, *args, **kwargs):
        super(Worker, self).__init__(url, database, *args, **kwargs)

    def work(self):
        self.open_url()
        self.get_elements()
        self.set_elements()
        print u'Url: {} | Загружен за: {} сек'.format(self.result[u'url'], self.result[u'load_time'])

        super(Parser, self).__init__(self.result)

        self.title()
        self.description()
        self.keywords()
        self.canonical()
        self.h1()
        self.h2()
        self.h3()
        self.text()
        self.anchors()
        self.load_time()
        self.size()
        self.script()
        self.js_files()
        self.in_links()
        self.out_links()

        print u'KeyWords: {}'.format(u' '.join(sorted(self.text_top5)))
        print '#'*50
        print u'Всего баллов {}'.format(str(self.ball))
        print '#'*50

if __name__ == '__main__':
    for url in URL:
        Worker(url, False).work()
