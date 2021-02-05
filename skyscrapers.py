"""
Git link: https://github.com/Tsalyk/skyscrapers
"""

def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    with open(path, "r") as file:
        return list(map(lambda el: el.strip("\n"), file.readlines()))


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
    buildings = list(input_line)[1:pivot]
    return buildings == sorted(buildings)


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    return not "?" in "".join(board)


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    row = True
    column = True
    column_lst = [[] for i in range(len(board)-2)]

    board = board[1:len(board)-1]
    board = list(map(lambda lst: lst[1:len(lst)-1], board))

    for el in board:
        if len(set(el)) != len(el):
            row = False
        for ind, subel in enumerate(el):
            column_lst[ind].append(subel)

    for el in column_lst:
        if len(set(el)) != len(el):
            column = False

    return row and column


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
    i.e., for line 412453* , hint is 4, and 1245 are the four buildings
    that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    board = board[1:len(board)-1]

    hint_ind = [-1 if el.count("*") >= 2 else el.find("*") for el in board]
    counter = 0

    for ind, el in enumerate(board):
        if hint_ind[ind] > 0:
            hint = int(el[0])
            el = el[:-1]
            const = int(el[1])
            for i in range(1, len(el)):
                if int(el[i]) >= const:
                    const = int(el[i])
                    counter += 1
            if counter != hint:
                return False
            counter = 0

        elif hint_ind[ind] == 0:
            hint = int(el[-1])
            el = el[::-1]
            el = el[:-1]
            const = int(el[1])
            for i in range(1, len(el)):
                if int(el[i]) >= const:
                    const = int(el[i])
                    counter += 1
            if counter != hint:
                return False
            counter = 0

    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    up_hint = [(board[0].find(el) - 1, el) for el in board[0]
                if el.isdigit()]
    down_hint = [(board[-1].find(el) - 1, el) for el in board[-1]
                if el.isdigit()]

    column_lst = [[] for i in range(len(board)-2)]

    board = board[1:len(board)-1]
    board = list(map(lambda lst: lst[1:len(lst)-1], board))

    for el in board:
        for ind, subel in enumerate(el):
            column_lst[ind].append(subel)
    
    for ind, el in enumerate(column_lst):
        column_lst[ind] = "".join(el)

    for i in down_hint:
        column_lst[i[0]] = "*" + column_lst[i[0]] + i[1]
    for ind, el in enumerate(column_lst):
        if "*" not in el:
            column_lst[ind] = "*" + column_lst[ind] + "*"
    down = check_horizontal_visibility(column_lst)
    
    column_lst = list(map(lambda lst: lst[1:len(lst)-1], column_lst))
    column_lst = list(map(lambda lst: lst[::-1], column_lst))

    for i in up_hint:
        column_lst[i[0]] = "*" + column_lst[i[0]] + i[1]
    for ind, el in enumerate(column_lst):
        if "*" not in el:
            column_lst[ind] = "*" + column_lst[ind] + "*"
    up = check_horizontal_visibility(column_lst)

    return up and down


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    buildings = read_input(input_path)

    return (check_not_finished_board(buildings) and
            check_uniqueness_in_rows(buildings) and
            check_horizontal_visibility(buildings) and
            check_columns(buildings))
