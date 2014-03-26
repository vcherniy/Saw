import unittest
#from saw.parsers.paragraphs import Paragraphs
from saw.parsers.sentences import Sentences
from saw.parsers.blocks import Blocks
#from saw.parsers.words import Words

from saw.parsers import Item


class TestMods(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def _form(iem):
        return [[item._before or [], item._text or '', item._after or []] for item in iem.children]

    def test_sentences(self):
        text = '?1 sentence! But what!!WTF   ? .That 12.45 points.   .   Length = 100m..'
        expect = [
            [['?'], '', ['!']],        # ?1 sentence!
            [[],    '', ['!', '!']],   # But what!!
            [[],    '', ['?']],        # WTF   ?
            [[],    '', ['.']],        # .That 12.45 points.
            [[],    '', ['.']],        # .
            [[],    '', ['.', '.']]    # Length = 100m..
        ]
        saw = Sentences.load(Item(), text)
        #print(self._form(saw))
        self.assertEqual(self._form(saw), expect)

        text = "Test! ! ft.?. start..end ..before and.  ?!.ending text"
        expect = [
            [[],         '', ['!']],            # Test!
            [[],         '', ['!']],            # !
            [[],         '', ['.', '?', '.']],  # ft.?.
            [[],         '', ['.']],            # start..end ..before and.
            [['?', '!'], '', []]                # ?!.ending text
        ]
        saw = Sentences.load(Item(), text)
        self.assertEqual(self._form(saw), expect)

    def test_blocks(self):
        # [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}', ]

        # :x  x:y
        # +y  x+y
        # -x  x-y
        for rule in [':', '+', '-']:
            text = 'Too long{0} *{0}smile t{0}o and {0}{0}simple {0} again {0} ={0}st text '.format(rule)
            expect = [
                [[],    '', [rule]],   # Too long{0}
                [['*'], '', [rule]],   # {0}smile t{0}o and {0}{0}simple {0}
                [[],    '', [rule]],   # again {0}
                [['='], '', []]        # ={0}st text
            ]
            saw = Blocks.load(Item(), text)
            self.assertEqual(self._form(saw), expect)

        # ( x -> before
        # [ x -> before
        for complex in [['(', ')'], ['[', ']']]:
            text = '{0}text{1} {0}  new {1} {0}{0}two{1}{1} {0} {0} aaa {1} {1} aa{0}bbb ccc{1}ddd'.format(complex[0], complex[1])
            expect = [
                [[],    '', [rule]],   # Too long{0}
                [[],    '', [rule]],   # {0}smile t{0}o and {0}{0}simple {0}
                [[],    '', [rule]],   # again {0}
                [['='], '', []]        # ={0}st text
            ]
            saw = Blocks.load(Item(), text)
            #self.assertEqual(self._form(saw), expect)

        # x*y
        text = 'Text*new bb**cc *new test* ***st -*bb *pt-*nn aaa**'
        expect = [
            [[],              '', []],          # Text*new bb**cc
            [['*'],           '', ['*']],       # *new test*
            [['*', '*', '*'], '', []],          # ***st 
            [['-', '*'],      '', []],          # -*bb
            [['*'],           '', ['-', '*']],  # *pt-*
            [[],              '', ['*', '*']]   # nn aaa**
        ]
        saw = Blocks.load(Item(), text)
        self.assertEqual(self._form(saw), expect)


if __name__ == "__main__":
    unittest.main()