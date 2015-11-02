# coding: utf-8
import random
import time
import logging

from selenium import webdriver
from lxml import html
from pymongo import MongoClient
from reppy.cache import RobotsCache
from settings import ROBOTS_LINK, DATABASE, START_LINK, REGULARS, IGNORE_LIST, \
    DOMAIN, AGENT, COUNT_URLS, RAND_NUM, DB_NAME

# import pdb
# pdb.set_trace()

FORMAT = '%(levelname)s : %(asctime)s : %(funcName)s : %(lineno)d : %(message)s'
logging.basicConfig(format=FORMAT, filename='parser.log')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Parser(object):

    urls_new = set()
    urls_old = set()
    count = 0
    robots = RobotsCache()
    rules = robots.cache(ROBOTS_LINK)
    client = MongoClient(DATABASE)
    db = client[DB_NAME]
    stop_flag = False
    logger.debug(u'Вызван класс Parser, закеширован robots и инициализировано соединение с базой')

    def __init__(self, url=START_LINK, database=True):
        self.url = url
        self.domain = url.split('/')[2]
        self.page = ''
        self.js_files = list()
        self.in_links = list()
        self.out_links = list()
        self.result = dict()
        self.page_load_time = 0
        self.errors = ''
        self.regulars = REGULARS
        Parser.urls_new.add(url)
        if database:
            for item in Parser.db.urls.find():
                Parser.urls_old.add(item[u'url'])
            if Parser.urls_old:
                Parser.count = len(Parser.urls_old)
                for url in random.sample(Parser.urls_old, RAND_NUM):
                    self.url = url
                    self.open_url()
                    self.get_links()
            logger.debug(u'Парсер инициализирован значениями из базы')
        logger.debug(u'Создан инстанс класса Parser')

    @staticmethod
    def find_stop(link):
        for stop_word in IGNORE_LIST:
            if stop_word in link.lower():
                logger.debug(u'Ссылка не прошла стоп лист: {}'.format(link))
                return False
        logger.debug(u'Ссылка в порядке: {}'.format(link))
        return link

    def set_elements(self):
        self.result[u'url'] = self.url
        self.result[u'load_time'] = self.page_load_time
        self.result[u'size'] = len(self.page)
        self.result[u'js_files'] = self.js_files
        self.result[u'in_links'] = self.in_links
        self.result[u'out_links'] = self.out_links
        self.result[u'a'] = self.in_links + self.out_links
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

    @staticmethod
    def check_meta_robots(robots):
        if not robots:
            return True, True
        robots = robots[0].split(u',')  # list --> srt --> list
        if len(robots) == 2:
            index = robots[0].strip()
            follow = robots[1].strip()
        elif len(robots) == 1:
            index = robots[0].strip()
            follow = True
        else:
            return True, True
        logger.debug(u'Meta robots: {}, {}'.format(index, follow))
        if index == u'none':
            index, follow = False, False
        if index == u'all':
            index, follow = True, True
        if index == u'noindex':
            index = False
        if index == u'index':
            index = True
        if follow == u'nofollow':
            follow = False
        if follow == u'follow':
            follow = True
        if type(index) != bool:
            index = True
        if type(follow) != bool:
            follow = True
        logger.debug(u'Meta robots: {}, {}'.format(index, follow))
        return index, follow

    def save(self):
        # Save result in Mongodb
        Parser.db.urls.insert_one(self.result)
        logger.debug(u'Сохраняю результат в базу данных')

    def clean(self):
        self.result, self.page, self.url, self.page_load_time, self.robots, self.errors = \
            {}, '', '', [], [], ''
        logger.debug(u'Сбрасываем параметры result, page, page_load_time, links, robots, errors')

    def open_url(self):
        time1 = time.time()
        try:
            browser = webdriver.PhantomJS(executable_path=r'C:\phantomjs\bin\phantomjs.exe')
            # PhantomJS executable_path=r'C:\phantomjs\bin\phantomjs.exe'
            browser.set_page_load_timeout(20)
            browser.get(self.url)
            self.page = browser.page_source
            browser.quit()
            logger.debug(u'Url открыт успешно')
        except KeyboardInterrupt:
            Parser.stop_flag = True
            print u'Сканирование отменено:'
            print u'Успел отсканировать: {}'.format(len(Parser.urls_old))
            print u'Осталось в очереди на сканирование: {}'.format(len(Parser.urls_new))
            logger.debug(u'Работа парсера прервана пользователем')
        except Exception, e:
            self.errors = u'Страница не загрузилась'
            self.page = ''
            print 'Error'
            logger.error(u'Возникла ошибка при открытии страницы {}'.format(self.url))
            logger.error(e, exc_info=True)
        time2 = time.time()
        self.page_load_time = time2 - time1

    def get_links(self):
        if not self.page:
            return
        tree = html.fromstring(self.page)
        tree.make_links_absolute(self.url)
        self.in_links = list()
        self.out_links = list()
        self.js_files = list()
        for link in tree.iterlinks():
            if not link[2]:
                continue
            if link[1] == 'href':
                if Parser.find_stop(link[2]):
                    if self.domain in link[2]:
                        if Parser.rules.allowed(link[2], AGENT):
                            self.in_links.append(link[2])
                    if self.domain not in link[2]:
                        self.out_links.append(link[2])
            elif link[1] == 'src' and '.js' in link[2]:
                self.js_files.append(link[2])
        Parser.urls_new = Parser.urls_new | set(self.in_links)
        logger.debug(u'Обработал все ссылки на странице {}'.format(self.url))

    def parser(self):
        while Parser.urls_new:
            self.url = Parser.urls_new.pop()
            if self.url not in Parser.urls_old:
                self.open_url()
                if self.page:
                    self.get_elements()
                    if Parser.check_meta_robots(self.result[u'robots'])[1]:
                        self.get_links()
                    if Parser.check_meta_robots(self.result[u'robots'])[0]:
                        self.set_elements()
                        self.save()
                        Parser.urls_old.add(self.url)
                        Parser.count += 1
                        print u'[{}] Отсканировал url {}'.format(Parser.count, self.url)
                        logger.debug(u'Проиндексировал url: {}'.format(self.url))
                self.clean()
            if Parser.count == COUNT_URLS:
                Parser.stop_flag = True
            if Parser.stop_flag:
                break
            logger.debug(u'Обработал url: {}'.format(self.url))


if __name__ == '__main__':
    a = Parser()
    print a.count
    a.parser()
