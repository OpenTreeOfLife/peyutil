#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peyutil import (any_early_exit, )
import unittest



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


if __name__ == "__main__":
    unittest.main()
