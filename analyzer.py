# coding: utf-8
import text_utils


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
            return text_utils.text_normalizer(new)
        else:
            return u' '.join(new.lower().split())
    if type(l) in (str, unicode):
        return text_utils.text_normalizer(l)
    if type(l) is None:
        return ''


class TextAnalyzer(object):

    def __init__(self, page_data):

        self.page_data_dict = page_data                                                 # dict
        self.url = page_data[u'url']                                                    # unicode
        self.ball = 0                                                                   # int

        self.load_time_ = page_data[u'load_time']                                       # float
        self.load_time_ball = 0                                                         # int

        self.size_ = page_data[u'size']                                                 # int
        self.size_ball = 0                                                              # int

        self.keys = text_utils.top_in_text(get_all(page_data[u'text']), 5)              # dict

        self.title_ = get_all(page_data[u'title'])                                      # unicode
        self.title_normal = get_all(page_data[u'title'], True)                          # unicode
        self.title_dlina = len(self.title_)                                             # int
        self.title_col_slov = len(self.title_normal.split())                            # int
        self.title_col_unik_slov = len(set(self.title_normal.split()))                  # int
        self.title_vse_slova = self.title_.split()                                      # list
        self.title_unik_slova = list(set(self.title_normal.split()))                    # list
        self.title_ball = 0                                                             # int

        self.description_ = get_all(page_data[u'description'])                          # unicode
        self.description_normal = get_all(page_data[u'description'], True)              # unicode
        self.description_dlina = len(self.description_)                                 # int
        self.description_col_slov = len(self.description_normal.split())                # int
        self.description_col_unik_slov = len(set(self.description_normal.split()))      # int
        self.description_vse_slova = self.description_.split()                          # list
        self.description_unik_slova = list(set(self.description_normal.split()))        # list
        self.description_ball = 0                                                       # int

        self.keywords_ = get_all(page_data[u'keywords'], True)                          # unicode
        self.keywords_slova = self.keywords_.split()                                    # list
        self.keywords_ball = 0                                                          # int

        self.canonical_ = get_one(page_data[u'canonical'])                              # unicode
        self.canonical_ball = 0                                                         # int

        self.h1_ = get_all(page_data[u'h1'])                                            # unicode
        self.h1_normal = get_all(page_data[u'h1'], True)                                # unicode
        self.h1_kolichestvo_na_str = len(page_data[u'h1'])                              # int
        self.h1_dlina = len(self.h1_)                                                   # int
        self.h1_col_slov = len(self.h1_normal.split())                                  # int
        self.h1_col_unik_slov = len(set(self.h1_normal.split()))                        # int
        self.h1_vse_slova = self.h1_.split()                                            # list
        self.h1_unik_slova = list(set(self.h1_normal.split()))                          # list
        self.h1_ball = 0                                                                # int

        self.h2_ = get_all(page_data[u'h2'])                                            # unicode
        self.h2_normal = get_all(page_data[u'h2'], True)                                # unicode
        self.h2_kolichestvo_na_str = len(page_data[u'h2'])                              # int
        self.h2_dlina = len(self.h2_)                                                   # int
        self.h2_col_slov = len(self.h2_normal.split())                                  # int
        self.h2_col_unik_slov = len(set(self.h2_normal.split()))                        # int
        self.h2_vse_slova = self.h2_.split()                                            # list
        self.h2_unik_slova = list(set(self.h2_normal.split()))                          # list
        self.h2_ball = 0                                                                # int

        self.h3_ = get_all(page_data[u'h3'])                                            # unicode
        self.h3_normal = get_all(page_data[u'h3'], True)                                # unicode
        self.h3_kolichestvo_na_str = len(page_data[u'h3'])                              # int
        self.h3_dlina = len(self.h3_)                                                   # int
        self.h3_col_slov = len(self.h3_normal.split())                                  # int
        self.h3_col_unik_slov = len(set(self.h3_normal.split()))                        # int
        self.h3_vse_slova = self.h3_.split()                                            # list
        self.h3_unik_slova = list(set(self.h3_normal.split()))                          # list
        self.h3_ball = 0                                                                # int

        self.text_ = get_all(page_data[u'text'])                                        # unicode
        self.text_normal = get_all(page_data[u'text'], True)                            # unicode
        self.text_kolichestvo_na_str = len(page_data[u'text'])                          # int
        self.text_dlina = len(self.text_)                                               # int
        self.text_col_slov = len(self.text_normal.split())                              # int
        self.text_col_unik_slov = len(set(self.text_normal.split()))                    # int
        self.text_vse_slova = self.text_.split()                                        # list
        self.text_unik_slova = list(set(self.text_normal.split()))                      # list
        self.text_ball = 0                                                              # int

        self.anchors_ = get_all(page_data[u'a'])                                        # unicode
        self.anchors_normal = get_all(page_data[u'a'], True)                            # unicode
        self.anchors_kolichestvo_na_str = len(page_data[u'a'])                          # int
        self.anchors_dlina = len(self.anchors_)                                         # int
        self.anchors_col_slov = len(self.anchors_normal.split())                        # int
        self.anchors_col_unik_slov = len(set(self.anchors_normal.split()))              # int
        self.anchors_vse_slova = self.anchors_.split()                                  # list
        self.anchors_unik_slova = list(set(self.anchors_normal.split()))                # list
        self.anchors_ball = 0                                                           # int

        self.script_ = get_all(page_data[u'script'])                                    # unicode
        self.script_kolichestvo_na_str = len(page_data[u'script'])                      # int
        self.script_dlina = len(self.anchors_)                                          # int
        self.script_procent_na_str = float(self.script_dlina) / self.size_ * 100        # float
        self.script_ball = 0                                                            # int

    def title(self):
        if 10 < self.title_dlina <= 70:
            self.title_ball += 5
        if 70 < self.title_dlina <= 150:
            self.title_ball += 3
        if self.title_col_slov == self.title_col_unik_slov:
            self.title_ball += 3
        for word in self.keys:
            if word in self.title_unik_slova:
                self.title_ball += 4
        self.ball += self.title_ball
        print u'За title {}'.format(self.title_ball)

    def description(self):
        if 100 < self.description_dlina <= 165:
            self.description_ball += 1
        if not self.description_ == self.title_:
            self.description_ball += 1
        for word in self.keys:
            if word in self.description_unik_slova:
                self.description_ball += 2
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
                self.h1_ball += 5
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
                self.h2_ball += 2
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
        if 500 <= self.text_dlina < 2000:
            self.text_ball += 5
        if 2000 <= self.text_dlina < 4000:
            self.text_ball += 10
        if 4000 <= self.text_dlina < 8000:
            self.text_ball += 3
        if self.text_dlina >= 8000:
            self.text_ball += 1

        best_word = text_utils.top_in_dict(self.keys, 1)

        if float(best_word.values()[0]) < 1.0:
            self.text_ball += -2
        elif 1.0 <= float(best_word.values()[0]) < 4.0:
            self.text_ball += 10
        elif 4.0 <= float(best_word.values()[0]) < 7.0:
            self.text_ball += 5
        elif float(best_word.values()[0]) >= 7.0:
            self.text_ball += -10

        self.ball += self.text_ball
        print u'За text {}'.format(self.text_ball)

    def anchors(self):
        for word in self.keys:
            if word in self.anchors_unik_slova:
                self.anchors_ball += 1

        best_word = text_utils.top_in_text(self.anchors_, 1)

        if float(best_word.values()[0]) < 3.0:
            self.anchors_ball += 1
        elif 3.0 <= float(best_word.values()[0]) < 5.0:
            self.anchors_ball += 5
        elif 5.0 <= float(best_word.values()[0]) < 10.0:
            self.anchors_ball += 10
        elif float(best_word.values()[0]) >= 10.0:
            self.anchors_ball += -10
        self.ball += self.anchors_ball
        print u'За анкоры {}'.format(self.anchors_ball)

    def load_time(self):
        if 0.01 <= self.load_time_ < 2:
            self.load_time_ball += 10
        elif 2 <= self.load_time_ < 5:
            self.load_time_ball += 5
        elif 5 <= self.load_time_ < 10:
            self.load_time_ball += 2
        elif 10 <= self.load_time_ < 20:
            self.load_time_ball += -5
        elif 20 <= self.load_time_ < 40:
            self.load_time_ball += -10
        elif self.load_time_ >= 40:
            self.load_time_ball += -20
        self.ball += self.load_time_ball
        print u'За время загрузки {}'.format(self.load_time_ball)

    def size(self):
        if 0 <= self.size_ < 50000:
            self.size_ball += 10
        elif 50000 <= self.size_ < 100000:
            self.size_ball += 5
        elif 100000 <= self.size_ < 200000:
            self.size_ball += 2
        elif 200000 <= self.load_time_ < 300000:
            self.size_ball += -5
        elif self.size_ >= 300000:
            self.size_ball += -10
        self.ball += self.size_ball
        print u'За размер страницы {}'.format(self.size_ball)

    def script(self):
        if 0 <= self.script_kolichestvo_na_str < 4:
            self.script_ball += 10
        elif 4 <= self.script_kolichestvo_na_str < 8:
            self.script_ball += 5
        elif self.script_kolichestvo_na_str >= 8:
            self.script_ball += -10
        if 0 <= self.script_procent_na_str < 5:
            self.script_ball += 5
        elif 5 <= self.script_procent_na_str < 10:
            self.script_ball += 3
        elif 10 <= self.script_procent_na_str < 30:
            self.script_ball += 1
        elif 30 <= self.script_procent_na_str < 50:
            self.script_ball += -3
        elif self.script_procent_na_str >= 50:
            self.script_ball += -10
        self.ball += self.script_ball
        print u'За скрипты {}'.format(self.script_ball)
