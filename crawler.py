# coding: utf-8

import random
import time

from selenium import webdriver
from lxml import html
from pymongo import MongoClient
from reppy.cache import RobotsCache
from settings import *


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

    for item in db.urls.find():
        urls_old.add(item[u'url'])

    if urls_old:
        count = len(urls_old)
        if COUNT_URLS < 10:
            old_rand_list = urls_old
        else:
            old_rand_list = random.sample(urls_old, 10)
    else:
        old_rand_list = list()

    def __init__(self, url=START_LINK):
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

    @staticmethod
    def normalize(link):
        # Return normal link or False
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

    def get_elements(self):
        if not self.errors:
            # Parse html page by XPath
            tree = html.fromstring(self.page)
            for page_element in self.regulars:
                self.result[page_element] = tree.xpath(self.regulars[page_element])
        else:
            self.result[u'error'] = self.errors
            self.result[u'robots'] = [u'index, follow']

    @staticmethod
    def meta_robots(robots):
        if not robots:
            return True, True
        index = robots[0].split(u',')[0].strip()
        follow = robots[0].split(u',')[1].strip()
        if index is u'none':
            index, follow = False, False
        elif index is u"all":
            index, follow = True, True
        elif index is u"noindex":
            index = False
        elif index is u"index":
            index = True
        elif follow is u"nofollow":
            follow = False
        elif follow is u"follow":
            follow = True
        else:
            index, follow = False, False
        return index, follow

    def save(self):
        # Save result in Mongodb
        Parser.db.urls.insert_one(self.result)

    def clean(self):
        self.result, self.page, self.url, self.page_load_time, self.links, self.robots = {}, '', '', 0, [], []

    def open_url(self):
        time1 = time.time()
        try:
            browser = webdriver.PhantomJS()  # executable_path=r'C:\phantomjs\bin\phantomjs.exe'
            browser.set_page_load_timeout(20)
            browser.get(self.url)
            self.page = browser.page_source
            browser.quit()
        except KeyboardInterrupt:
            Parser.stop_flag = True
            print u'Сканирование отменено:'
            print u'Успел отсканировать: {}'.format(len(Parser.urls_old))
            print u'Осталось в очереди на сканирование: {}'.format(len(Parser.urls_new))
        except:
            self.errors = u'Страница не загрузилась'
            print 'Error'
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
        if CHECK_OUTLINKS:
            Parser.urls_new = Parser.urls_new | set(self.out_links)

    def parser(self):
        while Parser.urls_new:

            if Parser.old_rand_list:
                for url in Parser.old_rand_list:
                    self.url = url
                    self.open_url()
                    self.get_links()
                Parser.old_rand_list = list()

            self.url = Parser.urls_new.pop()
            if self.url not in Parser.urls_old:
                self.open_url()
                if self.page:
                    self.get_elements()
                    if Parser.meta_robots(self.result[u'robots'])[1]:
                        self.get_links()
                    if Parser.meta_robots(self.result[u'robots'])[0]:
                        self.set_elements()
                        self.save()
                        print u'[{}] Отсканировал url {}'.format(Parser.count, self.url)
                        Parser.urls_old.add(self.url)
                        Parser.count += 1
                    self.clean()
            if Parser.count == COUNT_URLS:
                Parser.stop_flag = True
            if Parser.stop_flag:
                break

if __name__ == '__main__':
    a = Parser()
    print a.count
    a.parser()
