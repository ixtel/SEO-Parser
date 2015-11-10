# coding: utf-8
import sys
sys.path.append('D:\\crawler\\')

from pymongo import MongoClient
from pars.analyzer import TextAnalyzer
from pars.crawler import Parser
from pars.settings import Settings

settings = Settings()


def main():

    client = MongoClient(settings.DATABASE)
    db_name = 'google-2015-11-03'
    db = client[db_name]
    gr = db.urls.find()

    for query in gr:
        print query['query']
        for i in range(100):
            if query['sites'][i].startswith('http'):
                print query['sites'][i]
                if db.index.find({u'url': query['sites'][i]}).count() == 1:
                    continue
                p = Parser()
                p.url = query['sites'][i]
                p.open_url()
                p.get_links()
                p.get_elements()
                p.set_elements()
                p.result['query'] = query['query']
                p.result['position'] = i + (query['search_page'] * 100)
                db.index.insert_one(p.result)
                t = TextAnalyzer(p.result)
                t.keys = query['query'].split()
                t.analyze()
                # print u"Отсканировал позицию {}".format(p.result['position'])
                # p.clean()
                # db.result.insert_one(t.__dict__)
                # print 'Done'
                # p.clean()

if __name__ == '__main__':
    main()
