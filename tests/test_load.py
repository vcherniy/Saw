import unittest

from saw.parsers.blocks import Blocks
from saw.parsers.words import Words
from saw.parsers.sentences import Sentences
from saw.parsers.paragraphs import Paragraphs

from saw.parsers import Parser


class TestLoad(unittest.TestCase):
    def setUp(self):
        Parser.enable_process_mods = False

    @staticmethod
    def _form(iem):
        return [[item.before(), item.text(), item.after()] for item in iem]

    def test_paragraphs(self):
        text = "Hi. Mine. \n These items:\n- First item,\n- Second item,   \n - Third item  .\n\nEnded\n"
        expect = [
            [[], '', ["\n"]],        # Hi. Mine. \n
            [[], '', ["\n"]],        # These items:\n
            [[], '', ["\n"]],        # - First item,\n
            [[], '', ["\n"]],        # - Second item,   \n
            [[], '', ["\n", "\n"]],  # - Third item  .\n\n
            [[], '', ["\n"]]         # Ended\n
        ]
        saw = Paragraphs.load(text)
        self.assertEqual(self._form(saw), expect)

    def test_sentences(self):
        text = '?1 sentence! But what!!WTF   ? .That 12.45 points.   .   Length = 100m..'
        expect = [
            [['?'], '', ['!']],        # ?1 sentence!
            [[],    '', ['!', '!']],   # But what!!
            [[],    '', ['?']],        # WTF   ?
            [['.'], '', ['.']],        # .That 12.
            [[],    '', ['.']],        # 45 points.
            [[],    '', ['.']],        # .
            [[],    '', ['.', '.']]    # Length = 100m..
        ]
        saw = Sentences.load(text)
        self.assertEqual(self._form(saw), expect)

        text = "Test! ! ft.?. start..end ..before and.  ?.ending text"
        expect = [
            [[],         '', ['!']],            # Test!
            [[],         '', ['!']],            # !
            [[],         '', ['.', '?', '.']],  # ft.?.
            [[],         '', ['.', '.']],       # start..
            [[],         '', []],               # end
            [['.', '.'], '', ['.']],            # ..before and.
            [['?', '.'], '', []]                # ?.ending text
        ]
        saw = Sentences.load(text)
        self.assertEqual(self._form(saw), expect)

    def test_blocks(self):
        rules = [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}', ]

        for rule in rules:
            text = "This example{0}   with {0} another. comb!  of {0}spaces".format(rule)
            expect = [
                [[],     '', [rule]],   # This example{0}
                [[],     '', [rule]],   # with {0}
                [[],     '', []],       # another. comb!  of
                [[rule], '', []]        # {0}spaces
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = "{0}This example{0}{0}   with. {0},{0} another {0}.{0} spaces{0}".format(rule)
            expect = [
                [[rule], '', [rule, rule]],         # {0}This example{0}{0}
                [[],     '', [rule, ',', rule]],    # with. {0},{0}
                [[],     '', []],                   # another
                [[rule], '', [rule]],               # {0}.{0}
                [[],     '', [rule]],               # spaces{0}
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = "Text {0}{0}no{0}br to t{0}{0}mobile".format(rule)
            expect = [
                [[],            '', []],            # Text
                [[rule, rule],  '', [rule]],        # {0}{0}no{0}
                [[],            '', [rule, rule]],  # br to t{0}{0}
                [[],            '', []]             # mobile
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

            text = "{0}{0} {0}This example{0}{0} spaces{0} {0}{0}".format(rule)
            expect = [
                [[],     '', [rule, rule]],  # {0}{0}
                [[rule], '', [rule, rule]],  # {0}This example{0}{0}
                [[],     '', [rule]],        # spaces{0}
                [[],     '', [rule, rule]],  # {0}{0}
            ]
            saw = Blocks.load(text)
            self.assertEqual(self._form(saw), expect)

    def test_words(self):
        text = "Test with  many  .   spaces. and: -,end  "
        expect = [
            [[], 'Test',    []],
            [[], 'with',    []],
            [[], 'many',    []],
            [[], '.',       []],
            [[], 'spaces.', []],
            [[], 'and:',    []],
            [[], '-,end',   []]
        ]
        saw = Words.load(text)
        self.assertEqual(self._form(saw), expect)


if __name__ == "__main__":
    unittest.main()
