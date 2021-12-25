from itertools import product
from typing import List, Tuple


def lettery_math_table_common(numbers: List[Tuple[int, str]],
                              operations: List[Tuple[str, str]]) -> List[str]:
    result = []
    for opsign, opstrrepr in operations:
        for (x, xstrrepr), (y, ystrrepr) in product(numbers, numbers):
            strresult = len(xstrrepr) + len(opstrrepr) + len(ystrrepr)
            line = str(x) + " " + opsign + " " + str(y) + " = " + str(strresult)
            result.append(line)
    return result


def lettery_math_table_ru() -> List[str]:
    numbers = [
        (0, "ноль"),
        (1, "один"),
        (2, "два"),
        (3, "три"),
        (4, "четыре"),
        (5, "пять"),
        (6, "шесть"),
        (7, "семь"),
        (8, "восемь"),
        (9, "девять"),
        (10, "десять"),
        (11, "одиннадцать"),
        (12, "двенадцать"),
        (13, "тринадцать"),
        (14, "четырнадцать"),
        (15, "пятнадцать"),
        (16, "шестнадцать"),
        (17, "семнадцать"),
        (18, "восемнадцать"),
        (19, "девятнадцать"),
        (20, "двадцать")
    ]
    operations = [
        ("+", "плюс"),
        ("-", "минус"),
    ]
    return lettery_math_table_common(numbers, operations)


def lettery_math_table_en() -> List[str]:
    numbers = [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
        (10, "ten"),
        (11, "eleven"),
        (12, "twelve")
    ]
    # should there be add/subtract instead?
    operations = [
        ("+", "plus"),
        ("-", "minus"),
        ("x", "times"),
    ]
    return lettery_math_table_common(numbers, operations)


def lettery_math_table() -> List[str]:
    result = ["RU"]
    result.extend(lettery_math_table_ru())
    result.append("EN")
    result.extend(lettery_math_table_en())
    return result


def roman_dashes_math_table() -> List[str]:
    numbers = [
        (1, 1),  # I
        (2, 2),  # II
        (3, 3),  # III
        (4, 3),  # IV
        (5, 2),  # V
        (6, 3),  # VI
        (7, 4),  # VII
        (8, 5),  # VIII
        (9, 3),  # XI
        (10, 2),  # X
        (11, 3),  # XI
        (12, 4),  # XII
        (50, 2),  # L
        (1000, 4),  # M
    ]
    # should there be add/subtract instead?
    operations = [
        ("+", 2),
        ("-", 1),
        ("x", 2),
    ]
    result = []
    for opsign, opdashes in operations:
        for (x, xdashes), (y, ystrrepr) in product(numbers, numbers):
            dashes_result = xdashes + opdashes + ystrrepr
            line = str(x) + " " + opsign + " " + str(y) + " = " + str(dashes_result)
            result.append(line)
    return result
