from itertools import product
from typing import List


def lettery_math_table() -> List[str]:
    result = []
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
    for opsign, opstrrepr in operations:
        for (x, xstrrepr), (y, ystrrepr) in product(numbers, numbers):
            strresult = len(xstrrepr) + len(opstrrepr) + len(ystrrepr)
            line = str(x) + " " + opsign + " " + str(y) + " = " + str(strresult)
            result.append(line)
    return result
