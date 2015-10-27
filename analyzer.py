# coding: utf-8
import normalizer


def get_max(l):
    max_l = 0
    item = ''
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
    if type(l) is None:
        return ''


def delete_none(l):
    for num, item in enumerate(l):
        if not item:
            del l[num]
    return l


def get_all(l):
    if type(l) is list:
        new = ' '.join(delete_none(l)).replace('\n', ' ').strip()
        return " ".join(new.lower().split()).strip()
    if type(l) in (str, unicode):
        return l
    if type(l) is None:
        return ''


class TextAnalyzer(object):

    def __init__(self, page):

        self.page = page                                                        # dict
        self.url = page[u'url']                                                 # unicode
        self.ball = 0                                                           # int

        self.keys = normalizer.top_in_text(get_all(page[u'text']), 10)          # dict

        self.title_ = get_all(page[u'title'])                                   # unicode
        self.title_dlina = len(self.title_)                                     # int
        self.title_col_slov = len(self.title_.split())                          # int
        self.title_col_unik_slov = len(set(self.title_.split()))                # int
        self.title_vse_slova = self.title_.split()                              # list
        self.title_unik_slova = list(set(self.title_.split()))                  # list
        self.title_ball = 0                                                     # int

        self.description_ = get_all(page[u'description'])                       # unicode
        self.description_dlina = len(self.description_)                         # int
        self.description_col_slov = len(self.description_.split())              # int
        self.description_col_unik_slov = len(set(self.description_.split()))    # int
        self.description_vse_slova = self.description_.split()                  # list
        self.description_unik_slova = list(set(self.description_.split()))      # list
        self.description_ball = 0                                               # int

        self.keywords_ = get_all(page[u'keywords'])                             # unicode

    def title(self):
        if 10 < self.title_dlina <= 70:
            self.title_ball += 5
        if 70 < self.title_dlina <= 150:
            self.title_ball += 3
        if self.title_col_slov == self.title_col_unik_slov:
            self.title_ball += 3
        for word in self.keys:
            if word in self.title_unik_slova:
                self.title_ball += 2
        self.ball += self.title_ball
        print u'За title {}'.format(self.title_ball)

    def description(self):
        if 100 < self.description_dlina <= 165:
            self.description_ball += 1
        if not self.description_ == self.title_:
            self.description_ball += 1
        for word in self.keys:
            if word in self.description_unik_slova:
                self.description_ball += 1
        self.ball += self.description_ball
        print u'За description {}'.format(self.description_ball)

    def keywords(self):
        keywords_ball = 0
        for word in self.keys.keys():
            if word in get_all(self.page[u'keywords']).split():
                keywords_ball += 1
                break
        self.ball += keywords_ball
        print u'За keywords {}'.format(keywords_ball)

    def canonical(self):
        canonical_ball = 0
        if get_one(self.page[u'canonical']) == self.url:
            canonical_ball += 1
        self.ball += canonical_ball
        print u'За canonical {}'.format(canonical_ball)

    def h1(self):
        h1_ball = 0
        if len(self.page[u'h1']) == 1:
            h1_ball += 3
        if len(self.page[u'h1']) > 1:
            h1_ball += -2
        if 5 < len(get_all(self.page[u'h1'])) < 100:
            h1_ball += 3
        if 1 < len(get_all(self.page[u'h1']).split()) < 6:
            h1_ball += 3
        if get_all(self.page[u'h1']) != get_all(self.page[u'title']):
            h1_ball += 3
        if len(get_all(self.page[u'h1']).split()) == len(set(get_all(self.page[u'h1']).split())):
            h1_ball += 3
        for word in self.keys.keys():
            if word in get_all(self.page[u'h1']).split():
                h1_ball += 3
        self.ball += h1_ball
        print u'За h1 {}'.format(h1_ball)

    def h2(self):
        h2_ball = 0
        if 0 < len(self.page[u'h2']) < 10:
            h2_ball += 2
        if len(self.page[u'h2']) >= 10:
            h2_ball += -2
        if 5 < len(get_one(self.page[u'h2'])) < 100:
            h2_ball += 1
        if 1 < len(get_one(self.page[u'h2']).split()) < 20:
            h2_ball += 1

        counter = 0
        for h2 in self.page[u'h2']:
            if h2 in self.page[u'h1']:
                counter += 1
        if not counter and self.page[u'h2']:
            h2_ball += 1
        else:
            h2_ball += -1

        for word in self.keys.keys():
            if word in get_all(self.page[u'h2']).split():
                h2_ball += 1
        self.ball += h2_ball
        print u'За h2 {}'.format(h2_ball)

    def h3(self):
        h3_ball = 0
        if 0 < len(self.page[u'h3']) < 20:
            h3_ball += 2
        if len(self.page[u'h3']) >= 20:
            h3_ball += -2
        if 5 < len(get_one(self.page[u'h3'])) < 100:
            h3_ball += 1
        if 1 < len(get_one(self.page[u'h3']).split()) < 30:
            h3_ball += 1

        counter = 0
        for h3 in self.page[u'h3']:
            if h3 in self.page[u'h2'] or h3 in self.page[u'h1']:
                counter += 1
        if not counter and self.page[u'h3']:
            h3_ball += 1
        else:
            h3_ball += -1

        for word in self.keys.keys():
            if word in get_all(self.page[u'h3']).split():
                h3_ball += 1
        self.ball += h3_ball
        print u'За h3 {}'.format(h3_ball)

    def text(self):
        text_ball = 0
        if len(get_all(self.page[u'text'])) < 500:
            text_ball += 2
        if 500 <= len(get_all(self.page[u'text'])) < 2000:
            text_ball += 5
        if 2000 <= len(get_all(self.page[u'text'])) < 4000:
            text_ball += 10
        if 4000 <= len(get_all(self.page[u'text'])) < 8000:
            text_ball += 3
        if len(get_all(self.page[u'text'])) >= 8000:
            text_ball += 1
        for word in self.keys.keys():
            if word in get_all(self.page[u'title']).split() and word in get_all(self.page[u'h1']).split():
                text_ball += 2
        best_word = normalizer.top_in_dict(self.keys, 1)
        if float(best_word.values()[0]) < 1.0:
            text_ball += 2
        elif 1.0 <= float(best_word.values()[0]) < 5.0:
            text_ball += 10
        elif 5.0 <= float(best_word.values()[0]) < 20.0:
            text_ball += 5
        elif float(best_word.values()[0]) >= 20.0:
            text_ball += -10
        self.ball += text_ball
        print u'За text {}'.format(text_ball)

    def anchors(self):
        anchors_ball = 0
        for word in self.keys.keys():
            if word in get_all(self.page[u'a']).split():
                anchors_ball += 1

        best_word = normalizer.top_in_text(get_all(self.page[u'a']), 1)

        if float(best_word.values()[0]) < 3.0:
            anchors_ball += 1
        elif 3.0 <= float(best_word.values()[0]) < 5.0:
            anchors_ball += 5
        elif 5.0 <= float(best_word.values()[0]) < 10.0:
            anchors_ball += 10
        elif float(best_word.values()[0]) >= 20.0:
            anchors_ball += -10
        self.ball += anchors_ball
        print u'За анкоры {}'.format(anchors_ball)
