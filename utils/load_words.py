from pathlib import Path


def load_words(cache_dir: Path, get_filepaths_and_captions):
    captions, filepaths = get_filepaths_and_captions(cache_dir)
    result = {}
    for name, fp in zip(captions, filepaths):
        with open(fp, "r") as fh:
            result[name] = [word.strip() for word in list(fh)]
    return result
