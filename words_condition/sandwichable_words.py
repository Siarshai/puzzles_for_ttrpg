from tqdm import tqdm
from typing import List, Dict


__all__ = ["find_double_sandwichable_words",
           "find_sandwichable_words_multistuffing"]


def _find_words_with_sandwich_inside(
        first_half: str,
        second_half: str,
        words_between_halfs: List[str],
        long_words: List[str]):
    result = []
    for stuffing_word in words_between_halfs:
        sandwich = first_half + stuffing_word + second_half
        result.extend((long_word for long_word in long_words if long_word.find(sandwich) != -1))
    return result


def find_double_sandwichable_words(all_words_by_class: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Finds all words which can be 'sandwiched' inside another valid word and
    the 'sandwiched' once more to form yet another valid word.
    Example:
    рост: королевство (ко/РО-лев-СТ/во)
    лето: лепесток (ЛЕ-пес-ТО/к)
    река: перегрузка, перевозка (пе/РЕ-груз-КА, пе/РЕ-воз-КА)
    ...
    """
    words = all_words_by_class["nouns"][:5000]
    small_words = [word for word in words if 3 <= len(word) <= 4]
    words_to_check = [word for word in words if 4 <= len(word) <= 6]
    long_words = [word for word in words if len(word) >= 7]
    sandwichable_words = {}
    for word in tqdm(words_to_check, total=len(words_to_check)):
        for split_idx in range(2, len(word)-1):
            first_half, second_half = word[:split_idx], word[split_idx:]
            sandwiches = _find_words_with_sandwich_inside(first_half, second_half, small_words, long_words)
            if sandwiches:
                sandwichable_words[word] = sandwiches
    return sandwichable_words


def _split_inplace(words: List[str], letters: str):
    result = {"": words}
    for new_letter in letters:
        split_update = {}
        for existing_letters, words in result.items():
            dont_have_new_letter, have_new_letter = [], []
            for word in words:
                (dont_have_new_letter, have_new_letter)[new_letter in word].append(word)
            result[existing_letters] = dont_have_new_letter
            split_update[existing_letters + new_letter] = have_new_letter
        result.update(split_update)
    return result


def _find_contained_words(containers_split: Dict[str, List[str]],
                          parts_split: Dict[str, List[str]],
                          min_num_threshold: int):
    total_result = {}
    for letters_in_containers_split, container_words in containers_split.items():
        parts_to_search_from = []
        for letter in letters_in_containers_split:
            for letters_in_parts_split, parts_words in parts_split.items():
                if letter in letters_in_parts_split:
                    parts_to_search_from.append(parts_words)
        parts_to_search_from.append(parts_split[""])

        for container_word in tqdm(container_words,
                                   desc=letters_in_containers_split + " words",
                                   total=len(container_words)):
            result = []
            for parts_words in parts_to_search_from:
                result.extend(filter(lambda word: word in container_word, parts_words))
            if len(result) >= min_num_threshold:
                total_result[container_word] = result
    return total_result


def find_sandwichable_words_multistuffing(all_words_by_class: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Finds words containing at least 4 other words inside them (possibly with intersection)
    Example:
    государство: удар, дар, уда, суд
        госУДАРство, госуДАРство, госУДАрство, гоСУДарство
    подарок: рок, под, ода, дар
        подаРОК, ПОДарок, пОДАрок, поДАРок
    транспорт: спор, спорт, порт, транс
        транСПОРт, транСПОРТ, трансПОРТ, ТРАНСпорт
    ...
    """
    nouns = all_words_by_class["nouns"]
    possible_container_words = [word for word in nouns if 6 < len(word)]
    possible_container_words.extend([word for word in all_words_by_class["verbs"] if 6 < len(word)])
    possible_container_words.extend([word for word in all_words_by_class["adjectives"] if 6 < len(word)])
    possible_part_words = [word for word in nouns if 2 < len(word) < 6 and word != "ост" and word != "ость"]
    # Using presplitting for optimization:
    # long words without certain letter can't contain small words with this letter
    container_words_split = _split_inplace(list(possible_container_words), "оаеи")
    part_words_split = _split_inplace(list(possible_part_words), "оаеи")
    result = _find_contained_words(container_words_split, part_words_split, 4)
    return result

