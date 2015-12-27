import unittest
from saw.saw import Saw


class TestParsers(unittest.TestCase):
    def setUp(self):
        pass

    def test_paragraphs(self):
        """
        Explode by: \n
        """
        text = "Ignore spaces around:   \n - no space,\ndouble\n\n ...and again \n \n , but \n.\n."
        expect = [[], 'Ignore spaces around:', ["\n"], '- no space,', ["\n"], 'double', ["\n", "\n"],
                      '...and again', ["\n", "\n"], ', but', ["\n"], '.', ["\n"], '.', []]
        self.assertEqual(Saw.paragraphs.parse(text), expect)

    def test_sentences(self):
        """
        Explode by: ? ! .
        """
        text = '?Around! Double after?!Spaces    ? .That 12.45 float.   .   Long space before and double dot..'
        expect = [['?'], 'Around', ['! '], 'Double after', ['?', '!'], 'Spaces', [' ? ', ' .'],
                         'That 12', ['.'], '45 float', ['. ', ' . '],
                         'Long space before and double dot', ['.', '.']]
        self.assertEqual(Saw.sentences.parse(text), expect)

        text = "Double over space! ! Three different.?. double..between ..double before, and one after.  end string"
        expect = [[], 'Double over space', ['! ', ' ! '], 'Three different', ['.', '?', '. '],
                      'double', ['.', '.'], 'between', [' .', '.'], 'double before, and one after', ['. '],
                      'end string', []]
        self.assertEqual(Saw.sentences.parse(text), expect)

    def test_blocks(self):
        """
        Explode by: follow list 'rules'
        """

        for rule in Saw.blocks._delimiters:
            l_rule = ' ' + rule
            r_rule = rule + ' '
            a_rule = ' ' + rule + ' '

            # Test: spaces before, after, around; another symbols; few spaces
            text = "Many spaces after{0}   and {0} around. Single!  and {0}before".format(rule)
            expect = [[], 'Many spaces after', [r_rule], 'and', [a_rule],
                          'around. Single!  and', [l_rule], 'before', []]
            self.assertEqual(Saw.blocks.parse(text), expect)

            # Test: another symbol between it; symbol in the end of string.
            text = "{0}In begin. {0},{0} with symbols between {0}.{0} and in end of text{0}".format(rule)
            expect = [[rule], 'In begin.', [l_rule, ',', r_rule], 'with symbols between', [l_rule], '.', [r_rule],
                              'and in end of text', [rule]]
            self.assertEqual(Saw.blocks.parse(text), expect)

            # Test: duplicated symbols
            text = "Double after{0}{0}   double before. {0}{0}and space after symbol in end{0} ".format(rule)
            expect = [[], 'Double after', [rule, r_rule], 'double before.', [l_rule, rule],
                          'and space after symbol in end', [r_rule]]
            self.assertEqual(Saw.blocks.parse(text), expect)

            # Test: inject symbols to strings
            text = "Inject in te{0}xt and double in{0}{0}ject".format(rule)
            expect = [[], 'Inject in te', [rule], 'xt and double in', [rule, rule], 'ject', []]
            self.assertEqual(Saw.blocks.parse(text), expect)

    def test_words(self):
        """
        Explode by: spaces
        """
        text = "Text with  many  .   spaces. and: -,end string  "
        expect = ['Text', 'with', 'many', '.', 'spaces.', 'and:', '-,end', 'string']
        self.assertEqual(Saw.words.parse(text), expect)

        # @TODO
        # test _append method if child class is none
        # to 100% test coverage
        #saw = Saw.words.load('Test it')
        #item = Saw.words._append(saw, 'Re')
        #saw.assertEqual(item.text(), 'Re')
        #saw.assertEqual(item.type(), '')


if __name__ == "__main__":
    unittest.main()
