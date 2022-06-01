from typing import List

from wordlesolver.game_state import GuessWord, GuessState


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class Position:
    def __init__(self):
        self.letters = set()
        for letter in ALPHABET:
            self.letters.add(letter)

    def set_letter(self, letter: str):
        self.letters = set([letter])

    def set_not_letter(self, letter: str):
        if len(self.letters) == 1:
            return
        if letter in self.letters:
            self.letters.remove(letter)

    def set_possible_letter(self, letter: str):
        self.letters.add(letter)

    def is_possible(self, letter: str) -> bool:
        return letter in self.letters

    def __repr__(self) -> str:
        return repr(self.letters)


class Possiblities:
    def __init__(self, num_letters: int):
        self.positions: List[Position] = []
        self.required_letters = set()
        for i in range(num_letters):
            self.positions.append(Position())

    def is_possible(self, word: str) -> bool:
        for i, letter in enumerate(word):
            position = self.positions[i]
            if not position.is_possible(letter):
                return False
        return self.has_all_required_letters(word)

    def has_all_required_letters(self, word: str) -> bool:
        for req in self.required_letters:
            if req not in word:
                return False
        return True

    def update_state(self, guess: GuessWord):
        for i, guess_letter in enumerate(guess.letters):
            if guess_letter.state == GuessState.correct:
                self.positions[i].set_letter(guess_letter.letter)
            elif guess_letter.state == GuessState.wrong_position:
                self.positions[i].set_not_letter(guess_letter.letter)
                self.required_letters.add(guess_letter.letter)
            else:
                for position in self.positions:
                    position.set_not_letter(guess_letter.letter)
