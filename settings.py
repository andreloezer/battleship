from copy import deepcopy
from math import floor


# Settings values interval
interval = {
    "board": [lambda ships: int(floor(ships)) * 1.5, 25],
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
captains = ["Captain Jack Sparrow",
            "Captain James T. Kirk",
            "Captain Ahab",
            "Admiral Ackbar",
            "Captain Hendrick van der Decken",
            "Admiral Motti",
            "Captain Haddock",
            "Captain Davy Jones",
            "Captain Hook",
            "Captain Han Solo",
            "Admiral General Aladeen"]


# Ship types
types = [{"type": "Dreadnought", "size": 6, "quantity": 0},
         {"type": "Destroyer", "size": 5, "quantity": 0},
         {"type": "Frigate", "size": 4, "quantity": 2},
         {"type": "Corvette", "size": 3, "quantity": 2},
         {"type": "PT Boat", "size": 2, "quantity": 2},
         {"type": "Decoy", "size": 1, "quantity": 2}]


# Default settings
default = {
    "board": [10, 10],  # Board Size [num of rows, num of cols]
    "cheat": True,  # Display other players ships and guesses
    "players": 5,  # Number of players
    "randomize": True,  # Randomize players ships
    "ai": 5,  # Number of AI players
    "timeout": 0.01,  # Timeout between moves
    "smart": True,  # AI smart guessing after a hit
    "decoy": True,  # Decoy doesn't count as a ship
    "space": "  ",  # Indentation of prints
    "shots": 1  # Number of shots of a salvo
}


# Determine the number of valid ships
default["ships"] = 0
for ship_type in types:
    if ship_type["type"] != "Decoy" or not default["decoy"]:
        default["ships"] += ship_type["quantity"]


# User settings
settings = deepcopy(default)
