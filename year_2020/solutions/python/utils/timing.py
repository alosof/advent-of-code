from functools import wraps
from time import time_ns
from typing import List, Tuple


def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start_time = time_ns()
        result = func(*args, **kwargs)
        end_time = time_ns()
        print(f'%%timeit | {func.__name__} :', format_duration(end_time - start_time))
        return result

    return wrap


def format_duration(duration_ns: int) -> str:
    decomposition: List[Tuple[int, str]] = decompose(duration_ns)
    return parse_decomposed_duration(decomposition)


def decompose(duration_ns: int) -> List[Tuple[int, str]]:
    components: List[Tuple[int, str]] = [(1000, 'ns'), (1000, 'μs'), (1000, 'ms'), (60, 's'), (60, 'min'), (1, 'h')]
    left_to_decompose: int = duration_ns
    decomposition: List[Tuple[int, str]] = []
    for component_divisor, component_unit in components:
        component_value: int = left_to_decompose % component_divisor if component_unit != 'h' else left_to_decompose
        decomposition = [(component_value, component_unit)] + decomposition
        left_to_decompose = left_to_decompose // component_divisor
        if left_to_decompose == 0:
            break
    return decomposition


def parse_decomposed_duration(decomposition: List[Tuple[int, str]]) -> str:
    principal_value: int = decomposition[0][0]
    principal_unit: str = decomposition[0][1]
    if principal_unit == 'ns':
        return f'{principal_value} {principal_unit}'
    else:
        secondary_value: int = decomposition[1][0]
        secondary_unit: str = decomposition[1][1]
        if principal_unit in ('min', 'h'):
            return f'{str(principal_value)} {principal_unit} {str(secondary_value)} {secondary_unit}'
        else:
            value: float = principal_value + secondary_value / 1000.
            formatted_value: str = '{:.3f}'.format(value)
            return f'{formatted_value} {principal_unit}'
