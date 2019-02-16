

"""

    File:       score.py
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


# Project modules
from settings import settings as sets
import menu


# Score class
class Score(object):
    def __init__(self, player):
        self.player = player
        self.score = {
            "hits": 0,
            "sinks": 0,
            "eliminations": 0,
            "misses": 0
        }
        self.percentages = {}

    # Register score
    def add(self, result):
        if result in ("already hit", "already guessed", "misses"):
            self.score["misses"] += 1
            menu.game.totals["misses"] += 1
        else:
            self.score["hits"] += 1
            menu.game.totals["hits"] += 1
            if result == "eliminates":
                self.score["eliminations"] += 1
                menu.game.totals["eliminations"] += 1
            elif result == "sinks":
                self.score["sinks"] += 1
                menu.game.totals["sinks"] += 1
            elif result == "win":
                self.score["sinks"] += 1
                menu.game.totals["sinks"] += 1
                self.score["eliminations"] += 1
                menu.game.totals["eliminations"] += 1

    # Calculate percentages of each score from the total
    def evaluate_percentages(self):
        self.percentages = {
            "accuracy": (self.score["hits"] /
                         (self.score["hits"] + self.score["misses"]) * 100),
            "sinks": (self.score["sinks"] /
                      menu.game.totals["sinks"] * 100),
            "eliminations": (self.score["eliminations"] /
                             menu.game.totals["eliminations"] * 100)
        }
        self.score["accuracy"] = self.percentages["accuracy"]

    # Print Score
    def __str__(self):
        self.evaluate_percentages()
        score = ""
        offset = 15
        score += "\n%s%s (Player %d)\n" %\
                 (sets["space"], self.player.name, self.player.index + 1)
        score += "%sTotals\n" % (sets["space"] * 2)
        for key, value in self.score.items():
            score += "%s%s:%s%d\n" %\
                     (sets["space"] * 3, key.capitalize(),
                      (" " * (offset + 6 - len(key) - len(str(value)))),
                      value)
        score += "\n%sPercentages\n" % (sets["space"] * 2)
        for key, value in self.percentages.items():
            score += "%s%s:%s%5.2f%%\n" %\
                     (sets["space"] * 3, key.capitalize(),
                      (" " * (offset - len(key))), value)
        score += "\n"
        return score
