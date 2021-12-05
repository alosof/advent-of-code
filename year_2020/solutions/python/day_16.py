import os
from math import prod
from typing import Tuple, List, Dict, Set

from year_2020.solutions.python.utils.dict import remove_key_from_mapping, remove_value_from_mapping
from year_2020.solutions.python.utils.files import INPUTS_FOLDER


def multiply_departure_fields(own_ticket: List[int],
                              other_tickets: List[List[int]],
                              rules: Dict[str, Tuple[range, range]]) -> int:
    field_positions: Dict[str, int] = find_exact_field_positions(tickets_for_field_inference=other_tickets, rules=rules)
    return prod(own_ticket[field_positions[field]] for field in field_positions if field.startswith('departure'))


def find_exact_field_positions(tickets_for_field_inference, rules: Dict[str, Tuple[range, range]]) -> Dict[str, int]:
    valid_tickets: List[List[int]] = [t for t in tickets_for_field_inference if is_ticket_valid(t, rules)]
    possible_fields_by_position: Dict[int, Set[str]] = find_possible_fields_by_position(valid_tickets, rules)
    field_positions: Dict[str, int] = assign_one_position_to_each_field(possible_fields_by_position, {})
    return field_positions


def assign_one_position_to_each_field(possible_fields_by_position: Dict[int, Set[str]],
                                      field_positions: Dict[str, int]) -> Dict[str, int]:
    if len(possible_fields_by_position) == 0:
        return field_positions
    else:
        for pos in possible_fields_by_position:
            possible_fields_for_pos = possible_fields_by_position[pos]
            if len(possible_fields_for_pos) == 1:
                identified_field: str = list(possible_fields_for_pos)[0]
                field_positions[identified_field] = pos
                possible_fields_by_position = remove_key_from_mapping(pos, possible_fields_by_position)
                possible_fields_by_position = remove_value_from_mapping(identified_field, possible_fields_by_position)
                return assign_one_position_to_each_field(possible_fields_by_position, field_positions)


def find_possible_fields_by_position(tickets: List[List[int]],
                                     rules: Dict[str, Tuple[range, range]]) -> Dict[int, Set[str]]:
    return dict((position, possible_fields(position, tickets, rules)) for position in range(len(tickets[0])))


def possible_fields(position: int, tickets: List[List[int]], rules: Dict[str, Tuple[range, range]]) -> Set[str]:
    same_position_values: List[int] = [ticket[position] for ticket in tickets]
    return set(field for field in rules if is_field_possible(field, same_position_values, rules))


def is_field_possible(field: str, same_position_values: List[int], rules: Dict[str, Tuple[range, range]]) -> bool:
    return all(is_value_in_ranges(value, rules[field]) for value in same_position_values)


def is_ticket_valid(ticket: List[int], rules: Dict[str, Tuple[range, range]]) -> bool:
    return all(is_value_valid(value, rules) for value in ticket)


def ticket_scanning_error_rate(tickets: List[List[int]], rules: Dict[str, Tuple[range, range]]) -> int:
    return sum([value for ticket in tickets for value in ticket if not is_value_valid(value, rules)])


def is_value_valid(value: int, rules: Dict[str, Tuple[range, range]]) -> bool:
    return any(is_value_in_ranges(value, range_pair) for range_pair in rules.values())


def is_value_in_ranges(value: int, range_pair: Tuple[range, range]) -> bool:
    return value in range_pair[0] or value in range_pair[1]


def read_rules_and_tickets(input_path: str) -> Tuple[Dict[str, Tuple[range, range]],
                                                     List[int],
                                                     List[List[int]]]:
    with open(input_path, 'r') as input_file:
        content = input_file.read()
        rules_block, my_ticket_block, nearby_tickets_block = content.split('\n\n')
        rules_parsed = dict(parse_rule_line(r) for r in rules_block.split('\n'))
        my_ticket_parsed: List[int] = parse_ticket_line(my_ticket_block.split('\n')[1])
        nearby_tickets_parsed: List[List[int]] = [parse_ticket_line(t) for t in nearby_tickets_block.split('\n')[1:]]
    return rules_parsed, my_ticket_parsed, nearby_tickets_parsed


def parse_ticket_line(ticket_line: str) -> List[int]:
    return [int(value) for value in ticket_line.split(',')]


def parse_rule_line(rule_line: str) -> Tuple[str, Tuple[range, range]]:
    field, ranges = rule_line.split(': ')
    first_range, second_range = tuple(parse_text_range(r) for r in ranges.split(' or '))
    return field, (first_range, second_range)


def parse_text_range(text_range: str) -> range:
    lower_bound, upper_bound = text_range.split('-')
    return range(int(lower_bound), int(upper_bound) + 1)


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_16', 'input.txt')
    field_rules, my_ticket, nearby_tickets = read_rules_and_tickets(input_path=input_file_path)

    # Part 1
    part_1_result: int = ticket_scanning_error_rate(tickets=nearby_tickets, rules=field_rules)
    assert part_1_result == 27802
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = multiply_departure_fields(own_ticket=my_ticket,
                                                   other_tickets=nearby_tickets,
                                                   rules=field_rules)
    assert part_2_result == 279139880759
    print('Part 2 result :', part_2_result)
