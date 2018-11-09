from colorama import Fore, Style
from settings import settings as set
from functions import input_num


from player import Player
import menu


class Human(Player):
    def __init__(self):
        Player.__init__(self)
        self.ai = False
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
            print("%s%s: %s%s" % (set["space"] * 2, name,
                                  " " * (12 - len(ship.name)), ship))
        print()

    def ask_name(self):
        self.name = input("\n%sChoose a name: " % (set["space"]))
        if not self.name:
            self.name = self.give_name()
            print("%sRandom name choosen: %s\n"
                  % (set["space"] * 2, self.name))

    # Print user readable board
    def print_board(self, target=False):
        if not target:
            target = self.target
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
        for row in self.guesses[target]:
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

    # Choose/determine the target
    def get_target(self):
        print("Your board:\n")
        self.print_board(self)
        targets = self.list_targets()
        if len(targets) == 1:
            self.target = targets[0]["player"]
        else:
            self.ask_target()
        self.init_boards(self)
        self.player_guess()
        return

    # Ask player to give a target
    def ask_target(self):
        print("%sPlayers:\n" % (set["space"]))
        for index, player in enumerate(menu.game.players):
            if player == self:
                player_color = Fore.CYAN
            elif not player.is_alive:
                player_color = Fore.RED
            else:
                player_color = Fore.GREEN

            print("%s%sPlayer %s: %s%s(%s Ships floating)%s"
                  % (set["space"] * 2, player_color, index + 1,
                     player.name, " " * (35 - len(player.name)),
                     set["ships"] - player.ships_sunked,
                     Style.RESET_ALL))
        print()
        while True:
            response_target = input_num("%sChoose a target by player number"
                                        % (set["space"]), 1, set["players"],
                                        "int")
            target = response_target - 1
            if menu.game.players[target] == self:
                print("%sCannot target yourself" % (set["space"] * 2))
            elif not menu.game.players[target].is_alive:
                print("%sCannot target a dead player" % (set["space"] * 2))
            else:
                self.target = menu.game.players[target]
                break

    # Ask player for a guess
    def player_guess(self):
        self.guess = []
        print("\nTargets board:\n")
        if set["cheat"]:
            print("%sEnemy Ships:" % (set["space"]))
            self.print_ships()
        self.print_board()
        return_key = "r"
        guessing = ("Row", "Col")
        for count, value in enumerate(guessing):
            answer = input_num("%sGuess %s   ('%s' to return)" % (set["space"],
                                                                  value,
                                                                  return_key),
                               1, set["board"][1 - count], "int", return_key)
            if answer:
                self.guess.append(answer)
            else:
                self.get_target()
                return
        print("Guess: %s" % self.guess)
        print()
        self.check()
