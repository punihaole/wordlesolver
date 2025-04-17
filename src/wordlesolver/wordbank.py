from pathlib import Path
from typing import List


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


file = Path(__file__).parent.parent / 'data' / 'sgb-words.txt'
default_word_bank = WordBank(file)
default_word_bank.load()
