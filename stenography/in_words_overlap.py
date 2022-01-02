import random
from io import StringIO
from typing import List, Dict, Union
from itertools import islice, chain


def hide_in_words_overlap(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str,
        count: Union[str, int] = 20):
    """
    Provides list of words encoding secret word. Last letter of first word and
    first letter of next word represent one letter of secret word.
    """
    count = int(count)
    nouns = all_words_by_class["nouns"]
    random.shuffle(nouns)  # for different results from different runs
    words_by_letter = {}
    for noun in nouns:
        words_by_letter.setdefault(noun[0], []).append(noun)

    buffer = StringIO()
    for first_letter, last_letter in zip(chain([None], secret_word), secret_word):
        if first_letter is None:
            subresult = islice(filter(
                lambda w: w[-1] == last_letter, nouns), count)
        elif last_letter is None:
            subresult = islice(filter(
                lambda w: w[0] == first_letter, nouns), count)
        else:
            subresult = islice(filter(
                lambda w: w[0] == first_letter and w[-1] == last_letter, nouns), count)

        buffer.write(f"{first_letter}-{last_letter}:\n")
        buffer.write("\n".join(subresult))
        buffer.write("\n---\n")

    return buffer.getvalue()
