

"""

    File:       ship.py
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
from random import randint
from colorama import Fore
from settings import settings as sets
from functions import input_num


# Ship Class
class Ship(object):
    def __init__(self, player, name, size, direction="random"):
        self.floating = True
        self.size = size
        self.direction = direction
        self.player = player
        self.name = name
        self.hits = 0
        self.positions = []
        self.create_ship()

    # Generate a random direction for the ship
    def gen_direction(self):
        if self.direction == "random":
            return ["horizontal", "vertical"][randint(0, 1)]
        else:
            return self.direction

    # Prepare a string for printing the Ship class (used on cheat)
    def __str__(self):
        string = ""
        for position in self.positions:
            if position["floating"]:
                string += Fore.GREEN + str(position["coord"] + 1)
            else:
                string += Fore.RED + str(position["coord"] + 1)
        return string

    # Place the ship at a random and valid place
    def gen_ship(self, hor, ver):
        positions = []
        for point in range(self.size):
            if self.direction == "horizontal":
                position = [hor, ver + point + 1]
            # When self.direction == "vertical"
            elif self.direction == "vertical":
                position = [hor + point + 1, ver]
            else:
                position = [hor, ver]
            if self.validate(position):
                positions.append({"floating": True, "coord": position})
            else:
                return False
        else:
            return positions

    # Create ship with size bigger than 1
    def create_ship(self):
        while True:
            if not self.player.choose_ship or self.player.ai:
                if self.size != 1:
                    self.direction = self.gen_direction()
                # Starting position + size must fit inside board
                start = [0, 0]
                if self.direction == "horizontal":
                    start[0] = self.size + 1
                elif self.direction == "vertical":
                    start[1] = self.size + 1
                hor = randint(0, sets["board"][1] - (start[1] + 1))
                ver = randint(0, sets["board"][0] - (start[0] + 1))
                ship = self.gen_ship(hor, ver)
            else:
                if self.size == 1:
                    ship = self.ask_position()
                else:
                    ship = self.ask_position_length()
            if ship:
                self.positions = ship
                break

    # Check if ship is still floating
    def is_floating(self):
        if self.hits == self.size:
            self.floating = False
            return False

    # Create position
    @staticmethod
    def random_position():
        row = randint(0, sets["board"][1] - 1)
        col = randint(0, sets["board"][0] - 1)
        return [row, col]

    # Ask human player for a direction for the ship
    def ask_direction(self):
        while True:
            direction = input("%sChoose the direction" % (sets["space"])
                              + "(horizontal, vertical, random): "
                              ).lower()
            if direction in ("h", "horizontal"):
                return "horizontal"
            elif direction in ("v", "vertical"):
                return "vertical"
            elif direction in ("r", "random"):
                self.direction = "random"
                return self.gen_direction()
            else:
                print("%sEnter a valid direction" % (sets["space"]))

    # Ask human player for the starting position of the ship
    def ask_position_length(self):
        print("\n%s%s (length: %d)" % (sets["space"], self.name, self.size))
        self.direction = self.ask_direction()
        print("%s%s direction: %s"
              % (sets["space"] * 2, self.name, self.direction))
        if self.direction == "horizontal":
            hor = input_num("%sChoose row" % (sets["space"] * 2),
                            1, sets["board"][1], "int")
            ver = input_num("%sChoose starting column" % (sets["space"] * 2),
                            1, sets["board"][0] - self.size, "int") - 1
        # When self.direction == "vertical"
        else:
            ver = input_num("%sChoose col" % (sets["space"] * 2),
                            1, sets["board"][0] - self.size, "int")
            hor = input_num("%sChoose starting row" % (sets["space"] * 2),
                            1, sets["board"][1], "int") - 1
        ship = self.gen_ship(hor, ver)
        return ship

    # Player chooses the ship position
    def ask_position(self):
        print("\n%s%s:" % (sets["space"], self.name))
        row = input_num("%sChoose %s row"
                        % (sets["space"], self.name),
                        1, sets["board"][1], "int")
        col = input_num("%sChoose %s column"
                        % (sets["space"], self.name),
                        1, sets["board"][0], "int")
        position = [row, col]
        if self.validate(position):
            return [[True, position]]
        else:
            return False

    # Check if position doesn't conflict with other ships
    def validate(self, position):
        row = position[0]
        col = position[1]
        for ship in self.player.ships:
            for ship_position in ship.positions:
                if ship_position["coord"] == [row, col]:
                    if not (sets["randomize"] or self.player.ai):
                        print("\n%sPosition already occupied"
                              % (sets["space"] * 3))
                    return False
                elif ship_position["coord"] in [[row - 1, col],
                                                [row + 1, col],
                                                [row, col - 1],
                                                [row, col + 1]]:
                    if not (sets["randomize"] or self.player.ai):
                        print("\n%sToo close to another ship"
                              % (sets["space"] * 3))
                    return False
        else:
            return True
