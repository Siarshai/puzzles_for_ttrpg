#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from anagrams.find_anagrams import find_anagrams
from ideation.random_sampling import sample_words
from patterns.most_complicated_phone_locks import find_most_complicated_phone_locks
from stenography.in_between_words import hide_in_between_words
from stenography.letters_before_sequence import hide_letters_before_sequence
from stenography.nth_letter import hide_in_nth_letters
from utils.output_formatting import write_ioi, write_doi, write_i
from words_condition.prefixes_suffixes import find_words_with_common_word_prefix, find_words_with_common_prefix, \
    find_words_with_common_suffix
from utils.load_words import load_words
from utils.preprocessing import download_freq2011, is_cache_ready, preprocess_freq2011
from words_condition.sandwichable_words import find_double_sandwichable_words, find_sandwichable_words_multistuffing
from words_condition.spinning_words import find_spinning_words
from words_condition.word_chains import find_word_chains
from words_condition.word_squares import find_magic_word_squares


registered_tasks_noinput = {
    "common_word_prefix": (find_words_with_common_word_prefix, write_ioi),
    "common_prefix": (find_words_with_common_prefix, write_ioi),
    "common_suffix": (find_words_with_common_suffix, write_ioi),
    "double_sandwichable": (find_double_sandwichable_words, write_doi),
    "sandwichable_multistuffing": (find_sandwichable_words_multistuffing, write_doi),
    "spinning": (find_spinning_words, write_ioi),
    "chains": (find_word_chains, write_ioi),
    "squares": (find_magic_word_squares, write_ioi),

    "phone_locks": (find_most_complicated_phone_locks, write_i)
}

registered_stenography_input = {
    "letters_before_sequence": (hide_letters_before_sequence, "SECRET_WORD,MARKING_SEQUENCE"),
    "nth_letter": (hide_in_nth_letters, "SECRET_WORD,N"),
    "between_words": (hide_in_between_words, "SECRET_WORD,MAXCOUNT")
}


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    group = parser.add_argument_group("Main parameters")
    group.add_argument(
        "--cache_dir",
        metavar="PATH",
        help="""Expecting to find nouns.txt, verbs.txt, adjectives.txt in this directory. 
             If not specified, will create 'cache' directory in current directory,
             then download and preprocess vocabulary here. 
             .txt are not rewritten after that, you can manipulate cache as you see fit.""",
        default=Path(os.getcwd()).joinpath("cache"))
    group.add_argument(
        "--cache_count",
        metavar="COUNT",
        type=int,
        help="""When rebuilding cache use this amount of most popular words""",
        default=100000)
    group.add_argument(
        "--result_dir",
        metavar="PATH",
        help="""Will write output to .txt files located in designated dir.
             If not specified, will create 'results' directory in current directory 
             and will use that""",
        default=Path(os.getcwd()).joinpath("results"))

    group = parser.add_argument_group(
        "Noinput"
        "Search words or patterns abiding certain rule")
    for key, (fn, _) in registered_tasks_noinput.items():
        group.add_argument(f"--{key}", help=fn.__doc__, action="store_true", default=False)
    group.add_argument(
        "--all_noinput",
        help=f"""
        Regenerates all output not requiring input (static words and patterns search). 
        Equivalent to: 
        '{" ".join([f"--{key}" for key in registered_tasks_noinput.keys()])}'""",
        action="store_true", default=False)

    group = parser.add_argument_group(
        "Stenography",
        "Hides secret word inside of innocuous message.")
    for key, (fn, metavar_hint) in registered_stenography_input.items():
        group.add_argument(f"--{key}", help=fn.__doc__, metavar=metavar_hint, default="")

    group = parser.add_argument_group("Other")
    group.add_argument(
        "--anagrams", help=find_anagrams.__doc__, metavar="WORD", default="")
    group.add_argument(
        "--sample", help=sample_words.__doc__, metavar="N", type=int, default=0)
    return parser.parse_args()


def main():
    args = vars(parse_args())
    cache_dir = Path(args["cache_dir"])
    result_dir = Path(args["result_dir"])

    for d, name in zip([cache_dir, result_dir], ["cache_dir", "result_dir"]):
        if not d.is_dir():
            raise OSError(f"{name} is not a directory")
        if not d.exists():
            d.mkdir(parents=True)

    if not is_cache_ready(cache_dir):
        print("Words cache is not ready, rebuilding...")
        download_freq2011(cache_dir)
        preprocess_freq2011(cache_dir, args["cache_count"])

    if args["all_noinput"]:
        for name in registered_tasks_noinput.keys():
            args[name] = True

    all_words_by_class = load_words(cache_dir)

    for name, (fn, writer_fn) in registered_tasks_noinput.items():
        if args[name]:
            print(f"Processing '{name}'...")
            result = fn(all_words_by_class)
            writer_fn(result_dir, name, result)

    for name, (fn, _) in registered_stenography_input.items():
        if args[name]:
            print(f"Processing '{name}'...")
            stenography_args = args[name].split(",")
            result = fn(all_words_by_class, *stenography_args)
            print(result)

    if args["anagrams"]:
        result = find_anagrams(all_words_by_class, args["anagrams"])
        print(result)
    if args["sample"]:
        result = sample_words(all_words_by_class, args["sample"])
        for word in result:
            print(word)


if __name__ == "__main__":
    main()
