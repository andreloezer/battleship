

"""

    File:       player.py
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


# Third-party module
from colorama import Fore, Style


# Project modules
from settings import types, settings as sets
import menu
from ship import Ship
from score import Score
from board import Board


# Player class
class Player(object):
    def __init__(self):
        self.is_alive = True
        self.ships = []
        self.ships_sunken = 0
        self.target = None
        self.guesses = {}
        self.salvo = None
        self.hits = []
        self.ship = None
        self.index = None
        self.name = None
        self.score = Score(self)
        self.init_boards(self, self)

    # Initializes ships class
    def init_ships(self):
        for ship_type in types:
            for ship_num in range(ship_type["quantity"]):
                ship = Ship(self, ship_type["ship_type"], ship_type["size"])
                self.ships.append(ship)
                for position in ship.positions:
                    hor = position["coord"][0]
                    ver = position["coord"][1]
                    self.guesses[self].board[hor][ver] = "F"

    # Randomize a name
    @staticmethod
    def give_name():
        name = menu.game.names[randint(0, len(menu.game.names) - 1)]
        menu.game.names.remove(name)
        return name

    # Initializes Guesses boards if don't exist
    @staticmethod
    def init_boards(player, target):
        # TODO: Add info about ship (pointer to instance) on each position
        #       Add land ("L for land), and land generator
        try:
            player.guesses[target]
        except KeyError:
            player.guesses[target] = Board(player, target)

    # List valid targets
    def list_targets(self):
        targets = []
        for player in menu.game.players:
            if player.is_alive and player != self:
                targets.append({"player": player,
                                "ship_type": player.name})
        return targets

    # Print own ships
    @staticmethod
    def print_ships(target):
        print("%sEnemy Ships:" % (sets["space"]))
        ships = target.ships
        for ship in ships:
            if ship.floating:
                color = Fore.GREEN
            else:
                color = Fore.RED
            name = color + ship.name + Style.RESET_ALL
            print("%s%s: %s%s" % (sets["space"] * 2, name,
                                  " " * (12 - len(ship.name)), ship))
        print()
