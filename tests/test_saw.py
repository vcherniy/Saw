import unittest
from saw.saw import Saw

class Test_Saw(unittest.TestCase):

    def setUp(self):
        text = "Starting right this second, it's way easier to merge Pull Requests! \
            We usually merge them from the comfortable glow of our computers, but with the\
            new mobile site we're comfortable merging smaller Pull Requests while sitting\
            on the hyperloop (or while on the bus, I guess).\n\n\
            >Seriously, you won't get anything meaningful out of this, people will vote \
            for the language they like and then bash the usual suspects (PHP, actionscript,\
            C++,...)\n\
            Why do you insist that is not meaningful? Of course they will vote for the\
            language they like, that is the purpose of the poll. Obviously people can \
            vote from ignorance, but that goes both ways. Just as some people 'dislike'\
            cobol despite a lack of experience with it."
        self.obj = Saw().load(text)

    def test_paragraphs(self):
        second_p = "Seriously, you won't get anything meaningful out of this, people will vote \
            for the language they like and then bash the usual suspects (PHP, actionscript,\
            C++,...)"
        obj = self.obj

        # count
        self.assertEqual(len(obj.paragraphs), 3)
        # str
        self.assertEqual(str(obj.paragraphs[1]), second_p)
        self.assertEqual(str(obj.paragraphs[1].full), second_p + "\n")
        # after/before
        self.assertEqual(obj.paragraphs[1].after, "\n")
        self.assertEqual(obj.paragraphs[1].before, '')
        # slices
        res = []
        for item in obj.paragraphs:
            res.append( item[:2] )
        self.assertEqual(res, ['St', '>S', 'Wh'])

    def test_sentences(self):
        four_c = 'Why do you insist that is not meaningful'
        obj = self.obj

        # children
        self.assertEqual(obj.paragraphs.sentences, obj.sentences)
        # count
        self.assertEqual(len(obj.sentences), 7)
        self.assertEqual(len(obj.paragraphs[-2:].sentences), len(obj.sentences[2:]))
        self.assertEqual(len(obj.paragraphs[1].sentences), 1)
        self.assertEqual(len(obj.paragraphs[1:].sentences), 5)
        # str
        self.assertEqual(str(obj.sentences[4]), four_c)
        self.assertEqual(obj.sentences[4].full, four_c + '?')
        self.assertEqual(str(obj.paragraphs[2]).sentences[0], four_c)
        self.assertEqual(str(obj.paragraphs[-2:].sentences), str(obj.sentences[2:]))
        # after/before
        self.assertEqual(obj.sentences[3].before, '')
        self.assertEqual(obj.sentences[4].after, '?')
        # slices
        s = ''
        for sen in obj.sentences:
            s += sen[0]
        self.assertEqual(s, 'SWSWOOJ')

    def test_blocks(self):
        third_from_end_b = 'Just as some people'
        obj = self.obj

        # children
        self.assertEqual(obj.paragraphs.sentences.blocks, obj.blocks)
        self.assertEqual(obj.sentences.blocks, obj.blocks)
        self.assertEqual(obj.paragraphs.blocks, obj.blocks)
        # count
        self.assertEqual(len(obj.blocks), 21)
        self.assertEqual(len(obj.paragraphs[2].blocks), len(obj.blocks[-8:]))
        self.assertEqual(len(obj.paragraphs[1:].sentences[2:].blocks), 7)
        # str
        self.assertEqual(str(obj.blocks[-3]), third_from_end_b)
        self.assertEqual(obj.blocks[-2].full, 'dislike')
        self.assertEqual(str(obj.paragraphs[2].blocks[5]), third_from_end_b)
        self.assertEqual(str(obj.blocks[-3:-1]), third_from_end_b + " 'dislike'")
        # after/before
        self.assertEqual(obj.blocks[4].before, '(')
        self.assertEqual(obj.blocks[4].after, ',')
        # slices
        s = ''
        for sen in obj.sentences:
            s += sen[0]
        self.assertEqual(s, 'SW>WOOJ')



if __name__ == "__main__":
    unittest.main()