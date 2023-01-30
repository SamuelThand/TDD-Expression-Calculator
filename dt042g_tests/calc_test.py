#!/usr/bin/env python

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import dt042g_src.calculator as src


class Test(unittest.TestCase):

    def test_tmp(self):
        self.assertTrue(True, "It's true")


if __name__ == '__main__':
    unittest.main()
