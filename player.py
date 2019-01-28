from random import randint

from colorama import Fore, Style

from settings import settings as set, types
import menu
from ship import Ship
from score import Score


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
        self.ship = None
        self.index = None
        self.score = Score(self)
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

    # List valid targets
    def list_targets(self):
        targets = []
        for player in menu.game.players:
            if player.is_alive:
                if player != self:
                    targets.append({"player": player, "type": player.name})
        return targets
