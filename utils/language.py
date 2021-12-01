from enum import Enum


class Language(Enum):
    NONE = 0,
    RUSSIAN = 1,
    ENGLISH = 2


def get_known_parts_of_speech():
    return ["nouns", "verbs", "adjectives"]