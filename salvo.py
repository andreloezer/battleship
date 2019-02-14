

"""

    File:       salvo.py
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


class Salvo(object):
    def __init__(self, player):
        self.player = player
        self.positions = []
        self.hits = []
        self.sink = False

    # Get/ask the guesses for the salvo
    def get_shots(self):
        if self.player.ai or not self.player.target.is_alive:
            self.player.get_target()
        for position in range(sets["shots"]):
            while True:
                if not self.player.ai:
                    print("\n%sGuess shot %i" % (sets["space"], position + 1))
                answer = self.player.get_guess()
                if answer:
                    if answer not in self.positions:
                        self.positions.append(answer)
                        break
                    elif not self.player.ai:
                        print("\n%sYou can't guess the same spot"
                              % sets["space"])
                else:
                    self.positions = []
                    self.player.get_target()
                    self.player.guesses[self.player.target].print_board()
                    self.get_shots()
                    return

    # Check each guess
    def check_shots(self):
        index = 1
        while len(self.positions) > 0:
            guess = self.positions.pop(0)
            print("\n%sShot %i" % (sets["space"], index))
            index += 1
            if sets["cheat"]:
                print("%s%s Shot: %s" % (sets["space"], self.player.name,
                                         guess))
            result = menu.game.check(self.player, self.player.target, guess)
            # Register score
            self.player.score.add(result)
            menu.game.print_result(self.player, self.player.target, result)
            if result == "hits":
                self.hits.append(guess)
            if result == "sinks":
                self.hits.append(guess)
                self.sink = True
            if result == "win":
                return "win"
        else:
            if self.sink:
                return "sinks"
            elif len(self.hits) > 0:
                return "hits"
            else:
                return "misses"
