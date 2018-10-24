from copy import deepcopy

# Default settings
default = {
    "board": [8, 8],
    "cheat": True,
    "ships": 2,
    "players": 3,
    "randomize": True,
    "ai": 2,
    "timeout": 0.001,
    "size": 4,
    "smart": True,
    "space": "  "
  }

# User settings
settings = deepcopy(default)

# Settings values interval
interval = {
    "board": [3, 15],
    "ships": [1, lambda size: ((size[0] + size[1]) / 2) * 0.6],
    "players": [2, 8],
    "ai": [0, lambda ai: ai - 1],
    "timeout": [0, 5],
    "size": [1, 5]
}

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
