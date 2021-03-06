

"""

    File:       human.py
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


# Project modules
from settings import settings as sets
from functions import input_num
from player import Player
import menu


class Human(Player):
    def __init__(self):
        Player.__init__(self)
        self.ai = False
        self.ask_name()
        if sets["randomize"]:
            self.choose_ship = False
        else:
            if str(input("%sChoose ships positions? "
                         % (sets["space"]))) in ("y", "yes"):
                self.choose_ship = True
                print("\n%s%s position your ships:"
                      % (sets["space"], self.name))
            else:
                self.choose_ship = False

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

    # Ask for the name of the human player
    def ask_name(self):
        self.name = input("\n%sChoose a name: " % (sets["space"]))
        if not self.name:
            self.name = self.give_name()
            print("%sRandom name chosen: %s\n"
                  % (sets["space"] * 2, self.name))

    # Choose/determine the target
    def get_target(self):
        targets = self.list_targets()
        if len(targets) == 1:
            self.target = targets[0]["player"]
        else:
            self.target = self.ask_target()
        self.init_boards(self, self.target)

    # Ask player to give a target
    def ask_target(self):
        print("%sPlayers:\n" % (sets["space"]))
        for index, player in enumerate(menu.game.players):
            if player == self:
                player_color = Fore.CYAN
            elif not player.is_alive:
                player_color = Fore.RED
            else:
                player_color = Fore.GREEN
            print("%s%sPlayer %s: %s%s(%s Ships floating)%s"
                  % (sets["space"] * 2, player_color, index + 1,
                     player.name, " " * (35 - len(player.name)),
                     sets["ships"] - player.ships_sunken,
                     Style.RESET_ALL))
        print()
        while True:
            response_target = input_num("%sChoose a target by player number"
                                        % (sets["space"]), 1, sets["players"],
                                        "int")
            target = response_target - 1
            if menu.game.players[target] == self:
                print("%sCannot target yourself" % (sets["space"] * 2))
            elif not menu.game.players[target].is_alive:
                print("%sCannot target a dead player" % (sets["space"] * 2))
            else:
                return menu.game.players[target]

    # Ask guess
    @staticmethod
    def get_guess():
        return_key = "r"
        guessing = ("Row", "Col")
        guess = []
        for count, axis in enumerate(guessing):
            if sets["players"] > 2:
                answer = input_num("%sGuess %s   ('%s' to return)" %
                                   (sets["space"], axis, return_key), 1,
                                   sets["board"][(len(guessing) - 1) - count],
                                   "int", return_key)
            else:
                answer = input_num("%sGuess %s" %
                                   (sets["space"], axis), 1,
                                   sets["board"][(len(guessing) - 1) - count],
                                   "int")
            if answer:
                guess.append(answer - 1)
            else:
                return False
        return guess

    def print_board(self, target):
        if target is self:
            print("Your board:\n")
            print(self.guesses[target])
        else:
            print("\nTargets board:\n")
            if sets["cheat"]:
                self.print_ships(target)
            print(self.guesses[target])

    # Ask player for a guess
    def player_guess(self, hits=False):
        self.print_board(self.target)
        if hits:
            print("%sYou were awarded with another shot!\n" % sets["space"])
        guess = self.get_guess()
        while not guess:
            self.get_target()
            self.print_board(self.target)
            guess = self.get_guess()
        print()
        return guess
