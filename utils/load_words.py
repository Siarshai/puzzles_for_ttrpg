from pathlib import Path
from utils.preprocessing import get_filepaths_to_cached_words


def load_words(cache_dir: Path):
    captions, filepaths = get_filepaths_to_cached_words(cache_dir)
    result = {}
    for name, fp in zip(captions, filepaths):
        with open(fp, "r") as fh:
            result[name] = [word.strip() for word in list(fh)]
    return result
