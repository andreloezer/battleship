

"""

    File:       game.py
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


# Python modules
from copy import deepcopy
from random import shuffle
from time import sleep


# Third-party module
from colorama import Fore, Style


# Project modules
from settings import settings as sets, captains
from functions import offset, clear_screen
from human import Human
from machine import Machine
from salvo import Salvo
import menu


# Game class
class NewGame(object):
    def __init__(self):
        self.rounds = 0
        self.players = []
        self.names = deepcopy(captains)
        self.totals = {
            "hits": 0,
            "sinks": 0,
            "eliminations": 0,
            "misses": 0
        }

    # Game start
    def start(self):
        print("\n%s New Game %s" % (offset() * '=',
                                    offset() * '='))
        # Initialize each Player(class)
        # Human players
        for human in range(sets["players"] - sets["ai"]):
            self.players.append(Human())
        # AI players
        for machine in range(sets["ai"]):
            self.players.append(Machine())
        # Randomize players list
        shuffle(self.players)
        for index, player in enumerate(self.players):
            player.index = index
            player.init_ships()
        # Loop through turns
        while True:
            self.rounds += 1
            if self.rounds < 10:
                off_right = 1
            else:
                off_right = 0
            print("\n%s Round %d %s\n" % (offset() * '=',
                                          self.rounds,
                                          (offset() + off_right) * '='))

            for player in self.players:
                if player.is_alive:
                    print("\n\n%s (Player %d) Turn\n\n" %
                          (player.name, player.index + 1))
                    self.move(player)

    # Control the flow of the player
    # TODO: Simplify
    def move(self, player, status="guess"):
        if not player.ai and status == "guess":
            print("Your board:\n")
            print(player.guesses[player])
        if status == "guess" or not player.target.is_alive:
            player.get_target()
        # Guess
        if status in ("guess", "hits") or sets["shots"] == 1:
            if status == "guess":
                guess = player.player_guess()
            # When status == "hits"
            else:
                guess = player.player_guess(True)
            if player.ai and sets["cheat"]:
                player.cheat(player.target, guess)
            # Check guess
            result = self.check(player, player.target, guess)
            # Register score
            player.score.add(result)
            # Print result
            self.print_result(player, player.target, result)
        # Salvo status is "sinks" or "eliminates" and sets["shots"] > 1
        else:
            if not player.ai:
                if sets["cheat"]:
                    print("\nTargets board:\n")
                    if sets["cheat"]:
                        player.print_ships(player.target)
                print(player.guesses[player.target])
            player.salvo = Salvo(player)
            player.salvo.get_shots()
            # Check salvo
            result = player.salvo.check_shots()
            player.salvo = None
        # Guess did not miss
        if result in ("hits", "eliminates", "sinks"):
            self.move(player, result)
        elif result == "win":
            self.endgame(player)

    # Checking system

    # Check guess
    @classmethod
    def check(cls, player, target, guess):
        for ship in target.ships:
            for position in ship.positions:
                if position["coord"] == guess:
                    return cls.hit(player, target, ship, position, guess)
        else:
            return cls.missed(player, target, guess)

    # Register the wrong guess in the guesses board
    @staticmethod
    def missed(player, target, guess):
        board = player.guesses[target].board
        board_player = target.guesses[target].board
        if board[guess[0]][guess[1]] == "X":
            return "already guessed"
        else:
            board[guess[0]][guess[1]] = "X"
            board_player[guess[0]][guess[1]] = "X"
            return "misses"

    # Hit a ship
    @classmethod
    def hit(cls, player, target, ship, position, guess):
        board = player.guesses[target].board
        board_player = target.guesses[target].board
        if board[guess[0]][guess[1]] == "F":
            board[guess[0]][guess[1]] = "H"
            board_player[guess[0]][guess[1]] = "H"
            if position["floating"]:
                position["floating"] = False
                ship.hits += 1
                if ship.hits == ship.size and \
                   not (sets["decoy"] and ship.name == "Decoy"):
                    result = cls.sink_ship(player, target, ship)
                    return result
            if player.ai:
                player.hits.append({"position": guess,
                                   "target": player.target})
            return "hits"
        else:
            return "already hit"

    # Ship sunken
    @classmethod
    def sink_ship(cls, player, target, ship):
        ship.floating = False
        cls.register_ship(player, target, ship)
        if player.ai and player.smart:
            player.smart = None
        player.target.ships_sunken += 1
        if player.target.ships_sunken == sets["ships"]:
            return cls.eliminate_player(player)
        else:
            player.ship = ship.name
            return "sinks"

    # Register the targets sunken ship in all players guesses board
    @staticmethod
    def register_ship(player, target, ship):
        for enemy in menu.game.players:
            player.init_boards(enemy, target)
            board = enemy.guesses[target].board
            for position in ship.positions:
                board[position["coord"][0]][position["coord"][1]] = "S"

    # Eliminate current target player, checks for endgame
    @classmethod
    def eliminate_player(cls, player):
        player.target.is_alive = False
        # All players but self is alive (Winner)
        if cls.is_endgame(player):
            return "win"
        else:
            return "eliminates"

    # Check if current player is the only one alive
    @staticmethod
    def is_endgame(player):
        for enemy in menu.game.players:
            if enemy != player and enemy.is_alive:
                return False
        else:
            return True

    # Print the result of the guess
    @staticmethod
    def print_result(player, target, result):
        # TODO: Consider using a GUI library
        print_player = "%s%s%s (Player %d)%s" %\
                       (sets["space"], Style.BRIGHT, player.name,
                        player.index + 1, Style.RESET_ALL)
        print_target = "%s%s (Player %d)%s" %\
                       (Style.BRIGHT, target.name, target.index + 1,
                        Style.RESET_ALL)
        if result in ("eliminates", "win"):
            print("%s sunken the last ship of %s!" %
                  (print_player, print_target))
            print("%s%s was %seliminated%s from the game.\n" %
                  (sets["space"], print_target, Fore.GREEN, Style.RESET_ALL))
            if result == "win":
                print("%s is the %swinner%s!!!\n" %
                      (print_player, Fore.GREEN, Style.RESET_ALL))
            elif sets["shots"] > 1:
                print("%s was awarded with a Salvo of %d shots.\n" %
                      (print_player, sets["shots"]))
        else:
            if result == "hits":
                print("%s %shits%s something in %s board.\n" %
                      (print_player, Fore.GREEN, Style.RESET_ALL, print_target))
            elif result == "already hit":
                print("%sPosition was already hit.\n"
                      % (sets["space"]))
            elif result == "already guessed":
                print("%s already guessed that position.\n" % print_player)
            elif result == "misses":
                print("%s %smissed%s the shot.\n" %
                      (print_player, Fore.RED, Style.RESET_ALL))
            elif result == "sinks":
                print("%s %ssunken%s a %s from %s." %
                      (print_player, Fore.GREEN, Style.RESET_ALL,
                       player.ship, print_target))
                print("%s have %d ships left.\n" %
                      (print_player, sets["ships"] - target.ships_sunken))
                if sets["shots"] > 1:
                    print("%s was awarded with a Salvo of %d shots.\n" %
                          (print_player, sets["shots"]))
                player.ship = None
        sleep(sets["timeout"])

    def game_statistics(self, best_player, winner):
        offset1 = 15
        offset2 = 35
        print("\n\n%s Game Statistics %s\n" % ((offset() - 2) * '=',
                                               (offset() - 1) * '='))
        print("%s%s (Player %d) has won the game in %d rounds!\n" %
              (sets["space"], winner.name, winner.index + 1, self.rounds))
        print("%sBests Scores\n" % sets["space"])
        for key, value in best_player.items():
            if key == "accuracy":
                percent = "%"
            else:
                percent = ""
            print("%s%s:%s%s (Player %d)%s(%d%s)" %
                  (sets["space"] * 2, key.capitalize(),
                   (" " * (offset1 - len(key))), value["player"].name,
                   value["player"].index + 1,
                   (" " * (offset2 - len(value["player"].name))),
                   value["score"], percent))
        print()

    # Game ends
    def endgame(self, winner):
        input("\n%sPress Enter to continue..." % sets["space"])
        clear_screen()
        best_player = {
            "hits": {"score": 0, "player": None},
            "accuracy": {"score": 0, "player": None},
            "sinks": {"score": 0, "player": None},
            "eliminations": {"score": 0, "player": None}
        }
        for player in self.players:
            player.score.evaluate_percentages()
            for key, value in best_player.items():
                if player.score.score[key] > best_player[key]["score"]:
                    best_player[key]["score"] = player.score.score[key]
                    best_player[key]["player"] = player
        self.game_statistics(best_player, winner)
        input("%sPress Enter to continue..." % sets["space"])
        if sets["scores"]:
            for player in self.players:
                print(player.score)
            input("%sPress Enter to continue..." % sets["space"])
        menu.menu()
