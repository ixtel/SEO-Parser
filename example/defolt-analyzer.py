# coding: utf-8
from pymongo import MongoClient

from analyzer import TextAnalyzer
from crawler import Parser
from settings import DATABASE


def main():

    client = MongoClient(DATABASE)
    db_name = 'google-2015-11-02'
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
                p.result['position'] = i
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
                except:
                    p.clean()
                    continue
                p.clean()
                db.result.insert_one(t.__dict__)
                print 'Done'

if __name__ == '__main__':
    main()