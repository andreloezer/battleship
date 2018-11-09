from random import randint
from time import sleep
from colorama import Fore, Style
from settings import settings as set, types
import menu
from ship import Ship


# Player class
class Player(object):
    def __init__(self):
        self.is_alive = True
        self.ships = []
        self.ships_sunked = 0
        self.target = None
        self.guesses = {}
        self.guess = []
        self.init_boards(self, self)

    # Initializes ships class
    def init_ships(self):
        for type in types:
            for ship in range(type["quantity"]):
                self.ships.append(Ship(self, type["type"],
                                       type["size"]))

    def give_name(self):
        name = menu.game.names[randint(0, len(menu.game.names) - 1)]
        menu.game.names.remove(name)
        return name

    # Initializes Guesses boards if don't exist
    def init_boards(self, player, target=False):
        if not target:
            target = self.target
        try:
            player.guesses[target]
        except KeyError:
            player.guesses[target] = []
            for row in range(set["board"][1]):
                player.guesses[target].append(["O"]
                                              * set["board"][0])

    # Check if current player is the only one alive
    def is_endgame(self):
        for player in menu.game.players:
            if player != self:
                if player.is_alive:
                    return False
        else:
            return True

    # List valid targets
    def list_targets(self):
        targets = []
        for player in menu.game.players:
            if player.is_alive:
                if player != self:
                    targets.append({"player": player, "type": player.name})
        return targets

    # Eliminate current target player, checks for endgame
    def eliminate_player(self):
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
        for player in menu.game.players:

            self.init_boards(player)
            board = player.guesses[self.target]
            for position in ship.positions:
                board[position["coord"][0] - 1][position["coord"][1] - 1] = "S"

            if self.ai and self.target == player.target and player.hitted:
                for ship_position in ship.positions:
                    if player.hitted[0] == ship_position["coord"]:
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
        if not self.ai:
            self.print_board()

    # Ship sunked
    def sink_ship(self, ship):
        self.register_ship(ship)
        ship.floating = False
        self.target.ships_sunked += 1
        if self.target.ships_sunked == set["ships"]:
            self.eliminate_player()
        else:
            print("%s%s%s%s %ssunked%s a %s from %s%s%s."
                  % (set["space"], Style.BRIGHT, self.name,
                     Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                     ship.name, Style.BRIGHT, self.target.name,
                     Style.RESET_ALL))
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
        if self.ai and set["cheat"]:
            self.cheat()
        board = self.guesses[self.target]
        board_player = self.target.guesses[self.target]
        if board[self.guess[0] - 1][self.guess[1] - 1] == "O":
            board[self.guess[0] - 1][self.guess[1] - 1] = "H"
            board_player[self.guess[0] - 1][self.guess[1] - 1] = "H"
            if position["floating"]:
                position["floating"] = False
                ship.hits += 1
                if ship.hits == ship.size and \
                   not (set["decoy"] and ship.name == "Decoy"):
                    self.sink_ship(ship)
                    return
            if not self.ai:
                self.print_board()
            print("%s%s%s%s %shitted%s something in %s%s%s board.\n"
                  % (set["space"], Style.BRIGHT, self.name,
                     Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                     Style.BRIGHT, self.target.name, Style.RESET_ALL))
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
        board_player = self.target.guesses[self.target]
        if (board[self.guess[0] - 1][self.guess[1] - 1] == "X"):
            if self.ai:
                self.player_guess()
            else:
                self.print_board()
                print("%s%s already guessed that position\n"
                      % (set["space"], self.name))
                return
        else:
            if self.ai and set["cheat"]:
                self.cheat()
            board[self.guess[0] - 1][self.guess[1] - 1] = "X"
            board_player[self.guess[0] - 1][self.guess[1] - 1] = "X"
            if not self.ai:
                self.print_board()
            print("%s%s%s%s %smissed%s the shot.\n"
                  % (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
                     Fore.RED, Style.RESET_ALL))
            return

    # Check guess
    def check(self):
        for ship in self.target.ships:
            for position in ship.positions:
                if position["coord"] == self.guess:
                    self.hit(ship, position)
                    return
        else:
            self.missed()
