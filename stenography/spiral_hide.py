from math import sqrt, ceil
from dataclasses import dataclass


def spiral_hide(_, secret_word: str):
    """
    Rolls message in spiral in square matrix:
        фиолетоваяантилопа
        ---
        фиоле
        опа-т
        л---о
        и---в
        тнаяа
    Where "-" designates any random letters
    Add random letters around square for extra difficulty
    """
    side = ceil(sqrt(len(secret_word)))
    square = [["-" for __ in range(side)] for _ in range(side)]

    @dataclass
    class Direction:
        xstride: int
        ystride: int
        boundary: int

        def is_on_boundary(self, x, y):
            return self.boundary == (x if self.xstride != 0 else y)

        def decrease_boundary(self):
            self.boundary -= self.xstride if self.xstride != 0 else self.ystride

    directions = [Direction(1, 0, side-1), Direction(0, 1, side-1),
                  Direction(-1, 0, 0), Direction(0, -1, 1)]
    direction_idx, x, y = 0, 0, 0
    for letter in secret_word:
        square[y][x] = letter
        current_direction = directions[direction_idx]
        x += current_direction.xstride
        y += current_direction.ystride
        if current_direction.is_on_boundary(x, y):
            current_direction.decrease_boundary()
            direction_idx = 0 if direction_idx == len(directions) - 1 else direction_idx + 1

    return "\n".join(("".join(ch for ch in line) for line in square))
