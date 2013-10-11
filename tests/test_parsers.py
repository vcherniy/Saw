import unittest

from saw.parser.blocks import Blocks

class Test_Saw(unittest.TestCase):

    def setUp(self):
        pass

    def test_blocks(self):
        res = Blocks.parse('John, stand up!')
        self.assertEqual(res, [['John', ','], ['stand up!', '']])

        res = Blocks.parse('Enter that: pin code.')
        self.assertEqual(res, [['Enter that', ':'], ['pin code.', '']])

        res = Blocks.parse('Limite it:: hey,')
        self.assertEqual(res, [['Limite it', '::'], ['hey', ',']])

if __name__ == "__main__":
    unittest.main()