#! /usr/bin/env python
import unittest
from copy import deepcopy
import os
from peyutil.test.support.pathmap import get_test_path_mapper
from peyutil import write_to_filepath
from peyutil import (NewickTokenizer, NewickEvents, NewickEventFactory, StringIO)

path_map = get_test_path_mapper()


class TestNewickTokenizer(unittest.TestCase):
    def testNoArg(self):
        self.assertRaises(ValueError, NewickTokenizer)

    def testNotStartingWithOpenParens(self):
        self.assertRaises(ValueError, NewickTokenizer, newick='hi')

    def testExtraSuffix(self):
        nt = NewickTokenizer(newick='(a,(b,c));suffix')
        self.assertRaises(ValueError, nt.tokens)

    def testUnclosed(self):
        nt = NewickTokenizer(newick='(a,(b,c)')
        self.assertRaises(ValueError, nt.tokens)

    def testExtraClosed(self):
        nt = NewickTokenizer(newick='(a,(b,c)));')
        self.assertRaises(ValueError, nt.tokens)

    def testPeekNone(self):
        nt = NewickTokenizer(newick='(a,(b,c));')
        nt.tokens()
        self.assertIsNone(nt._peek())

    def testSansComma(self):
        nt = NewickTokenizer(newick='(a,(b,c)(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def testUnclosedComment(self):
        nt = NewickTokenizer(newick='(a,(b,c),[(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def testCommaBefSemicolon(self):
        nt = NewickTokenizer(newick='(a,(b,c),(d,e)),;')
        self.assertRaises(ValueError, nt.tokens)

    def testUnexpectedComma(self):
        nt = NewickTokenizer(newick='(a,(b,c),,(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def testLabel(self):
        nt = NewickTokenizer(newick="(a\n'b',(b,c),(d,e));")
        self.assertRaises(ValueError, nt.tokens)

    def testQuotedEdgeInfo(self):
        exp = ['(', 'a', ',', '(', 'b', ',', 'c', ')', ':', '4', ',', '(', 'd', ',', 'e', ')', ')', ';']
        self._do_test("(a,(b,c):'4',(d,e));", exp)

    def testOpenClosed(self):
        nt = NewickTokenizer(newick='(a,(),(d,e));')
        self.assertRaises(ValueError, nt.tokens)

    def testSimple(self):
        exp = ['(', '(', 'h', ',', 'p', ')', 'hp', ',', 'g', ')', 'hpg', ';']
        content = '((h,p)hp,g)hpg;'
        self._do_test(content, exp)
        content = '((h,p[test])hp,g)hpg;'
        self._do_test(content, exp)
        content = '  ( (  h , p[test] [test2])  hp,  g) hpg ;'
        self._do_test(content, exp)

    def testQuoted(self):
        exp = ['(', '(', 'h ', ',', 'p', ')', 'h p', ',', "g()[],':_", ')', 'hpg', ';']
        content = "((h_ ,'p')h p,'g()[],'':_')hpg;"
        self._do_test(content, exp)
        content = "(('h ',p)h p,'g()[],'':_')hpg;"
        self._do_test(content, exp)

    def _do_test(self, content, expected):
        self.assertEqual([i for i in NewickTokenizer(StringIO(content))], expected)
        self.assertEqual([i for i in NewickTokenizer(newick=content)], expected)
        fp = path_map.next_unique_scratch_filepath('tok_test')
        try:
            write_to_filepath(content, fp)
            self.assertEqual([i for i in NewickTokenizer(filepath=fp)], expected)
        finally:
            try:
                os.unlink(fp)
            except:  # pragma: no cover
                pass

    def testOddQuotes(self):
        content = "((h_ ,'p)h p,g()[],:_)hpg;"
        tok = NewickTokenizer(StringIO(content))
        self.assertRaises(Exception, tok.tokens)
        content = "((h_ ,'p')h p,'g()[]',:_')hpg;"
        tok = NewickTokenizer(StringIO(content))
        self.assertRaises(Exception, tok.tokens)

    def testBranchLen(self):
        exp = ['(', '(', 'h', ':', '4.0', ',', 'p', ':', '1.1461E-5', ')',
               'hp', ':', '1351.146436', ',', 'g', ')', 'hpg', ';']
        content = '((h:4.0,p:1.1461E-5)hp:1351.146436,g)hpg;'
        self._do_test(content, exp)


class TestNewickEvents(unittest.TestCase):
    def testSimple(self):
        exp = [{'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'h'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'p'},
               {'edge_info': '1', 'type': NewickEvents.CLOSE_SUBTREE, 'comments': [], 'label': 'hp'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'g'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE, 'comments': [], 'label': 'hpg'}
               ]
        content = '((h,p)hp:1,g)hpg;'
        self._do_test(content, exp)
        content = '((h,[pretest]p[test][posttest])hp,g)hpg;'
        exp = [{'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'type': NewickEvents.OPEN_SUBTREE, 'comments': []},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'h'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': ['pretest', 'test', 'posttest'], 'label': 'p'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE, 'comments': [], 'label': 'hp'},
               {'edge_info': None, 'type': NewickEvents.TIP, 'comments': [], 'label': 'g'},
               {'edge_info': None, 'type': NewickEvents.CLOSE_SUBTREE, 'comments': [], 'label': 'hpg'}
               ]
        self._do_test(content, exp)

    def testNoArg(self):
        self.assertRaises(ValueError, NewickEventFactory)

    def _do_test(self, content, expected):
        e = [deepcopy(i) for i in NewickEventFactory(tokenizer=NewickTokenizer(stream=StringIO(content)))]
        self.assertEqual(e, expected)
        new_e = []

        def append_to_new_e(event):
            new_e.append(deepcopy(event))

        NewickEventFactory(newick=content, event_handler=append_to_new_e)
        self.assertEqual(new_e, expected)


if __name__ == "__main__":
    unittest.main()
