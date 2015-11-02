# coding: utf-8
import csv
from pymongo import MongoClient
from settings import DATABASE

client = MongoClient(DATABASE)
db_name = 'google-2015-11-02'
db = client[db_name]
col = db.urls.find_one({u'query': u'купить макароны'})

head = ['url', 'poz', 'ball']

f = open('result2.csv', 'wb')
w = csv.writer(f, delimiter='\t')
w.writerow(head)

for i in col['sites']:
    print (i)
    if i:
        t = db.result.find_one({u'url': i})
        p = db.index.find_one({u'url': i})
        if t and p:
            w.writerow([t['url'], p['position'], t['size_']/t['load_time_']])
f.close()