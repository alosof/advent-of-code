import os
from typing import List, Tuple, Set

from year_2020.solutions.python.utils.files import INPUTS_FOLDER
from year_2020.solutions.python.utils.timing import timer


@timer
def solve_2(player_1: List[int], player_2: List[int]) -> int:
    player_1_copy, player_2_copy = player_1.copy(), player_2.copy()
    winner_id, winner_deck = recursive_combat(player_1_copy, player_2_copy, set())
    return sum(winner_deck[i] * (len(winner_deck) - i) for i in range(len(winner_deck)))


def recursive_combat(player_1: List[int],
                     player_2: List[int],
                     memory: Set[Tuple[List[int], List[int]]]) -> Tuple[int, List[int]]:
    if len(player_1) == 0 or len(player_2) == 0:
        winner_id, winner_deck = winner(player_1, player_2)
        return winner_id, winner_deck
    else:
        while len(player_1) > 0 and len(player_2) > 0 and (len(player_1) <= player_1[0] or len(player_2) <= player_2[0]):
            if (tuple(player_1), tuple(player_2)) in memory:
                return 1, player_1
            memory.add((tuple(player_1), tuple(player_2)))
            top_p1 = player_1.pop(0)
            top_p2 = player_2.pop(0)
            if top_p1 > top_p2:
                player_1 = player_1 + [top_p1] + [top_p2]
            else:
                player_2 = player_2 + [top_p2] + [top_p1]
            if (tuple(player_1), tuple(player_2)) in memory:
                return 1, player_1
        if len(player_1) == 0 or len(player_2) == 0:
            winner_id, winner_deck = winner(player_1, player_2)
            return winner_id, winner_deck
        else:
            top_p1 = player_1.pop(0)
            top_p2 = player_2.pop(0)
            p1_sub_deck = player_1[:top_p1]
            p2_sub_deck = player_2[:top_p2]
            round_winner_id, _ = recursive_combat(p1_sub_deck, p2_sub_deck, set())
            if round_winner_id == 1:
                player_1 = player_1 + [top_p1] + [top_p2]
            elif round_winner_id == 2:
                player_2 = player_2 + [top_p2] + [top_p1]
            return recursive_combat(player_1, player_2, memory)


@timer
def solve_1(player_1: List[int], player_2: List[int]) -> int:
    player_1_copy, player_2_copy = player_1.copy(), player_2.copy()
    winner_id, winner_deck = combat(player_1_copy, player_2_copy)
    return sum(winner_deck[i] * (len(winner_deck) - i) for i in range(len(winner_deck)))


def combat(player_1: List[int], player_2: List[int]) -> Tuple[int, List[int]]:
    while len(player_1) > 0 and len(player_2) > 0:
        top_card_player_1: int = player_1.pop(0)
        top_card_player_2: int = player_2.pop(0)
        if top_card_player_1 > top_card_player_2:
            player_1.extend([top_card_player_1, top_card_player_2])
        else:
            player_2.extend([top_card_player_2, top_card_player_1])
    return winner(player_1, player_2)


def winner(player_1: List[int], player_2: List[int]) -> Tuple[int, List[int]]:
    if len(player_1) == 0:
        return 2, player_2
    elif len(player_2) == 0:
        return 1, player_1
    else:
        raise ValueError('Both players still have cards in their decks !')


def read_players_decks(input_path: str) -> Tuple[List[int], List[int]]:
    with open(input_path, 'r') as input_file:
        content = input_file.read()
        player_1_block, player_2_block = content.split('\n\n')
        return [int(c) for c in player_1_block.split('\n')[1:]], [int(c) for c in player_2_block.split('\n')[1:]]


if __name__ == "__main__":
    input_file_path: str = os.path.join(INPUTS_FOLDER, 'day_22', 'input.txt')
    player_1_deck, player_2_deck = read_players_decks(input_path=input_file_path)

    # Part 1
    part_1_result: int = solve_1(player_1=player_1_deck, player_2=player_2_deck)
    print('Part 1 result :', part_1_result)
    assert part_1_result == 36257

    # Part 2
    part_2_result: int = solve_2(player_1=player_1_deck, player_2=player_2_deck)
    print('Part 2 result :', part_2_result)
    assert part_2_result == 33304
