# coding: utf-8
import analyzer
from crawler import Parser
from selenium import webdriver


URL = ['http://kiev.prom.ua/Markizy',
       'http://www.ua.all.biz/markizy-bgg1068719',
       'http://markizy.kiev.ua/',
       'http://kiev.all.biz/markiza-gorizontalnaya-g8531585',
       'http://prom.ua/Gorizontalnaya-loktevaya-markiza.html']

url = URL[0]

driver = webdriver.Firefox()
driver.get(url)
elem = driver.find_element_by_xpath('//*')
page = elem.get_attribute('outerHTML')
driver.quit()

p = Parser(url)
# p.get_html()
p.page = page
p.get_elements()
p.result[u'url'] = url


t = analyzer.TextAnalyzer(p.result)
print u'Url {}'.format(p.url)
for x in t.__dict__:
    if x != 'page':
        print x, t.__dict__[x]
t.title()
t.description()
t.keywords()
t.canonical()
t.h1()
t.h2()
t.h3()
t.text()
t.anchors()

print u'Всего баллов {}'.format(str(t.ball))
p.result[u'quality'] = t.ball
p.save()