# coding: utf-8

import urllib2
import random
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
from pymongo import MongoClient

from settings import *


class Parser(object):

    urls_new = set()
    urls_old = set()
    
    count = 0

    client = MongoClient(DATABASE)
    db = client.prom_all
    stop_flag = False

    if urls_old:
        count = len(urls_old)
        old_rand_list = random.sample(urls_old, 10)
        parse_flag = True
    else:
        old_rand_list = []
        parse_flag = False

    def __init__(self, url=START_LINK, database=False):
        self.url = url
        self.driver = True
        self.page = ''
        self.result = dict()
        self.page_load_time = 0
        self.regulars = REGULARS
        Parser.urls_new.add(url)

        if database:
            for item in Parser.db.urls.find():
                Parser.urls_old.add(item['url'])

    @staticmethod
    def normalize(link):
        # Return normal link or False
        link = unicode(link)
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

    def get_elements(self):
        self.result[u'url'] = self.url
        self.result[u'load_time'] = self.page_load_time
        self.result[u'size'] = len(self.page)

        # Parse html page by XPath
        tree = html.fromstring(self.page)
        for page_element in self.regulars:
            self.result[page_element] = tree.xpath(self.regulars[page_element])

    def save(self):
        # Save result in Mongodb
        return Parser.db.urls.insert_one(self.result).inserted_id

    def open_url(self):
        time1 = time.time()
        if self.driver:
            driver = webdriver.Firefox()
            driver.get(self.url)
            elem = driver.find_element_by_xpath('//*')
            self.page = elem.get_attribute('outerHTML')
            driver.quit()
        else:
            self.page = unicode(urllib2.urlopen(self.url, timeout=TIMEOUT).read().decode('utf-8'))
        time2 = time.time()
        self.page_load_time = time2 - time1

    def get_html(self):
        try:
            self.open_url()
        except:
            self.result[u'error'] = u'Страница не загрузилась'

        soup = BeautifulSoup(self.page, 'lxml')
        for link in soup.find_all('a'):
            normal_link = Parser.normalize(link.get('href'))
            if not normal_link:
                continue
            if DOMAIN in normal_link:
                Parser.urls_new.add(normal_link)

    def parser(self):
        while Parser.urls_new:

            if Parser.old_rand_list:
                for url in Parser.old_rand_list:
                    Parser.get_html(url)
                Parser.old_rand_list = []
                Parser.parse_flag = False
                
            self.url = Parser.urls_new.pop()
            if self.url not in Parser.urls_old:
                Parser.count += 1
                print u'[{}] Сканирую url {}'.format(Parser.count, self.url)
                Parser.urls_old.add(self.url)
                self.get_html()
                self.save()
            if Parser.count == COUNT_URLS - TREADS + 1:
                Parser.stop_flag = True
            if Parser.stop_flag:
                break

if __name__ == '__main__':
    a = Parser()
    a.parser()
