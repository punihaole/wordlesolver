import unittest
from unittest import TestCase

from possibilities import Possiblities
from solver import Guesser, GameRules
from game_state import GuessLetter, GuessState, GuessWord


class TestGuesser(TestCase):
    def test_decode_guess(self):
        guesser = Guesser(None)
        guess = guesser.decode_guess('a+b!c-')
        expected_result = GuessWord([
            GuessLetter('a', GuessState.correct),
            GuessLetter('b', GuessState.wrong_position),
            GuessLetter('c', GuessState.incorrect),
        ])
        self.assertEqual(expected_result, guess)

    def test_valid_first_guess(self):
        rules = GameRules(None, 1, 5)
        guesser = Guesser(rules, 'guess')
        self.assertTrue(guesser._validate_first_guess())

    def test_invalid_first_guess(self):
        rules = GameRules(None, 1, 5)
        guesser = Guesser(rules)
        guesser.first_guess = 'blah'
        self.assertFalse(guesser._validate_first_guess())


class TestPossibilities(TestCase):
    def setUp(self) -> None:
        p = Possiblities(5)
        guess1 = GuessWord([
            GuessLetter('c', GuessState.incorrect),
            GuessLetter('h', GuessState.incorrect),
            GuessLetter('o', GuessState.wrong_position),
            GuessLetter('i', GuessState.incorrect),
            GuessLetter('r', GuessState.correct),
        ])
        p.update_state(guess1)
        guess2 = GuessWord([
            GuessLetter('p', GuessState.incorrect),
            GuessLetter('o', GuessState.wrong_position),
            GuessLetter('l', GuessState.incorrect),
            GuessLetter('a', GuessState.wrong_position),
            GuessLetter('r', GuessState.correct),
        ])
        p.update_state(guess2)
        self.possibilities = p

    def test_major(self):
        self.assertTrue(self.possibilities.is_possible('major'))

    def test_other(self):
        self.assertFalse(self.possibilities.is_possible('other'))

    def test_spoon(self):
        self.assertFalse(self.possibilities.is_possible('spoon'))

    def test_simple_game(self):
        p = Possiblities(5)
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            for position in p.positions:
                self.assertTrue(position.is_possible(letter))
        p.positions[0].set_not_letter('a')
        self.assertFalse(p.positions[0].is_possible('a'))
        for position in p.positions[1:]:
            self.assertTrue(position.is_possible('a'))


class TestGame(TestCase):
    def test_manor(self):
        guesser = Guesser.construct()
        guesser.first_guess = 'choir'
        guess1 = guesser.next_guess()
        self.assertEqual('choir', guess1)
        guesser.add_guess('c-h-o!i-r+')
        guess2 = guesser.next_guess()
        self.assertEqual('order', guess2)
        guesser.add_guess('o!r-d-e-r+')
        guess3 = guesser.next_guess()
        self.assertEqual('major', guess3)
        guesser.add_guess('m+a+j-o+r+')
        guess4 = guesser.next_guess()
        self.assertEqual('mayor', guess4)
        guesser.add_guess('m+a+y-o+r+')
        guess5 = guesser.next_guess()
        self.assertEqual('manor', guess5)
        guesser.add_guess('m+a+n+o+r+')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
