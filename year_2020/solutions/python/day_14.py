import os
from itertools import product
from typing import List, Union, Tuple, Dict

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def memory_size_after_initialization(initialization_program: List[str], version: int) -> int:
    memory: Dict[int, int] = {}
    mask: str = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    for line in initialization_program:
        parsed_line: Union[str, Tuple[int, int]] = parse_line(line)
        if isinstance(parsed_line, str):
            mask = parsed_line
        else:
            address, value = parsed_line
            if version == 1:
                masked_value: int = apply_mask_to_value(mask, value)
                memory[address] = masked_value
            elif version == 2:
                masked_addresses: List[int] = apply_mask_to_address(mask, address)
                for masked_address in masked_addresses:
                    memory[masked_address] = value
    return sum(memory.values())


def apply_mask_to_address(mask: str, address: int) -> List[int]:
    binary_address: str = str(bin(address))[2:]
    padded_binary_address: str = '0' * (len(mask) - len(binary_address)) + binary_address
    floating_masked_address: str = ''.join([a if m == '0' else m for (m, a) in zip(mask, padded_binary_address)])
    possible_addresses: List[int] = []
    nb_floating_values: int = floating_masked_address.count('X')
    for combination in product(*(range(2) for _ in range(nb_floating_values))):
        masked_address = floating_masked_address
        for floating_val in combination:
            floating_pos: int = masked_address.index('X')
            masked_address: str = masked_address[:floating_pos] + str(floating_val) + masked_address[floating_pos + 1:]
        possible_addresses.append(int(masked_address, base=2))
    return possible_addresses


def apply_mask_to_value(mask: str, value: int) -> int:
    binary_value: str = str(bin(value))[2:]
    padded_binary_value: str = '0' * (len(mask) - len(binary_value)) + binary_value
    masked_binary_value: str = ''.join([m if m != 'X' else v for (m, v) in zip(mask, padded_binary_value)])
    return int(masked_binary_value, base=2)


def parse_line(line: str) -> Union[str, Tuple[int, int]]:
    if line.startswith('mask'):
        return line.split(' = ')[-1]
    else:
        address = line[line.index('[') + 1:line.index(']')]
        value = line.split(' = ')[-1]
        return int(address), int(value)


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_14', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = memory_size_after_initialization(initialization_program=input_list, version=1)
    assert part_1_result == 7440382076205
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = memory_size_after_initialization(initialization_program=input_list, version=2)
    assert part_2_result == 4200656704538
    print('Part 2 result :', part_2_result)
