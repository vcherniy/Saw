import unittest
#from saw.parsers.paragraphs import Paragraphs
from saw.parsers.sentences import Sentences
from saw.parsers.blocks import Blocks
#from saw.parsers.words import Words

from saw.parsers import Item


class TestMods(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def _form(iem):
        return [[item._before or [], item._text or '', item._after or []] for item in iem.children]

    def test_sentences(self):
        text = '?1 sentence! But what!!WTF   ? .That 12.45 points.   .   Length = 100m..'
        expect = [
            [['?'], '', ['!']],        # ?1 sentence!
            [[],    '', ['!', '!']],   # But what!!
            [[],    '', ['?']],        # WTF   ?
            [[],    '', ['.']],        # .That 12.45 points.
            [[],    '', ['.']],        # .
            [[],    '', ['.', '.']]    # Length = 100m..
        ]
        saw = Sentences.load(Item(), text)
        self.assertEqual(self._form(saw), expect)

        text = "Test! ! ft.?. start..end ..before and.  .!.ending text"
        expect = [
            [[],         '', ['!']],            # Test!
            [[],         '', ['!']],            # !
            [[],         '', ['.', '?', '.']],  # ft.?.
            [[],         '', ['.']],            # start..end ..before and.
            [['.', '!'], '', []]                # .!.ending text
        ]
        saw = Sentences.load(Item(), text)
        self.assertEqual(self._form(saw), expect)

    def test_blocks(self):
        # [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}', ]
        text = 'Too long: :smil:e, for-and and -simple=at, (connect af) 12; *test* and "now" {text again }'
        expect = [
            [[], '', [',']],    # Too long smile. for-and and -simple
            [[], '', ['(']],    # (
            [[], '', [')']],     # connect af)
            [[], '', []]        # 12
        ]
        saw = Blocks.load(Item(), text)
        self.assertEqual(self._form(saw), expect)


if __name__ == "__main__":
    unittest.main()