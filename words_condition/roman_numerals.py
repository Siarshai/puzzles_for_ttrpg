import itertools

from tqdm import tqdm
from typing import Set, Dict, List

__all__ = ["find_roman_numeral_removable"]


def find_roman_numeral_removable(all_words_by_class: Dict[str, List[str]],
                                 chain_threshold: int = 4):
    """
    Finds all unique chains of english words which when you remove letters
    designating Roman numerals (ivxlcdm) form new words
    Example:
    crackling, cracking, racking, raking
    classics, classis, cassis, assis
    classism, classis, cassis, assis  <-- different from former chain
    Starting words are no longer than 12 letters and no shorter than 5
    (because then end of chain becomes trivial)
    """
    all_words = [word for word in
                       itertools.chain.from_iterable(all_words_by_class.values())
                       if len(word) <= 12]
    # Let's optimize it a little bit - split words by length to
    # search chain pieces only in list of words of relevant length
    # Also provide alternative (improbable) recursion end
    words_by_length = {i: [] for i in range(13)}
    for word in all_words:
        words_by_length[len(word)].append(word)

    all_chains: List[List[str]] = []

    def find_chain(current_chain: List[str]):
        at_least_one_child = False
        for i in range(len(current_chain[-1])):
            if current_chain[-1][i] in "ivxlcdm":
                word_with_removed_letter = current_chain[-1][:i] + current_chain[-1][i+1:]
                if word_with_removed_letter in words_by_length[len(word_with_removed_letter)]:
                    at_least_one_child = True
                    find_chain(current_chain + [word_with_removed_letter])
        if not at_least_one_child:
            if len(current_chain) >= chain_threshold:
                all_chains.append(current_chain)

    total_iterations = len(list(range(12, 5, -1)))
    for l in tqdm(range(12, 5, -1), total=total_iterations):
        for word in words_by_length[l]:
            find_chain([word])

    return all_chains
