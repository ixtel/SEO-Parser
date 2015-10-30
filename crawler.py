# coding: utf-8

import random
import time

from selenium import webdriver
from lxml import html
from pymongo import MongoClient

from settings import *


class Parser(object):

    urls_new = set()
    urls_old = set()
    
    count = 0

    db_name = 'allbiz'
    client = MongoClient(DATABASE)
    db = client[db_name]
    stop_flag = False

    for item in db.urls.find():
        urls_old.add(item[u'url'])

    if urls_old:
        count = len(urls_old)
        old_rand_list = random.sample(urls_old, 3)
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
        link = unicode(link).replace('\n', '')
        if not link:
            return False
        for stop_word in IGNORE_LIST:
            if stop_word in link.lower():
                return False
        if link.startswith('http'):
            return link
        elif link.startswith(DOMAIN):
            return 'http://' + link
        elif link.startswith('/') and DOMAIN not in link:
            return 'http://' + DOMAIN + link
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

    def save(self):
        # Save result in Mongodb
        Parser.db.urls.insert_one(self.result)
        self.result, self.page, self.url, self.page_load_time, self.links = {}, '', '', 0, []

    def open_url(self):
        time1 = time.time()
        try:
            browser = webdriver.PhantomJS()  # executable_path=r'C:\phantomjs\bin\phantomjs.exe'
            browser.get(self.url)
            self.page = browser.page_source
            browser.quit()
        except KeyboardInterrupt:
            Parser.stop_flag = True
            print 'Stop parsing'
        except:
            self.errors = u'Страница не загрузилась'
            print 'Error'
        time2 = time.time()
        self.page_load_time = time2 - time1

    def get_links(self):
        tree = html.fromstring(self.page)
        self.links = tree.xpath(u'//a//@href')
        self.in_links = list()
        self.out_links = list()

        for link in self.links:
            normal_link = Parser.normalize(link)
            if not normal_link:
                continue
            if DOMAIN in normal_link:
                self.in_links.append(link)
                Parser.urls_new.add(normal_link)
            else:
                self.out_links.append(link)

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
                    Parser.count += 1
                    print u'[{}] Отсканировал url {}'.format(Parser.count, self.url)
                    Parser.urls_old.add(self.url)
                    self.get_links()
                    self.get_elements()
                    self.set_elements()
                    self.save()
            if Parser.count == COUNT_URLS:
                Parser.stop_flag = True
            if Parser.stop_flag:
                break

if __name__ == '__main__':
    a = Parser()
    print a.count
    a.parser()
