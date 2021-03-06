# coding: utf-8
import threading
import logging
logger = logging.getLogger()

from pars.crawler import Parser
from pars.settings import Settings

Settings.START_LINK = 'http://kharkov.all.biz/'
se = Settings()
se.THREADS = 10
se.TIMEOUT = 40
Parser.settings = se
i = ['#', ';', '/pl/', '/de/', '/es/', '/zh/', '/ro/', '/fr/', '/cs/', '/lv/', '/pt/', '/it/', '/ar/', '/fa/',
     '/hu/', '/bg/', '/ja/', '/ko/', '/nl/', '/vi/', '/el/', '/he/', '/no/', '/fi/', '/sv/', '/en/', '/uk/', '/tr/',
     '/ru/', '.php']
Parser.IGNORE_LIST.extend(i)


def worker():
    p = Parser()
    p.install(se.START_LINK)
    print u"Инициализирован парсер"

    th = list()
    for _ in range(Parser.settings.THREADS):
        p = Parser()
        t = threading.Thread(target=p.parser)
        t.start()
        th.append(t)

    while True:
        print u"Чтобы остановить парсинг введите - S (Stop)\n"
        ex = raw_input()
        if ex.lower() == 's':
            Parser.stop_flag = True
            break

    for t in th:
        t.join()

    with open('urls_new.txt', 'w') as f:
        for u in Parser.urls_new:
            f.write(u + '\n')
    print u'***Неотсканированные урлы записаны в файл***'

    p.scan_errors()

    print u'*******Сканирование прекращено*******'
    print u'Успел отсканировать: {}'.format(len(Parser.urls_old))
    print u'Осталось в очереди на сканирование: {}'.format(len(Parser.urls_new))
    print u'*******Ошибок всего: {}*******'.format(len(Parser.errors))


def do_index():
    pass

if __name__ == '__main__':
    worker()
