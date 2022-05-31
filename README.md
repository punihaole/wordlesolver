# wordlesolver
Helps you solve wordle by maintaining the game state and returning the first possible guess that could work.

Example:

Say the word we are trying to guess is regal...

```
>>> guesser = Guesser.construct()
>>> guesser.next_guess()
'pudgy'
>>> guesser.add_guess('p-u-d-g!y-')  # g is in the wrong spot
>>> guesser.next_guess()
'right'
>>> guesser.add_guess('r+i-g+h-t-'). # r and g are in the correct spots
>>> guesser.next_guess()
'regal'
```


The first guess will be random, unless you hard set the first_guess attribute.
```
>>> guesser = Guesser.construct()
>>> guesser.first_guess = 'guess'
>>> guesser.next_guess()
'guess'
```

You can change the rules of the game by customizing the constructor arguments.
```
>>> from solver import Guesser, GameRules
>>> from wordbank import WordBank
>>> seven_letter_words = WordBank(Path('/path/to/seven_letter_words.txt'))
>>> seven_letter_words.load()
>>> rules = GameRules(word_bank=seven_letter_words, max_guesses=10, word_length=7)
>>> guesser = Guesser(rules, first_guess='pythons')
```
