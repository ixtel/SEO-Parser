# coding: utf-8
import sys
sys.path.append('D:\\crawler\\')

from pymongo import MongoClient

from pars.analyzer import TextAnalyzer
from pars.crawler import Parser
from pars.settings import DATABASE


def main():

    client = MongoClient(DATABASE)
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
                p = Parser(query['sites'][i], False)
                p.open_url()
                p.get_links()
                p.get_elements()
                p.set_elements()
                p.result['query'] = query['query']
                p.result['position'] = i + (query['search_page'] * 100)
                db.index.insert_one(p.result)
                try:
                    t = TextAnalyzer(p.result)
                    t.keys = query['query'].split()
                    t.title()
                    t.description()
                    t.keywords()
                    t.canonical()
                    t.h1()
                    t.h2()
                    t.h3()
                    t.text()
                    t.anchors()
                    t.load_time()
                    t.size()
                    t.script()
                    t.js_files()
                    t.in_links()
                    t.out_links()
                    print u"Отсканировал позицию {}".format(p.result['position'])
                    p.clean()
                    db.result.insert_one(t.__dict__)
                    print 'Done'
                except:
                    p.clean()
                    print 'Error'
                    continue


if __name__ == '__main__':
    main()
