#!/usr/bin/env python

import argparse
import re
from enum import Enum
from dataclasses import dataclass
import json
import sys

__version__ = '1.0'
__desc__ = "A simple calculator that evaluates a mathematical expression using + - / * ()"

from typing import Optional


class TokenType(Enum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    EXPONENT = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7


class OperationType(Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3
    EXPONENTIATION = 4
    PLUS = 5
    MINUS = 6


@dataclass
class Token:
    type: TokenType
    value: any

    def __repr__(self):
        return f'{self.type.name} "{self.value}"'


@dataclass
class NumberNode:
    value: any

    def __repr__(self):
        return f'{self.value}'


@dataclass
class OperationNode:
    type: OperationType
    left_node: any
    right_node: Optional[any] = None

    def __repr__(self):
        if self.type == OperationType.ADD:
            return f"({self.left_node}+{self.right_node})"
        elif self.type == OperationType.SUBTRACT:
            return f"({self.left_node}-{self.right_node})"
        elif self.type == OperationType.MULTIPLY:
            return f"({self.left_node}*{self.right_node})"
        elif self.type == OperationType.DIVIDE:
            return f"({self.left_node}/{self.right_node})"
        elif self.type == OperationType.EXPONENTIATION:
            return f"({self.left_node}^{self.right_node})"
        elif self.type == OperationType.PLUS:
            return f"(+{self.left_node})"
        elif self.type == OperationType.MINUS:
            return f"(-{self.left_node})"


class Calculator:

    expression: str
    tokens: list
    current_token_index: int
    current_token: Token

    ## TODO fixa så att man initialiserar kalkylatorn med ett expression istället

    # def __init__(self, expression):
    #     self.expression = expression

    def calculate(self, calculation) -> OperationNode:
        self.tokens = self.tokenize_expression(calculation)
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        operations = self.parse_tokens()
        return operations

    def parse_tokens(self) -> OperationNode:

        if self.current_token is None:
            return None

        operations_tree = self.identify_expression()

        if self.current_token is not None:
            print('value of last token before returning', self.current_token)
            # raise Exception('Incorrect mathematical expression')

        print('value of last operations_tree before returning', operations_tree)

        return operations_tree

    def identify_expression(self):
        term_a = self.identify_term()

        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.next_token()
                # return OperationNode(OperationType.ADD, term_a, self.identify_term())
                term_a = OperationNode(OperationType.ADD, term_a, self.identify_term())

            elif self.current_token.type == TokenType.MINUS:
                self.next_token()
                # return OperationNode(OperationType.SUBTRACT, term_a, self.identify_term())
                term_a = OperationNode(OperationType.SUBTRACT, term_a, self.identify_term())

        return term_a

    def identify_term(self):
        factor_a = self.identify_factor()

        while (self.current_token is not None and self.current_token.type in
               (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.EXPONENT)):

            if self.current_token.type == TokenType.MULTIPLY:
                self.next_token()
                factor_a = OperationNode(OperationType.MULTIPLY, factor_a, self.identify_factor())
                # return OperationNode(OperationType.MULTIPLY, factor_a, self.identify_factor())

            elif self.current_token.type == TokenType.DIVIDE:
                self.next_token()
                factor_a = OperationNode(OperationType.DIVIDE, factor_a, self.identify_factor())
                # return OperationNode(OperationType.DIVIDE, factor_a, self.identify_factor())

            elif self.current_token.type == TokenType.EXPONENT:
                self.next_token()
                factor_a = OperationNode(OperationType.EXPONENTIATION, factor_a, self.identify_factor())
                # return OperationNode(OperationType.EXPONENTIATION, factor_a, self.identify_factor())

        return factor_a

    ## TODO nånting fel med inkrementeringen här
    def identify_factor(self):

        token = self.current_token

        if token.type == TokenType.LEFT_PARENTHESIS:
            self.next_token()
            factor = self.identify_expression()

            if self.current_token.type != TokenType.RIGHT_PARENTHESIS:
                raise Exception('Incorrect mathematical expression')

            self.next_token()
            return factor

        elif token.type == TokenType.NUMBER:
            self.next_token()
            return NumberNode(token.value)

        elif token.type == TokenType.PLUS:
            self.next_token()
            return OperationNode(OperationType.PLUS, left_node=self.identify_factor())

        elif token.type == TokenType.MINUS:
            self.next_token()
            return OperationNode(OperationType.MINUS, left_node=self.identify_factor())

        raise Exception('Incorrect mathematical expression')

    def next_token(self):
        self.current_token_index += 1
        try:
            self.current_token = self.tokens[self.current_token_index]
        except IndexError:
            self.current_token = None

        print('current token after incrementing', self.current_token)

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
                    tokens.append(Token(type=TokenType.PLUS, value=expression[i]))
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


def main():
    epilog = 'DT042G Calculator V' + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-c', '--calculate', dest='calculate', type=str,
                        help='The expression to calculate. Ex: 2+(4-5)/5*3')
    arguments = parser.parse_args()

    calculator = Calculator()
    print(calculator.calculate(arguments.calculate))


if __name__ == '__main__':
    main()
