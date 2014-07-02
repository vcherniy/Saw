import unittest
from saw.parsers.words import Node, Words


class TestLoad(unittest.TestCase):
    def setUp(self):
        pass

    def test_type(self):
        node = Words.load('aa')
        self.assertEquals(node.type(), 'words')
        node.type('test')
        self.assertEquals(node.type(), 'test')

    def test_before(self):
        node = Node()

        node.before([',', ':', '.'])
        self.assertEqual(node.before(), [',', ':', '.'])

        node.before('-', True)
        node.before('!', True)
        self.assertEqual(node.before(), [',', ':', '.', '-', '!'])

    def test_after(self):
        node = Node()

        node.after([',', ':', '.'])
        self.assertEqual(node.after(), [',', ':', '.'])

        node.after('-', True)
        node.after('!', True)
        self.assertEqual(node.after(), [',', ':', '.', '-', '!'])

    def test_text(self):
        node = Node()

        node.text('Any text')
        self.assertEqual(node.text(), 'Any text')

        node.text(', second', True)
        node.text(', third', True)
        self.assertEqual(node.text(), 'Any text, second, third')

    def test___repr(self):
        pass

    def test___str(self):
        pass

    def test___getattr(self):
        pass

    def test___getitem(self):
        #self.assertEqual(node[0].__class__, Node)
        #self.assertEqual(node[2].__class__, Node)
        pass

    def test___getslice(self):
        node = Words.load('Any text, second, third')

        sl_1 = node[:3]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), node.type())
        #self.assertEqual(sl_1, Words.load('Any text, second'))

        sl_2 = node[1:3]
        self.assertEqual(sl_2.__class__, Node)
        self.assertEqual(sl_2.type(), node.type())
        #self.assertEqual(sl_2, Words.load('text, second'))

        sl_3 = node[1:]
        self.assertEqual(sl_3.__class__, Node)
        self.assertEqual(sl_3.type(), node.type())
        #self.assertEqual(sl_3, Words.load('text, second, third'))

    def test_get_item_and_slice(self):
        pass

    def test___eq(self):
        pass

    def test_copy(self):
        #node = Paragraphs.load('Any text, second, third')
        pass


if __name__ == "__main__":
    unittest.main()