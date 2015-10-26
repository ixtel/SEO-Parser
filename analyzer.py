# coding: utf-8
import normalizer


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


def delete_none(l):
    for num, item in enumerate(l):
        if not item:
            del l[num]
    return l


def get_all(l):
    if type(l) is list:
        new = ' '.join(delete_none(l)).replace('\n', ' ').strip()
        return " ".join(new.split()).strip()
    if type(l) in (str, unicode):
        return l


class TextAnalyzer(object):
    ball = 0

    def __init__(self, page):
        self.url = page['url']
        self.page = page
        self.keys = normalizer.top_in_text(get_all(page[u'text']), 10)

    def title(self):
        if 10 < len(get_all(self.page[u'title'])) <= 70:
            TextAnalyzer.ball += 5
        if 70 < len(get_all(self.page[u'title'])) <= 150:
            TextAnalyzer.ball += 3
        if len(get_all(self.page[u'title']).split()) == len(set(get_all(self.page[u'title']).split())):
            TextAnalyzer.ball += 3
        for word in self.keys.keys():
            if word in get_all(self.page[u'title']).split():
                TextAnalyzer.ball += 2
        print 'За title {}'.format(TextAnalyzer.ball)

    def description(self):
        if 100 < len(get_all(self.page[u'description'])) <= 165:
            TextAnalyzer.ball += 1
        if not get_all(self.page[u'title']) == get_all(self.page[u'description']):
            TextAnalyzer.ball += 1
        for word in self.keys.keys():
            if word in get_all(self.page[u'description']).split():
                TextAnalyzer.ball += 1
        print 'За description {}'.format(TextAnalyzer.ball)

    def keywords(self):
        for word in self.keys.keys():
            if word in get_all(self.page[u'keywords']).split():
                TextAnalyzer.ball += 1
                break
        print 'За keywords {}'.format(TextAnalyzer.ball)

    def canonical(self):
        if get_one(self.page[u'canonical']) == self.url:
            TextAnalyzer.ball += 1
        print 'За canonical {}'.format(TextAnalyzer.ball)

    def h1(self):
        if len(self.page[u'h1']) == 0:
            TextAnalyzer.ball += 3
        if 5 < len(get_all(self.page[u'h1'])) < 100:
            TextAnalyzer.ball += 3
        if 1 < len(get_all(self.page[u'h1']).split()) < 6:
            TextAnalyzer.ball += 3
        if get_all(self.page[u'h1']) != get_all(self.page[u'title']):
            TextAnalyzer.ball += 3
        if len(get_all(self.page[u'h1']).split()) == len(set(get_all(self.page[u'h1']).split())):
            TextAnalyzer.ball += 3
        for word in self.keys.keys():
            if word in get_all(self.page[u'h1']).split():
                TextAnalyzer.ball += 3
        print 'За h1 {}'.format(TextAnalyzer.ball)

    def text(self):
        if len(get_all(self.page[u'text'])) < 500:
            TextAnalyzer.ball += 2
        if 500 <= len(get_all(self.page[u'text'])) < 2000:
            TextAnalyzer.ball += 5
        if 2000 <= len(get_all(self.page[u'text'])) < 4000:
            TextAnalyzer.ball += 10
        if 4000 <= len(get_all(self.page[u'text'])) < 8000:
            TextAnalyzer.ball += 3
        if len(get_all(self.page[u'text'])) >= 8000:
            TextAnalyzer.ball += 1

        for word in self.keys.keys():
            if word in get_all(self.page[u'title']).split() and word in get_all(self.page[u'h1']).split():
                TextAnalyzer.ball += 2

        best_word = normalizer.top_in_dict(self.keys, 1)

        if float(best_word.values()[0]) < 1.0:
            TextAnalyzer.ball += 2
        elif 1.0 <= float(best_word.values()[0]) < 5.0:
            TextAnalyzer.ball += 10
        elif 5.0 <= float(best_word.values()[0]) < 20.0:
            TextAnalyzer.ball += 5
        elif float(best_word.values()[0]) >= 20.0:
            TextAnalyzer.ball -= 10

        print 'За text {}'.format(TextAnalyzer.ball)