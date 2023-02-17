#!/usr/bin/env python

import argparse
import re
from collections.abc import Iterator
from enum import Enum
from dataclasses import dataclass

__version__ = '1.0'
__desc__ = "A simple calculator that evaluates a mathematical expression using + - / * ()"


class TokenType(Enum):
    """Defines the types of tokens"""
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    EXPONENT = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7
    END = 8


@dataclass
class Token:
    """Defines a token, with a type and value"""
    type: TokenType
    value: str

    def __repr__(self):
        """Returns a string representation of the token"""
        return f'{self.type.name} "{self.value}"'


class Operations:
    """Operations the calculator can do."""
    @staticmethod
    def add(a, b): return a + b

    @staticmethod
    def subtract(a, b): return a - b

    @staticmethod
    def multiply(a, b): return a * b

    @staticmethod
    def divide(a, b): return a / b

    @staticmethod
    def exponentiation(a, b): return a ** b

    @staticmethod
    def negate(value): return -value


class Calculator:
    """Calculates a mathematical expression via the calculate method"""
    __calculation: str
    __tokens: Iterator or None
    __current_token: Token or None

    def __init__(self, calculation):
        """Initializes fields including the calculation to be calculated"""
        self.__calculation = calculation
        self.__current_token = None
        self.__tokens = None

    def calculate(self) -> float or int:
        """Calculates the expression in __calculation using helper methods and handles errors

        :returns The value of the __calculation
        """
        self.__tokens = iter(self.__tokenize_calculation())
        self.__next_token()
        try:
            result = self._calculate_expression()
            if result % 1 == 0:
                return int(result)
            else:
                return result
        except ValueError as e:
            print(f'{e}\nInvalid mathematical expression, exiting..')
            exit(1)

    def __tokenize_calculation(self) -> list:
        """Strips quotes, whitespace and parses the calculation string into Tokens

        :returns Tokens extracted from the expression
        """
        calculation = re.sub('[ "\n\t]', '', self.__calculation)
        operators = ['+', '-', '*', '/', '^', '(', ')']
        i = 0
        tokens = []
        while i < len(calculation):
            if calculation[i].isdigit():
                number = ''
                while i < len(calculation) and calculation[i].isdigit():
                    number += calculation[i]
                    i += 1
                tokens.append(Token(type=TokenType.NUMBER, value=number))
            elif calculation[i] in operators:
                if calculation[i] == operators[0]:
                    tokens.append(Token(type=TokenType.PLUS, value=calculation[i]))
                elif calculation[i] == operators[1]:
                    tokens.append(Token(type=TokenType.MINUS, value=calculation[i]))
                elif calculation[i] == operators[2]:
                    tokens.append(Token(type=TokenType.MULTIPLY, value=calculation[i]))
                elif calculation[i] == operators[3]:
                    tokens.append(Token(type=TokenType.DIVIDE, value=calculation[i]))
                elif calculation[i] == operators[4]:
                    tokens.append(Token(type=TokenType.EXPONENT, value=calculation[i]))
                elif calculation[i] == operators[5]:
                    tokens.append(Token(type=TokenType.LEFT_PARENTHESIS, value=calculation[i]))
                elif calculation[i] == operators[6]:
                    tokens.append(Token(type=TokenType.RIGHT_PARENTHESIS, value=calculation[i]))
                i += 1
            else:
                i += 1

        return list(tokens)

    def __next_token(self):
        """Iterates the __tokens iterator and assigns the token to __current_token"""
        self.__current_token = next(self.__tokens, Token(TokenType.END, ''))

    def _calculate_expression(self, expected_end_of_expression=Token(TokenType.END, '')) -> float:
        """Identifies and calculates the value of an expression by finding PLUS/MINUS tokens and
        executing add/subtract operations on its two terms.

        :param expected_end_of_expression: The Token on which the expression is expected to end. Defaults to
        a Token with type END
        :raises ValueError if the current token is not a PLUS/MINUS or expected_end_of_expression
        - which means an invalid expression
        :returns The value of the expression
        """
        term_a = self._calculate_term()
        while self.__current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.__current_token.type == TokenType.PLUS:
                self.__next_token()
                term_b = self._calculate_term()
                term_a = Operations.add(term_a, term_b)
            elif self.__current_token.type == TokenType.MINUS:
                self.__next_token()
                term_b = self._calculate_term()
                term_a = Operations.subtract(term_a, term_b)

        else:
            if self.__current_token.type is not expected_end_of_expression.type:
                raise ValueError(f'Expected the end of an expression with a Token of type: '
                                 f'{expected_end_of_expression.type} but received {self.__current_token.type}')
            else:
                self.__next_token()
                return term_a

    def _calculate_term(self) -> float:
        """Identifies and calculates the value of a term by finding MULTIPLY/DIVIDE tokens and
        executing multiply/divide operations on its two factors.

        :returns The value of the term, which has been accumulated into the factor_a variable
        """
        factor_a = self._calculate_factor()
        while self.__current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.__current_token.type == TokenType.MULTIPLY:
                self.__next_token()
                factor_b = self._calculate_factor()
                factor_a = Operations.multiply(factor_a, factor_b)
            elif self.__current_token.type == TokenType.DIVIDE:
                self.__next_token()
                factor_b = self._calculate_factor()
                factor_a = Operations.divide(factor_a, factor_b)
        else:
            return factor_a

    def _calculate_factor(self) -> float:
        """Identifies and calculates the value of a factor and determines if the factor
        should be negated by finding unary PLUS/MINUS tokens.

        :returns The value of the factor.
        """
        while self.__current_token.type in (TokenType.MINUS, TokenType.PLUS):
            if self.__current_token.type == TokenType.MINUS:
                self.__next_token()
                return Operations.negate(self._calculate_factor())
            elif self.__current_token.type == TokenType.PLUS:
                self.__next_token()
                return self._calculate_factor()
        else:
            return self._calculate_exponentiation()

    def _calculate_exponentiation(self) -> float:
        """Identifies and calculates the value of an exponentiation by determining if an expression
        in parenthesis should be calculated, then identifying and calculating the base and exponent
        and executing the exponentiation operation with these if applicable.

        :returns The value of the exponentiation, or the base if no exponentiation exists
        """
        if self.__current_token.type == TokenType.LEFT_PARENTHESIS:
            self.__next_token()
            return self._calculate_expression(expected_end_of_expression=Token(TokenType.RIGHT_PARENTHESIS, ')'))
        else:
            base = self._identify_number()
            self.__next_token()

            if self.__current_token.type == TokenType.EXPONENT:
                self.__next_token()
                exponent = self._calculate_factor()
                return Operations.exponentiation(base, exponent)
            else:
                return base

    def _identify_number(self) -> float:
        """Identifies and returns the value of a number

        :raises ValueError if the current token is not a number - which means an invalid expression
        :returns The value of the number
        """
        if self.__current_token.type != TokenType.NUMBER:
            raise ValueError(f"Expected TokenType.NUMBER, got '{self.__current_token.type}'")
        else:
            return float(self.__current_token.value)


def main():
    """Parses arguments, passes calculate argument to the calculator and prints the result"""
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()
    calculator = Calculator(arguments.calculate)
    print(f'{arguments.calculate} = {calculator.calculate()}')


if __name__ == '__main__':
    main()
