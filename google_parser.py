# coding: utf-8
from datetime import date
import urllib
from crawler import Parser

queries = [u'купить мармелад',
           u'сигареты оптом',
           u'купить пшеницу',
           u'купить дрова']

google = u'https://www.google.com.ua/search?num=100&hl=ru&q='
# example url is: https://www.google.com.ua/search?num=100&hl=ru&q=купить+мармелад


def qa(q):
    return q.strip().replace(u' ', u'+')


def main():
    p = Parser()

    db_name = '<google::' + date.today().isoformat() + '>'
    Parser.db = Parser.client[db_name]
    p.regulars = {u'sites': u'//h3[@class="r"]/a/@href'}

    for n, q in enumerate(queries):
        p.url = google + urllib.quote(qa(q).encode('cp1251'))
        p.open_url()
        p.get_elements()
        p.result[u'query'] = q

        for num, url in enumerate(p.result[u'sites']):
            url = url.replace('/url?q=', '')
            url = url.split('&sa=U')[0]
            p.result[u'sites'][num] = url

        del(p.result[u'links'], p.result[u'in_links'], p.result[u'out_links'])

        p.save()
        print u'Запрос: [{}] "{}" отсканирован и сохранен'.format(n, q)

if __name__ == '__main__':
        main()
