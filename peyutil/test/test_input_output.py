#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import os

from peyutil.test.support.pathmap import get_test_path_mapper

from peyutil import (expand_path,
                     open_for_group_write,
                     parse_study_tree_list,
                     pretty_dict_str,
                     read_as_json,
                     read_filepath,
                     write_as_json,
                     write_pretty_dict_str,
                     write_to_filepath,)

path_map = get_test_path_mapper()

class TestIO(unittest.TestCase):
    def test_expand_path(self):
        os.environ['BOGUS'] = 'somebogus'
        expy = os.path.join('somebogus', 'path')
        self.assertEqual(expand_path('${BOGUS}/path'), expy)
        inp = '~/${BOGUS}/path'
        y = expand_path(inp)
        self.assertTrue(y.endswith(expy))
        self.assertFalse(y.startswith('~'))

    def test_parse_study_tree_list(self):
        stl = path_map.nexson_source_path('study_tree_list.json')
        x = parse_study_tree_list(stl)
        exp = [{'study_id': 'pg_1', 'tree_id': 'tree2'}, {'study_id': 'pg_2', 'tree_id': 'tree3'}]
        self.assertEqual(x, exp)
        aj = read_as_json(stl)
        self.assertEqual(aj, exp)
        raw = '''[
  {"study_id":  "pg_1", "tree_id": "tree2"},
  {"study_id":  "pg_2", "tree_id": "tree3"}
]'''
        self.assertEqual(raw, read_filepath(stl))
        self.assertEqual(raw, read_filepath(stl, encoding='utf-8'))
        z = '''{
  "study_id": "pg_1",
  "tree_id": "tree2"
}'''
        self.assertEqual(z, pretty_dict_str(exp[0]))
        try:
            tdf = tempfile.TemporaryDirectory
        except:  # pragma: no cover
            # Skip this test on Python2.7. just feeling lazy...
            return
        noindentraw = '''[
{
"study_id": "pg_1",
"tree_id": "tree2"
},
{
"study_id": "pg_2",
"tree_id": "tree3"
}
]
'''
        with tdf() as tmpdir:
            tfp = os.path.join(tmpdir, 'x.json')
            write_as_json(exp, tfp)
            self.assertEqual(noindentraw, read_filepath(tfp))
            rtfp = os.path.join(tmpdir, 'raw.txt')
            write_to_filepath(noindentraw, rtfp)
            self.assertEqual(noindentraw, read_filepath(rtfp))
            pdfp = os.path.join(tmpdir, 'prettydictfp')
            with open_for_group_write(pdfp, 'w') as gro:
                write_pretty_dict_str(gro, exp[0])

            self.assertEqual(z, read_filepath(pdfp))

if __name__ == "__main__":
    unittest.main()
