#!/usr/bin/env python
import json
import os
import sys
import unittest
from dt042g_src.calculator import Calculator, Token, TokenType, Operations

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_validation_test(self):
        for expression, expected_result in self.test_data.items():
            with self.subTest(expression=expression, expected_result=expected_result):
                calculator = Calculator(expression)
                self.assertEqual(expected_result, calculator.calculate())

    def test_non_decimal_result_should_be_int(self):
        calculator = Calculator("4/4")
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertIsInstance(calculator.calculate(), int)

    def test_decimal_result_should_be_float(self):
        calculator = Calculator("4/3")
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertIsInstance(calculator.calculate(), float)

    # def tearDownClass(cls) -> None:


class TestTokenizeExpression(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
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
                calculator = Calculator(expression)
                self.assertFalse(len(calculator.tokenize_calculation()) == 0)

    def test_tokens_should_not_contain_whitespace(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in calculator.tokenize_calculation():
                    self.assertNotIn(' ', token.value)

    def test_tokens_should_not_contain_quotemarks(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in calculator.tokenize_calculation():
                    self.assertNotIn('"', token.value)

    def test_tokens_should_be_list(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                self.assertIsInstance(calculator.tokenize_calculation(), list)

    # TODO - rewrite tests to be dynamic and use test data?

    def test_should_group_digits(self):
        expression = '0-(123)+2'
        calculator = Calculator(expression)
        self.assertEqual('123', calculator.tokenize_calculation()[3].value)

    def test_should_identify_plus(self):
        expression = '0-1+3*(2/3)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[3].type == TokenType.PLUS, f'Token type is {tokens[3].type}')

    def test_should_identify_minus(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[1].type == TokenType.MINUS, f'Token type is {tokens[1].type}')

    def test_should_identify_multiply(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[5].type == TokenType.MULTIPLY, f'Token type is {tokens[5].type}')

    def test_should_identify_divide(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[8].type == TokenType.DIVIDE, f'Token type is {tokens[8].type}')

    def test_should_identify_exponent(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[11].type == TokenType.EXPONENT, f'Token type is {tokens[11].type}')

    def test_should_identify_left_parenthesis(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[6].type == TokenType.LEFT_PARENTHESIS, f'Token type is {tokens[6].type}')

    def test_should_identify_right_parenthesis(self):
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = calculator.tokenize_calculation()
        self.assertTrue(tokens[10].type == TokenType.RIGHT_PARENTHESIS, f'Token type is {tokens[10].type}')

    def test_tokens_should_be_token_objects(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in calculator.tokenize_calculation():
                    self.assertIsInstance(token, Token)


class TestNextToken(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_malformed_expression_should_raise_error(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                tokens_copy = calculator.tokenize_calculation()
                calculator.next_token()
                calculator.next_token()
                self.assertEqual(tokens_copy[1], calculator.current_token)


class TestCalculateExpression(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_malformed_expression_should_raise_error(self):
        calculator = Calculator("5+((3/2)")
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertRaises(ValueError, calculator.calculate_expression)

    def test_should_return_value_of_expression(self):
        for expression, expected_result in self.test_data.items():
            with self.subTest(expression=expression, expected_result=expected_result):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertEqual(expected_result, calculator.calculate_expression())

    def test_should_handle_leading_parenthesis(self):
        expression = "(2*2/4^4-3+1+2*2+2)"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(4.015625, calculator.calculate_expression())

    def test_should_return_float(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertIsInstance(calculator.calculate_expression(), float)


class TestIdentifyTerm(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertIsInstance(calculator.identify_term(), float)

    def test_should_return_first_term(self):
        expression = "2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(2 * 3 * 5 / 2, calculator.identify_term())


class TestIdentifyFactor(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertIsInstance(calculator.identify_factor(), float)

    def test_should_return_first_factor(self):
        expression = "2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(2, calculator.identify_factor())

    def test_should_handle_negation(self):
        expression = "-2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(-2, calculator.identify_factor())


class TestIdentifyExponentiation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertIsInstance(calculator.identify_exponentiation(), float)

    def test_should_return_first_exponentiation(self):
        expression = "5^2^2+3/2^3"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(625, calculator.identify_exponentiation())

    def test_should_handle_leading_parenthesis(self):
        expression = "(2^2^(1+2*2)+2)"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(4294967298, calculator.identify_exponentiation())

    def test_should_return_first_number_if_no_exponentiation(self):
        expression = "45+34"
        calculator = Calculator(expression)
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertEqual(45, calculator.identify_exponentiation())


class TestIdentifyNumber(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        for expression in self.test_data:
            if expression.startswith('('):
                break
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.tokens = iter(calculator.tokenize_calculation())
                calculator.next_token()
                self.assertIsInstance(calculator.identify_number(), float)

    def test_non_number_token_should_raise_error(self):
        calculator = Calculator("^5+(3/2)")
        calculator.tokens = iter(calculator.tokenize_calculation())
        calculator.next_token()
        self.assertRaises(ValueError, calculator.identify_number)


class TestOperations(unittest.TestCase):

    def test_add(self):
        a = 2
        b = 3
        self.assertEqual(5, Operations.add(a, b))

    def test_subtract(self):
        a = 2
        b = 3
        self.assertEqual(-1, Operations.subtract(a, b))

    def test_multiply(self):
        a = 2
        b = 3
        self.assertEqual(6, Operations.multiply(a, b))

    def test_divide(self):
        a = 6
        b = 3
        self.assertEqual(2, Operations.divide(a, b))

    def test_exponentiation(self):
        a = 6
        b = 3
        self.assertEqual(216, Operations.exponentiation(a, b))

    def test_negate(self):
        value = 6
        self.assertEqual(-6, Operations.negate(value))


class TestToken(unittest.TestCase):

    def test_tmp(self):
        self.assertTrue(True)


class TestTokenType(unittest.TestCase):

    def test_tmp(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
