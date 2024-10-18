"""
A nomenclator (/ˈnoʊmən.kleɪtər/ NOH-mən-KLAY-tər; English plural nomenclators, Latin plural
nomenclatores; derived from the Latin nomen- name + calare – to call), in classical times, referred
to a slave whose duty was to recall the names of persons his master met during a political
campaign.[1] Later, the scope was expanded to include names of people in any social context and also
other socially important information about them.[2]

However, it has taken on several other meanings and also refers to a book containing collections or
lists of words.[2] It also denotes a person, generally a public official, who announces the names of
guests at a party or other social gathering or ceremony.[2]

In more general terms still, it is a person who provides or creates the names for things,[3] and
this can apply to the application of names in a scientific or any other context, but especially in
relation to specialist terminologies, glossaries etc.[2][4]

"""

import os.path
import random
from copy import deepcopy
from typing import Any, Dict, Tuple, Union

import yaml

from younameit._antirandom import random_generator_poisoning
from younameit._base import BookDictType, GroupChoices, ParityType, WordSkeleton, list_books
from younameit._hashing_function import from_any_to_hash


class Nomenclator:
    def __init__(self, language_name: str):
        self.the_book: BookDictType = self._load_book_from_yaml(language_name)
        self.books: Dict[str, BookDictType] = {language_name: self.the_book}

    @classmethod
    def _load_book_from_yaml(cls, language: str) -> BookDictType:
        book_file = dict(list_books())
        if language not in book_file:
            raise ValueError(f"Unknown language: {language!r}.")

        if not os.path.isfile(book_file[language]):
            raise ValueError(f"Book yaml file not found for language: {language!r}.")

        with open(book_file[language], "r") as f:
            book = yaml.safe_load(f)
        return book

    def from_any_to_word(
        self, anything: Union[bytes, Any], *number_of_groups: int, parity: ParityType = "any", num_words: int = 1
    ) -> str:
        words = []
        the_seed = from_any_to_hash(anything)
        with random_generator_poisoning(the_seed):
            for _ in range(num_words):
                word = self.pseudo_random_word(*number_of_groups, parity=parity)
                words.append(word)
        return " ".join(words)

    def pseudo_random_word(self, *number_of_groups: int, parity: ParityType = "any") -> str:
        """Make a random word out of the book of certain length. Not reproducible"""
        skeleton = self.pick_word_kind(number_of_groups, parity=parity)
        return "".join(self.pick_weighted(g) for g in skeleton)

    def pick_word_kind(self, number_of_groups: Tuple[int, ...], parity: ParityType) -> WordSkeleton:
        """Randomly decide the number of clusters and parity for a word."""
        assert self.the_book, f"Empty or no book in the class {self.__name__!r}"
        assert isinstance(parity, str) and parity in ["any", "even", "odd"], f"Invalid parity: {parity!r}"

        the_book = deepcopy(self.the_book)
        assert isinstance(number_of_groups, tuple), f"Invalid type(number_of_groups)={type(number_of_groups).__name__}"
        if number_of_groups:
            assert all(isinstance(n, int) for n in number_of_groups), f"Invalid number_of_groups={number_of_groups!r}"

            the_book = {k: v for k, v in the_book.items() if any(k.startswith(f"{n} ") for n in number_of_groups)}

        if parity != "any":
            the_book = {k: v for k, v in the_book.items() if f" {parity} " in k}
        assert the_book, f"No words matching the word kind: {number_of_groups} parity: {parity}."
        counts, values = zip(*the_book.values())
        return random.choices(values, counts)[0]

    @staticmethod
    def pick_weighted(group: GroupChoices) -> str:
        """Randomly pick letters group basing of its probability."""
        population, weights = zip(*list(group.items()))
        return random.choices(population, weights)[0]
