import itertools

from tqdm import tqdm
import copy


__all__ = ["find_most_complicated_phone_locks"]


_legal_moves = [
    (1, 0),
    (0, 1),

    (2, 1),
    (1, 1),
    (1, 2),

    (2, -1),
    (1, -1),
    (1, -2),
]


def _index(col, row):
    return col + 3 * row


def _is_outside_of_board(col, row):
    return not (0 <= col <= 2 and 0 <= row <= 2)


def find_most_complicated_phone_locks():
    """
    Finds list of all "the most complicated" graphical phone lock patterns
    See
    https://www.youtube.com/watch?v=PKjbBQ0PBCQ&t=488s&ab_channel=Dr.Zye
    for what counts as "the most complicated pattern"
    Exactly 296 solutions exist. This function returns order of points to
    be used to generate lock for each of them.
    """
    solutions = []

    def solve(board, col, row, step, moves_left):
        if moves_left:
            for i, origin_move in enumerate(moves_left):
                for direction in [1, -1]:
                    directed_move = tuple(direction * m for m in origin_move)
                    new_col, new_row = col + directed_move[0], row + directed_move[1]
                    if _is_outside_of_board(new_col, new_row):
                        continue
                    idx = _index(new_col, new_row)
                    if board[idx] != 0 and origin_move in {(1, 0), (0, 1), (1, 1), (1, -1)}:
                        # In this situation we can skip that dot!
                        new_col, new_row = new_col + directed_move[0], new_row + directed_move[1]
                        if _is_outside_of_board(new_col, new_row):
                            continue
                        idx = _index(new_col, new_row)
                    if board[idx] == 0:
                        board_copy = copy.deepcopy(board)
                        board_copy[idx] = step
                        solve(board_copy, new_col, new_row, step + 1, moves_left[:i] + moves_left[i + 1:])
        else:
            solutions.append(copy.deepcopy(board))  # recursion bottom

    for c, r in tqdm(itertools.product(range(3), range(3)), total=9):
        board = [0] * 9
        board[_index(c, r)] = 1
        solve(board, c, r, 2, _legal_moves[:])

    def _stringify_solutions():
        solutions_str = []
        for solution in solutions:
            solutions_str.append("\n".join([" ".join(map(str, solution[3 * col: 3 * col + 3])) for col in range(3)]))
        return solutions_str

    return _stringify_solutions()
