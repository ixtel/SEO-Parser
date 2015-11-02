# coding: utf-8
import string


def text_normalizer(text):
    text = unicode(text.lower())
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    text = text.replace(u'\n', u' ')
    text = text.translate(remove_punctuation_map).split()
    new = list()
    for i in text:
        if len(i) > 3:
            new.append(i)
    text = u' '.join(new)
    return u' '.join(text.split())


def words_count(text, is_percent=False):
    words = text.split()
    if words:
        percent = 100.0 / len(words)
    else:
        percent = 0
    d = dict()
    for word in words:
        if word not in d:
            d[word] = 1
        else:
            d[word] += 1
    if is_percent:
        for word in d:
            d[word] = float(format((d[word] * percent), '.2f'))
    return d


def top_in_dict(d, num):
    top = dict()
    values = sorted(d.values())[-num:]
    for key in d:
        if d[key] in values:
            top[key] = d[key]
    return top


def distance(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1)  # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1, n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def top_in_text(text, num):
    text = text_normalizer(text)
    words = words_count(text, True)
    return top_in_dict(words, num)


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
            return __init__.text_normalizer(new)
        else:
            return u' '.join(new.lower().split())
    if type(l) in (str, unicode):
        return __init__.text_normalizer(l)
    if type(l) is None:
        return ''


def mistake(f):
    def wrap():
         try:
             f()
         except:
            return
    return wrap()

'''
text = u"""
Вам нужны клиенты? Чтобы добавить товары и услуги в каталог Prom.ua, зарегистрируйте свою компанию / Спасибо, но я покупатель
Товары и услуги — бизнес-каталог компаний Украины, создание сайтов, товары и услуги, прайс-листы"""

k = top_in_text(text, 1)

for i in k:
    print i, k[i]
'''
