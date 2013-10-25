import unittest

from saw.parsers.blocks import Blocks
from saw.parsers.words import Words
from saw.parsers.sentences import Sentences
from saw.parsers.paragraphs import Paragraphs

class Test_Saw(unittest.TestCase):

    def setUp(self):
        pass

    def test_blocks(self):
        single_rules = [',', ':', '=', '+', ';', '*',\
            '{', '(', '[', ']', ')', '}', '"'\
            , '- ', "' ", \
            ' -', " '", '-', "'"]

        for rule in single_rules:
            # striped rule
            srule = rule.strip()
            """
            Test with:
            space after, space before, space around, another symbols
            few spaces - to one space
            """
            text = "This example{0}   with {0} another. comb!  of {0}spaces".format(rule)
            if rule in [' -', " '", '-', "'"]:
                expect = ['This example', [srule], 'with', [srule], 'another. comb!  of ' + rule + 'spaces']
            else:
                expect = ['This example', [srule], 'with', [srule], 'another. comb!  of', [srule], 'spaces']
            self.assertEqual(Blocks.parse(text), expect)

            """
            Test with:
            dublicated symbols, another symbol beetwen dublicated (or from this range)
            symbol in end of string - not empty value
            """
            text = "{0}This example{0}{0}   with. {0},{0} another {0}.{0} spaces{0}".format(rule)
            if rule in ['- ', "' "]:
                expect = [[srule], 'This example', [srule], [srule], 'with.', [srule], [',', srule], 'another', [srule], '.', [srule], 'spaces', [srule]]
            elif rule in [' -', " '"]:
                expect = [srule + 'This example', [srule], [srule], 'with.', [srule, ','], [srule], 'another ' + rule + '.', [srule], 'spaces', [srule]]    
            elif rule in ['-', "'"]:
                expect = [rule + 'This example', [srule, srule], 'with.', [srule, ',', srule], 'another ' + rule + '.', [srule], 'spaces', [srule]]
            else:
                expect = [[srule], 'This example', [srule, srule], 'with.', [srule, ',', srule], 'another',  [srule], '.', [srule], 'spaces', [srule]]
            self.assertEqual(Blocks.parse(text), expect)

            """Test with:
            inject nodes to strings
            """
            text = "Text {0}{0}no{0}br to t{0}{0}mobile".format(rule)
            if rule in ['- ', "' "]:
                expect = ['Text', [srule], [srule], 'no', [srule], 'br to t', [srule], [srule], 'mobile']
            elif rule in [' -', " '"]:
                expect = ['Text', [srule], srule + 'no' + rule + 'br to t', [srule], srule + 'mobile']
            elif rule in ['-', "'"]:
                expect = ['Text ' + rule + rule + 'no' + rule + 'br to t' + rule + rule + 'mobile']
            else:
                expect = ['Text', [srule, srule], 'no', [srule], 'br to t', [srule, srule], 'mobile']
            self.assertEqual(Blocks.parse(text), expect)
            

    def test_words(self):
        text = "Test with  many  . spaces. and: -,end  "
        expect = ['Test', 'with', 'many', '.', 'spaces.', 'and:', '-,end']
        self.assertEqual(Words.parse(text), expect)

    def test_sentences(self):
        text = '?1 sentence! But what!!WTF ? .That 12.45 points. . Lenght = 100m..'
        expect = [['?'], '1 sentence', ['!'], 'But what', ['!', '!'], 'WTF', ['?'], '.That 12.45 points', ['.'], ['.'], 'Lenght = 100m', ['.', '.']]
        self.assertEqual(Sentences.parse(text), expect)

        text = "Test! ! ft.?. a..b ..before and. ending text"
        expect = ['Test', ['!'], ['!'], 'ft', ['.', '?', '.'], 'a..b ..before and', ['.'], 'ending text']
        self.assertEqual(Sentences.parse(text), expect)

    def test_paragraphs(self):
        text = "Hi. Hola. \n These items:\n- First item,\n- Second item,   \n - Third item  .\n\nEnded\n"
        expect = ['Hi. Hola.', ["\n"], 'These items:', ["\n"], '- First item,', ["\n"], '- Second item,', ["\n"], '- Third item  .', ["\n", "\n"], "Ended", ["\n"]]
        self.assertEqual(Paragraphs.parse(text), expect)


if __name__ == "__main__":
    unittest.main()