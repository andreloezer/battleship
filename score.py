

from settings import settings as set


# Score class
class Score(object):
    def __init__(self, player):
        self.player = player
        self.score = {
            "hits": 0,
            "sinks": 0,
            "eliminates": 0,
            "misses": 0
        }

    # Register score
    def add(self, result):
        if result in ("already hitted", "already guessed", "misses"):
            self.score["misses"] += 1
        else:
            self.score["hits"] += 1
            if result not in ("hits", "win"):
                self.score[result] += 1

    # Print Score
    def print_score(self):
        score = self.score
        offset = 15
        print("%sTotals" % (set["space"] * 2))
        for key, value in score.items():
            print("%s%s:%s%d" % (set["space"] * 3, key.capitalize(),
                                 (" " * (offset + 6 - len(key) -
                                  len(str(value)))),
                                 value))
        percents = {}
        if score["hits"] == 0:
            percents["accuracy"] = 0
        else:
            percents["accuracy"] = (score["hits"] /
                                    (score["hits"] + score["misses"]) * 100)
        if score["sinks"] == 0:
            percents["sinks"] = 0
        else:
            percents["sinks"] = (score["sinks"] /
                                 (set["ships"] * set["players"]) * 100)
        if score["eliminates"] == 0:
            percents["eliminates"] = 0
        else:
            percents["eliminates"] = (score["eliminates"] /
                                      set["players"] * 100)

        print("\n%sPercentages" % (set["space"] * 2))
        for key, value in percents.items():
            print("%s%s:%s%5.2f%%" % (set["space"] * 3, key.capitalize(),
                                      (" " * (offset - len(key))), value))
        print()
