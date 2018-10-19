from colorama import Fore, Style
from settings import settings as set
from functions import input_num


from player import Player


class Human(Player):
    def __init__(self, players, key, names):
        Player.__init__(self, players, key, names)
        self.ai = False
        print("\n\n%s" % (self.key))
        self.ask_name()
        if set["randomize"]:
            self.choose_ship = False
        else:
            if str(input("%sChoose ships positions? "
                         % (set["space"]))) in ("y", "yes"):
                self.choose_ship = True
                print("\n%s%s position your ships:"
                      % (set["space"], self.name))
            else:
                self.choose_ship = False
        self.init_ships()

    # Print own ships
    def print_ships(self):
        ships = self.target.ships
        for ship in ships:
            if ship.floating:
                color = Fore.GREEN
            else:
                color = Fore.RED
            name = color + ship.name + Style.RESET_ALL
            print("%s%s: %s" % (set["space"] * 2, name, ship))
        print()

    def ask_name(self):
        self.name = input("\n%sChoose a name: " % (set["space"]))
        if not self.name:
            self.name = self.give_name()
            print("%sRandom name choosen: %s\n"
                  % (set["space"] * 2, self.name))

    # Print user readable board
    def print_board(self):
        header = "%s     " % (set["space"])
        for col in range(set["board"][0]):
            if col >= 9:
                space = "  "
            else:
                space = "   "
            header += str(col + 1) + space
            i = 1
        print(header)
        sub_header = "%s     |%s" % (set["space"],
                                     "   |" * (set["board"][0] - 1))
        print(sub_header)
        print()
        for row in self.guesses[self.target]:
            if i >= 10:
                print_row = "%s%d-  " % (set["space"], i)
            else:
                print_row = "%s %d-  " % (set["space"], i)
            for item in row:
                if item == "X":
                    color = Fore.RED
                elif item == "H":
                    color = Fore.GREEN
                elif item == "S":
                    color = Fore.CYAN
                else:
                    color = Fore.BLUE
                print_row += color + item + Style.RESET_ALL + "   "
            print_row += "-%d" % (i)
            print(print_row)
            print()
            i += 1
        print(sub_header)
        print(header)
        print()

    # Ask player to give a target
    def ask_target(self):
        print("%sPlayers:\n" % (set["space"]))
        for player in self.players.values():
            if player.key == self.key:
                player_color = Fore.CYAN
            elif not player.is_alive:
                player_color = Fore.RED
            else:
                player_color = Fore.GREEN

            print("%s%s%s: %s%s(%s Ships floating)%s"
                  % (set["space"] * 2, player_color, player.key,
                     player.name, " " * (35 - len(player.name)),
                     set["ships"] - player.ships_sunked,
                     Style.RESET_ALL))
        print()
        while True:
            response_target = input_num("%sChoose a target by player number"
                                        % (set["space"]), 1, set["players"],
                                        "int")
            target = "Player " + str(response_target)
            if target == self.key:
                print("%sCannot target yourself" % (set["space"] * 2))
            elif not self.players[target].is_alive:
                print("%sCannot target a dead player" % (set["space"] * 2))
            else:
                self.target = self.players[target]
                break

    # Ask player for a guess
    def player_guess(self):
        if set["cheat"]:
            print("%sEnemy Ships:" % (set["space"]))
            self.print_ships()
        self.print_board()
        self.guess = [input_num("%sGuess Row   " % (set["space"]),
                                1, set["board"][1], "int"),
                      input_num("%sGuess Column" % (set["space"]),
                                1, set["board"][0], "int")]
        print()
        self.check()
