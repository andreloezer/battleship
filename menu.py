from sys import exit
from colorama import Fore, Back, Style
from settings import settings as set, default as dv, interval as inr
from functions import input_num
from game import NewGame


game = None


# Starting screen with some options
def menu():
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
    print("\n========================")
    print("====== %sBattleship%s ======" % (Back.BLUE, Style.RESET_ALL))
    print("========================\n")
    print("New Game (g)")
    print("Board Size (b)          Current: (%d, %d)"
          % (set["board"][0], set["board"][1]))
    print("Number of Players (p)   Current: %d" % (set["players"]))
    print("Number of Ships (ns)    Current: %d" % (set["ships"]))
    print("Ship Size (ss)          Current: %d" % (set["size"]))
    print("Cheat (c)               Current: %s%s%s"
          % (debug_color, set["cheat"], Style.RESET_ALL))
    print("Randomize Ships (r)     Current: %s%s%s"
          % (randomize_color, set["randomize"], Style.RESET_ALL))
    print("AI Players (a)          Current: %d" % (set["ai"]))
    print("AI Pause Time (t)       Current: %ss" % (set["timeout"]))
    print("AI Smart Guessing (sg)  Current: %s%s%s"
          % (smart_color, set["smart"], Style.RESET_ALL))
    print("Restore Default (d)")
    print("Exit/Quit (e/q)\n")

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
                                    inr["board"][0],
                                    inr["board"][1],
                                    "int")
        set["board"][1] = input_num("Choose the height of the board",
                                    inr["board"][0],
                                    inr["board"][1],
                                    "int")
        max_ships = inr["ships"][1](set["board"])
        if set["ships"] > max_ships:
            set["ships"] = int(max_ships)
            print("The number of ships was reduced to the new maximum: %d"
                  % (max_ships))
        menu()
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
        menu()
        return
    elif answer in ("c",
                    "cheat"):
        set["cheat"] = not set["cheat"]
        print("Cheat: %s" % (set["cheat"]))
        print()
        menu()
        return
    elif answer in ("sg",
                    "smart",
                    "ai smart",
                    "smart guessing",
                    "ai smart guessing"):
        set["smart"] = not set["smart"]
        print("smart: %s" % (set["smart"]))
        print()
        menu()
        return
    elif answer in ("e",
                    "exit",
                    "q",
                    "quit"):
        print("Exit game\n")
        exit()
    elif answer in ("ns",
                    "number of ships",
                    "number_of_ships",
                    "numberofships"):
        if int(inr["ships"][1](set["board"])) == 1:
            set["ships"] = 1
            print("At the current board size (%d, %d)"
                  + "there can be only one ship.\n"
                  % (set["board"][0], set["board"][1]))
        else:
            set["ships"] = input_num("Choose the number of ships",
                                     inr["ships"][0],
                                     inr["ships"][1](set["board"]),
                                     "int")
        menu()
        return
    elif answer in ("ss",
                    "ship size",
                    "ship_size",
                    "shipsize"):
        set["size"] = input_num("Choose the size of the ships",
                                inr["size"][0],
                                inr["size"][1],
                                "int")
        menu()
        return
    elif answer in ("d",
                    "restore",
                    "default",
                    "restore default",
                    "restore_default",
                    "restoredefault"):
        set = dv.copy()

        menu()
        return
    elif answer in ("r",
                    "randomize",
                    "randomize ships",
                    "randomize_ships",
                    "randomizeships"):
        set["randomize"] = not set["randomize"]
        print("Randomize Ships: %s" % (set["randomize"]))
        print()
        menu()
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
        menu()
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
        menu()
        return
    else:
        print("Enter a valid answer!")
        menu()
        return
