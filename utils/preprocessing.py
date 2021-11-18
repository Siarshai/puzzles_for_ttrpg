from pathlib import Path
from typing import List, Tuple
import requests
from zipfile import ZipFile


# freqrnc2011.csv:
# О. Н. Ляшевская, С. А. Шаров
# НОВЫЙ ЧАСТОТНЫЙ СЛОВАРЬ РУССКОЙ ЛЕКСИКИ
# See http://dict.ruslang.ru/freq.php


def download_freq2011(cache_dir: Path):
    if not cache_dir.is_dir():
        raise OSError(f"{str(cache_dir)} is not a dir")
    zip_filepath = cache_dir.joinpath("Freq2011.zip")
    print("Downloading data...")
    request = requests.get("http://dict.ruslang.ru/Freq2011.zip")
    with open(zip_filepath, "wb") as fh:
        fh.write(request.content)
    print("Extracting archive...")
    with ZipFile(zip_filepath, 'r') as fh:
        fh.extract("freqrnc2011.csv", cache_dir)


def get_filepaths_to_cached_words(cache_dir: Path):
    return (
        ["nouns", "verbs", "adjectives"],
        [cache_dir.joinpath(f"{caption}.txt") for caption in ["nouns", "verbs", "adjectives"]]
    )


def preprocess_freq2011(cache_dir: Path, count=100000):
    print(f"Preparing words cache count={count}...")
    csv_filepath = cache_dir.joinpath("freqrnc2011.csv")
    nouns, verbs, adjectives = [], [], []
    with open(csv_filepath, "r") as fh:
        first = True
        for line in fh:
            if first:
                first = False
                continue
            lemma, pos, freq, _, _, _ = line.split()
            if pos == "s":
                nouns.append((lemma, float(freq)))
            elif pos == "v":
                verbs.append((lemma, float(freq)))
            elif pos == "a":
                adjectives.append((lemma, float(freq)))

    def sort_by_ipm_then_discard_ipm(words: List[Tuple[str, float]]) -> List[str]:
        return [tup[0] for tup in sorted(words, key=lambda tup: -tup[1])[:count]]

    for caption, words in [("nouns", nouns), ("verbs", verbs), ("adjectives", adjectives)]:
        words = sort_by_ipm_then_discard_ipm(words)
        with open(cache_dir.joinpath(f"{caption}.txt"), "w") as f:
            f.write("\n".join(words))


def is_cache_ready(cache_dir: Path):
    return all([p.exists() for p in get_filepaths_to_cached_words(cache_dir)[1]])

