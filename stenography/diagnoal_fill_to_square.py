from typing import List, Dict
from tqdm import tqdm
from random import shuffle


def diagonal_fill_to_square(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str,
        index: int):
    nouns_by_size = {}
    for noun in all_words_by_class["nouns"][:10000]:  # take more or less known words...
        if len(noun) <= len(secret_word):
            nouns_by_size.setdefault(len(noun), []).append(noun)
    result = {}
    total = len(nouns_by_size.keys())
    for size in tqdm(sorted(list(nouns_by_size.keys()), reverse=True), total=total):
        nouns = nouns_by_size[size]
        shuffle(nouns)  # ...but shuffle then to make encoding different
        for noun in nouns:
            if noun[index] == secret_word[size-1]:
                result[size] = noun
                break
    return "\n".join((result[s] for s in sorted(list(result.keys()))))


def diagonal_fill_to_square_last(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str):
    """
    Provides list of words with missing LAST letter. Filled LAST letters form new word.
    Example:
        СОБАКА
        -
        [no output for first letter]
        г[о]
        бо[б]
        нор[а]
        рыба[к]
        калек[а]
    They are convenient to be placed in a square with missing last column
    (words are spelled diagonally):
        крнбг?
        -аыоо?
        --лбр?
        ---еа?
        ----к?
        -----?
    With "-" as any other letters
    """
    return diagonal_fill_to_square(all_words_by_class, secret_word, -1)


def diagonal_fill_to_square_first(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str):
    """
    Provides list of words with missing FIRST letter. Filled FIRST letters form new word.
    Example:
        СОБАКА
        -
        [no output for first letter]
        [о]м
        [б]ек
        [а]том
        [к]ишка
        [а]ммиак
    They are convenient to be placed in a square with missing first row
    (words are spelled diagonally):
        ??????
        -митем
        --мшок
        ---икм
        ----аа
        -----к
    With "-" as any other letters
    """
    return diagonal_fill_to_square(all_words_by_class, secret_word, 0)
