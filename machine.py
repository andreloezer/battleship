

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


# Python module
from random import randint


# Project modules
from settings import settings as sets
from player import Player
from smart import SmartGuessing


class Machine(Player):
    sides = {
        "up": [-1, 0],
        "down": [1, 0],
        "left": [0, -1],
        "right": [0, 1]
    }

    def __init__(self):
        Player.__init__(self)
        self.ai = True
        self.choose_ship = False
        self.name = self.give_name()
        self.smart = sets["smart"]
        self.smart = None

    # Choose/determine the target
    def get_target(self):
        if len(self.hits) == 0 and not self.smart:
            targets = self.list_targets()
            self.target = targets[randint(0, len(targets) - 1)]["player"]
        self.init_boards(self, self.target)

    # Player guess
    def player_guess(self, hits=False):
        guess = False
        board = self.guesses[self.target].board
        # Smart Guessing ship still floating
        if self.smart and\
           board[self.smart.hits[0][0]][self.smart.hits[0][1]] != "S":
            # Smart Guessing guess hits
            if hits and self.hits[-1]["target"] == self.smart.target:
                self.smart.hits.append(self.hits.pop()["position"])
            guess = self.smart.shoot()
        # No Smart Guessing
        else:
            while len(self.hits) > 0:
                hit = self.hits.pop()
                if board[hit["position"][0]][hit["position"][1]] != "S":

                    self.smart = SmartGuessing(self, self.target, hit)
                    guess = self.smart.shoot()
        if guess:
            return guess
        else:
            self.smart = None
            self.get_target()
            guess = self.get_guess()
        return guess

    def get_sides(self, guess):
        sides = {}
        col = range(0, sets["board"][1])
        row = range(0, sets["board"][0])
        for key, value in self.sides.items():
            position = [value[0] + guess[0], value[1] + guess[1]]
            if position[0] in col and position[1] in row:
                sides[key] = position
        return sides

    # Random guess
    def get_guess(self):
        board = self.guesses[self.target].board
        valid_positions = []
        for row_index, row in enumerate(self.guesses[self.target].board):
            for col_index, col in enumerate(row):
                if col in ("O", "F"):
                    valid_positions.append([row_index, col_index])
        while True:
            guess = valid_positions.pop(randint(0, len(valid_positions) - 1))
            if sets["decoy"]:
                sides = self.get_sides(guess)
                for side in sides.values():
                    if board[side[0]][side[1]] in ("O", "F"):
                        return guess
            else:
                return guess

    # Display guessing info of the AI
    @staticmethod
    def cheat(target, guess):
        print("%sAI Target: %s" % (sets["space"], target.name))
        print("%sAI Guess: %s\n" %
              (sets["space"], [guess[0] + 1, guess[1] + 1]))
