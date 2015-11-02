# coding: utf-8
import urllib
from datetime import date

from crawler import Parser

queries = [u'купить мармелад', u'купить макароны']

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
        p.url = google + urllib.quote(qa(q).encode('cp1251'))
        p.open_url()
        p.get_elements()
        p.set_elements()
        p.result[u'query'] = q
        p.result[u'sites'] = norm(p.result[u'sites'])
        p.save()
        p.clean()
        print u'Запрос: [{}] "{}" отсканирован и сохранен'.format(n, q)

if __name__ == '__main__':
        main()