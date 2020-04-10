#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from peyutil import (flush_utf_8_writer,
                     get_utf_8_string_io_writer,
                     increment_slug,
                     is_int_type,
                     is_str_type,
                     reverse_dict,
                     slugify,
                     underscored2camel_case,
                     UNICODE)


class TestStrUtil(unittest.TestCase):
    def test_underscored2camel_case(self):
        self.assertEqual(underscored2camel_case('ott_id'), 'ottId')
        self.assertEqual(underscored2camel_case('ott__id'), 'ottId')
        self.assertEqual(underscored2camel_case('ott_i_d'), 'ottID')
        self.assertEqual(underscored2camel_case('Ott_i_d'), 'OttID')

    def test_slugify(self):
        self.assertEqual(slugify("My favorites!"), 'my-favorites')
        self.assertEqual(slugify(""), 'untitled')
        self.assertEqual(slugify("Trees about bees"), 'trees-about-bees')
        self.assertEqual(increment_slug('trees-about-bees'), 'trees-about-bees-2')
        self.assertEqual(increment_slug('trees-about-bees-2'), 'trees-about-bees-3')

    def test_rev_dict(self):
        x = {1: 2, 3: 4}
        self.assertEqual({2: 1, 4: 3}, reverse_dict(x))
        self.assertEqual(1, len(reverse_dict({1: 2, 3: 2})))

    def test_is_str_type(self):
        self.assertFalse(is_str_type(3))
        self.assertFalse(is_str_type(12345678901234567890))
        self.assertTrue(is_str_type('3'))
        self.assertFalse(is_str_type(3.2))
        self.assertTrue(is_str_type(u'διακριτικός'))

    def test_any_early_exit(self):
        buf, wrapper = get_utf_8_string_io_writer()
        wrapper.write('test string')
        wrapper.write(u'διακριτικός')
        wrapper.write(' test string')
        flush_utf_8_writer(wrapper)
        x = buf.getvalue()
        if not isinstance(x, UNICODE):  # pragma: no cover
            # py2.7 compat
            x = x.decode('utf-8')
        self.assertEqual(u'test stringδιακριτικός test string', x)

    def test_is_int_type(self):
        self.assertTrue(is_int_type(3))
        self.assertTrue(is_int_type(12345678901234567890))
        self.assertFalse(is_int_type('3'))
        self.assertFalse(is_int_type(3.2))


if __name__ == "__main__":
    unittest.main()
