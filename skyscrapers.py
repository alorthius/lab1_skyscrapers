"""
GitHub link: https://github.com/alorthius/lab1_skyscrapers
"""


def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.
    """
    if not isinstance(path, str):
        return None

    board_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            board_list.append(str(line))
    return board_list


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if not isinstance(input_line, str) or not isinstance(pivot, int):
        return None

    board = input_line[1:]
    highest_building = board[0]
    building_number = 1
    visible_buildings = 1

    while building_number != len(board):
        current_building = board[building_number]
        building_number += 1

        if current_building > highest_building:
            highest_building = current_building
            visible_buildings += 1

    if visible_buildings != pivot:
        return False

    return True


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', \
    '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    """
    if not isinstance(board, list):
        return None

    for row in board:
        for element in row:
            if element == '?':
                return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', \
    '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', \
    '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', \
    '*41532*', '*2*1***'])
    False
    """
    if not isinstance(board, list):
        return None

    for row in board:
        if row.startswith('*') and row.endswith('*'):
            continue

        row = row[1:-1]
        row = row.replace('*', '')

        if len(row) != len(set(row)):
            return False
    return True


def check_by_left_hint(row: str) -> int:
    """
    Check row-wise visibility in left-right way.
    Return the integer of the visible buildings.
    """
    if not isinstance(row, str):
        return None

    highest_building = row[0]
    building_number = 1
    visible_buildings = 1

    while building_number != len(row):
        current_building = row[building_number]
        building_number += 1

        if current_building > highest_building:
            highest_building = current_building
            visible_buildings += 1

    return visible_buildings


def check_by_right_hint(row: str) -> int:
    """
    Check row-wise visibility in right-left way.
    Return the integer of the visible buildings.
    """
    if not isinstance(row, str):
        return None

    highest_building = row[-1]
    building_number = len(row)
    visible_buildings = 1

    while building_number != 0:
        current_building = row[building_number - 1]
        building_number -= 1

        if current_building > highest_building:
            highest_building = current_building
            visible_buildings += 1

    return visible_buildings


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
    i.e., for line 412453* , hint is 4, and 1245 are the four buildings
    that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    """
    if not isinstance(board, list):
        return None

    for row in board:
        try:
            left_hint = int(row[0])
        except ValueError:
            left_hint = False

        try:
            right_hint = int(row[-1])
        except ValueError:
            right_hint = False

        row = row[1:-1]

        if left_hint:
            visible_buildings = check_by_left_hint(row)

            if visible_buildings != left_hint:
                return False

        if right_hint:
            visible_buildings = check_by_right_hint(row)

            if visible_buildings != right_hint:
                return False

    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', \
    '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', \
    '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', \
    '*2*1***'])
    False
    """
    if not isinstance(board, list):
        return None

    board = [row[1:-1] for row in board]
    new_board = []
    index = 0
    while index != len(board[0]):
        new_row = ''
        for row in board:
            new_row += row[index]
        new_board.append(new_row)
        index += 1

    if not check_uniqueness_in_rows(new_board) or not check_horizontal_visibility(new_board):
        return False

    return True


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    if not isinstance(input_path, str):
        return None

    board = read_input(input_path)
    if (not check_uniqueness_in_rows(board) or not check_horizontal_visibility(board)
            or not check_columns(board)):
        return False
    return True
