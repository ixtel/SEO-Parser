import analyzer
import normalizer
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


text = ' '.join(p.result.get(u'text'))

t = analyzer.TextAnalyzer(p.result)
t.keys = ''.join(normalizer.top_in_text(text, 20).keys())
t.title()
t.description()
t.keywords()
t.canonical()
t.h1()
print t.ball
p.result[u'quality'] = t.ball
p.save()