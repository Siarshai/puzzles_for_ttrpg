import itertools

from tqdm import tqdm
from typing import Dict, List

__all__ = ["find_magic_word_squares"]


def find_magic_word_squares(all_words_by_class: Dict[str, List[str]],
                            length: int = 5,
                            fullmagic=False) -> List[List[str]]:
    """
    Finds all word squares which when being transposed form the same squares.
    (or, alternatively, which read the same from left to right and from top to bottom).
    Default size of square is 5.
    Example:
    бачок
    акула
    чубик
    олива
    какао
    ...
    """
    all_words = all_words_by_class["nouns"]
    all_words = [word for word in all_words if len(word) == length]
    total_result = []

    def _magic_word_squares_recursive(words, current_chain):

        def filter_have_possible_further_letters(words, current_chain, current_depth):
            return [word for word in words if word[current_depth - 1] in current_chain[-1][current_depth + 1:]]

        def filter_against_words_already_in_chain(words, current_chain, current_depth):
            result = []
            for word in words:
                for d, word_already_in_chain in enumerate(current_chain):
                    if word[d] != word_already_in_chain[current_depth]:
                        break
                else:
                    result.append(word)
            return result

        current_depth = len(current_chain)
        if current_depth == 0:
            for next_word_in_chain in tqdm(words, total=len(words)):
                possible_further_words = filter_have_possible_further_letters(words, [next_word_in_chain], 0)
                _magic_word_squares_recursive(possible_further_words, [next_word_in_chain])
        elif current_depth == length - 1:
            possible_next_step_words = filter_against_words_already_in_chain(words, current_chain, current_depth)
            for next_word_in_chain in possible_next_step_words:
                total_result.append(tuple(current_chain + [next_word_in_chain]))
        else:
            possible_further_words = filter_have_possible_further_letters(words, current_chain, current_depth)
            possible_next_step_words = filter_against_words_already_in_chain(words, current_chain, current_depth)
            for next_word_in_chain in possible_next_step_words:
                _magic_word_squares_recursive(possible_further_words, current_chain + [next_word_in_chain])

    _magic_word_squares_recursive(all_words, [])

    def filter_chains_with_duplicate_words(total_result):
        result = []
        for chain in total_result:
            for pair in itertools.combinations(chain, r=2):
                if pair[0] == pair[1]:
                    break
            else:
                result.append(chain)
        return result

    total_result = filter_chains_with_duplicate_words(total_result)

    if fullmagic:
        # fullmagic means diagonals also form words
        # No russian fullmagic squares found :(
        result = []
        for chain in total_result:
            diag_tl_br = "".join((word[i] for i, word in enumerate(chain)))
            diag_br_tl = "".join((word[len(chain) - i - 1] for i, word in enumerate(reversed(chain))))
            diag_tr_bl = "".join((word[len(chain) - i - 1] for i, word in enumerate(chain)))
            # no need to check diag_bl_tr as they are necessary palindromes with diag_tr_bl
            if diag_tr_bl in all_words or diag_tl_br in all_words or diag_br_tl in all_words:
                result.append(chain)
        total_result = result

    return total_result
