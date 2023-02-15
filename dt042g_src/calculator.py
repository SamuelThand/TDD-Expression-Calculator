#!/usr/bin/env python

import argparse
import re
from collections.abc import Iterator
from enum import Enum
from dataclasses import dataclass

__version__ = '1.0'
__desc__ = "A simple calculator that evaluates a mathematical expression using + - / * ()"


class TokenType(Enum):
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
    type: TokenType
    value: str

    def __repr__(self):
        return f'{self.type.name} "{self.value}"'


class Operations:
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
    __calculation: str
    __tokens: Iterator or None
    __current_token: Token or None

    def __init__(self, calculation):
        self.__calculation = calculation
        self.__current_token = None
        self.__tokens = None

    def calculate(self) -> float or int:
        self.__tokens = iter(self.tokenize_calculation())
        self.next_token()
        try:
            result = self.calculate_expression()
            if result % 1 == 0:
                return int(result)
            else:
                return result
        except ValueError as e:
            print(f'{e}\nInvalid mathematical expression, exiting..')
            exit(1)

    def tokenize_calculation(self) -> list:
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

    def next_token(self):
        self.__current_token = next(self.__tokens, Token(TokenType.END, ''))

    def calculate_expression(self, end_of_expression=Token(TokenType.END, '')) -> float:
        term_a = self.identify_term()
        while self.__current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.__current_token.type == TokenType.PLUS:
                self.next_token()
                term_b = self.identify_term()
                term_a = Operations.add(term_a, term_b)
            elif self.__current_token.type == TokenType.MINUS:
                self.next_token()
                term_a = term_a - self.identify_term()

        else:
            if self.__current_token.type is not end_of_expression.type:
                raise ValueError(f'Expected the end of an expression with a Token of type: {end_of_expression.type}'
                                 f' but received {self.__current_token.type}')
            else:
                self.next_token()
                return term_a

    def identify_term(self) -> float:
        factor_a = self.identify_factor()
        while self.__current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.__current_token.type == TokenType.MULTIPLY:
                self.next_token()
                factor_b = self.identify_factor()
                factor_a = Operations.multiply(factor_a, factor_b)
            elif self.__current_token.type == TokenType.DIVIDE:
                self.next_token()
                factor_a = factor_a / self.identify_factor()
        else:
            return factor_a

    def identify_factor(self) -> float:
        while self.__current_token.type in (TokenType.MINUS, TokenType.PLUS):
            if self.__current_token.type == TokenType.MINUS:
                self.next_token()
                return Operations.negate(self.identify_factor())
            elif self.__current_token.type == TokenType.PLUS:
                self.next_token()
                return self.identify_factor()
        else:
            return self.identify_exponentiation()

    def identify_exponentiation(self) -> float:
        if self.__current_token.type == TokenType.LEFT_PARENTHESIS:
            self.next_token()
            return self.calculate_expression(end_of_expression=Token(TokenType.RIGHT_PARENTHESIS, ')'))
        else:
            base = self.identify_number()
            self.next_token()

            if self.__current_token.type == TokenType.EXPONENT:
                self.next_token()
                exponent = self.identify_factor()
                return Operations.exponentiation(base, exponent)
            else:
                return base

    def identify_number(self) -> float:
        if self.__current_token.type != TokenType.NUMBER:
            raise ValueError(f"Expected TokenType.NUMBER, got '{self.__current_token.type}'")
        else:
            return float(self.__current_token.value)


def main():
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()
    calculator = Calculator(arguments.calculate)
    print(f'{arguments.calculate} = {calculator.calculate()}')


if __name__ == '__main__':
    main()
