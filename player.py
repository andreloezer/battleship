from random import randint
from time import sleep
from colorama import Fore, Style
from settings import settings as set
import menu
from ship import Ship


# Player class
class Player(object):
    def __init__(self):
        self.is_alive = True
        self.ships = []
        self.ships_sunked = 0
        self.guesses = {}
        self.guess = []

    # Initializes ships class
    def init_ships(self):
        for ship in range(set["ships"]):
            self.ships.append(Ship(self, self.ships, "Ship "
                                   + str(ship + 1), set["size"]))

    def give_name(self):
        name = menu.game.names[randint(0, len(menu.game.names) - 1)]
        menu.game.names.remove(name)
        return name

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
        for player in menu.game.players.values():
            if player != self:
                if player.is_alive:
                    return False
        else:
            return True

    # Choose/determine the target
    def get_target(self):
        if self.ai and len(self.hitted) > 0:
            self.player_guess()
            return
        else:
            targets = []
            for player in menu.game.players.values():
                if player.is_alive:
                    if player != self:
                        targets.append([player, player.name])
            if self.ai or len(targets) == 1:
                target = targets[randint(0, len(targets) - 1)][0]
                self.target = target

            else:
                self.ask_target()
            self.init_boards(self)
            self.player_guess()
            return

    # Eliminate current target player, checks for endgame
    def eliminate_player(self):
        if not self.ai:
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
        for player in menu.game.players.values():

            self.init_boards(player)
            board = player.guesses[self.target]
            for position in ship.positions:
                board[position[1][0] - 1][position[1][1] - 1] = "S"
            if self.ai and self.target == player.target and player.hitted:
                for ship_position in ship.positions:
                    if player.hitted[0] == ship_position[1]:
                        player.try_guess = []
                        player.hitted = []
                        player.directions = {
                            "up": True,
                            "down": True,
                            "right": True,
                            "left": True
                        }
                        player.direction = None
                        break

    # Ship sunked
    def sink_ship(self, ship):
        self.register_ship(ship)
        if not self.ai:
            self.print_board()
        ship.floating = False
        self.target.ships_sunked += 1
        if self.target.ships_sunked == set["ships"]:
            self.eliminate_player()
        else:
            print("%s%s%s%s %ssunked%s %s%s%s %s."
                  % (set["space"], Style.BRIGHT, self.name,
                     Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                     Style.BRIGHT, self.target.name,
                     Style.RESET_ALL, ship.name))
            print("%s%s%s%s have %d ships left.\n"
                  % (set["space"], Style.BRIGHT, self.target.name,
                     Style.RESET_ALL, set["ships"]
                     - self.target.ships_sunked))
            if self.ai:
                sleep(set["timeout"])
            self.get_target()
            return

    # Hit a ship
    def hit(self, ship, position):
        board = self.guesses[self.target]
        if board[self.guess[0] - 1][self.guess[1] - 1] == "O":
            board[self.guess[0] - 1][self.guess[1] - 1] = "H"
            if position[0]:
                position[0] = False
                ship.hits += 1
                if ship.hits == ship.size:
                    self.sink_ship(ship)
                    return
            print("%s%s%s%s %shitted%s %s%s%s %s.\n"
                  % (set["space"], Style.BRIGHT, self.name,
                     Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                     Style.BRIGHT, self.target.name, Style.RESET_ALL,
                     ship.name))
            if self.ai:
                self.hitted.append(self.guess)
            self.player_guess()
            return
        else:
            print("%sPosition was already hitted\n"
                  % (set["space"]))
            return

    # Register the wrong guess in the guesses board
    def missed(self):
        if self.ai and self.direction:
            self.directions[self.direction] = False
        board = self.guesses[self.target]
        if (board[self.guess[0] - 1][self.guess[1] - 1] == "X"):
            if self.ai:
                self.player_guess()
            else:
                print("%s%s already guessed that position\n"
                      % (set["space"], self.name))
                return
        else:
            board[self.guess[0] - 1][self.guess[1] - 1] = "X"
            print("%s%s%s%s %smissed%s the shot.\n"
                  % (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
                     Fore.RED, Style.RESET_ALL))
            return

    # Check guess
    def check(self):
        for ship in self.target.ships:
            for position in ship.positions:
                if position[1] == self.guess:
                    self.hit(ship, position)
                    return
        else:
            self.missed()
