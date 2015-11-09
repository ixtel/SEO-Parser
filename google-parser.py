# coding: utf-8
import sys
sys.path.append('D:\\crawler\\')

import urllib
from datetime import date

from parser.crawler import Parser

queries = [u'купить макароны']

google = u'https://www.google.com.ua/search?num=100&hl=ru&q='
# example url is: https://www.google.com.ua/search?num=100&hl=ru&q=купить+мармелад


def qa(q):
    return q.strip().replace(u' ', u'+')


def norm(l):
    new = []
    for url in l:
        url = url.replace(u'/url?q=', u'')
        url = url.replace(u'%25', u'%')
        url = url.split(u'&sa=U')[0]
        new.append(url)
    return new


def main():
    p = Parser('http://google.com.ua/', False)
    db_name = 'google-' + date.today().isoformat()
    Parser.db = Parser.client[db_name]
    p.regulars = {u'sites': u'//h3[@class="r"]/a/@href'}

    for n, q in enumerate(queries):
        for j in range(3):
            start = j * 100
            start = '&start=' + str(start)
            p.url = google + urllib.quote(qa(q).encode('cp1251')) + start
            p.open_url()
            p.get_elements()
            p.set_elements()
            p.result[u'query'] = q
            p.result[u'sites'] = norm(p.result[u'sites'])
            p.result[u'search_page'] = j
            p.save()
            p.clean()
            print u'Запрос: [{}] "{}" отсканирован и сохранен'.format(n, q)

if __name__ == '__main__':
        main()
