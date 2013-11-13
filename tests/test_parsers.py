import unittest

from saw.parsers.blocks import Blocks
from saw.parsers.words import Words
from saw.parsers.sentences import Sentences
from saw.parsers.paragraphs import Paragraphs


class TestSaw(unittest.TestCase):
    def setUp(self):
        pass

    def test_paragraphs(self):
        """
        Explode by: \n
        """
        text = "Hi. Mine. \n These items:\n- First item,\n- Second item,   \n - Third item  .\n\nEnded\n"
        expect = ['Hi. Mine.', ["\n"], 'These items:', ["\n"], '- First item,', ["\n"], '- Second item,', ["\n"],
                  '- Third item  .', ["\n", "\n"], 'Ended', ["\n"]]
        self.assertEqual(Paragraphs.parse(text), expect)

    def test_sentences(self):
        """
        Explode by: ? ! .
        """
        text = '?1 sentence! But what!!WTF   ? .That 12.45 points.   .   Length = 100m..'
        expect = [['?'], '1 sentence', ['! '], 'But what', ['!', '!'], 'WTF', [' ? ', ' .'], 'That 12',
                  ['.'], '45 points', ['. ', ' . '], 'Length = 100m', ['.', '.']]
        self.assertEqual(Sentences.parse(text), expect)

        text = "Test! ! ft.?. start..end ..before and.  ending text"
        expect = ['Test', ['! ', ' ! '], 'ft', ['.', '?', '. '], 'start', ['.', '.'], 'end',
                  [' .', '.'], 'before and', ['. '], 'ending text']
        self.assertEqual(Sentences.parse(text), expect)

    def test_blocks(self):
        """
        Explode by: follow list 'rules'
        """
        rules = [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}', ]

        for rule in rules:
            l_rule = ' ' + rule
            r_rule = rule + ' '
            a_rule = ' ' + rule + ' '

            # Test: spaces before, after, around; another symbols; few spaces
            text = "This example{0}   with {0} another. comb!  of {0}spaces".format(rule)
            expect = ['This example', [r_rule], 'with', [a_rule], 'another. comb!  of', [l_rule], 'spaces']
            self.assertEqual(Blocks.parse(text), expect)

            # Test: duplicated symbols, another symbol between it; symbol in the end of string.
            text = "{0}This example{0}{0}   with. {0},{0} another {0}.{0} spaces{0}".format(rule)
            expect = [[rule], 'This example', [rule, r_rule], 'with.', [l_rule, ',', r_rule], 'another',
                      [l_rule], '.', [r_rule], 'spaces', [rule]]
            self.assertEqual(Blocks.parse(text), expect)

            # Test: inject symbols to strings
            text = "Text {0}{0}no{0}br to t{0}{0}mobile".format(rule)
            expect = ['Text', [l_rule, rule], 'no', [rule], 'br to t', [rule, rule], 'mobile']
            self.assertEqual(Blocks.parse(text), expect)

    def test_words(self):
        """
        Explode by: spaces
        """
        text = "Test with  many  .   spaces. and: -,end  "
        expect = ['Test', 'with', 'many', '.', 'spaces.', 'and:', '-,end']
        self.assertEqual(Words.parse(text), expect)


if __name__ == "__main__":
    unittest.main()