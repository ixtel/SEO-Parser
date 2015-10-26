import analyzer
from crawler import Parser
from selenium import webdriver


URL = ['http://kiev.prom.ua/Markizy',
       'http://www.ua.all.biz/markizy-bgg1068719',
       'http://markizy.kiev.ua/',
       'http://kiev.all.biz/markiza-gorizontalnaya-g8531585',
       'http://prom.ua/Gorizontalnaya-loktevaya-markiza.html']

url = URL[4]

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
print 'Url {}'.format(p.url)
t.title()
t.description()
t.keywords()
t.canonical()
t.h1()
t.text()
'''
for x in t.keys:
    print x, t.keys[x]'''
p.result[u'quality'] = t.ball
p.save()