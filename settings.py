from copy import deepcopy
from math import floor


# Default settings
default = {
    "board": [10, 10],  # Board Size [num of rows, num of cols]
    "cheat": True,  # Display other players ships and guesses
    "ships": 1,  # Number of ships
    "players": 3,  # Number of players
    "randomize": True,  # Randomize players ships
    "ai": 2,  # Number of AI players
    "timeout": 0.1,  # Timeout between AI moves
    "smart": True,  # AI smart guessing after a hit
    "decoy": True,  # Decoy doesn't count as a ship
    "space": "  "  # Indentation of prints
  }


# User settings
settings = deepcopy(default)


# Settings values interval
interval = {
    "board": [lambda ships: int(floor(ships)) * 1.5, 25],
    "players": [2, 8],
    "ai": [0, lambda ai: ai - 1],
    "timeout": [0, 5],
    "Dreadnought": [0, 1],
    "Destroyer": [0, 1],
    "Frigate": [0, 2],
    "Corvette": [1, 2],
    "PT Boat": [1, 3],
    "Decoy": [0, 2]
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
types = [{"type": "Dreadnought", "size": 6, "quantity": 1},
         {"type": "Destroyer", "size": 5, "quantity": 0},
         {"type": "Frigate", "size": 4, "quantity": 0},
         {"type": "Corvette", "size": 3, "quantity": 2},
         {"type": "PT Boat", "size": 2, "quantity": 0},
         {"type": "Decoy", "size": 1, "quantity": 1}]
