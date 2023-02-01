#!/usr/bin/env python

import argparse
import re
from enum import Enum
from dataclasses import dataclass
import json
import sys

__version__ = '1.0'
__desc__ = "A simple calculator that evaluates a mathematical expression using + - / * ()"


class Calculator:

    def calculate(self, calculation) -> str:
        return "result"

    def tokenize_expression(self, expression) -> list:
        expression = re.sub('[ "\n\t]', '', expression)
        operators = ['+', '-', '*', '/', '^', '(', ')']
        i = 0
        tokens = []
        while i < len(expression):
            if expression[i].isdigit():
                number = ''
                while i < len(expression) and expression[i].isdigit():
                    number += expression[i]
                    i += 1
                tokens.append(Token(type=TokenType.NUMBER, value=number))

            elif expression[i] in operators:
                if expression[i] == operators[0]:
                    tokens.append(Token(type=TokenType.PlUS, value=expression[i]))
                elif expression[i] == operators[1]:
                    tokens.append(Token(type=TokenType.MINUS, value=expression[i]))
                elif expression[i] == operators[2]:
                    tokens.append(Token(type=TokenType.MULTIPLY, value=expression[i]))
                elif expression[i] == operators[3]:
                    tokens.append(Token(type=TokenType.DIVIDE, value=expression[i]))
                elif expression[i] == operators[4]:
                    tokens.append(Token(type=TokenType.EXPONENT, value=expression[i]))
                elif expression[i] == operators[5]:
                    tokens.append(Token(type=TokenType.LEFT_PARENTHESIS, value=expression[i]))
                elif expression[i] == operators[6]:
                    tokens.append(Token(type=TokenType.RIGHT_PARENTHESIS, value=expression[i]))
                i += 1

            else:
                i += 1

        return list(tokens)


class TokenType(Enum):
    NUMBER = 0
    PlUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    EXPONENT = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7


@dataclass
class Token:
    type: TokenType
    value: any

    def __repr__(self):
        return f'{self.type.name} "{self.value}"'


def main():
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()

    print(Calculator().calculate(arguments.calculate))


if __name__ == '__main__':
    main()
