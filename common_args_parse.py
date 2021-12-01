import argparse
import os
from pathlib import Path

from utils.words_cache import is_cache_ready, build_cache, load_caches


def prepare_argsparse():
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
    return parser


def _ensure_dir_exists(d):
    if not d.is_dir():
        raise OSError(f"{d!r} is not a directory")
    if not d.exists():
        d.mkdir(parents=True)


def prepare_result_dir(args):
    result_dir = Path(args["result_dir"])
    _ensure_dir_exists(result_dir)
    return result_dir


def prepare_data(args):
    cache_dir = Path(args["cache_dir"])
    _ensure_dir_exists(cache_dir)
    if not is_cache_ready(cache_dir):
        print("Words cache is not ready, rebuilding...")
        build_cache(cache_dir, args["cache_count"])
    all_words = load_caches(cache_dir)
    return all_words
