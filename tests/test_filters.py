import unittest
from saw.parsers import Parser
from saw.saw import Saw
from saw.filters import Filter


class TestFilters(unittest.TestCase):
    def setUp(self):
        pass

    def test_index(self):
        # create instance for each use
        text = 'xaa, dfs-* na. pa?'
        node = Saw.load(text)
        _ = node.pure()
        self.assertEqual(str(node), text)

        # Filter.init already called
        self.assertEqual(Filter.exists('lower'), True)
        self.assertEqual(Filter.exists('fake'), False)

    def test_pure(self):
        node = Saw.load('xaa , dfs -* na. pa?')
        self.assertEqual(str(node.pure()), 'xaa dfs na pa')

        # with enabled mods
        node = Saw.load(':test .its any*text -fuck')
        self.assertEqual(str(node.pure()), ':test .its any*text-fuck')
        # without enabled mods
        Parser.enable_process_mods = False
        node = Saw.load(':test .its any*text -fuck')
        self.assertEqual(str(node.pure()), 'test its any text fuck')
        Parser.enable_process_mods = True

    def test_lower(self):
        node = Saw.load('Any TEXT, 12Month aNu -- o')
        self.assertEqual(str(node.lower()), 'any text, 12month anu-- o')

    def test_filter(self):
        node = Saw.words.load('Any fucking words may be there')
        result = node.filter(lambda x: len(x.text()) > 3)
        self.assertEqual(str(result), 'fucking words there')
        self.assertEqual(result, Saw.words.load('fucking words there'))

    def test_filter_not_exists(self):
        try:
            node = Saw.load('Any')
            Filter.get('no_filter_exists', node)
            assert False
        except Exception, e:
            assert str(e) == "Filter not found!"

    def test_not_exists_method_filter(self):
        node = Saw.load('Any')
        # check correct init and executing incorrect named method
        from saw.filters.bad_filter_for_test import Bad_Filter_For_Test
        _filter = Bad_Filter_For_Test()
        _filter.filter__(node, lambda x: x)

        try:
            Filter.get('bad_filter_for_test', node)
            assert False
        except Exception, e:
            assert str(e) == "Filter '%s' has not main method!" % 'bad_filter_for_test'

    def test_each(self):
    	node = Saw.load('Test it, for each')

    	self.assertEqual(node.each().get(), node.type(''))
    	#self.assertEqual(node.blocks.each()[0].get().words, Saw.load('test for').words)
    	#self.assertEqual(node.words.each()[:2].upper().get(true), Saw.words.load('TE IT FO EA').type(''))


if __name__ == "__main__":
    unittest.main()
