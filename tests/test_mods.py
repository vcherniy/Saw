import unittest
from saw.saw import Saw
from saw.parsers import Mod, Parser


class TestMods(unittest.TestCase):
    def setUp(self):
        Parser.enable_process_mods = True

    @staticmethod
    def _form(iem):
        return [[item.before() or [], item.text() or '', item.after() or []] for item in iem]

    def test_sentences(self):
        """
        Explode by: ? ! .
        """
        text = '?Around! Double after?!Spaces    ? .That 12.45 float.   .   Long space before and double dot..'
        expect = [['?'], 'Around', ['! '], 'Double after', ['?', '!'], 'Spaces', [' ? '],
                         '.That 12.45 float', ['. ', ' . '], 'Long space before and double dot', ['.', '.']]
        self.assertEqual(Saw.sentences.process_mods(Saw.sentences.parse(text)), expect)

        text = "Double over space! ! Three different.?. double..between ..double before, and one after.  end string"
        expect = [[], 'Double over space', ['! ', ' ! '], 'Three different', ['.', '?', '. '],
                      'double..between ..double before, and one after', ['. '], 'end string', []]
        self.assertEqual(Saw.sentences.process_mods(Saw.sentences.parse(text)), expect)

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
            saw = Saw.blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = 'Too long{0}{0} {0}{0}newer new{0}{0}text '.format(rule)
            expect = [
                [[],           '', [rule, rule]],  # Too long{0}{0}
                [[rule, rule], '', [rule, rule]],  # {0}{0}newer new{0}{0}
                [[],           '', []],            # text
            ]
            saw = Saw.blocks.load(text)
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
            saw = Saw.blocks.load(text)
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
            saw = Saw.blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = 'aa*{0}bbb ccc{1}ddd {1}{0}aaa cc *{1}{0} htc{1}'.format(st, fn)
            expect = [
                [[],   '', ['*']],      # aa*
                [[st], '', [fn]],       # {0}bbb ccc{1}
                [[],   '', [fn]],       # ddd {1}
                [[st], '', ['*', fn]],  # {0}aaa cc *{1}
                [[st], '', [fn]],       # {0} htc{1}
            ]
            saw = Saw.blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = '{0} aa{0} fdf - {1}fdf{1}  {0} * kt'.format(st, fn)
            expect = [
                [[st], '', []],         # {0} aa
                [[st], '', ['-', fn]],  # {0} fdf - {1}
                [[],   '', [fn]],       # fdf{1}
                [[st], '', ['*']],      # {0}*
                [[],   '', []],         # kt
            ]
            saw = Saw.blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = '{1}aabc{0}'.format(st, fn)
            expect = [
                [[],   '', [fn]],  # {1}
                [[],   '', []],    # aabc
                [[st], '', []],    # {0}
            ]
            saw = Saw.blocks.load(text)
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
        saw = Saw.blocks.load(text)
        self.assertEqual(self._form(saw), expect)

        text = '*begin string'
        expect = [
            [['*'], '', []],       # *begin string
        ]
        saw = Saw.blocks.load(text)
        self.assertEqual(self._form(saw), expect)

    def test_no_type(self):
        try:
            Mod.get('no_type_exists', [], 'any text', [], False)
            assert False
        except Exception, e:
            assert str(e) == "Mods not found!"


if __name__ == "__main__":
    unittest.main()
