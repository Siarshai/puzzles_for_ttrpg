from typing import List, Dict
from tqdm import tqdm
from collections import Counter
from utils.word_validation import is_cyrillic


def _find_anagrams_with_depth(anagram_source: str, all_words: List[str], maxdepth):
    anagram_source = anagram_source.lower()
    if maxdepth < 1:
        maxdepth = 1

    anagram_decomposed = Counter([l for l in anagram_source if is_cyrillic(l)])
    letters_present = anagram_decomposed.keys()
    eligible_words = [word for word in all_words if all((letter in letters_present for letter in word))]
    possible_parts = []

    def search_for_anagrams_inner(words: List[str],
                                  words_decomposed: Counter, depth: int, current_path=List[str]):
        for j, word in enumerate(words):
            new_words_decomposed = words_decomposed + Counter([l for l in word if is_cyrillic(l)])
            new_current_path = current_path + [word]
            if depth < maxdepth:
                if any(new_words_decomposed[letter] > value for letter, value in anagram_decomposed.items()):
                    continue  # already too much certain letters - optimization
                search_for_anagrams_inner(words[j + 1:], new_words_decomposed, depth + 1, new_current_path)
            else:
                if new_words_decomposed == anagram_decomposed:
                    possible_parts.append(new_current_path)

    for i, word in tqdm(enumerate(eligible_words), total=len(eligible_words)):
        words_decomposed = Counter([l for l in word if is_cyrillic(l)])
        current_path = [word]
        search_for_anagrams_inner(eligible_words[i + 1:], words_decomposed, 1, current_path)

    return possible_parts


def find_anagrams(all_words_by_class: Dict[str, List[str]], anagram_source: str):
    """
    Finds all possible ways to split phrase into into multiple (2-4) nouns
    forming anagram of that phrase. Caution: works way to long for phrases
    longer than 20 letters, but may not find anything for phrases of less
    than 10 letters. Example:
    фиолетовая антилопа
    ---
    тело,фон,апатия,виола
    тело,фон,апатия,олива
    тело,пятно,авиа,олифа
    тело,фото,алия,павиан
    ...
    """
    if not any([is_cyrillic(l) for l in anagram_source]):
        raise RuntimeError("Found non cyrillic symbol or space or hyphen")
    nouns = [w for w in all_words_by_class["nouns"] if 3 <= len(w) <= 7]
    possible_parts = _find_anagrams_with_depth(anagram_source, nouns, 1) \
                     + _find_anagrams_with_depth(anagram_source, nouns, 2) \
                     + _find_anagrams_with_depth(anagram_source, nouns, 3)
    return "\n".join([",".join(parts) for parts in possible_parts])
