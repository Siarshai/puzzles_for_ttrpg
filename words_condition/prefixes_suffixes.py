from typing import List, Dict
from dataclasses import dataclass
from itertools import chain

from tqdm import tqdm


@dataclass
class PrefixRecord:
    prefix: str
    current_streak: List[str]


def find_words_with_common_prefix(
        all_words_by_class: Dict[str, List[str]],
        prefix_size: int = 6,
        cluster_size_threshold: int = 4) -> List[List[str]]:
    """
    Finds nouns starting with same prefix of a certain length (6 by default)
    Example:
    абсолют, абсолютизация, абсолютизм, абсолютность
    абстрагирование, абстракционизм, абстракционист, абстракция
    авантюра, авантюризм, авантюрист, авантюристка
    ...
    Mostly captures single-rooted words but there're a couple of interesting
    overlaps like
    контра, контрабанда, контрабандист, контрабас, контрабасист,
        контрагент, контракт, контрактник, контральто,
        контрамарка, контрапункт, контраргумент, контраст,
        контрастность, контратака, контрацептив, контрацепция
    Using only nouns because verbs and adjectives add too many single-rooted
    garbage
    """
    eligible_words = [word for word in all_words_by_class["nouns"]
                      if len(word) >= prefix_size]
    eligible_words = sorted(eligible_words)

    words_with_common_prefix = []
    prefix = ""
    current_streak = []
    for word in tqdm(eligible_words, total=len(eligible_words)):
        if prefix == word[0:prefix_size]:
            current_streak.append(word)
        else:
            if len(current_streak) >= cluster_size_threshold:
                words_with_common_prefix.append(current_streak)
            prefix = word[0:prefix_size]
            current_streak = [word]
    if len(current_streak) >= cluster_size_threshold:
        words_with_common_prefix.append(current_streak)

    return words_with_common_prefix


def find_words_with_common_word_prefix(
        all_words_by_class: Dict[str, List[str]],
        prefix_size: int = 4,
        cluster_size_threshold: int = 4) -> List[List[str]]:
    """
    Finds words starting with same prefix *which is also a valid word* of a
    certain length (4 by default)
    Example:
    авто, автобан, автобус, автоген, автомат, автор ...
        (АВТО)бан, (АВТО)бус, (АВТО)ген, (АВТО)мат, (АВТО)р
    арка, аркада, аркадия, аркан
        (АРКА)да, (АРКА)дия, (АРКА)н
    балл, баллада, балласт, баллон ...
        (БАЛЛ)ада, (БАЛЛ)аст, (БАЛЛ)он
    ...
    """
    nouns = all_words_by_class["nouns"]
    eligible_starting_words = sorted([word for word in nouns if len(word) == prefix_size])
    eligible_words = sorted([word for word in
                             chain.from_iterable(all_words_by_class.values())
                             if len(word) >= prefix_size])

    words_with_common_prefix = []
    is_streak_started = False
    current_streak = []
    for word in tqdm(eligible_words, total=len(eligible_words)):
        if is_streak_started:
            if word[0:prefix_size] == current_streak[0]:
                current_streak.append(word)
            else:
                if len(current_streak) >= cluster_size_threshold:
                    words_with_common_prefix.append(current_streak)
                is_streak_started = False
                eligible_starting_words.pop(0)
        # not elif since we can end previous streak and start new one on the same time
        if word == eligible_starting_words[0]:
            current_streak = [word]
            is_streak_started = True
    return words_with_common_prefix

