from enum import Enum
from pathlib import Path
from typing import List, Tuple, Dict
import requests
from zipfile import ZipFile
from utils.language import get_known_parts_of_speech, Language


# freqrnc2011.csv:
# О. Н. Ляшевская, С. А. Шаров
# НОВЫЙ ЧАСТОТНЫЙ СЛОВАРЬ РУССКОЙ ЛЕКСИКИ
# See http://dict.ruslang.ru/freq.php


def _get_cache_filepaths_russian(cache_dir: Path):
    return {pos: cache_dir.joinpath(f"{pos}_russian.txt") for pos in
            get_known_parts_of_speech()}


def _get_cache_filepaths_english(cache_dir: Path):
    return {pos: cache_dir.joinpath(f"{pos}_english.txt") for pos in
            get_known_parts_of_speech()}


def _write_cache(cache_filepahs_by_pos, words_by_pos):
    for pos, words in words_by_pos.items():
        filepath = cache_filepahs_by_pos[pos]
        with open(filepath, "w") as f:
            f.write("\n".join(words))


def _download_freq2011(cache_dir: Path):
    if not cache_dir.is_dir():
        raise OSError(f"{str(cache_dir)} is not a dir")
    zip_filepath = cache_dir.joinpath("Freq2011.zip")
    print("Downloading RU data...")
    request = requests.get("http://dict.ruslang.ru/Freq2011.zip")
    with open(zip_filepath, "wb") as fh:
        fh.write(request.content)
    print("Extracting archive...")
    with ZipFile(zip_filepath, 'r') as fh:
        fh.extract("freqrnc2011.csv", cache_dir)


def _preprocess_freq2011(cache_dir: Path, count=100000):
    print(f"Preparing RU words cache count={count}...")
    csv_filepath = cache_dir.joinpath("freqrnc2011.csv")

    words_by_pos = {pos: [] for pos in get_known_parts_of_speech()}
    with open(csv_filepath, "r") as fh:
        first = True
        for line in fh:
            if first:
                first = False
                continue
            lemma, pos, freq, _, _, _ = line.split()
            if pos == "s":
                words_by_pos["nouns"].append((lemma, float(freq)))
            elif pos == "v":
                words_by_pos["verbs"].append((lemma, float(freq)))
            elif pos == "a":
                words_by_pos["adjectives"].append((lemma, float(freq)))

    def sort_by_ipm_then_discard_ipm(words: List[Tuple[str, float]]) -> List[str]:
        return [tup[0] for tup in sorted(words, key=lambda tup: -tup[1])[:count]]

    words_by_pos = {pos: sort_by_ipm_then_discard_ipm(words)
                    for pos, words in words_by_pos.items()}

    cache_filepahs_by_pos = _get_cache_filepaths_russian(cache_dir)
    _write_cache(cache_filepahs_by_pos, words_by_pos)


# The Center for Reading Research vocabulary
# http://crr.ugent.be


def _download_crrugent_subtlex_us(cache_dir: Path):
    if not cache_dir.is_dir():
        raise OSError(f"{str(cache_dir)} is not a dir")
    zip_filepath = cache_dir.joinpath("SUBTLEX-US_frequency_list_with_PoS_information_final_text_version.zip")
    print("Downloading EN data...")
    request = requests.get(
        "http://crr.ugent.be/papers/SUBTLEX-US_frequency_list_with_PoS_information_final_text_version.zip")
    with open(zip_filepath, "wb") as fh:
        fh.write(request.content)
    print("Extracting archive...")
    with ZipFile(zip_filepath, 'r') as fh:
        fh.extract("SUBTLEX-US frequency list with PoS information text version.txt", cache_dir)


def _preprocess_crrugent_subtlex_us(cache_dir: Path, count=100000):
    print(f"Preparing EN words cache count={count}...")
    csv_filepath = cache_dir.joinpath("SUBTLEX-US frequency list with PoS information text version.txt")

    words_by_pos = {pos: [] for pos in get_known_parts_of_speech()}
    with open(csv_filepath, "r") as fh:
        first = True
        for line in fh:
            if first:
                first = False
                continue
            splitted = line.split()
            lemma, pos, freq = splitted[0], splitted[9], splitted[1]
            if pos == "Noun":
                words_by_pos["nouns"].append((lemma, float(freq)))
            elif pos == "Verb":
                words_by_pos["verbs"].append((lemma, float(freq)))
            elif pos == "Adjective":
                words_by_pos["adjectives"].append((lemma, float(freq)))

    def sort_by_freq_then_discard_freq(words: List[Tuple[str, float]]) -> List[str]:
        return [tup[0] for tup in sorted(words, key=lambda tup: -tup[1])[:count]]

    words_by_pos = {pos: sort_by_freq_then_discard_freq(words)
                    for pos, words in words_by_pos.items()}

    cache_filepahs_by_pos = _get_cache_filepaths_english(cache_dir)
    _write_cache(cache_filepahs_by_pos, words_by_pos)


def is_cache_ready(cache_dir: Path) -> bool:
    return all([p.exists() for p in _get_cache_filepaths_russian(cache_dir).values()]) and \
           all([p.exists() for p in _get_cache_filepaths_english(cache_dir).values()])


def build_cache(cache_dir, cache_count=100000) -> None:
    _download_freq2011(cache_dir)
    _preprocess_freq2011(cache_dir, cache_count)
    _download_crrugent_subtlex_us(cache_dir)
    _preprocess_crrugent_subtlex_us(cache_dir, cache_count)


def load_caches(cache_dir) -> Dict[Enum, Dict[str, List[str]]]:
    def load_single_cache(pos_filepaths: Dict[str, Path]):
        result = {}
        for part_of_speech, filepath in pos_filepaths.items():
            with open(filepath, "r") as fh:
                result[part_of_speech] = [word.strip() for word in list(fh)]
        return result

    return {
        Language.RUSSIAN: load_single_cache(_get_cache_filepaths_russian(cache_dir)),
        Language.ENGLISH: load_single_cache(_get_cache_filepaths_english(cache_dir))
    }
