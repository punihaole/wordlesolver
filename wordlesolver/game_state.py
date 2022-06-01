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
        if self.state == GuessState.incorrect:
            return '-'
        elif self.state == GuessState.wrong_position:
            return '!'
        elif self.state == GuessState.correct:
            return '+'
        else:
            return '?'


class GuessWord:
    def __init__(self, letters: List[GuessLetter] = []):
        self.letters = letters

    def __len__(self) -> int:
        return len(self.letters)

    def __eq__(self, other) -> bool:
        if not isinstance(other, GuessWord):
            return False
        for a, b in zip(self.letters, other.letters):
            if a != b:
                return False
        return True

    def __repr__(self) -> str:
        r = []
        for l in self.letters:
            r.append(repr(l))
        return ''.join(r)

    def __str__(self) -> str:
        s = []
        for l in self.letters:
            s.append(l.letter)
        return ''.join(s)
