from typing import List, Dict
from dataclasses import dataclass
from itertools import chain


@dataclass
class PrefixRecord:
    prefix: str
    current_streak: List[str]


def find_words_with_common_word_prefix(all_words_by_class: Dict[str, List[str]]) -> List[List[str]]:
    """
    Finds words starting with same prefix which is also a valid word of a
    certain length (4 by default)
    Example:
    авто, автобан, автобус, автоген, автомат, автор
        (АВТО)бан, (АВТО)бус, (АВТО)ген, (АВТО)мат, (АВТО)р
    арка, аркада, аркадия, аркан
        (АРКА)да, (АРКА)дия, (АРКА)н
    балл, баллада, балласт, баллон
        (БАЛЛ)ада, (БАЛЛ)аст, (БАЛЛ)он
    ...
    """
    eligible_words = [word for word in chain.from_iterable(all_words_by_class.values())
                      if 4 <= len(word) <= 7]
    eligible_words = sorted(eligible_words)
    nouns = all_words_by_class["nouns"]
    eligible_starting_words = {
        3: {word for word in nouns if len(word) == 3},
        4: {word for word in nouns if len(word) == 4},
    }
    n_prefix_streaks = {3: PrefixRecord("", []), 4: PrefixRecord("", [])}
    clusters_starting_with_word = {3: [], 4: []}
    cluster_size_threshold = 4
    for word in eligible_words:
        for prefix_n, record in n_prefix_streaks.items():
            if record.prefix == word[0:prefix_n]:
                record.current_streak.append(word)
            else:
                if len(record.current_streak) >= cluster_size_threshold and \
                        record.prefix in eligible_starting_words[prefix_n]:
                    clusters_starting_with_word[prefix_n].append(record.current_streak)
                record.prefix = word[0:prefix_n]
                record.current_streak = [word]
    return clusters_starting_with_word[4]

