import os
from math import prod
from typing import List, Callable

from year_2020.solutions.python.utils.files import INPUTS_FOLDER, read_lines
from year_2020.solutions.python.utils.timing import timer
from operator import add, mul

OPS = {
    '+': add,
    '*': mul
}


@timer
def do_homework(expressions: List[str], simple_expression_evaluator: Callable[[str], int]) -> int:
    return sum(evaluate(expression, simple_expression_evaluator) for expression in expressions)


def evaluate(expression: str, simple_expression_evaluator: Callable[[str], int]) -> int:
    last_opening_pos: int = expression.rfind('(')
    if last_opening_pos == -1:
        return simple_expression_evaluator(expression)
    else:
        matching_closing_pos: int = last_opening_pos + expression[last_opening_pos:].find(')')
        expression_between_parentheses: str = expression[(last_opening_pos + 1):matching_closing_pos]
        new_expression: str = expression[:last_opening_pos] \
                              + str(simple_expression_evaluator(expression_between_parentheses)) \
                              + expression[(matching_closing_pos + 1):]
        return evaluate(new_expression, simple_expression_evaluator)


def evaluate_with_no_precedence(expression_without_parentheses: str):
    operand_1_limit = expression_without_parentheses.index(' ')
    operand_1 = int(expression_without_parentheses[:operand_1_limit])
    operand_2 = ''
    op = None
    for c in expression_without_parentheses[operand_1_limit:]:
        if c in ('+', '*'):
            if len(operand_2) > 0:
                operand_1 = OPS[op](operand_1, int(operand_2))
                operand_2 = ''
            op = c
        elif c.isnumeric():
            operand_2 += c
    operand_1 = OPS[op](operand_1, int(operand_2))
    return operand_1


def evaluate_with_addition_precedence(expression_without_parentheses: str):
    return prod(eval(e) for e in expression_without_parentheses.split(' * '))


if __name__ == "__main__":
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_18', 'input.txt')
    input_lines: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = do_homework(expressions=input_lines,
                                     simple_expression_evaluator=evaluate_with_no_precedence)
    assert part_1_result == 1890866893020
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = do_homework(expressions=input_lines,
                                     simple_expression_evaluator=evaluate_with_addition_precedence)
    assert part_2_result == 34646237037193
    print('Part 2 result :', part_2_result)
