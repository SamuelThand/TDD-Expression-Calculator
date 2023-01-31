#!/usr/bin/env python

import argparse
import json
import sys

__version__ = '1.0'
__desc__ = "A simple calculator that evaluates a mathematical expression using + - / * ()"


class Calculator:

    def calculate(self, calculation) -> str:
        pass

    def tokenize_expression(self, expression) -> str:

        expression = expression.replace(' ', '')

        return expression



def main():
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()

    print(Calculator().calculate(arguments.calculate))


if __name__ == '__main__':
    main()
