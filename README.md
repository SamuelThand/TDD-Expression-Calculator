# Assignment 2 

## Environment & Tools
Ubuntu 20.04, PyCharm 2021.2.1 (Professional Edition), Git 2.25.1, Python 3.8

## Purpose
The purpose of this assignment was to provide experience in TDD(Test Driven Development) by developing an expression
calculator using the principles of TDD.

The concrete goals were:

* Class-based solution
* No use of third-party libraries for challenges, automating calculations or parsing
* Include `lab2_expressions.git` as a Git submodule
* Unit testing using `unittest`
  * Conduct the work according to the principles of TDD, with incremental progression and small/concise tests.
  * Integrity tests for the class design using reflection/introspection
  * Validation tests from math expressions provided in `lab2_expressions.git` need to be built, and passed
* Classes, methods, and tests documented
* Parse arguments using `argparse` library
* Read math expressions using `json` library
* Implement calculator
  * Takes arguments from the command line as a single string
  * Parse and calculate expression using operator precedence
  * Support `+ - * / ^ ( )` symbols
  * Return the correct result for the test expressions

## Procedures

### Test module
The tests are structured with one class inheriting from unittest.TestCase for each method in the calculator, one for 
validation testing of the program, and one class for each of the TestTokenType, TestToken, and Operations classes. 

Where applicable the test data is loaded into the class using the setUpClass() class method together with the json library. The
tests are parameterized using the unittest.TestCase.subTest() method, under which each parameterized test is executed once for each 
test expression.

### Argument parsing
Created an argument parser using the `argparse` library, and added the `calculate` argument, which would allow for
passing a math expression using `-c [expression]`. This argument was parsed and passed to the `Calculator.calculate()`
method. The behavior of the calculator is tested with the `TestCalculator.test_calculator_returns_correct_result()` test
case which validates that all test expressions are evaluated correctly.

### Tokenization
The Calculator.calculate() method uses the `__tokenize_calculation()` method to parse the characters of the input string.
Whitespace and quotes are removed using the `re` (regex) library and then each token is iterated over and pattern-matched
against the `operators` list: `['+', '-', '*', '/', '^', '(', ')']` and using the `isdigit()` method. Multiple following digits are grouped into a single number.

Upon a match, an object of the class `Token` is created, with a field of type `TokenType` and the actual value, which is
stored in a list. This list of tokens is then returned. These classes are tested by the `TestToken` and `TestTokenType` classes.

The `__tokenize_calculation()` method is tested by the `TestTokenizeExpression` class which tests that whitespace and quotes are removed,
a populated list of tokens is returned, and each token is identified correctly.

### Parsing and Calculation
The tokens are used to create an iterator object using the `iter()` method. This is used to iterate over the tokens
throughout the series of parsing functions without specifying multiple loops and manually incrementing counters.

`The __next_token()` method calls the `iterator.next()` method and assigns the next token to the `__current_token`
field for access throughout the class. The token to be returned where the tokens list ends is `Token(TokenType.END, '')`
which is used to identify the end of the original expression. This method is used by each parsing method to iterate to the
next token after the processing of the current one is completed. This method is tested by the class `TestNextToken`
for correct iteration.

Each of the parsing methods uses operations defined in the `Operations` class. These are tested for correct functionality by
the `TestOperations` class.

The result of the expression is returned from the `_calculate_expression()` method, which makes use of the `_calculate_term()`
method to calculate each of the terms in the expression, as long as the existence of a term is indicated by the appearance
of a `PLUS`or `MINUS` token. The terms are then added or subtracted. This method takes a parameter for the expected end of the expression,
which has the default value of `END` or `RIGHT_PARENTHESIS` if called by `_calculate_exponentiation()`. When the token being examined is neither 
a `PLUS or MINUS` the expression should be iterated fully and the token should be equal to the expected end. If this is not the case, the expression is not formatted correctly,
and an error is thrown. If the expression is ended, as indicated by the studied token being of the `END` or `RIGHT_PARENTHESIS` type, the value is returned.
The `_calculate_expression()` method is tested by the `TestCalculateExpression` class which tests that it raises errors for
invalid expressions, returns the value of the expression, handles parenthesis, and returns float values.

The `_calculate_term()` method uses the `calculate_factor()` method in the same way, to calculate each of the factors
making up the term, then multiply or divide them. The `_calculate_term()` method is tested by the `TestCalculateTerm` class which tests that it identifies and
returns the value of a term, and returns float values.

The `_calculate_factor()` method also identifies `PLUS` and `MINUS` Tokens, but on this level, these token signifies
the negation operator, and the method uses recursion together with negation to calculate a negative factor where
applicable. This method uses the `_calculate_exponentiation()` method to determine if the current factor is part
of an exponentiation operation, and calculate it. The `_calculate_factor()` method is tested by the `TestCalculateFactor`
class which tests that it identifies and returns the value of the first factor, handles negation, and returns float values.

The `_calculate_exponentiation()` uses the `_calculate_expression()` method to identify an expression, if the token currently being studied is
a `LEFT_PARENTHESIS`. The expected end of the token is specified as `RIGHT_PARENTHESIS`. If there is no `LEFT_PARENTHESIS`, the
method uses the `_identify_number()` method to identify the numbers making up the factor. If an `EXPONENT` operator is found,
exponentiation is executed upon the two factors. Exponentiation involves factors but has higher precedence than division or multiplication, which is why they are handled
with higher priority. The `_calculate_exponentiation()` method is tested by the `TestCalculateExponentiation` class which tests that it 
identifies and calculates the value of the first exponentiation, handles leading parenthesis, returns the first number if no exponentiation exists,
and returns float values.

The `_identify_number()` method checks if the current token is of the type `NUMBER` as expected. If not, it raises an error indicating an
invalid expression. If it is, it returns the value of the number.

## Discussion
The concrete goals of the assignment has been fulfilled:

* The solution is class based
* No third party libraries have been used for challenges, automating calculations or parsing
*  `lab2_expressions.git` included as a Git submodule
* Unit tested with `unittest`
  * Work has been conducted in accordance with TDD
  * Integrity tests have been done using both reflection/introspection
  * Validation tests from math expressions provided in `lab2_expressions.git` exist, and are passed
* Classes, methods and tests are documented
* Arguments are parsed using `argparse` library
* Test expressions read using `json` library
* Calculator implemented
  * Takes arguments from commandline as a single string
  * Parses and calculates expression using operator precedence
  * Supports `+ - * / ^ ( )` symbols
  * Returns the correct result for the test expressions

My approach was a for me, advanced parsing program which took inspiration from building a compiler for a
programming language, including recursion use. Initially, this would include parsing symbols, building a binary tree of operations, and
then executing them in order of priority according to binary tree theory. However, due to TDD being very slow because of the complexity of 
the design, and a very tight time schedule because of other concurrent courses the operations tree was scrapped in favor of a more
direct and simplified approach - but still keeping some characteristics of more general token parsing.

It was hard to strictly adhere to clean TDD when the design of the project with its public interface and methods weren't
completely decided. This led to stress and very slow progress, because of the fear of having to rewrite both code and tests if the
design proved impractical down the line. Some aspects of the design seem to be impossible to just think out beforehand, without
writing code and "getting a foot through the door of the problem". The uncertainty of the final design also caused a hesitance
to commit changes that weren't a certainty to include, because of the added overhead of doing so many commits each with a descriptive 
message, just to undo all these commits down the line. This caused fewer large commits and waiting for each part of the program to 
"prove itself" for use in other parts of the program. This was unsafe from a data storage perspective, since
much work would be lost if there would be a hardware failure on the development pc before changes had been pushed to remote. 

The domain knowledge also needs to be high to efficiently design how the system modules should look, behave and interact. The
domain of this project was parsing, and to do the parsing there needed to be an understanding of mathematics, with a focus on 
understanding expressions, being built up by terms, being built up by factors, being built up atomic tokens in the form of numbers. Unary
operators were also needed in the form of the negation operator `-`, and the special case of exponentiation which is similar to multiplication and
division, but has a higher priority. And this had to be translated to understand how it should be parsed to reflect the model.

The lesson I have learned from this is that it is very easy to trip up and be tempted to step away from the clean TDD principles, and sometimes
probably necessary to figure out problems, prototype and get some code on the screen and learn about the problem domain - since one can go
crazy without being allowed to just act and try to actively work with the problem instead of just sitting and thinking for days. This seems especially
true if methods call each other much, are intertwined in each other's functionality, and the exact functionality of each function
couldn't be figured out beforehand. But this should probably be done outside the official development tree, as a separate part of the process as a preparation 
for test-driven development of a project. But this also requires extra time which may not always be available.

The best approach for this assignment would likely have been to make a much simpler parsing procedure just based on looping
over the characters. I only realized this about halfway through, but this would have made the TDD process less frustrating and 
allowed for more time to plan out the design. This experience was very educative on how to think about TDD, its pitfalls, and how 
to utilize it for maximum benefit - and it will hopefully lead to an even better process for the final project.  

