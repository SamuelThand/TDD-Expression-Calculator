#!/usr/bin/env python
import json
import os
import sys
import unittest
from dt042g_src.calculator import Calculator, Token, TokenType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):

    def validationtest_tmp(self):
        #   TODO validation test on calculate method using json data
        pass


class TestTokenizeExpression(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.calculator = Calculator()
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    #   TODO error handling for bad input
    #   Ska dessa metoder höra hit eller till calculator testing?

    def test_should_not_allow_bad_input(self):
        pass

    def test_should_not_allow_unmatched_parenthesis(self):
        pass

    def test_should_not_allow_wierd_stuff(self):
        # (+)(+) (+(+(-))) for example
        pass

    def test_tokens_should_not_be_empty(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                self.assertFalse(len(self.calculator.tokenize_expression(expression)) == 0)

    def test_tokens_should_not_contain_whitespace(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                for token in self.calculator.tokenize_expression(expression):
                    self.assertNotIn(' ', token.value)

    def test_tokens_should_not_contain_quotemarks(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                for token in self.calculator.tokenize_expression(expression):
                    self.assertNotIn('"', token.value)

    def test_tokens_should_be_list(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                self.assertIsInstance(self.calculator.tokenize_expression(expression), list)

    # TODO - rewrite tests to be dynamic and use test data?

    def test_should_group_digits(self):
        expression = '0-(123)+2'
        self.assertEqual(self.calculator.tokenize_expression(expression)[3].value, '123')

    def test_should_identify_plus(self):
        expression = '0-1+3*(2/3)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[3].type == TokenType.PlUS, f'Token type is {tokens[3].type}')

    def test_should_identify_minus(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[1].type == TokenType.MINUS, f'Token type is {tokens[1].type}')

    def test_should_identify_multiply(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[5].type == TokenType.MULTIPLY, f'Token type is {tokens[5].type}')

    def test_should_identify_divide(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[8].type == TokenType.DIVIDE, f'Token type is {tokens[8].type}')

    def test_should_identify_exponent(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[11].type == TokenType.EXPONENT, f'Token type is {tokens[11].type}')

    def test_should_identify_left_parenthesis(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[6].type == TokenType.LEFT_PARENTHESIS, f'Token type is {tokens[6].type}')

    def test_should_identify_right_parenthesis(self):
        expression = '0-1+323*(2/355)^5'
        tokens = self.calculator.tokenize_expression(expression)
        self.assertTrue(tokens[10].type == TokenType.RIGHT_PARENTHESIS, f'Token type is {tokens[10].type}')

    def test_tokens_should_be_token_objects(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                for token in self.calculator.tokenize_expression(expression):
                    self.assertIsInstance(token, Token)


class TestToken(unittest.TestCase):

    def test_tmp(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
