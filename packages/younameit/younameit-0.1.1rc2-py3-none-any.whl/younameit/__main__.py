#!/usr/bin/env python3

import argparse
import sys
from typing import List, get_args

from younameit import Nomenclator
from younameit._base import ParityType, list_books

# The actual number of groups depends on the book, so defining it here is improper.
# However, making it correct would require much more code than it's worth of.

MIN_GROUPS = 2
MAX_GROUPS = 8


def main(language: str, text_or_bytes: str | bytes, groups: List[int], parity: ParityType) -> None:
    nom = Nomenclator(language)
    word = nom.from_any_to_word(text_or_bytes, *groups, parity=parity)
    print(word)


def validate_groups(value):
    try:
        groups = [int(x) for x in value.split(",")]
        if not all(MIN_GROUPS <= x <= MAX_GROUPS for x in groups):
            raise argparse.ArgumentTypeError(
                f"Each group number must be a integer between {MIN_GROUPS} and {MAX_GROUPS}."
            )
        return groups
    except ValueError:
        raise argparse.ArgumentTypeError("Groups must be a comma-separated list of integers.")


def validate_parity(value):
    if value not in get_args(ParityType):
        raise argparse.ArgumentTypeError("Parity must be 'any', 'odd', or 'even'.")
    return value


def cli_main(*raw_cli_args: str):
    raw_cli_args = raw_cli_args or sys.argv[1:]
    parser = argparse.ArgumentParser(description="Younameit")
    parser.add_argument("--list", "--list-languages", action="store_true", help="List available languages and exit.")
    parser.add_argument(
        "-l", "--language", default="american-english", help="Language to be used for generating a word."
    )
    parser.add_argument(
        "-g",
        "--num-groups",
        type=validate_groups,
        required=False,
        help=f"Comma-separated integer between {MIN_GROUPS} and {MAX_GROUPS}.",
    )
    parser.add_argument(
        "-p",
        "--parity",
        type=validate_parity,
        choices=get_args(ParityType),
        default="any",
        help="Specify parity: 'any', 'odd', or 'even'. Default is 'any'.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--tf", "--text-file", type=argparse.FileType("r"), help="Path to the input text file.")
    group.add_argument("-b", "--bf", "--bin-file", type=argparse.FileType("rb"), help="Path to the input binary file.")

    args = parser.parse_args(raw_cli_args)
    if args.list:
        for language, _ in list_books():
            print(language)
        sys.exit(0)

    if args.tf:
        text_or_bytes_ = args.tf.read()
        args.tf.close()

    elif args.bf:
        text_or_bytes_ = args.bf.read()
        args.bf.close()
    else:
        if not sys.stdin.isatty():  # Check if input is piped
            text_or_bytes_ = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)

    return main(args.language, text_or_bytes_, args.num_groups or (), args.parity)


if __name__ == "__main__":
    cli_main()
