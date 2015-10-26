import unittest

from crawler import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        return

    def test_find_title(self):
        @
        REGULARS = {
            u'title': u'//title/text()',
            u'h1': u'//h1/*/text()',
            u'text': u'//*/text()'
            }
        p = Parser()
        p.url = 'http://example.com/'
        title = "Example Domain"
        self.assertEqual(p.get_elements(p.get_html(p.url), REGULARS), title)

if __name__ == "__main__":
    unittest.main()
