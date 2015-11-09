# coding: utf-8
import sys
sys.path.append('D:\\crawler\\')

import csv
from pymongo import MongoClient
from parser.settings import DATABASE

client = MongoClient(DATABASE)
db_name = 'google-2015-11-03'
db = client[db_name]
col = db.urls.find()

head = ['url', 'poz', 'ball']

f = open('result5.csv', 'wb')
w = csv.writer(f, delimiter='\t')
w.writerow(head)

for item in db.result.find():
    p = db.index.find_one({u'url': item['url']})
    if p and '%3' not in item['url']:
        d = dict()
        count = 0
        for key in item['text_top5']:
            d[key] = item['text_top5'][key] * item['text_col_slov'] / 100
            if key in item['keys']:
                count += d[key]
        w.writerow([item['url'], p['position'], count])

f.close()
