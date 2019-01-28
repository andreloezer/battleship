

from settings import settings as set
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

    # Register score
    def add(self, result):
        if result in ("already hitted", "already guessed", "misses"):
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
    def print_score(self):
        self.evaluate_percentages()
        offset = 15
        print("%sTotals" % (set["space"] * 2))
        for key, value in self.score.items():
            print("%s%s:%s%d" % (set["space"] * 3, key.capitalize(),
                                 (" " * (offset + 6 - len(key) -
                                  len(str(value)))),
                                 value))
        print("\n%sPercentages" % (set["space"] * 2))
        for key, value in self.percentages.items():
            print("%s%s:%s%5.2f%%" % (set["space"] * 3, key.capitalize(),
                                      (" " * (offset - len(key))), value))
        print()
