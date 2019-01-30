

from random import randint


from colorama import Fore, Style


from settings import settings as sets, types
import menu
from ship import Ship
from score import Score


# Player class
class Player(object):
    def __init__(self):
        self.is_alive = True
        self.ships = []
        self.ships_sunken = 0
        self.target = None
        self.guesses = {}
        self.salvo = None
        self.hits = []
        self.ship = None
        self.index = None
        self.name = None
        self.score = Score(self)
        self.init_boards(self, self)

    # Print own ships
    def print_ships(self):
        print("%sEnemy Ships:" % (sets["space"]))
        ships = self.target.ships
        for ship in ships:
            if ship.floating:
                color = Fore.GREEN
            else:
                color = Fore.RED
            name = color + ship.name + Style.RESET_ALL
            print("%s%s: %s%s" % (sets["space"] * 2, name,
                                  " " * (12 - len(ship.name)), ship))
        print()

    # Initializes ships class
    def init_ships(self):
        for ship_type in types:
            for ship in range(ship_type["quantity"]):
                self.ships.append(Ship(self, ship_type["ship_type"],
                                       ship_type["size"]))

    # Randomize a name
    @staticmethod
    def give_name():
        name = menu.game.names[randint(0, len(menu.game.names) - 1)]
        menu.game.names.remove(name)
        return name

    # Initializes Guesses boards if don't exist
    def init_boards(self, player, target=None):
        if not target:
            target = self.target
        try:
            player.guesses[target]
        except KeyError:
            player.guesses[target] = []
            for row in range(sets["board"][1]):
                player.guesses[target].append(["O"]
                                              * sets["board"][0])

    # List valid targets
    def list_targets(self):
        targets = []
        for player in menu.game.players:
            if player.is_alive:
                if player != self:
                    targets.append({"player": player,
                                    "ship_type": player.name})
        return targets
