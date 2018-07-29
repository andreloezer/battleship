from random import randint
from time import sleep
from colorama import Fore, Style
from settings import settings as set
from functions import input_num
import menu
from ship import Ship


# Player class
class Player(object):
    def __init__(self, players, key, ai, names):
        self.is_alive = True
        self.names = names
        self.players = players
        self.key = key
        self.ai = ai
        self.ships = []
        self.ships_sunked = 0
        self.guesses = {}
        self.guess = []
        self.init_ships()

    # Initializes ships class
    def init_ships(self):
        self.get_name()
        if not (self.ai or set["randomize"]):
            print("\n%s%s position your ships:" % (set["space"], self.name))
        for ship in range(set["ships"]):
            self.ships.append(Ship(self, self.ships, "Ship "
                                   + str(ship + 1), set["size"]))

    def give_name(self):
        name = self.names[randint(0, len(self.names) - 1)]
        self.names.remove(name)
        return name

    def get_name(self):
        if self.ai:
            self.name = self.give_name()
        else:
            self.name = input("Player name: ")
            if not self.name:
                self.name = self.give_name()
                print("\n%sRandom name choosen: %s"
                      % (set["space"], self.name))

    # Print own ships
    def print_ships(self):
        ships = self.target.ships
        for ship in ships:
            if ship.floating:
                name = Fore.GREEN + ship.name + Style.RESET_ALL
            else:
                name = Fore.RED + ship.name + Style.RESET_ALL
            print("%s%s: %s" % (set["space"] * 2, name, ship))
        print()

    # Print user readable board
    def print_board(self):
        header = "%s     " % (set["space"])
        for col in range(set["board"][0]):
            if col >= 9:
                header = header + str(col + 1) + "  "
            else:
                header = header + str(col + 1) + "   "
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
                    print_row += Fore.RED + item + Style.RESET_ALL
                elif item == "H":
                    print_row += Fore.GREEN + item + Style.RESET_ALL
                elif item == "S":
                    print_row += Fore.WHITE + item + Style.RESET_ALL
                else:
                    print_row += Fore.BLUE + item + Style.RESET_ALL
                print_row += "   "
            print_row += "-%d" % (i)
            print(print_row)
            print()
            i += 1
        print(sub_header)
        print(header)
        print()

    # Initializes Guesses boards if don't exist
    def init_boards(self, player):
        try:
            player.guesses[self.target]
        except KeyError:
            player.guesses[self.target] = []
            for row in range(set["board"][1]):
                player.guesses[self.target].append(["O"]
                                                   * set["board"][0])

    # Check if current player is the only one alive
    def is_endgame(self):
        count = 0
        for player in self.players:
            if not self.players[player].is_alive:
                count += 1
        if count == len(self.players) - 1:
            return True
        else:
            return False

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

    # Choose/determine the target
    def get_target(self):
        targets = []
        for player in self.players.values():
            if player.is_alive:
                if player.name != self.name:
                    targets.append([player.key, player.name])
        if self.ai or len(targets) == 1:
            target = targets[randint(0, len(targets) - 1)][0]
            self.target = self.players[target]
        else:
            self.ask_target()
        print("\n%sTarget: %s %s (%s Ships floating)\n"
              % (set["space"], self.target.key, self.target.name,
                 set["ships"] - self.target.ships_sunked))

        self.init_boards(self)
        self.player_guess()
        return

    # Player guess
    def player_guess(self):
        if not self.ai:
            if set["cheat"]:
                print("%sEnemy Ships:" % (set["space"]))
                self.print_ships()
            self.print_board()
        if self.ai:
            self.guess = [randint(1, set["board"][1]),
                          randint(1, set["board"][0])]
            if set["cheat"]:
                print("%sAI Guess: %s\n" % (set["space"], self.guess))
        else:
            self.guess = [input_num("%sGuess Row   " % (set["space"]),
                                    1, set["board"][1], "int"),
                          input_num("%sGuess Column" % (set["space"]),
                                    1, set["board"][0], "int")]
            print()
        self.check()

    # Eliminate current target player, checks for endgame
    def eliminate_player(self):
        self.print_board()
        self.target.is_alive = False
        print("%s%s%s%s sunked the last ship of %s%s%s!" %
              (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
               Style.BRIGHT, self.target.name, Style.RESET_ALL))
        print("%s%s%s%s was %seliminated%s from the game.\n" %
              (set["space"], Style.BRIGHT, self.target.name, Style.RESET_ALL,
               Fore.GREEN, Style.RESET_ALL))
        # All players but self is alive (Winner)
        if self.is_endgame():
            print("%s%s%s%s is the %swinner%s!!!\n"
                  % (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
                     Fore.GREEN, Style.RESET_ALL))
            menu.menu()
        self.get_target()

# Register the targets sunked ship in all players guesses board
    def register_ship(self, ship):
        for player in self.players.values():
            self.init_boards(player)
            board = player.guesses[self.target]
            for position in ship.positions:
                board[position[1][0] - 1][position[1][1] - 1] = "S"

# Hit a ship
    def hit(self, ship, position):
        board = self.guesses[self.target]
        board[self.guess[0] - 1][self.guess[1] - 1] = "H"
        if position[0]:
            position[0] = False
            ship.hits += 1
            # Ship sunked
            if ship.hits == ship.size:
                self.register_ship(ship)
                self.print_board()
                ship.floating = False
                self.target.ships_sunked += 1
                if self.target.ships_sunked == set["ships"]:
                    self.eliminate_player()
                else:
                    print("%s%s%s%s %ssunked%s %s%s%s %s."
                          % (set["space"], Style.BRIGHT, self.name,
                             Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                             Style.BRIGHT, self.target.name, Style.RESET_ALL,
                             ship.name))
                    print("%s%s%s%s have %d ships left.\n"
                          % (set["space"], Style.BRIGHT, self.target.name,
                             Style.RESET_ALL, set["ships"]
                             - self.target.ships_sunked))
                    if self.ai:
                        sleep(set["timeout"])
                    self.get_target()
                    return
        print("%s%s%s%s %shitted%s %s%s%s %s.\n"
              % (set["space"], Style.BRIGHT, self.name,
                 Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                 Style.BRIGHT, self.target.name, Style.RESET_ALL,
                 ship.name))
        if self.ai:
            sleep(set["timeout"])
        self.player_guess()
        return

    # Register the wrong guess in the guesses board
    def missed(self):
        board = self.guesses[self.target]
        if (board[self.guess[0] - 1][self.guess[1] - 1] == "X"):
            if self.ai:
                self.player_guess()
            else:
                print("%s%s already guessed that position\n"
                      % (set["space"], self.name))
        else:
            board[self.guess[0] - 1][self.guess[1] - 1] = "X"
            print("%s%s%s%s %smissed%s the shot.\n"
                  % (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
                     Fore.RED, Style.RESET_ALL))

    # Check guess
    def check(self):
        board = self.guesses[self.target]
        for ship in self.target.ships:
            for position in ship.positions:
                if position[1] == [self.guess[0], self.guess[1]]:
                    if board[self.guess[0] - 1][self.guess[1] - 1] == "O":
                        # Position is floating
                        self.hit(ship, position)
                    else:
                        print("%sPosition was already hitted\n"
                              % (set["space"]))
                        return
                    return
        else:
            self.missed()
        if self.ai:
            sleep(set["timeout"])
        else:
            self.print_board()
