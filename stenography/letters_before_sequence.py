from collections import Counter, defaultdict
from random import shuffle
from typing import List, Dict

from utils.word_validation import validate_word


def hide_letters_before_sequence(
        all_words_by_class: Dict[str, List[str]], secret_word: str, sequence: str):
    """
    Hides secret word one letter by one in other words before every designated
    marking sequence of words.
    Example:
    огуре,кот
    высокотехнологический мягкотелость чукотский коверкотовый щекотать
    выс/о/КОТ/ехнологический мя/г/КОТ/елость ч/у/КОТ/ский кове/р/КОТ/овый щ/е/КОТ/ать
    """
    words = all_words_by_class["nouns"] + all_words_by_class["verbs"] + all_words_by_class["adjectives"]
    shuffle(words)
    validate_word(secret_word)
    secret_word = secret_word.lower()
    words = [word for word in words if word.find(sequence) > 0]
    needed_letters = Counter(secret_word)
    gathered_words = defaultdict(list)
    for letter, count in needed_letters.items():
        for word in words:
            if word[word.find(sequence) - 1] == letter:
                gathered_words[letter].append(word)
            if len(gathered_words[letter]) >= count:
                break
        else:
            raise RuntimeError(f"Not enough words for letter {letter}")
    return " ".join([gathered_words[letter].pop() for letter in secret_word])

