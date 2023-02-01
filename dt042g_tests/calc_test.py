#!/usr/bin/env python

import os
import sys
import unittest
from dt042g_src import calculator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = calculator.Calculator()
        self.expression = '" 2+ 3 / (23*9) ^ 4 - (42) - 456 "'

    def validationtest_tmp(self):
        #   TODO validation test on calculate method using json data
        pass

    #
    #   Tokenize
    #
    def test_tokens_should_not_be_empty(self):
        self.assertFalse(len(self.calculator.tokenize_expression(self.expression)) == 0)

    def test_tokens_should_not_contain_whitespace(self):
        for token in self.calculator.tokenize_expression(self.expression):
            self.assertNotIn(' ', token)

    def test_tokens_should_be_list(self):
        self.assertIsInstance(self.calculator.tokenize_expression(self.expression), list)

    def test_should_group_digits(self):
        expression = '0-(123)+2'
        self.assertEqual(self.calculator.tokenize_expression(expression)[3], '123')

    def test_tokens_should_be_token_objects(self):
        for token in self.calculator.tokenize_expression(self.expression):
            self.assertIsInstance(token, calculator.Token)



class TestToken(unittest.TestCase):

    def test_tmp(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
