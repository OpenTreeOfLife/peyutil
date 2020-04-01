#! /usr/bin/env python
from .struct_diff import DictDiff
import logging



def equal_blob_check(unit_test, diff_file_tag, first, second):
    from nexson.test.support import pathmap
    if first != second:
        dd = DictDiff.create(first, second)
        ofn = pathmap.next_unique_scratch_filepath(diff_file_tag + '.obtained_rt')
        efn = pathmap.next_unique_scratch_filepath(diff_file_tag + '.expected_rt')
        write_as_json(first, ofn)
        write_as_json(second, efn)
        er = dd.edits_expr()
        if first != second:
            m_fmt = "Conversion failed see files {o} and {e}"
            m = m_fmt.format(o=ofn, e=efn)
            unit_test.assertEqual("", m)


def raise_http_error_with_more_detail(err):
    # show more useful information (JSON payload) from the server
    details = err.response.text
    raise ValueError("{e}, details: {m}".format(e=err, m=details))


__all__ = ['helper', 'pathmap', 'struct_diff']