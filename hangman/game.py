from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()

        self.letter = letter.lower()
        self.hit = hit
        self.miss = miss

    def is_hit(self):
        return self.hit == True

    def is_miss(self):
        return self.miss == True


class GuessWord(object):
    def __init__(self, word):
        if not len(word):
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = '*' * len(word)

    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException()

        self.guessedletter = letter.lower()
        masked_temp = ''.join([self.answer[i] if self.answer[i] == self.guessedletter else self.masked[i] for i in
                               range(len(self.answer))])

        if masked_temp != self.masked:
            self.masked = masked_temp
            return GuessAttempt(letter, hit=True)
        else:
            return GuessAttempt(letter, miss=True)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list = None, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        selected_word = self.select_random_word(word_list if word_list else HangmanGame.WORD_LIST)
        self.word = GuessWord(selected_word.lower())
        self.previous_guesses = []

    @classmethod
    def select_random_word(cls, word_list):
        if len(word_list) > 0:
            return random.choice(word_list)
        elif len(word_list) == 0:
            raise InvalidListOfWordsException()

    def guess(self,letter):
        self.letter = letter.lower()
        if not self.is_finished():
            result = self.word.perform_attempt(letter = self.letter)
            self.previous_guesses += letter.lower()
            if result.miss == True:
                self.remaining_misses -= 1
                # if self.remaining_misses <=0:
                #     raise GameLostException()
            if self.is_lost():
                raise GameLostException()
            if self.is_won():
                raise GameWonException()
            return result
        else:
            raise GameFinishedException()

    def is_finished(self):
        if self.remaining_misses <=0 or self.word.answer == self.word.masked:
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    def is_lost(self):
        if self.word.answer != self.word.masked and self.remaining_misses <=0:
            return True
        return False


