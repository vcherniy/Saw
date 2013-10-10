import unittest
from saw.saw import Saw

class Test_Saw(unittest.TestCase):

    def setUp(self):
        text = "Starting right this second, it's way easier to merge Pull Requests! \
            We usually merge them from the comfortable glow of our computers, but with the\
            new mobile site we're comfortable merging smaller Pull Requests while sitting\
            on the hyperloop (or while on the bus, I guess)."
        self.obj = Saw().load(text)

    def test_saw(self):
        self.assertEqual(self.obj.paragraphs[0].sentences[0].blocks, self.obj.blocks)


if __name__ == "__main__":
    unittest.main()