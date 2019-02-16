

"""

    File:       menu.py
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


from sys import exit
from math import floor
from time import sleep


from colorama import Fore, Back, Style


from settings import settings, default as dv, interval as inr, types
from functions import input_num, offset, clear_screen
from game import NewGame


sets = settings


game = None


# Main menu
def menu():
    clear_screen()
    print("\n\n%s" % ((offset() + 5) * '=' * 2))
    print("%s %sBattleship%s %s" % ((offset() - 1) * '=',
                                    Back.BLUE,
                                    Style.RESET_ALL,
                                    (offset() - 1) * '='))
    print("%s\n" % ((offset() + 5) * '=' * 2))

    print("New Game (g)")
    print("Options (o)")
    print("Exit/Quit (e/q)\n")

    answer = input("What's your choice? ").lower()
    print()

    if answer in ("g",
                  "game",
                  "new game",
                  "new_game",
                  "newgame"):

        global game
        game = NewGame()
        game.start()
        return
    elif answer in ("a",
                    "o",
                    "ao",
                    "advanced",
                    "options",
                    "advanced options"):
        options()
    elif answer in ("e",
                    "exit",
                    "q",
                    "quit"):
        print("Exit game\n")
        exit()
    else:
        print("Enter a valid answer!")
        menu()
        return


# Starting screen with some options
def options():
    clear_screen()
    global sets
    # Colors for boolean settings
    colors = {}
    for key, value in sets.items():
        if str(value) in ("True", "False"):
            if value:
                colors[key] = Fore.GREEN
            else:
                colors[key] = Fore.RED
    # Calculate valid ships
    sets["ships"] = 0
    decoys = ""
    for ship_type in types:
        if ship_type["ship_type"] != "Decoy" or not sets["decoy"]:
            sets["ships"] += ship_type["quantity"]
        if ship_type["ship_type"] == "Decoy":
            if sets["decoy"]:
                if ship_type["quantity"] == 1:
                    decoys = " and a decoy"
                elif ship_type["quantity"] > 1:
                    decoys = " and %d decoys" % ship_type["quantity"]
    print("\n\n%s %sOptions%s %s" % (offset() * '=',
                                     Back.BLUE,
                                     Style.RESET_ALL,
                                     (offset() + 1) * '='))

    print("\nThere are %d ships%s:" % (sets["ships"], decoys))
    for ship_type in types:
        if ship_type["quantity"] > 1:
            plural = "s"
        else:
            plural = ""
        if ship_type["quantity"] > 0:
            print("%s%s %s%s with size of %d" % (sets["space"],
                                                 ship_type["quantity"],
                                                 ship_type["ship_type"],
                                                 plural,
                                                 ship_type["size"]))
    print("\nChange Ships (s)")
    print("Board Size (b)          Current: (%d, %d)"
          % (sets["board"][0], sets["board"][1]))
    print("Number of Players (p)   Current: %d" % (sets["players"]))
    print("AI Players (a)          Current: %d" % (sets["ai"]))
    print("Salvo shots (ss)        Current: %d" % (sets["shots"]))
    print("AI Pause Time (t)       Current: %4.2fs" % (sets["timeout"]))
    print("AI Smart Guessing (sg)  Current: %s%s%s"
          % (colors["smart"], sets["smart"], Style.RESET_ALL))
    print("Ignore Decoys (ig)      Current: %s%s%s"
          % (colors["decoy"], sets["decoy"], Style.RESET_ALL))
    print("Cheat (c)               Current: %s%s%s"
          % (colors["cheat"], sets["cheat"], Style.RESET_ALL))
    print("Randomize Ships (r)     Current: %s%s%s"
          % (colors["randomize"], sets["randomize"], Style.RESET_ALL))
    print("Players Scores (sc)     Current: %s%s%s"
          % (colors["scores"], sets["scores"], Style.RESET_ALL))
    print("Restore Default (d)")
    print("Back to menu (m)")
    print()

    answer = input("What's your choice? ").lower()
    print()

    # Player choice
    if answer in ("g",
                  "game",
                  "new game",
                  "new_game",
                  "newgame"):

        global game
        game = NewGame()
        game.start()
        return
    elif answer in ("b",
                    "size",
                    "board size",
                    "board_size",
                    "boardsize"):
        sets["board"][0] = input_num("Choose the width of the board",
                                     inr["board"][0](sets["ships"]),
                                     inr["board"][1],
                                     "int")
        sets["board"][1] = input_num("Choose the height of the board",
                                     inr["board"][0](sets["ships"]),
                                     inr["board"][1],
                                     "int")
    elif answer in ("p",
                    "players",
                    "number of players",
                    "number_of_players",
                    "numberofplayers"):
        sets["players"] = input_num("Choose the number of players",
                                    inr["players"][0],
                                    inr["players"][1],
                                    "int")
        if sets["ai"] > sets["players"] - 1:
            sets["ai"] = sets["players"] - 1
            print("AI players reduced to %d." % (sets["ai"]))
    elif answer in ("c",
                    "cheat"):
        sets["cheat"] = not sets["cheat"]
        print("Cheat: %s" % (sets["cheat"]))
    elif answer in ("sg",
                    "smart",
                    "ai smart",
                    "smart guessing",
                    "ai smart guessing"):
        sets["smart"] = not sets["smart"]
        print("Smart Guessing: %s" % (sets["smart"]))
    elif answer in ("s",
                    "cs",
                    "ships",
                    "choose ships"):
        for ship in types:
            ship["quantity"] = input_num("Choose the quantity of %s(Size: %d)"
                                         % (ship["ship_type"], ship["size"]),
                                         inr[ship["ship_type"]][0],
                                         inr[ship["ship_type"]][1], "int")
            if ship["ship_type"] != "Decoy":
                sets["ships"] += ship["quantity"]
        board = int(floor(sets["ships"] * 1.15))
        sets["board"] = [board, board]
        print("\nThe board size has been adjusted to (%d, %d)" %
              (sets["board"][0], sets["board"][1]))
    elif answer in ("ig",
                    "decoy",
                    "ignore",
                    "ignore decoy"):
        sets["decoy"] = not sets["decoy"]
        print("Ignore Decoys: %s" % (sets["decoy"]))
    elif answer in ("e",
                    "exit",
                    "q",
                    "quit"):
        print("Exit game\n")
        exit()
    elif answer in ("d",
                    "restore",
                    "default",
                    "restore default",
                    "restore_default",
                    "restoredefault"):
        sets = dv.copy()
    elif answer in ("r",
                    "randomize",
                    "randomize ships",
                    "randomize_ships",
                    "randomizeships"):
        sets["randomize"] = not sets["randomize"]
        print("Randomize Ships: %s" % (sets["randomize"]))
    elif answer in ("sc",
                    "scores"):
        sets["scores"] = not sets["scores"]
        print("Players Scores: %s" % (sets["scores"]))
    elif answer in ("a",
                    "ai",
                    "ai players",
                    "ai_players",
                    "aiplayers"):
        sets["ai"] = input_num("Choose the number of AI players",
                               inr["ai"][0],
                               inr["ai"][1](sets["players"]),
                               "int")
    elif answer in ("ss",
                    "salvo",
                    "shots",
                    "salvo shots",
                    "salvo_shots"):
        sets["shots"] = input_num("Choose the number of shots during a Salvo",
                                  inr["shots"][0],
                                  inr["shots"][1],
                                  "int")
    elif answer in ("t",
                    "pause",
                    "time",
                    "pause time",
                    "pause_time",
                    "pausetime"):
        sets["timeout"] = input_num("Choose a pause time in"
                                    + " seconds for AI action",
                                    inr["timeout"][0],
                                    inr["timeout"][1],
                                    "float")
    elif answer in ("m",
                    "menu",
                    "return"):
        menu()
    else:
        print("Enter a valid answer!")
    sleep(sets["timeout"] * 2)
    options()
    return
