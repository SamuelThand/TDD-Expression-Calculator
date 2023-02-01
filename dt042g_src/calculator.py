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

        i = 0
        tokens = []
        while i < len(expression):
            if expression[i].isdigit():
                number = ''
                while i < len(expression) and expression[i].isdigit():
                    number += expression[i]
                    i += 1
                tokens.append(Token(type=TokenType.NUMBER, value=number))
                continue

            # elif
            tokens.append(Token(type=TokenType.NUMBER, value=expression[i]))
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


def main():
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()

    print(Calculator().calculate(arguments.calculate))


if __name__ == '__main__':
    main()
