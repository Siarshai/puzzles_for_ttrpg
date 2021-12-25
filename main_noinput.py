#!/usr/bin/env python3

from anagrams.find_anagrams import find_anagrams
from mathy.strange_math import lettery_math_table, roman_dashes_math_table
from patterns.most_complicated_phone_locks import find_most_complicated_phone_locks
from common_args_parse import prepare_argsparse, prepare_result_dir, prepare_data
from utils.output_formatting import write_ioi, write_doi, write_i
from words_condition.prefixes_suffixes import find_words_with_common_word_prefix, find_words_with_common_prefix, \
    find_words_with_common_suffix, find_words_with_common_word_suffix
from utils.language import Language, UnsupportedLanguageForAlgorithm
from words_condition.roman_numerals import find_roman_numeral_removable
from words_condition.sandwichable_words import find_double_sandwichable_words, find_sandwichable_words_multistuffing
from words_condition.spinning_words import find_spinning_words
from words_condition.word_chains import find_word_chains
from words_condition.word_squares import find_magic_word_squares


registered_tasks_noinput = {
    "common_word_prefix": (find_words_with_common_word_prefix, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "common_prefix": (find_words_with_common_prefix, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "common_word_suffix": (find_words_with_common_word_suffix, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "common_suffix": (find_words_with_common_suffix, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "double_sandwichable": (find_double_sandwichable_words, write_doi, (Language.RUSSIAN, Language.ENGLISH)),
    "sandwichable_multistuffing": (find_sandwichable_words_multistuffing, write_doi, (Language.RUSSIAN, Language.ENGLISH)),
    "spinning": (find_spinning_words, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "chains": (find_word_chains, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "squares": (find_magic_word_squares, write_ioi, (Language.RUSSIAN, Language.ENGLISH)),
    "roman_removable": (find_roman_numeral_removable, write_ioi, (Language.ENGLISH,)),

    "phone_locks": (find_most_complicated_phone_locks, write_i, (Language.NONE,)),

    "lettery_math": (lettery_math_table, write_i, (Language.NONE,)),
    "roman_dashes_math": (roman_dashes_math_table, write_i, (Language.NONE,))
}


def parse_args():
    parser = prepare_argsparse()
    group = parser.add_argument_group(
        "Noinput"
        "Search words or patterns abiding certain rule")
    for key, (fn, _, _) in registered_tasks_noinput.items():
        group.add_argument(f"--{key}", help=fn.__doc__, action="store_true", default=False)
    group.add_argument(
        "--language",
        help=f"""
        Specifies which language to use for content generation. Will regenerate
        all supported languages if not specified""",
        default=str(Language.ALL),
        const='all',
        nargs='?',
        choices=[lang.value for lang in Language],
    )
    group.add_argument(
        "--all_noinput",
        help=f"""
        Regenerates all output not requiring input (static words and patterns search). 
        Equivalent to: 
        '{" ".join([f"--{key}" for key in registered_tasks_noinput.keys()])}'""",
        action="store_true", default=False)
    return parser.parse_args()


def main():
    args = vars(parse_args())
    result_dir = prepare_result_dir(args)
    all_words = prepare_data(args)

    selected_language = Language.from_str(args["language"])
    if args["all_noinput"]:
        for algo_name in registered_tasks_noinput.keys():
            args[algo_name] = True

    for algo_name, (fn, writer_fn, supported_languages) in registered_tasks_noinput.items():
        def process_algo_for_language(lang):
            result = fn() if lang is Language.NONE else fn(all_words[lang])
            writer_fn(result_dir, f"{algo_name}_{lang.value}", result)
        if args[algo_name]:
            print(f"Processing {algo_name!r}...")
            if selected_language is Language.ALL:
                for lang in supported_languages:
                    print(f"Processing language {lang.value!r}...")
                    process_algo_for_language(lang)
            else:
                if selected_language not in supported_languages:
                    raise UnsupportedLanguageForAlgorithm(algo_name, selected_language, supported_languages)
                process_algo_for_language(selected_language)


if __name__ == "__main__":
    main()
