from collections import defaultdict
from typing import List, Dict
from tqdm import tqdm


__all__ = ["find_word_chains"]


def find_word_chains(all_words_by_class: Dict[str, List[str]]) -> List[List[str]]:
    """
    Finds all unique chains of words which can be formed by adding
    one letter to preceding word.
    Example:
    пол, поле, полет, эполет <-- first added "e" (tail) then "т" (tail) than "э" (head)
    бар, барк, барка, баркан <-- "е" (tail), "а" (tail), "н" (tail)
    бар, барк, барка, баркас <-- "е" (tail), "а" (tail), "с" (tail)
        those are different chains since they are different in at least one word
    ...
    """
    words = all_words_by_class["nouns"]
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    nouns_by_length = defaultdict(list)
    for word in words:
        if 3 <= len(word) <= 9:
            nouns_by_length[len(word)].append(word)
    chains = []
    chain_length_threshold = 4

    def subsearch(current_chain: List[str]):
        subword = current_chain[-1]
        found_longer_chain = False
        for letter in russian_letters:
            subword_prefixed = letter + subword
            subword_suffixed = subword + letter
            for word in nouns_by_length[len(subword_prefixed)]:
                if word == subword_prefixed:
                    found_longer_chain = True
                    subsearch(current_chain + [subword_prefixed])
                if word == subword_suffixed:
                    found_longer_chain = True
                    subsearch(current_chain + [subword_suffixed])
        if not found_longer_chain and len(current_chain) >= chain_length_threshold:
            chains.append(current_chain)

    for word in tqdm(nouns_by_length[3],
                     total=len(nouns_by_length[3]),
                     desc="Words of lenght 3"):
        subsearch([word])
    for word in tqdm(nouns_by_length[4],
                     total=len(nouns_by_length[4]),
                     desc="Words of lenght 4"):
        if any(word == chain[1] for chain in chains):
            continue
        subsearch([word])
    for word in tqdm(nouns_by_length[5],
                     total=len(nouns_by_length[5]),
                     desc="Words of lenght 5"):
        if any(word == chain[1] or word == chain[2] for chain in chains):
            continue
        subsearch([word])

    return chains
