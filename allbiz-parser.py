# coding: utf-8
import threading
import random
import logging
logger = logging.getLogger()

from pars.crawler import Parser
from pars.settings import Settings

Settings.START_LINK = 'http://skirest.com/'
se = Settings()
se.THREADS = 10
se.TIMEOUT = 40
Parser.settings = se
i = ['#', '?p=', '/feed/', '.php']
Parser.IGNORE_LIST.extend(i)


class ParserAllbis (Parser):
    def __init__(self, database=True):
        super(ParserAllbis, self).__init__()

        if database:
            for item in Parser.settings.db.urls.find():
                Parser.urls_old.append(item[u'url'])
            if Parser.urls_old:
                Parser.d['count'] = len(Parser.urls_old)
                for url in random.sample(Parser.urls_old, Parser.settings.RAND_NUM):
                    self.url = url
                    self.open_url()
                    self.get_links()
                logger.debug(u'Парсер инициализирован значениями из базы')
            else:
                self.url = Parser.settings.START_LINK
                self.open_url()
                self.get_links()
                Parser.urls_new.append(self.url)


class Worker(object):

    def __init__(self):
        ParserAllbis(database=True)
        print u"Инициализирован парсер"

        th = list()

        for _ in range(Parser.settings.THREADS):
            p = ParserAllbis(database=False)
            t = threading.Thread(target=p.parser)
            t.start()
            th.append(t)

        while True:
            print u"Чтобы остановить парсинг введите - S (Stop)\n"
            ex = raw_input()
            if ex.lower() == 's':
                Parser.d['stop_flag'] = True
                break

        for t in th:
            t.join()

        print u'*******Сканирование прекращено*******'
        print u'Успел отсканировать: {}'.format(len(ParserAllbis.urls_old))
        print u'Осталось в очереди на сканирование: {}'.format(len(ParserAllbis.urls_new))
        print u'*******Ошибок всего: {}*******'.format(len(Parser.errors))
        print Parser.errors

        Parser.urls_new = Parser.errors
        Parser.d['stop_flag'] = False
        for url in Parser.errors:
            Parser.urls_old.remove(url)

        p = ParserAllbis(database=False)
        p.parser()

if __name__ == '__main__':
    Worker()
