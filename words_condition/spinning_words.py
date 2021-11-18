from tqdm import tqdm
from typing import Set, Dict, List

__all__ = ["find_spinning_words"]


def find_spinning_words(all_words_by_class: Dict[str, List[str]]) -> Set[frozenset]:
    """
    Finds all words which after being cycled form new valid words.
    Example:
    никель, ельник
    насос, сосна
    казна, наказ
    ...
    """
    nouns = all_words_by_class["nouns"]
    possible_spinning_words = [word for word in nouns if 3 < len(word) < 8]
    result = set()
    for word in tqdm(possible_spinning_words, total=len(possible_spinning_words)):
        chain = {word}
        cycled_word = word
        for _ in range(len(word) - 1):
            cycled_word = cycled_word[1:] + cycled_word[0]
            if cycled_word in possible_spinning_words:
                chain.add(cycled_word)
        if len(chain) > 1:
            result.add(frozenset(chain))
    return result
