#!/usr/bin/env python
import json
import os
import sys
import unittest
from dt042g_src.calculator import Calculator, Token, TokenType, Operations

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):
    """Validation tests for the behaviour of the Calculator"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_calculator_returns_correct_result(self):
        """Validation tests for the behaviour of the program, using the public method calculate"""
        for expression, expected_result in self.test_data.items():
            with self.subTest(expression=expression, expected_result=expected_result):
                calculator = Calculator(expression)
                self.assertEqual(expected_result, calculator.calculate())


class TestCalculate(unittest.TestCase):
    """Tests for the Calculator.calculate() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_has_method_calculate(self):
        """Tests if the calculator has the calculate method"""
        calculator = Calculator('')
        self.assertTrue(hasattr(calculator, 'calculate') and callable(getattr(calculator, 'calculate')))

    def test_should_exit_on_bad_input(self):
        """Tests if the calculate method exits on bad input"""
        calculator = Calculator('f09jj0jf02jf402j49jf2')
        self.assertRaises(SystemExit, calculator.calculate)

    def test_non_decimal_result_should_be_int(self):
        """Tests if non decimal results return int"""
        calculator = Calculator("4/4")
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertIsInstance(calculator.calculate(), int)

    def test_decimal_result_should_be_float(self):
        """Tests if decimal result returns float"""
        calculator = Calculator("4/3")
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertIsInstance(calculator.calculate(), float)


class TestTokenizeExpression(unittest.TestCase):
    """Tests for the Calculator.__tokenize_calculation() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_tokens_should_not_be_empty(self):
        """Tests that tokens are not empty"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                self.assertFalse(len(getattr(calculator, '_Calculator__tokenize_calculation')()) == 0)

    def test_tokens_should_not_contain_whitespace(self):
        """Tests that tokens do not contains whitespace"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in getattr(calculator, '_Calculator__tokenize_calculation')():
                    self.assertNotIn(' ', token.value)

    def test_tokens_should_not_contain_quotes(self):
        """Tests that tokens do not contain quotes"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in getattr(calculator, '_Calculator__tokenize_calculation')():
                    self.assertNotIn('"', token.value)

    def test_tokens_should_be_list(self):
        """Tests that tokens are returned as a list"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                self.assertIsInstance(getattr(calculator, '_Calculator__tokenize_calculation')(), list)

    def test_should_group_digits(self):
        """Tests that sequential digits are grouped"""
        expression = '0-(123)+2'
        calculator = Calculator(expression)
        self.assertEqual('123', getattr(calculator, '_Calculator__tokenize_calculation')()[3].value)

    def test_should_identify_plus(self):
        """Tests that + are identified"""
        expression = '0-1+3*(2/3)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[3].type == TokenType.PLUS, f'Token type is {tokens[3].type}')

    def test_should_identify_minus(self):
        """Tests that - are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[1].type == TokenType.MINUS, f'Token type is {tokens[1].type}')

    def test_should_identify_multiply(self):
        """Tests that * are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[5].type == TokenType.MULTIPLY, f'Token type is {tokens[5].type}')

    def test_should_identify_divide(self):
        """Tests that / are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[8].type == TokenType.DIVIDE, f'Token type is {tokens[8].type}')

    def test_should_identify_exponent(self):
        """Tests that ^ are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[11].type == TokenType.EXPONENT, f'Token type is {tokens[11].type}')

    def test_should_identify_left_parenthesis(self):
        """Tests that ( are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[6].type == TokenType.LEFT_PARENTHESIS, f'Token type is {tokens[6].type}')

    def test_should_identify_right_parenthesis(self):
        """Tests that ) are identified"""
        expression = '0-1+323*(2/355)^5'
        calculator = Calculator(expression)
        tokens = getattr(calculator, '_Calculator__tokenize_calculation')()
        self.assertTrue(tokens[10].type == TokenType.RIGHT_PARENTHESIS, f'Token type is {tokens[10].type}')

    def test_tokens_should_be_token_objects(self):
        """Tests that tokens are Token objects"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                for token in getattr(calculator, '_Calculator__tokenize_calculation')():
                    self.assertIsInstance(token, Token)


class TestNextToken(unittest.TestCase):
    """Tests for the Calculator.__next_token() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_iterate_token(self):
        """Tests that the Tokens are iterated correctly"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                tokens_copy = getattr(calculator, '_Calculator__tokenize_calculation')()
                getattr(calculator, '_Calculator__next_token')()
                getattr(calculator, '_Calculator__next_token')()
                self.assertEqual(tokens_copy[1], calculator.__dict__["_Calculator__current_token"])


class TestCalculateExpression(unittest.TestCase):
    """Tests for the Calculator._calculate_expression() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_invalid_expression_should_raise_error(self):
        """Tests that invalid expressions causes raised error"""
        calculator = Calculator("5+((3/2)")
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertRaises(ValueError, calculator._calculate_expression)

    def test_should_return_value_of_expression(self):
        """Tests that the value of the expression is returned"""
        for expression, expected_result in self.test_data.items():
            with self.subTest(expression=expression, expected_result=expected_result):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertEqual(expected_result, calculator._calculate_expression())

    def test_should_handle_leading_parenthesis(self):
        """Tests that leading parenthesis are handled"""
        expression = "(2*2/4^4-3+1+2*2+2)"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(4.015625, calculator._calculate_expression())

    def test_should_return_float(self):
        """Tests that result is returned as float"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertIsInstance(calculator._calculate_expression(), float)


class TestCalculateTerm(unittest.TestCase):
    """Tests for the Calculator._calculate_term() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_value_of_first_term(self):
        """Tests that the value of the first term is returned"""
        expression = "2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(2 * 3 * 5 / 2, calculator._calculate_term())

    def test_should_return_float(self):
        """Loads test data"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertIsInstance(calculator._calculate_term(), float)


class TestCalculateFactor(unittest.TestCase):
    """Tests for the Calculator._calculate_factor() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        """Tests that result is returned as float"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertIsInstance(calculator._calculate_factor(), float)

    def test_should_return_value_of_first_factor(self):
        """Tests that the value of the first factor is returned"""
        expression = "2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(2, calculator._calculate_factor())

    def test_should_handle_negation(self):
        """Tests that negation is handled"""
        expression = "-2*3*5/2+5"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(-2, calculator._calculate_factor())


class TestCalculateExponentiation(unittest.TestCase):
    """Tests for the Calculator._calculate_exponentiation() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_float(self):
        """Tests that result is returned as float"""
        for expression in self.test_data:
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertIsInstance(calculator._calculate_exponentiation(), float)

    def test_should_return_value_of_first_exponentiation(self):
        """Tests that the value of the first exponentiation is returned"""
        expression = "5^2^2+3/2^3"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(625, calculator._calculate_exponentiation())

    def test_should_handle_leading_parenthesis(self):
        """Tests that leading parenthesis is handled"""
        expression = "(2^2^(1+2*2)+2)"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(4294967298, calculator._calculate_exponentiation())

    def test_should_return_first_number_if_no_exponentiation(self):
        """Tests that the first number is returned if no exponentiation"""
        expression = "45+34"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(45, calculator._calculate_exponentiation())


class TestIdentifyNumber(unittest.TestCase):
    """Tests for the Calculator._identify_number() method"""

    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data"""
        with open('../lab2_expressions/expressions.json') as file_handle:
            cls.test_data = json.load(file_handle)

    def test_should_return_first_number(self):
        """Tests that the first number is returned"""
        expression = "5^2^2+3/2^3"
        calculator = Calculator(expression)
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertEqual(5, calculator._identify_number())

    def test_should_return_float(self):
        """Tests that the result is returned as float"""
        for expression in self.test_data:
            if expression.startswith('('):
                break
            with self.subTest(expression=expression):
                calculator = Calculator(expression)
                calculator.__dict__["_Calculator__tokens"] = \
                    iter(getattr(calculator, '_Calculator__tokenize_calculation')())
                getattr(calculator, '_Calculator__next_token')()
                self.assertIsInstance(calculator._identify_number(), float)

    def test_non_number_token_should_raise_error(self):
        """Tests that the a non number raises error"""
        calculator = Calculator("^5+(3/2)")
        calculator.__dict__["_Calculator__tokens"] = iter(getattr(calculator, '_Calculator__tokenize_calculation')())
        getattr(calculator, '_Calculator__next_token')()
        self.assertRaises(ValueError, calculator._identify_number)


class TestOperations(unittest.TestCase):
    """Tests for the Operations class """

    def test_has_method_add(self):
        """Tests that Operations has the method add()"""
        self.assertTrue(hasattr(Operations, 'add') and callable(getattr(Operations, 'add')))

    def test_has_method_subtract(self):
        """Tests that Operations has the method subtract()"""
        self.assertTrue(hasattr(Operations, 'subtract') and callable(getattr(Operations, 'subtract')))

    def test_has_method_multiply(self):
        """Tests that Operations has the method multiply()"""
        self.assertTrue(hasattr(Operations, 'multiply') and callable(getattr(Operations, 'multiply')))

    def test_has_method_divide(self):
        """Tests that Operations has the method divide()"""
        self.assertTrue(hasattr(Operations, 'divide') and callable(getattr(Operations, 'divide')))

    def test_has_method_exponentiation(self):
        """Tests that Operations has the method exponentiation()"""
        self.assertTrue(hasattr(Operations, 'exponentiation') and callable(getattr(Operations, 'exponentiation')))

    def test_has_method_negate(self):
        """Tests that Operations has the method negate()"""
        self.assertTrue(hasattr(Operations, 'negate') and callable(getattr(Operations, 'negate')))

    def test_add(self):
        """Tests add works"""
        a = 2
        b = 3
        self.assertEqual(5, Operations.add(a, b))

    def test_subtract(self):
        """Tests subtract works"""
        a = 2
        b = 3
        self.assertEqual(-1, Operations.subtract(a, b))

    def test_multiply(self):
        """Tests multiply works"""
        a = 2
        b = 3
        self.assertEqual(6, Operations.multiply(a, b))

    def test_divide(self):
        """Tests divide works"""
        a = 6
        b = 3
        self.assertEqual(2, Operations.divide(a, b))

    def test_exponentiation(self):
        """Tests exponentiation works"""
        a = 6
        b = 3
        self.assertEqual(216, Operations.exponentiation(a, b))

    def test_negate(self):
        """Tests negate works"""
        value = 6
        self.assertEqual(-6, Operations.negate(value))


class TestToken(unittest.TestCase):
    """Tests for the Token class"""

    def test_has_type(self):
        """Tests that a Token has a type"""
        token = Token(TokenType.END, '')
        self.assertTrue(hasattr(token, 'type'))

    def test_has_value(self):
        """Tests that a Token has a value"""
        token = Token(TokenType.END, '')
        self.assertTrue(hasattr(token, 'value'))

    def test_has_correct_type(self):
        """Tests that a Token has the correct type"""
        token = Token(TokenType.END, '')
        self.assertEqual(TokenType.END, token.type)

    def test_has_correct_value(self):
        """Tests that a Token has the correct value"""
        token = Token(TokenType.NUMBER, '123')
        self.assertEqual('123', token.value)


class TestTokenType(unittest.TestCase):
    """Tests for the TokenType class"""

    def test_defines_number(self):
        """Tests that the class defines a number"""
        self.assertTrue(hasattr(TokenType, 'NUMBER'))

    def test_defines_plus(self):
        """Tests that the class defines a plus"""
        self.assertTrue(hasattr(TokenType, 'PLUS'))

    def test_defines_minus(self):
        """Tests that the class defines a minus"""
        self.assertTrue(hasattr(TokenType, 'MINUS'))

    def test_defines_multiply(self):
        """Tests that the class defines a multiply"""
        self.assertTrue(hasattr(TokenType, 'MULTIPLY'))

    def test_defines_divide(self):
        """Tests that the class defines a divide"""
        self.assertTrue(hasattr(TokenType, 'DIVIDE'))

    def test_defines_exponent(self):
        """Tests that the class defines a exponent"""
        self.assertTrue(hasattr(TokenType, 'EXPONENT'))

    def test_defines_left_parenthesis(self):
        """Tests that the class defines a left parenthesis"""
        self.assertTrue(hasattr(TokenType, 'LEFT_PARENTHESIS'))

    def test_defines_right_parenthesis(self):
        """Tests that the class defines a right parenthesis"""
        self.assertTrue(hasattr(TokenType, 'RIGHT_PARENTHESIS'))

    def test_defines_end(self):
        """Tests that the class defines an end"""
        self.assertTrue(hasattr(TokenType, 'END'))


if __name__ == '__main__':
    unittest.main()
