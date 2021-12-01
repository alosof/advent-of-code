from pathlib import Path
from typing import List

YEAR_DIRECTORY = Path(__file__).parent.parent.parent.parent
PYTHON_SOLUTIONS_DIRECTORY = YEAR_DIRECTORY / 'solutions' / 'python'
INPUTS_FOLDER = YEAR_DIRECTORY / 'inputs'


def read_lines(input_file_path: Path, line_type: type) -> list:
    with open(input_file_path, 'r') as input_file:
        return [line_type(line) for line in input_file.read().splitlines()]
