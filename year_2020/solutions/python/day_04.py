import os
import re
from typing import List, Callable

from year_2020.solutions.python.utils.files import read_blocks, INPUTS_FOLDER


def count_valid_passports(passports: List[str],
                          mandatory_fields: List[str],
                          validation_function: Callable[[str, str], bool]) -> int:
    return sum(all((validation_function(field, passport) for field in mandatory_fields)) for passport in passports)


def validate_presence(field: str, passport: str) -> bool:
    return field in passport


def validate_presence_and_value(field: str, passport: str) -> bool:
    field_pos: int = passport.find(field)
    if field_pos == -1:
        return False
    else:
        value: str = passport[field_pos:].split(' ')[0].split(':')[-1]
        return check_field(field, value)


def check_field(field: str, value: str) -> bool:
    if field == 'byr':
        return bool(re.fullmatch(r'\d{4}', value)) and (1920 <= int(value) <= 2002)
    elif field == 'iyr':
        return bool(re.fullmatch(r'\d{4}', value)) and (2010 <= int(value) <= 2020)
    elif field == 'eyr':
        return bool(re.fullmatch(r'\d{4}', value)) and (2020 <= int(value) <= 2030)
    elif field == 'hgt':
        return bool(re.fullmatch(r'\d+cm', value)) and (150 <= int(value[:-2]) <= 193) or \
               bool(re.fullmatch(r'\d+in', value)) and (59 <= int(value[:-2]) <= 76)
    elif field == 'hcl':
        return bool(re.fullmatch(r'#[a-f0-9]{6}', value))
    elif field == 'ecl':
        return bool(re.fullmatch(r'(amb|blu|brn|gry|grn|hzl|oth)', value))
    elif field == 'pid':
        return bool(re.fullmatch(r'\d{9}', value))
    else:
        raise ValueError(f'Unknown validation rule for field {field}')


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_04', 'input.txt')
    input_list: List[str] = read_blocks(input_file_path)

    fields_to_check: List[str] = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    # Part 1
    part_1_result: int = count_valid_passports(passports=input_list,
                                               mandatory_fields=fields_to_check,
                                               validation_function=validate_presence)
    assert part_1_result == 228
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_valid_passports(passports=input_list,
                                               mandatory_fields=fields_to_check,
                                               validation_function=validate_presence_and_value)
    assert part_2_result == 175
    print('Part 2 result :', part_2_result)
