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
