#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peyutil import (flush_utf_8_writer,
                     get_utf_8_string_io_writer,
                     increment_slug,
                     is_int_type,
                     is_str_type,
                     reverse_dict,
                     slugify,
                     underscored2camel_case,
                     UNICODE)
import unittest
import tempfile
import time
import os

class TestStrUtil(unittest.TestCase):
    def test_any_early_exit(self):
        buf, wrapper = get_utf_8_string_io_writer()
        wrapper.write('test string')
        wrapper.write(u'διακριτικός')
        wrapper.write(' test string')
        flush_utf_8_writer(wrapper)
        x = buf.getvalue()
        if not isinstance(x, UNICODE): #py2.7 compat
            x = x.decode('utf-8')
        self.assertEqual(u'test stringδιακριτικός test string', x)

    def test_is_int_type(self):
        self.assertTrue(is_int_type(3))
        self.assertTrue(is_int_type(12345678901234567890))
        self.assertFalse(is_int_type('3'))
        self.assertFalse(is_int_type(3.2))

if __name__ == "__main__":
    unittest.main()
