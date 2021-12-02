from year_2020.solutions.python.utils.timing import timer


@timer
def find_encryption_key(door_public_key: int, card_public_key: int) -> int:
    card_loop_size: int = 1
    while True:
        if pow(7, card_loop_size, 20201227) == card_public_key:
            return pow(door_public_key, card_loop_size, 20201227)
        card_loop_size += 1


if __name__ == '__main__':
    door_pub: int = 17607508
    card_pub: int = 15065270

    # Part 1
    part_1_result: int = find_encryption_key(door_public_key=door_pub, card_public_key=card_pub)
    assert part_1_result == 12285001
    print('Part 1 result :', part_1_result)

    # Part 2
    part_2_result: str = '🎄'
    assert part_2_result == '🎄'
    print('Part 2 result :', part_2_result)
