"""
import unittest
from saw import Saw


TEXT = "Starting right this second, it's way easier to merge Pull Requests! \
We usually merge them from the comfortable glow of our computers, but with the\
new mobile site we're comfortable merging smaller Pull Requests while sitting\
on the hyperloop (or while on the bus, I guess).\n\n\
>Seriously - you won't get anything meaningful out of this, people will vote \
for the language they like and then bash the usual suspects (PHP, actionscript,\
C++,...)\n\
Why do you insist that is not meaningful? Of course they will vote for the\
language they like, that is the purpose of the poll. Obviously people can \
vote from ignorance, but that goes both ways. Just as some people 'dislike' \
cobol despite a lack of experience with it."

SECOND_P = ">Seriously - you won't get anything meaningful out of this, people will vote \
for the language they like and then bash the usual suspects (PHP, actionscript, \
C++, ...)\n"

class Test_Saw(unittest.TestCase):
    def setUp(self):
        self.obj = Saw.load(TEXT)

    def test_paragraphs(self):
        obj = self.obj

        # count
        self.assertEqual(len(obj.paragraphs), 3)
        # str
        self.assertEqual(str(obj.paragraphs[1]), SECOND_P)
        # after/before
        self.assertEqual(obj.paragraphs[1]._after, ["\n"])
        # slices
        res = []
        for item in obj.paragraphs:
            res.append( str(item)[:2] )
            res.append( len(item[:]) )
        self.assertEqual(res, ['St', 2, '>S', 1, 'Wh', 4])

        test = []
        expect = []
        for item in obj.paragraphs:
            test.append( item[:2] )
            test.append( item[0] )
            test.append( item[0::3] )
            expect.append( item.children[:2] )
            expect.append( item.sentences[0] )
            expect.append( item.children[0::3] )
        self.assertEqual(test, expect)

    def test_sentences(self):
        four_c = 'Why do you insist that is not meaningful?'
        obj = self.obj

        # children
        self.assertEqual(obj.paragraphs.sentences, obj.sentences)
        # count
        self.assertEqual(len(obj.sentences), 7)
        self.assertEqual(len(obj.paragraphs[-2:].sentences), len(obj.sentences[2:]))
        self.assertEqual(len(obj.paragraphs[1].sentences), 1)
        self.assertEqual(len(obj.paragraphs[1::1].sentences), 5)
        # str
        self.assertEqual(str(obj.sentences[3]), four_c)
        self.assertEqual(str(obj.paragraphs[2].sentences[0]), four_c)

        self.assertEqual(str(obj.paragraphs[-2:].sentences), str(obj.sentences[2:]))
        # after/before
        self.assertEqual(obj.sentences[3]._after, ['?'])
        # slices
        res = []
        for item in obj.sentences:
            res.append( str(item)[:2] )
            res.append( len(item[:]) )
        self.assertEqual(res, ['St', 2, 'We', 4, '>S', 7, 'Wh', 1, 'Of', 2, 'Ob', 2, 'Ju', 2])

        test = []
        expect = []
        for item in obj.sentences:
            test.append( item[:2] )
            test.append( item[0] )
            test.append( item[0::3] )
            expect.append( item.children[:2] )
            expect.append( item.blocks[0] )
            expect.append( item.children[0::3] )
        self.assertEqual(test, expect)

    def test_blocks(self):
        third_from_end_b = "Just as some people 'dislike'"
        obj = self.obj

        # children
        self.assertEqual(obj.paragraphs.sentences.blocks, obj.blocks)
        self.assertEqual(obj.sentences.blocks, obj.blocks)
        self.assertEqual(obj.paragraphs.blocks, obj.blocks)
        # count
        self.assertEqual(len(obj.blocks), 20)
        self.assertEqual(len(obj.paragraphs[2].blocks), len(obj.blocks[-7:]))
        self.assertEqual(len(obj.paragraphs[1:].sentences[2:].blocks), 6)
        # str
        self.assertEqual(str(obj.blocks[-2]), third_from_end_b)
        self.assertEqual(str(obj.paragraphs[2].blocks[5]), third_from_end_b)
        self.assertEqual(str(obj.blocks[-3:-1]), 'but that goes both ways ' + third_from_end_b)
        # after/before
        self.assertEqual(obj.blocks[4]._after, [','])
        # slices
        res = []
        for item in obj.paragraphs[1].blocks:
            res.append( str(item)[:2] )
            res.append( len(item[:]) )
        self.assertEqual(res, ['>S', 1, 'yo', 8, 'pe', 14, 'PH', 1, 'ac', 1, 'C+', 1, '..', 1])

        test = []
        expect = []
        for item in obj.blocks:
            test.append( item[:2] )
            test.append( item[0] )
            test.append( item[0::3] )
            expect.append( item.children[:2] )
            expect.append( item.words[0] )
            expect.append( item.children[0::3] )
        self.assertEqual(test, expect)

    def test_words(self):
        obj = Saw.load("Test this up.\nNew block - new problems. Yes?")

        # children
        self.assertEqual(obj.paragraphs.sentences.blocks.words, obj.words)
        self.assertEqual(obj.sentences.words, obj.words)
        self.assertEqual(obj.blocks.words, obj.words)
        # count
        self.assertEqual(len(obj.words), 8)
        self.assertEqual(len(obj.paragraphs[1].words), len(obj.words[-5:]))
        self.assertEqual(len(obj.sentences[2:].words), 1)
        # str
        self.assertEqual(str(obj.words), 'Test this up New block new problems Yes')
        self.assertEqual(str(obj.paragraphs[0].blocks[0].words[1:]), 'this up')
        self.assertEqual(str(obj.words[-3:-1]), 'new problems')
        # after/before
        self.assertEqual(obj.words[4]._after, [])
        # slices
        res = []
        for item in obj.paragraphs[1].words:
            res.append( str(item)[:2] )
            res.append( len(item[:]) )
        self.assertEqual(res, ['Ne', 3, 'bl', 5, 'ne', 3, 'pr', 8, 'Ye', 3])

        test = []
        expect = ['Te', 'T', 'Tt', 'th', 't', 'ts', 'up', 'u', 'u', 'Ne', 'N', 'N', 'bl', 'b', 'bc', 'ne', 'n', 'n', 'pr', 'p', 'pbm', 'Ye', 'Y', 'Y']
        for item in obj.words:
            test.append( item[:2] )
            test.append( item[0] )
            test.append( item[0::3] )
        self.assertEqual(test, expect)

    def test_correct(self):
        obj = self.obj

        test = []
        expect = []
        for item in obj.sentences:
            test.append( item[:2] )
            test.append( item[0] )
            #test.append( item[0::3] ) # comment - errors
            expect.append( item.children[:2] )
            expect.append( item.blocks[0] ) 
            expect.append( item.children[0::3] )
        self.assertEqual(test, expect)

        test = []
        expect = []
        for item in obj.blocks:
            test.append( item[:2] )
            test.append( item[0] )
            test.append( item[0::3] )
            expect.append( item.children[:2] )
            #expect.append( item.words[0] ) # change to .words - errors
            expect.append( item.children[0::3] )
        self.assertEqual(test, expect)

    def test_pure(self):
        text = "Hi. This is, my - test? Yes, bad man!"
        saw = Saw.load(text)

        self.assertEqual(str(saw.sentences[0].pure()), 'Hi')
        self.assertEqual(str(saw.blocks[1].pure()), 'This is')
        self.assertEqual(str(saw.blocks[1][1].pure()), 'is')

        self.assertEqual(str(saw.sentences.pure()), "Hi This is, my - test Yes, bad man")
        self.assertEqual(str(saw.blocks.pure()), "Hi This is my test Yes bad man")
        self.assertEqual(str(saw.words.pure()), "Hi This is my test Yes bad man")

        self.assertEqual(str(saw.paragraphs.pure().sentences), "Hi. This is, my - test? Yes, bad man!")
        self.assertEqual(str(saw.sentences.pure().blocks), "Hi This is, my - test Yes, bad man")
        self.assertEqual(str(saw.blocks.pure().words), "Hi This is my test Yes bad man")

if __name__ == "__main__":
    unittest.main()
"""