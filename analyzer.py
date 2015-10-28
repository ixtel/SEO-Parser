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


def get_all(l, flag=False):
    if type(l) is list:
        new = u' '.join(delete_none(l))
        if flag:
            return normalizer.text_normalizer(new)
        else:
            return u' '.join(new.lower().split())
    if type(l) in (str, unicode):
        return normalizer.text_normalizer(l)
    if type(l) is None:
        return ''


class TextAnalyzer(object):

    def __init__(self, page):

        self.page = page                                                        # dict
        self.url = page[u'url']                                                 # unicode
        self.ball = 0                                                           # int

        self.keys = normalizer.top_in_text(get_all(page[u'text']), 3)           # dict

        self.title_ = get_all(page[u'title'])                                   # unicode
        self.title_normal = get_all(page[u'title'], True)                       # unicode
        self.title_dlina = len(self.title_)                                     # int
        self.title_col_slov = len(self.title_normal.split())                    # int
        self.title_col_unik_slov = len(set(self.title_normal.split()))          # int
        self.title_vse_slova = self.title_.split()                              # list
        self.title_unik_slova = list(set(self.title_normal.split()))            # list
        self.title_ball = 0                                                     # int

        self.description_ = get_all(page[u'description'])                               # unicode
        self.description_normal = get_all(page[u'description'], True)                   # unicode
        self.description_dlina = len(self.description_)                                 # int
        self.description_col_slov = len(self.description_normal.split())                # int
        self.description_col_unik_slov = len(set(self.description_normal.split()))      # int
        self.description_vse_slova = self.description_.split()                          # list
        self.description_unik_slova = list(set(self.description_normal.split()))        # list
        self.description_ball = 0                                                       # int

        self.keywords_ = get_all(page[u'keywords'], True)                       # unicode
        self.keywords_slova = self.keywords_.split()                            # list
        self.keywords_ball = 0                                                  # int

        self.canonical_ = get_one(page[u'canonical'])                           # unicode
        self.canonical_ball = 0                                                 # int

        self.h1_ = get_all(page[u'h1'])                                         # unicode
        self.h1_normal = get_all(page[u'h1'], True)                             # unicode
        self.h1_kolichestvo_na_str = len(page[u'h1'])                           # int
        self.h1_dlina = len(self.h1_)                                           # int
        self.h1_col_slov = len(self.h1_normal.split())                          # int
        self.h1_col_unik_slov = len(set(self.h1_normal.split()))                # int
        self.h1_vse_slova = self.h1_.split()                                    # list
        self.h1_unik_slova = list(set(self.h1_normal.split()))                  # list
        self.h1_ball = 0                                                        # int

        self.h2_ = get_all(page[u'h2'])                                         # unicode
        self.h2_normal = get_all(page[u'h2'], True)                             # unicode
        self.h2_kolichestvo_na_str = len(page[u'h2'])                           # int
        self.h2_dlina = len(self.h2_)                                           # int
        self.h2_col_slov = len(self.h2_normal.split())                          # int
        self.h2_col_unik_slov = len(set(self.h2_normal.split()))                # int
        self.h2_vse_slova = self.h2_.split()                                    # list
        self.h2_unik_slova = list(set(self.h2_normal.split()))                  # list
        self.h2_ball = 0                                                        # int

        self.h3_ = get_all(page[u'h3'])                                         # unicode
        self.h3_normal = get_all(page[u'h3'], True)                             # unicode
        self.h3_kolichestvo_na_str = len(page[u'h3'])                           # int
        self.h3_dlina = len(self.h3_)                                           # int
        self.h3_col_slov = len(self.h3_normal.split())                          # int
        self.h3_col_unik_slov = len(set(self.h3_normal.split()))                # int
        self.h3_vse_slova = self.h3_.split()                                    # list
        self.h3_unik_slova = list(set(self.h3_normal.split()))                  # list
        self.h3_ball = 0                                                        # int

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
        for word in self.keys:
            if word in self.keywords_slova:
                self.keywords_ball += 1
                break
        self.ball += self.keywords_ball
        print u'За keywords {}'.format(self.keywords_ball)

    def canonical(self):
        if self.canonical_ == self.url:
            self.canonical_ball += 1
        self.ball += self.canonical_ball
        print u'За canonical {}'.format(self.canonical_ball)

    def h1(self):
        if self.h1_kolichestvo_na_str == 0:
            self.h1_ball += -3
        if self.h1_kolichestvo_na_str == 1:
            self.h1_ball += 3
        if self.h1_kolichestvo_na_str > 1:
            self.h1_ball += -2
        if 5 < self.h1_dlina < 100:
            self.h1_ball += 3
        if 1 < self.h1_col_slov < 6:
            self.h1_ball += 3
        if self.h1_col_slov == self.h1_col_unik_slov:
            self.h1_ball += 3
        for word in self.keys:
            if word in self.h1_unik_slova:
                self.h1_ball += 3
        self.ball += self.h1_ball
        print u'За h1 {}'.format(self.h1_ball)

    def h2(self):
        if 1 < self.h2_kolichestvo_na_str < 10:
            self.h2_ball += 2
        if self.h2_kolichestvo_na_str >= 10:
            self.h2_ball += -2
        if 20 < self.h2_dlina < 100:
            self.h2_ball += 1
        if 4 < self.h2_col_slov < 50:
            self.h2_ball += 1
        for word in self.keys:
            if word in self.h2_unik_slova:
                self.h2_ball += 1
        self.ball += self.h2_ball
        print u'За h2 {}'.format(self.h2_ball)

    def h3(self):
        if 1 < self.h3_kolichestvo_na_str < 20:
            self.h3_ball += 2
        if self.h3_kolichestvo_na_str >= 20:
            self.h3_ball += -2
        if 10 < self.h3_dlina < 100:
            self.h3_ball += 1
        if 3 < self.h3_col_slov < 30:
            self.h3_ball += 1
        for word in self.keys:
            if word in self.h3_unik_slova:
                self.h3_ball += 1
        self.ball += self.h3_ball
        print u'За h3 {}'.format(self.h3_ball)

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
