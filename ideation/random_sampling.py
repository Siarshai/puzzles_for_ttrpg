from itertools import chain
from random import shuffle

from typing import Dict, List


def sample_words(all_words_by_class: Dict[str, List[str]], count=200):
    """
    Generates a random sample of words. Good for idea generation.
    See "Serious Creativity: Using the Power of Lateral Thinking to Create New Ideas"
    by Edward de Bono for examples of usage
    """
    result = list(chain(*all_words_by_class.values()))
    shuffle(result)
    return result[count:]
