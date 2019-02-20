

"""

    File:       settings.py
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


# Python modules
from copy import deepcopy
from math import floor


# Settings values interval
interval = {
    "board": [lambda ships: int(floor(ships)) * 1.15, 20],
    "players": [2, 8],
    "ai": [0, lambda ai: ai - 1],
    "timeout": [0, 5],
    "shots": [1, 5],
    "Dreadnought": [0, 1],
    "Destroyer": [0, 1],
    "Frigate": [0, 2],
    "Corvette": [1, 2],
    "PT Boat": [1, 3],
    "Decoy": [0, 2],
}


# Names for AI players and nameless humans
captains = ["Henry Morgan",
            "Blackbeard",
            "Captain Kidd",
            "Jean Lafitte",
            "Stede Bonnet",
            "L'Olonnais",
            "Roc Brasiliano",
            "Bart Roberts",
            "Jack Rackham"]


# Ship types
types = [{"ship_type": "Dreadnought", "size": 6, "quantity": 0},
         {"ship_type": "Destroyer", "size": 5, "quantity": 1},
         {"ship_type": "Frigate", "size": 4, "quantity": 1},
         {"ship_type": "Corvette", "size": 3, "quantity": 1},
         {"ship_type": "PT Boat", "size": 2, "quantity": 0},
         {"ship_type": "Decoy", "size": 1, "quantity": 2}]


# Default settings
default = {
    "board": [12, 12],  # Board Size [num of rows, num of cols]
    "cheat": True,  # Display other players ships and guesses
    "players": 4,  # Number of players
    "randomize": True,  # Randomize players ships
    "ai": 3,  # Number of AI players
    "ships": 0,  # Number of valid ships
    "timeout": 0.25,  # Timeout between moves
    "smart": True,  # AI smart guessing after a hit
    "decoy": True,  # Decoy doesn't count as a ship
    "space": "  ",  # Indentation of prints
    "shots": 4,  # Number of shots of a salvo
    "scores": True  # Print all players scores
}


# Determine the number of valid ships
for ship_type in types:
    if ship_type["ship_type"] != "Decoy" or not default["decoy"]:
        default["ships"] += ship_type["quantity"]


# User settings
settings = deepcopy(default)
