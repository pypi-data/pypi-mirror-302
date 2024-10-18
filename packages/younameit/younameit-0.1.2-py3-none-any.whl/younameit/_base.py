import glob
import os
from typing import Dict, List, Literal, Tuple, Union

WordKind = str
# WordKind is a string describing word kind, e.g.:
# `2 even letter groups` describes a word of type `CV`
# `4 even letter groups` describes a word of type  `CVCV`
# `4 odd letter groups` describes a word of type  `VCVC`
# where `C` means one or a number of consonants
# and `V` means one or a number of vowels
# Eg: word `weighted` is of type `5 even`, because got split to `w-ei-ght-e-d` (`CVCVC`)

LettersGroup = str
# LettersGroup is a string with a half of a syllable (C or V)
# E.g., ntly, rk, sch, ei, a

NumOccurrences = int
# It's the type of value with the count of given choice's occurrence.
# E.g., 14 means that given letter group has been met at the position
# 14 times in words of given word kind.

ParityType = Literal["even", "odd", "any"]

GroupChoices = Dict[LettersGroup, NumOccurrences]
# GroupChoices maps a certain letters group to its probability

WordSkeleton = Union[
    # tuple with a variable number of GroupChoices
    Tuple[GroupChoices],
    Tuple[GroupChoices, GroupChoices],
    Tuple[GroupChoices, GroupChoices, GroupChoices],
    Tuple[GroupChoices, GroupChoices, GroupChoices, GroupChoices],
    # and so on up to 10+ elements
    # We could annotate it like that below, but python 3.9 doesn't like the ellipsis used:
    # Tuple[GroupChoices, GroupChoices, GroupChoices, GroupChoices, ...],
]

BookDictType = Dict[WordKind, Tuple[NumOccurrences, WordSkeleton]]

THashingResult = bytes


def in_this_project(*path_parts: str) -> str:
    this_dir = str(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(this_dir, *path_parts)


def list_books() -> List[Tuple[str, str]]:
    books = []
    for book_file in sorted(glob.glob(in_this_project("books", "*-book.yaml"))):
        book_name = os.path.basename(book_file).replace("-book.yaml", "")
        books.append((book_name, book_file))
    return books
