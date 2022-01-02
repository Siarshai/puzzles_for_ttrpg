#!/usr/bin/env python3

from common_args_parse import prepare_argsparse, prepare_result_dir, prepare_data
from stenography.in_words_overlap import hide_in_words_overlap
from stenography.spiral_hide import spiral_hide
from stenography.diagnoal_fill_to_square import diagonal_fill_to_square_last, diagonal_fill_to_square_first
from stenography.hide_image_in_words import hide_image
from stenography.in_between_words import hide_in_between_words
from stenography.letters_before_sequence import hide_letters_before_sequence
from stenography.nth_letter import hide_in_nth_letters
from utils.language import Language


# Right now there is only stenography, but I intend to add cyphers
# which are better combined with stenography


registered_stenography_input = {
    "letters_before_sequence": (hide_letters_before_sequence, "SECRET_WORD,MARKING_SEQUENCE"),
    "nth_letter": (hide_in_nth_letters, "SECRET_WORD,N"),
    "between_words": (hide_in_between_words, "SECRET_WORD,MAXCOUNT"),
    "words_overlap": (hide_in_words_overlap, "SECRET_WORD,COUNT"),
    "hide_image": (hide_image, "IMAGE_LINE;IMAGE_LINE;IMAGE_LINE,..."),
    "diagonal_fill_last": (diagonal_fill_to_square_last, "SECRET_WORD"),
    "diagonal_fill_first": (diagonal_fill_to_square_first, "SECRET_WORD"),
    "spiral_hide": (spiral_hide, "SECRET_WORD"),
}


def parse_args():
    parser = prepare_argsparse()
    group = parser.add_argument_group(
        "Stenography and cyphers")
    group.add_argument(
        "--terminal",
        help=f"""
        Redirects output to terminal instead of file in result_dir""",
        action="store_true", default=False)
    for key, (fn, metavar_hint) in registered_stenography_input.items():
        group.add_argument(f"--{key}", help=fn.__doc__, metavar=metavar_hint, default="")
    return parser.parse_args()


def main():
    args = vars(parse_args())
    result_dir = prepare_result_dir(args)
    all_words = prepare_data(args)

    for algo_name, (fn, _) in registered_stenography_input.items():
        if args[algo_name]:
            print(f"Processing '{algo_name}'...")
            stenography_args = args[algo_name].split(",")
            result = fn(all_words[Language.RUSSIAN], *stenography_args)
            if args["terminal"]:
                print(result)
            else:
                with open(result_dir.joinpath(algo_name + ".txt"), "w") as fh:
                    fh.write(result)


if __name__ == "__main__":
    main()
