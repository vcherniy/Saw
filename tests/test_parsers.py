import unittest

from saw.parser.blocks import Blocks
from saw.parser.words import Words
from saw.parser.sentences import Sentences
from saw.parser.paragraphs import Paragraphs

class Test_Saw(unittest.TestCase):

    def setUp(self):
        pass

    def test_blocks(self):
        single_rules = [',', ':', '=', '+', ';', '*', ' -', '- '\
            '{', '(', '[', ']', ')', '}', '"', "'"]

        for rule in single_rules:
            # striped rule
            srule = rule.strip()
            """
            Test with:
            space after, space before, space around, another symbols
            few spaces - to one space
            """
            text = "This example%s   with %s anoher. comb!  of %sspaces" % [rule] * 3
            expect = ['This example', [srule], 'with', [srule], 'another. comb!  of', [srule], 'spaces']
            self.assertEqual(Blocks.parse(text), expect)

            """
            Test with:
            dublicated symbols, another symbol beetwen dublicated (or from this range)
            symbol in end of string - not empty value
            """
            text = "%s This example%s%s   with. %s,%s anoher %s.%s spaces%s" % [rule] * 8
            expect = [[srule], 'This example', [srule, srule], 'with.', [srule, ',', srule], 'another',  [srule], '.', [srule], 'spaces', [srule]]
            self.assertEqual(Blocks.parse(text), expect)

    def test_words(self):
        text = "Test with  many  . spaces. and: -,end  "
        expect = ['Test', 'with', 'many', '.', 'spaces.', 'and:', '-,end']
        self.assertEqual(Words.parse(text), expect)

    def test_sentences(self):
        text = '1 sentence! But what!!WTF ? That 12.45 points. '
        expect = ['1 sentence', ['!'], 'But what', ['!', '!'], 'WTF', ['?'], 'That 12.45 points', ['.']]
        self.assertEqual(Sentences.parse(text), expect)

    def test_paragraphs(self):
        text = "Hi. Hola. \n These items:\n- First item,\n- Second item,   \n - Third item  .\n\nEnded\n"
        expect = ['Hi. Hola.', ["\n"], 'These items:', ["\n"], '- First item,', ["\n"], '- Second item,', ["\n"], '- Third item  .', ["\n", "\n"], "Ended", ["\n"]]
        self.assertEqual(Paragraphs.parse(text), expect)


if __name__ == "__main__":
    unittest.main()