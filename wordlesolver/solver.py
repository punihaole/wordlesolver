import dataclasses
import random
from typing import List

from wordlesolver.game_state import GuessWord, GuessLetter, GuessState
from wordlesolver.possibilities import Possiblities
from wordlesolver.wordbank import WordBank, default_word_bank


@dataclasses.dataclass(frozen=True)
class GameRules:
    word_bank: WordBank
    max_guesses: int
    word_length: int


class Guesser:
    word_bank: WordBank = None
    possibilities: Possiblities = None
    max_guesses: int = None
    word_length: int = None

    def __init__(self, rules: GameRules, first_guess: str = None):
        self.rules = rules
        self.guesses: List[GuessWord] = []
        if rules:
            self._unpack_rules()
        self.first_guess = first_guess
        if first_guess:
            if not self._validate_first_guess():
                raise ValueError(f'First guess must be {self.word_length} letters long!')

    def _unpack_rules(self):
        self.word_bank = self.rules.word_bank
        self.possibilities = Possiblities(num_letters=self.rules.word_length)
        self.max_guesses = self.rules.max_guesses
        self.word_length = self.rules.word_length

    def _validate_first_guess(self) -> bool:
        if len(self.first_guess) != self.word_length:
            return False
        return True

    def next_guess(self) -> str:
        num_guesses = len(self.guesses)
        if num_guesses == 0:
            word = self.get_first_guess()
        elif num_guesses < self.max_guesses:
            word = self.get_best_guess()
        else:
            raise RuntimeError('You are out of guesses!')
        if not word:
            raise RuntimeError('No more guesses found!')
        return word

    def get_first_guess(self) -> str:
        if self.first_guess:
            return self.first_guess
        return random.choice(self.word_bank.words)

    def get_best_guess(self) -> str:
        try:
            return self.get_all_possible_guesses()[0]
        except IndexError:
            return None

    def get_all_possible_guesses(self) -> List[str]:
        guesses = []
        for word in self.word_bank:
            if self.possibilities.is_possible(word):
                guesses.append(word)
        return guesses

    @classmethod
    def construct(cls):
        rules = GameRules(word_bank=default_word_bank,  max_guesses=6, word_length=5)
        return Guesser(rules)

    def add_guess(self, guess_str: str):
        guess = self.decode_guess(guess_str)
        self.guesses.append(guess)
        self.possibilities.update_state(guess)

    def decode_guess(self, guess: str) -> GuessWord:
        guess_letters: List[GuessLetter] = []
        guess_list = list(guess)
        while len(guess_list) >= 2:
            letter = guess_list.pop(0)
            key = guess_list.pop(0)
            state = self._key_to_guess_state(key)
            guess_letters.append(GuessLetter(letter, state))
        if guess_list:
            raise ValueError(f'Invalid guess string: Some letters were leftover: {guess_list}!')
        if self.word_length and len(guess_letters) != self.word_length:
            raise ValueError(f'Invalid guess, must be {self.word_length} letters long!')
        guess = GuessWord(guess_letters)
        return guess

    def _key_to_guess_state(self, key: str) -> GuessState:
        if key == '-':
            return GuessState.incorrect
        if key == '!':
            return GuessState.wrong_position
        if key == '+':
            return GuessState.correct
        raise ValueError('Invalid key')
