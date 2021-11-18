import re


def is_cyrillic(letter):
    # TODO: rework
    return bool(re.search('[а-яА-Я]', letter))


def validate_word(word):
    if not any([is_cyrillic(l) for l in word]):
        raise RuntimeError("Found non cyrillic symbol or space or hyphen")