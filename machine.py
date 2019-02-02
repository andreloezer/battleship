

"""

    File:       machine.py
    Project:    Console Battleship
    Author:     André César Loezer
    Email:      andrecesarloezer@gmail.com
    Date:       2018/2019

    A python 3.6 Battleship game with no UI, just console

    Written on Atom and PyCharm, following PEP8 standards

    Inspired on Codecademy's Python 2 'List and Function - Battleship!'
    www.codecademy.com/courses/learn-python/lessons/battleship/

    This project was done with the sole purpose of learning

    Dependencies
        Colorama (pypi.org/project/colorama)

    Features
         8 players (humans or not),
         Salvo (variable number of shots),
         Smart guessing for machine players,
         Variable board sizes for each coordinate,
         Multiples ships with different sizes,
         Decoys (does not count to the number of ships),
         Score tracking,
         Options to change settings about all this features

"""


from random import randint


from settings import settings as sets
from player import Player
from smart import SmartGuessing


class Machine(Player):
    def __init__(self):
        Player.__init__(self)
        self.ai = True
        self.choose_ship = False
        self.name = self.give_name()
        self.init_ships()
        self.smart = sets["smart"]
        self.smart_guess = None

    # Choose/determine the target
    def get_target(self):
        if len(self.hits) == 0:
            targets = self.list_targets()
            self.target = targets[randint(0, len(targets) - 1)]["player"]
        self.init_boards(self, self.target)

    # Validate guess position
    def is_position_valid(self, target, position):
        board = self.guesses[target]
        col = range(1, sets["board"][1] + 1)
        row = range(1, sets["board"][0] + 1)
        if position[0] in col and position[1] in row:
            # Position in board
            if board[position[0] - 1][position[1] - 1] == "O":
                return True
            else:
                return False

    # Random guess
    @staticmethod
    def random_guess():
        return [randint(1, sets["board"][1]),
                randint(1, sets["board"][0])]

    def still_floating(self, target, hit):
        board = self.guesses[target]
        if board[hit[0] - 1][hit[1] - 1] == "S":
            return False
        else:
            return True

    # Player guess
    def player_guess(self, hits=False):
        # Smart Guessing ship still floating
        if self.smart_guess and self.still_floating(self.target,
                                                    self.smart_guess.hits[0]):
            # Smart Guessing guess hits
            if hits and self.hits[-1]["target"] == self.smart_guess.target:
                self.smart_guess.hits.append(self.hits.pop()["position"])
            guess = self.smart_guess.shoot()
        # No Smart Guessing
        else:
            while len(self.hits) > 0:
                hit = self.hits.pop()
                if self.still_floating(self.target, hit["position"]):
                    self.smart_guess = SmartGuessing(self, self.target, hit)
                    guess = self.smart_guess.shoot()
                    break
            else:
                self.smart_guess = None
                guess = self.get_guess()
        if not guess:
            self.smart_guess = None
            guess = self.player_guess(self.target)
        return guess

    # Random guess
    def get_guess(self):
        while True:
            guess = self.random_guess()
            if self.is_position_valid(self.target, guess):
                return guess

    # Display guessing info of the AI
    @staticmethod
    def cheat(target, guess):
        print("%sAI Target: %s" % (sets["space"], target.name))
        print("%sAI Guess: %s\n" % (sets["space"], guess))
