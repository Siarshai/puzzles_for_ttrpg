from anagrams.find_anagrams import find_anagrams
from common_args_parse import prepare_argsparse, prepare_result_dir, prepare_data
from ideation.random_sampling import sample_words
from utils.language import Language


def parse_args():
    parser = prepare_argsparse()
    group = parser.add_argument_group("Other")
    group.add_argument(
        "--anagrams", help=find_anagrams.__doc__, metavar="WORD", default="")
    group.add_argument(
        "--sample", help=sample_words.__doc__, metavar="N", type=int, default=0)
    return parser.parse_args()


def main():
    args = vars(parse_args())
    result_dir = prepare_result_dir(args)
    all_words = prepare_data(args)

    if args["anagrams"]:
        result = find_anagrams(all_words[Language.RUSSIAN], args["anagrams"])
        print(result)
    if args["sample"]:
        result = sample_words(all_words[Language.RUSSIAN], args["sample"])
        for word in result:
            print(word)


if __name__ == "__main__":
    main()
