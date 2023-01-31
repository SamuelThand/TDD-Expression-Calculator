#!/usr/bin/env python

import os
import sys
import unittest
from dt042g_src import calculator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = calculator.Calculator()

    def validationtest_tmp(self):
        #   TODO validation test on calculate method using json data
        pass

    #   Tokenize

    def test_expression_should_not_contain_whitespace(self):
        expression = ' 2+ 3'
        self.assertNotIn(' ', self.calculator.tokenize_expression(expression))


if __name__ == '__main__':
    unittest.main()
