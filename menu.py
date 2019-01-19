from sys import exit
from math import floor
from colorama import Fore, Back, Style
from settings import settings as set, default as dv, interval as inr, types
from functions import input_num, offset
from game import NewGame


game = None


# Main menu
def menu():
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
    global set
    if set["cheat"]:
        debug_color = Fore.GREEN
    else:
        debug_color = Fore.RED
    if set["randomize"]:
        randomize_color = Fore.GREEN
    else:
        randomize_color = Fore.RED
    if set["smart"]:
        smart_color = Fore.GREEN
    else:
        smart_color = Fore.RED
    if set["decoy"]:
        decoy_color = Fore.GREEN
    else:
        decoy_color = Fore.RED
    set["ships"] = 0
    for ship_type in types:
        if ship_type["type"] != "Decoy" or not set["decoy"]:
            set["ships"] += ship_type["quantity"]
        if ship_type["type"] == "Decoy":
            if set["decoy"]:
                if ship_type["quantity"] == 0:
                    decoys = " and a decoy"
                elif ship_type["quantity"] > 1:
                    decoys = " and %d decoys" % ship_type["quantity"]
                else:
                    decoys = ""
            else:
                decoys = ""
    print("%s %sOptions%s %s" % (offset() * '=',
                                 Back.BLUE,
                                 Style.RESET_ALL,
                                 offset() * '='))

    print("\nThere are %d ships%s:" % (set["ships"], decoys))
    for ship_type in types:
        if ship_type["quantity"] > 1:
            plural = "s"
        else:
            plural = ""
        if ship_type["quantity"] > 0:
            print("%s%s %s%s with size of %s" % (set["space"],
                                                 ship_type["quantity"],
                                                 ship_type["type"],
                                                 plural,
                                                 ship_type["size"]))
    print("\nChange Ships (s)")
    print("Board Size (b)          Current: (%d, %d)"
          % (set["board"][0], set["board"][1]))
    print("Number of Players (p)   Current: %d" % (set["players"]))
    print("AI Players (a)          Current: %d" % (set["ai"]))
    print("Salvo shots (ss)        Current: %d" % (set["shots"]))
    print("AI Pause Time (t)       Current: %ss" % (set["timeout"]))
    print("AI Smart Guessing (sg)  Current: %s%s%s"
          % (smart_color, set["smart"], Style.RESET_ALL))
    print("Ignore Decoys (ig)      Current: %s%s%s"
          % (decoy_color, set["decoy"], Style.RESET_ALL))
    print("Cheat (c)               Current: %s%s%s"
          % (debug_color, set["cheat"], Style.RESET_ALL))
    print("Randomize Ships (r)     Current: %s%s%s"
          % (randomize_color, set["randomize"], Style.RESET_ALL))
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
        set["board"][0] = input_num("Choose the width of the board",
                                    inr["board"][0](set["ships"]),
                                    inr["board"][1],
                                    "int")
        set["board"][1] = input_num("Choose the height of the board",
                                    inr["board"][0](set["ships"]),
                                    inr["board"][1],
                                    "int")
        options()
        return
    elif answer in ("p",
                    "players",
                    "number of players",
                    "number_of_players",
                    "numberofplayers"):
        set["players"] = input_num("Choose the number of players",
                                   inr["players"][0],
                                   inr["players"][1],
                                   "int")
        if set["ai"] > set["players"] - 1:
            set["ai"] = set["players"] - 1
            print("AI players reduced to %d." % (set["ai"]))
        options()
        return
    elif answer in ("c",
                    "cheat"):
        set["cheat"] = not set["cheat"]
        print("Cheat: %s" % (set["cheat"]))
        print()
        options()
        return
    elif answer in ("sg",
                    "smart",
                    "ai smart",
                    "smart guessing",
                    "ai smart guessing"):
        set["smart"] = not set["smart"]
        print("Smart Guessing: %s" % (set["smart"]))
        print()
        options()
        return
    elif answer in ("s",
                    "cs",
                    "ships",
                    "choose ships"):
        for type in types:
            type["quantity"] = input_num("Choose the quantity of %s (Size: %s)"
                                         % (type["type"], type["size"]),
                                         inr[type["type"]][0],
                                         inr[type["type"]][1], "int")
            if type["type"] != "Decoy":
                set["ships"] += type["quantity"]
        board = int(floor(set["ships"] * 1.5))
        set["board"] = [board, board]
        print("\nThe board size has been adjusted to %s" % set["board"])
        print()
        options()
    elif answer in ("ig",
                    "decoy",
                    "ignore",
                    "ignore decoy"):
        set["decoy"] = not set["decoy"]
        print("Ignore Decoys: %s" % (set["decoy"]))
        print()
        options()
        return
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
        set = dv.copy()

        options()
        return
    elif answer in ("r",
                    "randomize",
                    "randomize ships",
                    "randomize_ships",
                    "randomizeships"):
        set["randomize"] = not set["randomize"]
        print("Randomize Ships: %s" % (set["randomize"]))
        print()
        options()
        return
    elif answer in ("a",
                    "ai",
                    "ai players",
                    "ai_players",
                    "aiplayers"):
        set["ai"] = input_num("Choose the number of AI players",
                              inr["ai"][0],
                              inr["ai"][1](set["players"]),
                              "int")
        options()
        return
    elif answer in ("ss",
                    "salvo",
                    "shots",
                    "salvo shots",
                    "salvo_shots"):
        set["shots"] = input_num("Choose the number of shots during a Salvo",
                                 inr["shots"][0],
                                 inr["shots"][1],
                                 "int")
        options()
        return
    elif answer in ("t",
                    "pause",
                    "time",
                    "pause time",
                    "pause_time",
                    "pausetime"):
        set["timeout"] = input_num("Choose a pause time in"
                                   + " seconds for AI action",
                                   inr["timeout"][0],
                                   inr["timeout"][1],
                                   "float")
        options()
        return
    elif answer in ("m",
                    "menu",
                    "return"):
        menu()
    else:
        print("Enter a valid answer!")
        options()
        return
