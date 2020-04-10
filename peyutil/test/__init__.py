#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
peyutil testing suite.
"""
from .support.pathmap import PathMapForTests, get_test_path_mapper
import unittest
import re
import os


def get_test_file_names():  # pragma: no cover
    """Get list of test file names."""
    path = os.path.dirname(__file__)
    files = os.listdir(path)
    t = []
    pat = re.compile(r'^test.*\.py$')
    for f in files:
        if pat.match(f):
            rp = 'peyutil.test.' + f[:-3]  # [:-3] to strip ".py"
            t.append(rp)
    return t


def get_test_suite(test_file_names=None):  # pragma: no cover
    """
    Creates a unittest.TestSuite from all of the modules in
    `peyutil.test`. Right now, assumes (a) no subdirectories (though
    this can easily be accommodated) and (b) every test to be run is
    sitting in a module with a file name of 'test*.py', and, conversely,
    every file with a name of 'test*.py' has test(s) to be run.
    """
    if test_file_names is None:
        test_file_names = get_test_file_names()
    tests = unittest.defaultTestLoader.loadTestsFromNames(test_file_names)
    return unittest.TestSuite(tests)


def run():  # pragma: no cover
    """Runs all of the unittests"""
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite())


if __name__ == "__main__":
    run()
