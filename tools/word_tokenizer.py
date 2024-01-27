import re
from hazm import WordTokenizer, Normalizer


class WordTokenizer:
    def __init__(self, join_verb_parts: bool = True, join_abbreviation: bool = True):
        self._join_verb_parts = join_verb_parts
        self._join_abbreviation = join_abbreviation

    def tokenize(self, text: str) -> list:
        tokens = text.split()
        if self._join_verb_parts:
            tokens = WordTokenizer._join_verb_parts(tokens)
        if self._join_abbreviation:
            tokens = WordTokenizer._join_abbreviation(tokens)
        return tokens

    @staticmethod
    def _join_verb_parts(text: list) -> list:
        return text

    @staticmethod
    def _join_abbreviation(text: list) -> list:
        return text
