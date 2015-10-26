import analyzer
from crawler import Parser
from selenium import webdriver


URL = ['http://kiev.prom.ua/Markizy',
       'http://www.ua.all.biz/markizy-bgg1068719']

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
t.title()
t.description()
t.keywords()
t.canonical()
t.h1()
t.text()
for x in t.keys:
    print x, t.keys[x]
print t.ball
p.result[u'quality'] = t.ball
p.save()