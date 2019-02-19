

"""

    File:       smart.py
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


# Project module
from settings import settings as sets
from functions import get_sides


# Guessing around a hit
class SmartGuessing(object):
    def __init__(self, player, target, start):
        self.player = player
        self.target = target
        self.hits = [start["position"]]
        self.try_shot = []
        # Each direction: True
        self.directions = {key: True for key in get_sides()}
        self.try_shot = self.next_shots()

    # Get guess
    def shoot(self):
        # Determine the direction of the ship
        if len(self.hits) > 1:
            if self.hits[0][1] - self.hits[1][1] != 0:
                # horizontal
                self.directions["up"] = False
                self.directions["down"] = False
            elif self.hits[0][0] - self.hits[1][0] != 0:
                # vertical
                self.directions["right"] = False
                self.directions["left"] = False
        self.try_shot = self.next_shots()
        if self.try_shot:
            # Randomize shot
            return self.try_shot.pop(randint(0, len(self.try_shot) - 1))
        else:
            # It's a decoy
            return False

    # Validate possible guess
    def is_guess_valid(self, guess, direction):
        board = self.player.guesses[self.target].board
        col = range(0, sets["board"][1])
        row = range(0, sets["board"][0])
        if guess[0] in col and guess[1] in row:
            # Guess in board
            if board[guess[0]][guess[1]] == "X":
                # Remove direction
                self.directions[direction] = False
            elif board[guess[0]][guess[1]] == "H":
                if guess not in self.hits:
                    # Salvo hit position not registered
                    self.hits.append(guess)
            else:
                # Position is "O" or "F"
                return True
        return False

    # Create possible guesses for each direction
    def next_shots(self):
        shots = []
        for hit in self.hits:
            row, col = hit[0], hit[1]
            for direction, side in zip(self.directions, get_sides(row, col)):
                if self.directions[direction]:
                    guess = side[1]
                    if self.is_guess_valid(guess, direction):
                        shots.append(guess)
        for direction in self.directions.values():
            if direction:
                return shots
        else:
            # It's a decoy
            return False
