#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peyutil import (any_early_exit,
                     doi2url,
                     pretty_timestamp)
import unittest
import time


class TestInit(unittest.TestCase):
    def test_any_early_exit(self):
        v = [1, 2, 3]
        self.assertFalse(any_early_exit(v, lambda x: x > 20))
        self.assertTrue(any_early_exit(v, lambda x: x > 2))
        self.assertTrue(any_early_exit(v, lambda x: x <2))
        def raiseIfGT2(x):
            if x > 2:
                raise ValueError('np')
            return True
        self.assertTrue(any_early_exit(v, lambda x: raiseIfGT2(x) and x < 2))
        self.assertTrue(any_early_exit(v, lambda x: True and x > 2))
        self.assertRaises(ValueError, any_early_exit, v, lambda x: raiseIfGT2(x) and x > 2)

    def test_pretty_timestamp(self):
        t = time.gmtime(1500000678)
        self.assertEqual('2017-07-14', pretty_timestamp(t))
        self.assertEqual('2017-07-14', pretty_timestamp(t, 0))
        self.assertEqual('20170714025118', pretty_timestamp(t, 1))
        self.assertEqual('14-07-2017', pretty_timestamp(t, '%d-%m-%Y'))
        # Warning: these next 2 tests are gonna break starting Jan-01-2100
        self.assertTrue(pretty_timestamp(style=1).startswith('20'))
        import datetime
        now = datetime.datetime.now()
        self.assertTrue('+20' in pretty_timestamp(now, '+%Y'))

    def test_doi2url(self):
        x = '10.1071/IS12017'
        exp = 'http://dx.doi.org/10.1071/IS12017'
        self.assertEqual(exp, doi2url(x))
        self.assertEqual(exp, doi2url(exp))
        self.assertEqual(exp, doi2url('doi: {}'.format(x)))
        self.assertEqual(exp, doi2url('doi:{}'.format(x)))
        self.assertEqual('http://gibberish', doi2url('gibberish'))

if __name__ == "__main__":
    unittest.main()
