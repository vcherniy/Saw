import unittest

from saw.parser.blocks import Blocks

class Test_Saw(unittest.TestCase):

    def setUp(self):
        pass

    def test_blocks(self):
        single_rules = [',', ':', '=', '+', ';', '*']
        for rule in single_rules:
            """
            Test with:
            space after, space before, space around, another symbols
            few spaces - to one space
            """
            t_rule = tuple([rule])
            text = "This example%s  with %s anoher. comb!  of %sspaces" % [rule] * 3
            expect = ['This example', t_rule, 'with', t_rule, 'another. comb!  of', t_rule, 'spaces']
            self.assertEqual(Blocks.parse(text), expect)

            """
            Test with:
            dublicated symbols, another symbol beetwen dublicated (or from this range)
            symbol in end of string - not empty value
            """
            d_rule = tuple([rule, rule])
            d_with_mixin = tuple([rule, ',', rule])
            text = "This example%s%s with %s,%s anoher %s.%s spaces%s" % [rule] * 7
            expect = ['This example', d_rule, 'with', d_with_mixin, 'another',  t_rule, '.', t_rule, 'spaces', t_rule]
            self.assertEqual(Blocks.parse(text), expect)

            #@TODO: "-"

        double_rule_begin = ['{', '(', '[', '"', "'"]
        double_rule_end   = ['}', ')', ']', '"', "'"]
        
        double_rules = zip(double_rule_begin, double_rule_end)

        for rule in double_rules:
            



        res = Blocks.parse('Nine - number')
        self.assertEqual(res, ['Nine', ('-'), 'number'])

        res = Blocks.parse('Cat (or dog) name')
        self.assertEqual(res, ['cat', ('('), 'or dog', (')'), 'name')

        res = Blocks.parse('Cat (or dog (or poni)) name')
        self.assertEqual(res, ['cat', ('('), 'or dog', ('('), 'or poni', (')', ')'), 'name')

        res = Blocks.parse('The Car "Micro" fired')
        self.assertEqual(res, ['The Car', ('"'), 'Micro', ('"'), 'fired'])

if __name__ == "__main__":
    unittest.main()