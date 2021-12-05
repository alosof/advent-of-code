import os
import re
from functools import reduce
from typing import List, Dict, Tuple, Set, Callable, Generator

from year_2020.solutions.python.utils.files import read_lines, INPUTS_FOLDER


def count_bags(bag_color: str,
               plain_text_rules: List[str],
               count_method: Callable[[str, Dict[str, List[Tuple[int, str]]]], int]) -> int:
    rule_dict: Dict[str, List[Tuple[int, str]]] = build_rule_dictionary(plain_text_rules)
    return count_method(bag_color, rule_dict)


def count_all_sub_bags(bag_color: str, rule_dict: Dict[str, List[Tuple[int, str]]]) -> int:
    sub_bags_with_counts: List[Tuple[int, str]] = rule_dict[bag_color]
    return sum([sub_bag[0] * (1 + count_all_sub_bags(sub_bag[1], rule_dict)) for sub_bag in sub_bags_with_counts])


def count_distinct_containers(bag_color: str, rule_dict: Dict[str, List[Tuple[int, str]]]) -> int:
    return sum((bag_color in find_distinct_sub_bags(color, rule_dict) for color in rule_dict))


def find_distinct_sub_bags(bag_color: str, rule_dict: Dict[str, List[Tuple[int, str]]]) -> Set[str]:
    sub_bags: Set[str] = set((sub_bag[1] for sub_bag in rule_dict[bag_color]))
    sub_sub_bags: Generator[Set[str], None, None] = (find_distinct_sub_bags(sub_bag, rule_dict) for sub_bag in sub_bags)
    return sub_bags.union(reduce(lambda x, y: x.union(y), sub_sub_bags, set()))


def build_rule_dictionary(rules: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    return reduce(lambda x, y: {**x, **y}, (parse_single_rule(rule) for rule in rules))


def parse_single_rule(rule: str) -> Dict[str, List[Tuple[int, str]]]:
    main_bag_color: str = re.search(r'[a-z]+ [a-z]+', string=rule).group()
    sub_bags: List[Tuple[int, str]] = [(int(sub_bag[0]), sub_bag[2:])
                                       for sub_bag in re.findall(r'\d [a-z]+ [a-z]+', string=rule)]
    return {main_bag_color: sub_bags}


if __name__ == '__main__':
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_07', 'input.txt')
    input_list: List[str] = read_lines(input_file_path=input_file_path, line_type=str)

    # Part 1
    part_1_result: int = count_bags('shiny gold', input_list, count_distinct_containers)
    assert part_1_result == 370
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: int = count_bags('shiny gold', input_list, count_all_sub_bags)
    assert part_2_result == 29547
    print('Part 2 result :', part_2_result)
