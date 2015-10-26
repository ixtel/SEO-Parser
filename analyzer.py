# coding: utf-8

def get_max(l):
    max_l = 0
    item = None
    for i in l:
        if not i:
            continue
        if len(i) > max_l:
            max_l = len(i)
            item = i
    return item


def get_one(l):
    if type(l) is list:
        return get_max(l)
    if type(l) in (str, unicode):
        return l


class TextAnalyzer(object):
    ball = 0

    def __init__(self, page):
        self.url = page['url']
        self.page = page
        self.keys = u'UkrSTK OOO BKF UkrSTK OOO Производител'

    def title(self):
        if 10 < len(get_one(self.page[u'title'])) <= 70:
            TextAnalyzer.ball += 5
        if 70 < len(get_one(self.page[u'title'])) <= 150:
            TextAnalyzer.ball += 3
        if len(get_one(self.page[u'title']).split()) == len(set(get_one(self.page[u'title']).split())):
            TextAnalyzer.ball += 3
        for word in self.keys.split():
            if word in get_one(self.page[u'title']).split():
                TextAnalyzer.ball += 5
                break

    def description(self):
        if 100 < len(get_one(self.page[u'description'])) <= 165:
            TextAnalyzer.ball += 1
        if not get_one(self.page[u'title']) == get_one(self.page[u'description']):
            TextAnalyzer.ball += 1
        for word in self.keys.split():
            if word in get_one(self.page[u'description']).split():
                TextAnalyzer.ball += 3
                break

    def keywords(self):
        for word in self.keys.split():
            if word in get_one(self.page[u'keywords']).split():
                TextAnalyzer.ball += 1
                break

    def canonical(self):
        if get_one(self.page[u'canonical']) == self.url:
            TextAnalyzer.ball += 1

    def h1(self):
        if len(self.page[u'h1']) == 0:
            TextAnalyzer.ball += 3
        if 5 < len(get_one(self.page[u'h1'])) < 100:
            TextAnalyzer.ball += 3
        if 1 < len(get_one(self.page[u'h1']).split()) < 6:
            TextAnalyzer.ball += 3
        if get_one(self.page[u'h1']) != get_one(self.page[u'title']):
            TextAnalyzer.ball += 3
        if len(get_one(self.page[u'h1']).split()) == len(set(get_one(self.page[u'h1']).split())):
            TextAnalyzer.ball += 3
        for word in self.keys.split():
            if word in get_one(self.page[u'h1']).split():
                TextAnalyzer.ball += 3

'''
t = TextAnalyzer(data)
print t.ball
t.title()
print t.ball
t.description()
print t.ball
t.keywords()
print t.ball
t.canonical()
print t.ball
t.h1()
print t.ball
'''