import hashlib
import os.path
from collections import Counter
from itertools import groupby
from typing import Callable, List, Tuple

import yaml

from younameit import BookDictType, GroupChoices, WordKind
from younameit.__version__ import __version__
from younameit._base import in_this_project

MAX_NUM_CLUSTERS = 8
MIN_NUM_CLUSTERS = 2
MIN_CLUSTER_VARIATIONS = 5
MAX_CLUSTER_VARIATIONS = 70


def build_cipher_book(dictionary_path: str) -> BookDictType:
    cipher_book: dict[WordKind, List] = {}
    dictionary_name = os.path.basename(dictionary_path)

    for word in iter_dictionary_words(dictionary_path):
        word_kind, letter_groups = classify_word(word, dictionary_name)

        if not (MIN_NUM_CLUSTERS <= len(letter_groups) <= MAX_NUM_CLUSTERS):
            continue

        if word_kind not in cipher_book:
            cipher_book[word_kind] = [0, tuple(Counter() for _ in letter_groups)]

        cipher_book[word_kind][0] += 1
        for group_idx, letters in enumerate(letter_groups):
            cluster_counter: Counter = cipher_book[word_kind][1][group_idx]
            cluster_counter.update([letters])

    the_book = {
        kind: (count, tuple(reduced_clusters_def(g) for g in groups)) for kind, (count, groups) in cipher_book.items()
    }
    return dict(sorted(the_book.items(), key=lambda x: (x[1][0], x[0]), reverse=True))


def iter_dictionary_words(dictionary_path: str):
    with open(dictionary_path, "r") as dict_f:
        for line in dict_f.readlines():
            line = line.rstrip()  # remove line ends
            if line.isalpha():  # reject words containing special characters
                yield line.lower()


def classify_word(word: str, language_name: str) -> (str, Tuple[str]):
    is_vowel = make_function_is_vowel(language_name)
    vowel_marks, letter_groups = zip(*((is_vowel_, "".join(letters)) for is_vowel_, letters in groupby(word, is_vowel)))
    parity = "odd" if vowel_marks[0] else "even"
    word_kind = f"{len(letter_groups)} {parity} letter groups"
    return word_kind, letter_groups


def make_function_is_vowel(language_name: str) -> Callable[[str], bool]:
    """Return a function specific for certain language that will be used
    for splitting a word into groups of either consonants or vowels."""

    default_vowels = "aoeiu"
    vowels_set: str = {
        # Please suggest a correction if the vowels are defined incorrectly for a given language.
        "american-english": "aoeiu",
        "british-english": "aoeiu",
        "german": "aoeiuäöü",
        "finnish": "aoeiuäöåy",
        "french": "aoeiu",
        "italian": "aoeiu",
        "spanish": "aoeiu",
        "polish": "aoeiuy",
    }.get(language_name, default_vowels)

    def is_vowel(letter: str) -> bool:
        return letter[0] in vowels_set

    return is_vowel


def reduced_clusters_def(cluster_counts: Counter) -> GroupChoices:
    desired_size = int(len(cluster_counts) * 0.75)  # that should remove minors
    num_blocks = max(MIN_CLUSTER_VARIATIONS, min(MAX_CLUSTER_VARIATIONS, desired_size))

    selected_clusters = cluster_counts.most_common(num_blocks)
    return dict(sorted(selected_clusters, key=lambda x: (x[1], x[0]), reverse=True))


def get_sha256_hex_digest_of_a_file(dict_file_path) -> str:
    with open(dict_file_path, "rb") as dict_file_:
        try:
            # requires python 3.11
            file_digest = hashlib.file_digest(dict_file_, "sha256")
        except AttributeError:
            try:
                # this should work since 3.9 (probably)
                file_digest = hashlib.sha256(dict_file_)
            except TypeError:
                # in old python like 3.7, this error may be raised with the following msg:
                # a bytes-like object is required, not '_io.BufferedReader'
                file_digest = hashlib.sha256(dict_file_.read())

    return file_digest.hexdigest()


def make_kebab_case_slug(dict_file_path: str) -> str:
    base_name, _ = os.path.splitext(os.path.basename(dict_file_path))
    parts = [part for p1 in base_name.split("-") for p2 in p1.split("_") for part in p2.split()]
    return "-".join(parts)


def dict_file_exists_or_raise(dictionary_path: str):
    if not os.path.isfile(dictionary_path):
        raise ValueError(
            f"Unable to find the dictionary file under the path: {dictionary_path!r}.\n"
            "Please install 'words' package (if it's a linux, otherwise specify `custom_path`).\n"
        )


def main(dict_file_path: str):
    dict_file_exists_or_raise(dict_file_path)
    book_obj = build_cipher_book(dict_file_path)
    digest = get_sha256_hex_digest_of_a_file(dict_file_path)

    file_header = f"""\
## This is a "cipher book" generated automatically.
##  * The younameit package version: {__version__}
##  * The dictionary name: {os.path.basename(dict_file_path)!r}
##  * The dictionary SHA-256: {digest}
##
## Parameters used for building this book:
##   MIN_NUM_CLUSTERS = {MIN_NUM_CLUSTERS}
##   MAX_NUM_CLUSTERS = {MAX_NUM_CLUSTERS}
##   MIN_CLUSTER_VARIATIONS = {MIN_CLUSTER_VARIATIONS}
##   MAX_CLUSTER_VARIATIONS = {MAX_CLUSTER_VARIATIONS}
""".encode()

    file_payload = file_header + yaml.safe_dump(
        book_obj,
        allow_unicode=True,
        encoding="utf-8",
        sort_keys=False,
        indent=1,
    )

    book_file_name = make_kebab_case_slug(dict_file_path)
    output_file = in_this_project(f"books/{book_file_name}-book.yaml")

    with open(output_file, "wb") as f:
        f.write(file_payload)

    print(f"yaml book written: {os.path.relpath(output_file)}")

    return book_obj


if __name__ == "__main__":

    for dict_file in [
        "/usr/share/dict/american-english",
        "/usr/share/dict/british-english",
        "/usr/share/dict/finnish",
        "/usr/share/dict/french",
        "/usr/share/dict/german",
        "/usr/share/dict/italian",
        "/usr/share/dict/spanish",
    ]:
        book = main(dict_file)
