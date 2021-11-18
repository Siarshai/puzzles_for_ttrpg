from collections import Counter, defaultdict
from random import shuffle

from utils.load_words import load_words
from typing import List, Dict

from utils.word_validation import is_cyrillic


def hide_in_nth_letters(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str,
        nth_letter: str):
    """
    The most common stenography technique - hides letters of secret word
    in nth letter of every word in the message
    Example:
    встречаемсявбаре,2
    деВственный наСмешливый моТор мэРия свЕрнутый туЧа усАдьба трЕск заМочный
    меСторождение неЯркий осВещать узБекский шлАнг каРманный увЕсти
    """
    nth_letter = int(nth_letter)
    words = all_words_by_class["nouns"][1000:5000] \
            + all_words_by_class["verbs"][1000:5000] \
            + all_words_by_class["adjectives"][1000:5000]
    shuffle(words)
    if not any([is_cyrillic(l) for l in secret_word]):
        raise RuntimeError("Found non cyrillic symbol or space or hyphen")
    secret_word = secret_word.lower()

    words = [word for word in words if len(word) > nth_letter]
    needed_letters = Counter(secret_word)
    gathered_words = defaultdict(list)
    for letter, count in needed_letters.items():
        for word in words:
            if word[nth_letter] == letter:
                gathered_words[letter].append(word)
            if len(gathered_words[letter]) >= count:
                break
        else:
            raise RuntimeError(f"Not enough words for letter {letter}")
    return " ".join([gathered_words[letter].pop() for letter in secret_word])
