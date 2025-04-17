from enum import Enum, auto
from typing import List


class GuessState(Enum):
    incorrect = auto()
    wrong_position = auto()
    correct = auto()


class GuessLetter:
    def __init__(self, letter: str = None, state: GuessState = None):
        self.letter: str = letter
        self.state: GuessState = state

    def __eq__(self, other) -> bool:
        if not isinstance(other, GuessLetter):
            return False
        same_state = self.state == other.state
        same_letter = self.letter == other.letter
        return same_letter and same_state

    def __repr__(self) -> str:
        pos_0 = self.letter or '?'
        pos_1 = self._encode_state()
        return f'{pos_0}{pos_1}'

    def _encode_state(self) -> str:
        res = '?'
        if self.state == GuessState.incorrect:
            res = '-'
        if self.state == GuessState.wrong_position:
            res = '!'
        if self.state == GuessState.correct:
            res = '+'
        return res


class GuessWord:
    def __init__(self, letters: List[GuessLetter] = None):
        self.letters = letters or []

    def __len__(self) -> int:
        return len(self.letters)

    def __eq__(self, other) -> bool:
        if not isinstance(other, GuessWord):
            return False
        for a_letter, b_letter in zip(self.letters, other.letters):
            if a_letter != b_letter:
                return False
        return True

    def __repr__(self) -> str:
        result = []
        for letter in self.letters:
            result.append(repr(letter))
        return ''.join(result)

    def __str__(self) -> str:
        result = []
        for guess_letter in self.letters:
            result.append(guess_letter.letter)
        return ''.join(result)
