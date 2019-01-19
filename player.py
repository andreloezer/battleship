from random import randint
from time import sleep

from colorama import Fore, Style

from settings import settings as set, types
import menu
from ship import Ship
from salvo import Salvo


# Player class
class Player(object):
    def __init__(self):
        self.is_alive = True
        self.ships = []
        self.ships_sunked = 0
        self.target = None
        self.guesses = {}
        self.salvo = None
        self.hits = []
        self.init_boards(self, self)

    # Print own ships
    def print_ships(self):
        print("%sEnemy Ships:" % (set["space"]))
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

    # Initializes ships class
    def init_ships(self):
        for type in types:
            for ship in range(type["quantity"]):
                self.ships.append(Ship(self, type["type"],
                                       type["size"]))

    # Randomize a name
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

    # Control the flow of the player
    def move(self, status):
        if not self.ai and status == "guess":
            self.print_board(self)
        if status == "guess" or not self.target.is_alive:
            self.get_target()
        if status in ("guess", "hit"):
            if not self.ai:
                self.print_board()
            if status == "guess":
                guess = self.player_guess()
            elif status == "hit" or (status == "shots" and set["shots"] <= 1):
                guess = self.player_guess(True)
            if self.ai and set["cheat"]:
                self.cheat(guess)
            result = self.check(guess)
            if not self.ai and not self.salvo and status not in ("hit",
                                                                 "sink",
                                                                 "eliminate",
                                                                 "guess"):
                self.print_board()
            self.print_result(result)
        elif status in ("sink", "eliminate") and set["shots"] > 1:
            if not self.ai:
                self.print_board()
            self.salvo = Salvo(self)
            self.salvo.get_shots()
            result = self.salvo.check_shots()
            self.salvo = None
            if result in ("hit", "eliminate", "sink"):
                self.move(result)
            return

        if result in ("hit", "eliminate", "sink"):
            self.move(result)
        elif result == "win":
            menu.menu()

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
        # All players but self is alive (Winner)
        if self.is_endgame():
            return "win"
        else:
            return "eliminate"

    # Register the targets sunked ship in all players guesses board
    def register_ship(self, ship):
        for player in menu.game.players:
            self.init_boards(player)
            board = player.guesses[self.target]
            for position in ship.positions:
                board[position["coord"][0] - 1][position["coord"][1] - 1] = "S"

    # Ship sunked
    def sink_ship(self, ship):
        self.register_ship(ship)
        ship.floating = False
        self.target.ships_sunked += 1
        if self.target.ships_sunked == set["ships"]:
            return self.eliminate_player()
        else:
            self.ship = ship.name
            return "sink"

    # Hit a ship
    def hit(self, ship, position, guess):
        board = self.guesses[self.target]
        board_player = self.target.guesses[self.target]
        if board[guess[0] - 1][guess[1] - 1] == "O":
            board[guess[0] - 1][guess[1] - 1] = "H"
            board_player[guess[0] - 1][guess[1] - 1] = "H"
            if position["floating"]:
                position["floating"] = False
                ship.hits += 1
                if ship.hits == ship.size and \
                   not (set["decoy"] and ship.name == "Decoy"):
                    result = self.sink_ship(ship)
                    return result
            if self.ai:
                self.hits.append({"position": guess,
                                 "target": self.target})
            return "hit"
        else:
            return "already hitted"

    # Register the wrong guess in the guesses board
    def missed(self, guess):
        board = self.guesses[self.target]
        board_player = self.target.guesses[self.target]
        if (board[guess[0] - 1][guess[1] - 1] == "X"):
            if not self.ai:
                return "already guessed"
        else:
            board[guess[0] - 1][guess[1] - 1] = "X"
            board_player[guess[0] - 1][guess[1] - 1] = "X"
            return "miss"

    # Check guess
    def check(self, guess):
        for ship in self.target.ships:
            for position in ship.positions:
                if position["coord"] == guess:
                    return self.hit(ship, position, guess)
        else:
            return self.missed(guess)

    # Print the result of the guess
    def print_result(self, result):
        if result in ("eliminate", "win"):
            print("%s%s%s%s sunked the last ship of %s%s%s!" %
                  (set["space"], Style.BRIGHT, self.name, Style.RESET_ALL,
                   Style.BRIGHT, self.target.name, Style.RESET_ALL))
            print("%s%s%s%s was %seliminated%s from the game.\n" %
                  (set["space"], Style.BRIGHT, self.target.name,
                   Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
            if result == "win":
                print("%s%s%s%s is the %swinner%s!!!\n"
                      % (set["space"], Style.BRIGHT, self.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
            else:
                print("%s%s%s%s was awarded with a Salvo of %i shots\n"
                      % (set["space"], Style.BRIGHT, self.name,
                         Style.RESET_ALL, set["shots"]))
        else:
            if result == "hit":
                print("%s%s%s%s %shitted%s something in %s%s%s board.\n"
                      % (set["space"], Style.BRIGHT, self.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                         Style.BRIGHT, self.target.name, Style.RESET_ALL))
            elif result == "already hitted":
                print("%sPosition was already hitted\n"
                      % (set["space"]))
            elif result == "already guessed":
                print("%s%s already guessed that position\n"
                      % (set["space"], self.name))
            elif result == "miss":
                print("%s%s%s%s %smissed%s the shot.\n"
                      % (set["space"], Style.BRIGHT, self.name,
                         Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
            elif result == "sink":
                print("%s%s%s%s %ssunked%s a %s from %s%s%s."
                      % (set["space"], Style.BRIGHT, self.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                         self.ship, Style.BRIGHT, self.target.name,
                         Style.RESET_ALL))
                print("%s%s%s%s have %d ships left.\n"
                      % (set["space"], Style.BRIGHT, self.target.name,
                         Style.RESET_ALL, set["ships"]
                         - self.target.ships_sunked))
                if set["shots"] > 1:
                    print("%s%s%s%s was awarded with a Salvo of %i shots\n"
                          % (set["space"], Style.BRIGHT, self.name,
                             Style.RESET_ALL, set["shots"]))
                self.ship = None
        sleep(set["timeout"])
