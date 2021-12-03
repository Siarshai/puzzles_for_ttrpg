from io import StringIO
from typing import List, Dict

from utils.word_validation import is_russian_vowel


def validate_image(image: List[str]):
    for line in image:
        if not all("B" == c or "W" == c for c in line):
            raise ValueError("Image should contain only B and W characters")


def vowels_as_b_consonant_as_w(word: str) -> str:
    return "".join(("B" if is_russian_vowel(char) else "W") for char in word)


def format_output(image_coding_variants: Dict[str, List[str]]) -> str:
    buffer = StringIO()
    for line, words in image_coding_variants.items():
        buffer.write(line)
        buffer.write(":\n")
        for word in words:
            buffer.write("\t")
            buffer.write(word)
            buffer.write("\n")
        buffer.write("---\n")
    return buffer.getvalue()


def hide_image(all_words_by_class: Dict[str, List[str]], image_strrepr: str) -> str:
    """
    Hides image in words.
    Image string representation should contain lines of image separated by semicolon
    Lines of image should contain only "B" and "W" characters
    Algorithm output list of words for every line where vowels encode black pixels
    and consonants - white pixels
    Example:
    BBWW;WWBB

    BBWW:
        июнь
        июль
        уезд
        ...
    WWBB:
        змея
        стая
        хвоя
        ...
    """
    image_lines = image_strrepr.split(";")
    validate_image(image_lines)
    nouns = all_words_by_class["nouns"]
    coding_words = {word: vowels_as_b_consonant_as_w(word) for word in nouns}
    image_coding_variants = {}
    for line in image_lines:
        image_coding_variants[line] = []
        for word, coding in coding_words.items():
            if coding == line:
                image_coding_variants[line].append(word)
        if not image_coding_variants[line]:
            raise ValueError(f"Words for line {line!r} not found")
    return format_output(image_coding_variants)
