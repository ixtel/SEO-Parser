# coding: utf-8
import time
import random
from selenium import webdriver
from lxml import html

from settings import Settings
from reppy.meta import check_meta_robots
# import pdb
# pdb.set_trace()

import logging
FORMAT = '%(levelname)s : %(asctime)s : %(funcName)s : %(lineno)d : %(message)s'
logging.basicConfig(format=FORMAT, filename='pars.log')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from threading import Lock
l = Lock()

# from multiprocessing import Manager
# manager = Manager()


class Parser(object):
    """
    Парсер сайтов. Внутри парсера реализованы меторы:
    open_url - открывает страницу любого сайта, работает через selenium + phantomjs
    get_links - обрабатывает полученную страницу, и собирает с нее все ссылки, ставит в очередь на сканирование
    get_elements - получает значения со страницы по XPATH выражениям из self.regulars
    set_elements - дополняет результат информацией о странице и ссылками
    clean - очищает переменные от значений прошлой страницы
    save - сохраняет словать результата (self.result) в базу данных из Parser.settings.db (Mongodb)
    parser - сканирование страниц поочередно из очереди, обход парсера по всему сайту
    install - устанавливает парсер в начальную точку, для многопоточности
    set_from_db - устанавливает парсер существующими значениями из базы для продолжения сканирования

    Переменные:
    urls_new - список очереди адресов на сканирование
    urls_old - список отсканированных адресов, страницы которые тут есть не будут отсканированы
    errors - список страниц которые не удалось отсканировать, в дальнейшем может быть просканирован дополнительно
    count - количество успешно просканированных адресов
    stop_flag - если True - прекращает сканирование
    IGNORE_LIST - если любой из элементов этого списка есть в url - он не будет добавлен в очередь сканирования
    """

    IGNORE_LIST = [".ico", ".gif", ".png", ".jpg", ".jpeg", ".bmp", ".mp4",
                   ".webm", ".apk", ".ogv", ".swf", ".svg", ".eot",
                   ".ttf", ".woff", "javascript:", "data:",
                   "@", ".zip", ".7z", ".rar", ".exe", ".pl", ".pdf", ".css", ".js"]

    settings = Settings()
    urls_new = list()
    urls_old = list()
    errors = list()
    count = 0
    stop_flag = False
    logger.debug(u'Вызван класс Parser, закеширован robots и инициализировано соединение с базой')

    def __init__(self):
        if Parser.count == 0:
            self.url = Parser.settings.START_LINK
        self.js_files, self.in_links, self.out_links, self.links, self.robots = [], [], [], [], []
        self.page, self.errors, self.result, self.page_load_time = '', '', {}, 0
        self.domain = Parser.settings.DOMAIN
        self.regulars = Parser.settings.REGULARS
        logger.debug(u'Создан инстанс класса Parser')

    def install(self, url):
        print Parser.settings.__dict__
        self.url = url
        self.open_url()
        self.get_links()
        Parser.urls_new.append(self.url)

    def set_from_db(self):
        for item in Parser.settings.db.urls.find():
            Parser.urls_old.append(item[u'url'])
        if Parser.urls_old:
            Parser.count = len(Parser.urls_old)
            for url in random.sample(Parser.urls_old, Parser.settings.RAND_NUM):
                self.url = url
                self.open_url()
                self.get_links()
            logger.debug(u'Парсер инициализирован значениями из базы')

    @staticmethod
    def find_stop(link):
        for stop_word in Parser.IGNORE_LIST:
            if stop_word in link.lower():
                return False
        return link

    def set_elements(self):
        self.result[u'url'] = self.url
        self.result[u'load_time'] = self.page_load_time
        self.result[u'size'] = len(self.page)
        self.result[u'js_files'] = self.js_files
        self.result[u'in_links'] = self.in_links
        self.result[u'out_links'] = self.out_links
        self.result[u'links'] = self.links
        logger.debug(u'Установил url, load_time, size, links, in_links, out_links для {}'.format(self.url))

    def get_elements(self):
        if not self.errors:
            # Parse html page by XPath
            tree = html.fromstring(self.page)
            for page_element in self.regulars:
                self.result[page_element] = tree.xpath(self.regulars[page_element])
            logger.debug(u'Спарсил элементы и записал в словарь result')
        else:
            self.result[u'error'] = self.errors
            self.result[u'robots'] = [u'index, follow']
            logger.warning(u'Не спарсил элементы так как пришел Error')

    def save(self):
        # Save result in Mongodb
        l.acquire()
        Parser.settings.db.urls.insert_one(self.result)
        l.release()
        logger.debug(u'Сохраняю результат в базу данных')

    def clean(self):
        self.result, self.page, self.url, self.page_load_time, self.robots, self.errors = \
            {}, '', '', 0, [], ''
        logger.debug(u'Сбрасываем параметры result, page, page_load_time, links, robots, errors')

    def open_url(self):
        try:
            browser = webdriver.PhantomJS()
            browser.set_page_load_timeout(Parser.settings.TIMEOUT)
            time1 = time.time()
            browser.get(self.url)
            time2 = time.time()
            self.page = browser.page_source.encode('utf-8')
            browser.quit()
            self.page_load_time = time2 - time1
            logger.debug(u'Url открыт успешно')
        except Exception, e:
            self.errors = 'Error'
            self.page = ''
            print u'[Error] Страница {} не загрузилась'.format(self.url)
            logger.error(u'Страница не загрузилась {}'.format(self.url))
            logger.error(e, exc_info=True)

    def get_links(self):
        tree = html.fromstring(self.page)
        tree.make_links_absolute(self.url)
        self.links, self.in_links, self.out_links, self.js_files = [], [], [], []
        for link in tree.iterlinks():
            if not link[2]:
                continue
            if link[1] == 'href':
                if Parser.find_stop(link[2]):
                    if self.domain in link[2]:
                        if Parser.settings.rules.allowed(link[2], Parser.settings.AGENT):
                            self.in_links.append(link[2])
                    else:
                        self.out_links.append(link[2])
                    self.links.append({'link': link[2], 'code': html.tostring(link[0], encoding='utf-8')})
            elif link[1] == 'src' and '.js' in link[2]:
                self.js_files.append(link[2])
        with l:
            for url in self.in_links:
                if url not in Parser.urls_new:
                    Parser.urls_new.append(url)
        logger.debug(u'Обработал все ссылки на странице {}'.format(self.url))

    def parser(self):
        while Parser.urls_new:
            with l:
                self.url = Parser.urls_new.pop()
            if self.url not in Parser.urls_old:
                with l:
                    Parser.urls_old.append(self.url)
                self.open_url()
                if self.page:
                    self.get_elements()
                    if check_meta_robots(self.page)[1]:
                        self.get_links()
                    if check_meta_robots(self.page)[0]:
                        self.set_elements()
                        self.save()
                        with l:
                            Parser.count += 1
                        print u'[{}] Отсканировал и сохранил url {}'.format(Parser.count, self.url)
                        logger.debug(u'[{}] Отсканировал и сохранил url {}'.format(Parser.count, self.url))
                else:
                    with l:
                        Parser.errors.append(self.url)
                    logger.debug(u'При открытии url: {} произошла ошибка'.format(self.url))
                self.clean()
            else:
                logger.debug(u'url: {} уже был отсканирован ранее'.format(self.url))
            if Parser.stop_flag:
                logger.debug(u'Работа парсера завершена url: {}'.format(self.url))
                break
        print u'Поток отсканировал {}'.format(len(Parser.urls_old))

    def scan_errors(self, num=5):
        for _ in range(num):
            if Parser.errors:
                logger.debug(u'Запушена обработка ошибок')
                with l:
                    Parser.urls_new = Parser.errors
                    for url in Parser.errors:
                        Parser.urls_old.remove(url)
                        logger.debug(u'Будет отсканирован снова: {}'.format(url))
                    Parser.errors = []
                    Parser.stop_flag = False
                self.parser()
                with l:
                    Parser.stop_flag = True


if __name__ == '__main__':
    par = Parser()
    par.open_url()
    par.get_links()
    par.get_elements()
    print par.result
    print "All Done"
