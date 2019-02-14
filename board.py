
"""

    File:       board.py
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


# Third-party module
from colorama import Fore, Style


# Project module
from settings import settings as sets


# Board class
class Board(object):
    def __init__(self, player, target):
        self.player = player
        self.target = target
        self.board = []
        self.fill_board()

    def fill_board(self):
        for row in range(sets["board"][1]):
            self.board.append(["O"] * sets["board"][0])
        if self.target is not self.player:
            for ship in self.target.ships:
                for position in ship.positions:
                    hor = position["coord"][0]
                    ver = position["coord"][1]
                    self.board[hor][ver] = "F"

    def __str__(self):
        board_string = ""
        header = "%s     " % (sets["space"])
        for col in range(sets["board"][0]):
            if col >= 9:
                space = "  "
            else:
                space = "   "
            header += str(col + 1) + space
        sub_header = "%s     |%s" % (sets["space"],
                                     "   |" * (sets["board"][0] - 1))
        board_string += header + "\n" + sub_header + "\n\n"
        col_count = 1
        for row in self.board:
            if col_count >= 10:
                print_row = "%s%d-  " % (sets["space"], col_count)
            else:
                print_row = "%s %d-  " % (sets["space"], col_count)
            for position in row:
                # Miss
                if position == "X":
                    color = Fore.RED + position
                # Hit
                elif position == "H":
                    color = Fore.GREEN + position
                # Sunk
                elif position == "S":
                    color = Fore.CYAN + position
                # Floating
                elif position == "F" and \
                        (sets["cheat"] or self.target is self.player):
                    color = Fore.WHITE + position
                # Water
                else:
                    color = Fore.BLUE + "O"
                print_row += color + Style.RESET_ALL + "   "
            print_row += "-%d" % col_count
            board_string += print_row + "\n\n"
            col_count += 1
        board_string += sub_header + "\n" + header + "\n"
        return board_string
