# coding: utf-8
import random
import time
import logging
# import pdb
# pdb.set_trace()

from selenium import webdriver
from lxml import html
from pymongo import MongoClient
from reppy.cache import RobotsCache
from settings import ROBOTS_LINK, DATABASE, START_LINK, REGULARS, IGNORE_LIST, DOMAIN, AGENT, COUNT_URLS

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
    db_name = 'www_bg_all_biz'
    client = MongoClient(DATABASE)
    db = client[db_name]
    stop_flag = False
    logger.debug(u'Вызван класс Parser, закеширован robots и инициализировано соединение с базой')

    def __init__(self, url=START_LINK, database=True):
        self.url = url
        self.page = ''
        self.links = list()
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
                for url in random.sample(Parser.urls_old, 5):
                    self.url = url
                    self.open_url()
                    self.get_links()
            logger.debug(u'Парсер инициализирован значениями из базы')
        logger.debug(u'Создан инстанс класса Parser')

    @staticmethod
    def normalize(link):
        # Return normal link or False
        logger.debug(u'Нормализую ссылку: {}'.format(link))
        link = unicode(link).replace(u'\n', u'')
        if not link:
            return False
        for stop_word in IGNORE_LIST:
            if stop_word in link.lower():
                return False
        if link.startswith(u'#'):
            return False
        elif link.startswith(u'http'):
            return link
        elif link.startswith(DOMAIN):
            return u'http://' + link
        elif link.startswith(u'/') and DOMAIN not in link:
            return u'http://' + DOMAIN + link
        else:
            return False

    def set_elements(self):
        self.result[u'url'] = self.url
        self.result[u'load_time'] = self.page_load_time
        self.result[u'size'] = len(self.page)
        self.result[u'links'] = self.links
        self.result[u'in_links'] = self.in_links
        self.result[u'out_links'] = self.out_links
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
        self.result, self.page, self.url, self.page_load_time, self.links, self.robots, self.errors = \
            {}, '', '', 0, [], [], ''
        logger.debug(u'Сбрасываем параметры result, page, page_load_time, links, robots, errors')

    def open_url(self):
        time1 = time.time()
        try:
            browser = webdriver.PhantomJS()  # executable_path=r'C:\phantomjs\bin\phantomjs.exe'
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
        self.links = tree.xpath(u'//a//@href')
        self.in_links = list()
        self.out_links = list()
        for link in self.links:
            normal_link = Parser.normalize(link)
            if not normal_link:
                continue
            if DOMAIN in normal_link:
                if Parser.rules.allowed(normal_link, AGENT):
                    self.in_links.append(normal_link)
            else:
                self.out_links.append(normal_link)
        Parser.urls_new = Parser.urls_new | set(self.in_links)
        logger.debug(u'Нашел и обработал все ссылки на странице {}'.format(self.url))

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
                        print u'[{}] Отсканировал url {}'.format(Parser.count, self.url)
                        Parser.urls_old.add(self.url)
                        Parser.count += 1
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
