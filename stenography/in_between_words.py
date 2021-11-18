from typing import List, Dict
from tqdm import tqdm


def hide_in_between_words(
        all_words_by_class: Dict[str, List[str]],
        secret_word: str,
        max_words_num: str = "100"):
    """
    Provides list of pairs of words to hide secret words in between
    Example:
    восемь,10
    слово, семья -> сло/ВО СЕМЬ/я
    право, семьянин -> пра/ВО СЕМЬ/ьянин
    """
    max_words_num = int(max_words_num)
    possible_starting_words = all_words_by_class["nouns"]
    possible_starting_words = [word for word in possible_starting_words
                               if word.find(secret_word[0]) != -1 and word.find(secret_word) == -1]
    possible_ending_words = all_words_by_class["nouns"]\
                            + all_words_by_class["verbs"]\
                            + all_words_by_class["adjectives"]
    possible_ending_words = [word for word in possible_ending_words
                             if word.find(secret_word[-1]) != -1 and word.find(secret_word) == -1]
    pairs = []
    for word1 in tqdm(possible_starting_words, total=len(possible_starting_words)):
        for idx, word2 in enumerate(possible_ending_words):
            merge = word1 + word2
            if merge.find(secret_word) != -1:
                pairs.append((word1, word2))
                possible_ending_words.pop(idx)
                max_words_num -= 1
                break
        if max_words_num <= 0:
            break
    return "\n".join([", ".join(pair) for pair in pairs])
