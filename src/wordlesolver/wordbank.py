from pathlib import Path
from typing import List

from sgb_words import WORD_LIST


class WordBank:
    def __init__(self, path: Path):
        self.path = path
        self.words: List[str] = []

    def load(self):
        self.words = []
        with self.path.open('r') as file_object:
            for word in file_object.readlines():
                self.words.append(word.strip())

    def __iter__(self):
        return iter(self.words)


default_word_bank = WordBank(None)
default_word_bank.words = WORD_LIST
