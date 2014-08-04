import unittest
from saw.parsers.words import Node, Words
from saw.parsers.blocks import Blocks
from saw.saw import Saw


class TestLoad(unittest.TestCase):
    def setUp(self):
        pass

    def test_type(self):
        node = Words.load('aa')
        self.assertEquals(node.type(), 'words')

        node.type('test')
        self.assertEquals(node.type(), 'test')

        self.assertEquals(node.type('none'), node)

    def test_before(self):
        node = Node()

        node.before([',', ':', '.'])
        self.assertEqual(node.before(), [',', ':', '.'])

        node.before('-', True).before('!', True)
        self.assertEqual(node.before(), [',', ':', '.', '-', '!'])

        self.assertEquals(node.before(['.', '-']), node)
        self.assertEquals(node.before(['.', '-'], True), node)

    def test_after(self):
        node = Node()

        node.after([',', ':', '.'])
        self.assertEqual(node.after(), [',', ':', '.'])

        node.after('-', True).after('!', True)
        self.assertEqual(node.after(), [',', ':', '.', '-', '!'])

        self.assertEquals(node.after(['.', '-']), node)
        self.assertEquals(node.after(['.', '-'], True), node)

    def test_text(self):
        node = Node()

        node.text('Any text')
        self.assertEqual(node.text(), 'Any text')

        node.text(', second', True).text(', third', True)
        self.assertEqual(node.text(), 'Any text, second, third')

        self.assertEquals(node.text('test'), node)
        self.assertEquals(node.text('test', True), node)

    def test___repr(self):
        pass

    def test___str(self):
        text = 'Any text, :yep:. Test it- test it fast?!'
        node = Saw.load(text)
        self.assertEqual(str(node), text)

    def test___getattr(self):
        pass

    def test___getitem(self):
        node = Blocks.load('Any text, second, third')

        self.assertEqual(node[0].__class__, Node)
        self.assertEqual(node[2].__class__, Node)

        self.assertEqual(node[0].type(), Words._type)
        self.assertEqual(node[2].type(), Words._type)

    def test___getslice(self):
        node = Words.load('Any text, second, third')

        sl_1 = node[:3]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), node.type())
        self.assertEqual(sl_1, Words.load('Any text, second,'))

        sl_2 = node[1:3]
        self.assertEqual(sl_2.__class__, Node)
        self.assertEqual(sl_2.type(), node.type())
        self.assertEqual(sl_2, Words.load('text, second,'))

        sl_3 = node[1:]
        self.assertEqual(sl_3.__class__, Node)
        self.assertEqual(sl_3.type(), node.type())
        self.assertEqual(sl_3, Words.load('text, second, third'))

    def test_get_item_and_slice(self):
        node = Blocks.load('Any advanced text, second, third')

        sl_1 = node[:3][2]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), Words._type)
        self.assertEqual(sl_1, Words.load('third'))

        sl_1 = node[0][:2]
        self.assertEqual(sl_1.__class__, Node)
        self.assertEqual(sl_1.type(), Words._type)
        self.assertEqual(sl_1, Words.load('Any advanced'))

    def test___eq(self):
        node = Blocks.load('*Any advanced text,')
        blocks = Node().type(Blocks._type)
        blocks.append(Node())

        block = blocks[0]
        self.assertNotEqual(blocks, node)
        block.before(['*'])
        self.assertNotEqual(blocks, node)
        block.after([','])
        self.assertNotEqual(blocks, node)
        block.type(Words._type)
        self.assertNotEqual(blocks, node)

        for word in Words.load('Any advanced text'):
            block.append(word)
        self.assertEqual(blocks, node)

    def test_copy(self):
        txt = 'Any text, yep. Test it!'
        sw = Blocks.load(txt)
        for a in sw.copy().words:
            a.text('_', True)

        self.assertEqual(str(sw), 'Any text, yep. Test it!')


if __name__ == "__main__":
    unittest.main()