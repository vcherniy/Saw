import unittest
from saw.parsers.sentences import Sentences
from saw.parsers.blocks import Blocks

from saw.parsers import Parser


class TestMods(unittest.TestCase):
    def setUp(self):
        Parser.enable_process_mods = True

    @staticmethod
    def _form(iem):
        return [[item.before() or [], item.text() or '', item.after() or []] for item in iem]

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
        saw = Sentences.load(text)
        self.assertEqual(self._form(saw), expect)

        text = "Test! ! ft.?. start..end ..before and.  ?!.ending text"
        expect = [
            [[],         '', ['!']],            # Test!
            [[],         '', ['!']],            # !
            [[],         '', ['.', '?', '.']],  # ft.?.
            [[],         '', ['.']],            # start..end ..before and.
            [['?', '!'], '', []]                # ?!.ending text
        ]
        saw = Sentences.load(text)
        self.assertEqual(self._form(saw), expect)

    def test_blocks(self):
        # [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}', ]
        # :x  x:y
        # +y  x+y
        # -x  x-y
        for rule in [':', '+', '-']:
            text = 'Too long{0} {0}newer dash.{0}new new{0}text'.format(rule)
            expect = [
                [[], '', [rule]],  # Too long{0}
                [[], '', []],      # {0}newer dash.{0}new new{0}text
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = 'Too long{0}{0} {0}{0}newer new{0}{0}text '.format(rule)
            expect = [
                [[],           '', [rule, rule]],  # Too long{0}{0}
                [[rule, rule], '', [rule, rule]],  # {0}{0}newer new{0}{0}
                [[],           '', []],            # text
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = 'Too long *{0} new{0}*text *{0}newer {0}*casual +-combo -'.format(rule)
            expect = [
                [[],          '', ['*', rule]],  # Too long *{0}
                [[],          '', [rule, '*']],  # new{0}*
                [[],          '', []],           # text
                [['*', rule], '', []],           # *{0}newer
                [[rule, '*'], '', []],           # {0}*casual
                [['+', '-'],  '', []],           # +-combo
                [[],          '', ['-']]         # -
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

        # ( x -> before
        # [ x -> before
        for st, fn in [['(', ')'], ['[', ']']]:
            text = '{0}text{1} {0}  new {1} {0}{0}two{1}{1} {0} {0} aaa {1} {1}'.format(st, fn)
            expect = [
                [[st], '', [fn]],  # {0}text{1}
                [[st], '', [fn]],  # {0}  new {1}
                [[st], '', []],    # {0}
                [[st], '', [fn]],  # {0}two{1}
                [[],   '', [fn]],  # {1}
                [[st], '', []],    # {0}
                [[st], '', [fn]],  # {0} aaa {1}
                [[],   '', [fn]],  # {1}
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = 'aa*{0}bbb ccc{1}ddd {1}{0}aaa cc *{1}{0} htc{1}'.format(st, fn)
            expect = [
                [[],   '', ['*']],      # aa*
                [[st], '', [fn]],       # {0}bbb ccc{1}
                [[],   '', [fn]],       # ddd {1}
                [[st], '', ['*', fn]],  # {0}aaa cc *{1}
                [[st], '', [fn]],       # {0} htc{1}
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = '{0} aa{0} fdf - {1}fdf{1}  {0} * kt'.format(st, fn)
            expect = [
                [[st], '', []],         # {0} aa
                [[st], '', ['-', fn]],  # {0} fdf - {1}
                [[],   '', [fn]],       # fdf{1}
                [[st], '', ['*']],      # {0}*
                [[],   '', []],         # kt
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = '{1}aabc{0}'.format(st, fn)
            expect = [
                [[],   '', [fn]],  # {1}
                [[],   '', []],    # aabc
                [[st], '', []],    # {0}
            ]
            saw = Blocks.load(text)
            #self.assertEqual(self._form(saw), expect)

    def test_blocks_asteriks(self):
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
        saw = Blocks.load(text)
        self.assertEqual(self._form(saw), expect)

        text = '*begin string'
        expect = [
            [['*'], '', []],       # *begin string
        ]
        saw = Blocks.load(text)
        self.assertEqual(self._form(saw), expect)


if __name__ == "__main__":
    unittest.main()