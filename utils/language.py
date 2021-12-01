from enum import Enum, unique

from typing import List


class UnknownLanguage(ValueError):
    def __init__(self, lang: str):
        super().__init__(f"Tried to convert to language string {lang!r}; "
                         f"known languages are: " + ", ".join([elem.value for elem in Language]))


@unique
class Language(str, Enum):
    NONE = "none",
    ALL = "all",
    RUSSIAN = "russian",
    ENGLISH = "english"

    @staticmethod
    def from_str(strrepr):
        try:
            return next(elem for elem in Language if elem.value == strrepr)
        except StopIteration as e:
            raise UnknownLanguage(strrepr) from e


def get_known_parts_of_speech() -> List[str]:
    return ["nouns", "verbs", "adjectives"]


