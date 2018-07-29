
from random import randint
from colorama import Fore
from settings import settings as set
from functions import input_num


# Ship Class
class Ship(object):
    def __init__(self, player, ships, name, size=1, direction="random"):
        self.floating = True
        self.size = size
        self.direction = direction
        self.player = player
        self.ships = ships
        self.name = name
        self.hits = 0
        self.positions = []
        self.create_ship()

    def gen_direction(self):
        if self.size == 1:
            return None
        else:
            if self.direction == "random":
                return ["horizontal", "vertical"][randint(0, 1)]
            else:
                return self.direction

    def __str__(self):
        string = ""
        for position in self.positions:
            if position[0]:
                string += Fore.GREEN + str(position[1])
            else:
                string += Fore.RED + str(position[1])
        return string

    def gen_ship(self, hor, ver):
        positions = []
        if self.direction is None:
            position = [hor, ver]
        for point in range(self.size):
            if self.direction == "horizontal":
                position = [hor, ver + point + 1]
            elif self.direction == "vertical":
                position = [hor + point + 1, ver]
            if self.validate(position):
                positions.append([True, position])
            else:
                return False
        else:
            return positions

    # Create ship with size bigger than 1
    def create_ship(self):
        while True:
            if set["randomize"] or self.player.ai:
                if self.direction in (None, "random"):
                    self.direction = self.gen_direction()
                if self.direction == "horizontal":
                    hor = randint(1, set["board"][1])
                    ver = randint(1, set["board"][0] - self.size - 1)
                elif self.direction == "vertical":
                    hor = randint(1, set["board"][1] - self.size - 1)
                    ver = randint(1, set["board"][0])
                else:
                    hor = randint(1, set["board"][1])
                    ver = randint(1, set["board"][0])
                ship = self.gen_ship(hor, ver)
            else:
                if self.size == 1:
                    ship = self.ask_position()
                else:
                    ship = self.ask_position_length()
            if ship:
                self.positions = ship
                break

    # Check if ship is still floating
    def is_floating(self):
        if self.hits == self.size:
            self.floating = False
            return False

    # Create position
    def random_position(self):
        row = randint(1, set["board"][1])
        col = randint(1, set["board"][0])
        return [row, col]

    def ask_direction(self):
        while True:
            direction = input("%sChoose the direction" % (set["space"])
                              + "(horizontal, vertical, random): "
                              ).lower()
            if direction in ("h", "horizontal"):
                return "horizontal"
            elif direction in ("v", "vertical"):
                return "vertical"
            elif direction in ("r", "random"):
                self.direction = "random"
                return self.gen_direction()
            else:
                print("%sEnter a valid direction" % (set["space"]))

    def ask_position_length(self):
        print("\n%s%s (lenght: %d)" % (set["space"], self.name, self.size))
        self.direction = self.ask_direction()
        print("%s%s direction: %s"
              % (set["space"] * 2, self.name, self.direction))
        if self.direction == "horizontal":
            hor = input_num("%sChoose row" % (set["space"]),
                            1, set["board"][1], "int")
            ver = input_num("%sChoose starting column" % (set["space"]),
                            1, set["board"][0] - self.size, "int") - 1
        elif self.direction == "vertical":
            ver = input_num("%sChoose col" % (set["space"]),
                            1, set["board"][0], "int")
            hor = input_num("%sChoose starting row" % (set["space"]),
                            1, set["board"][1] - self.size, "int") - 1
        ship = self.create_ship(hor, ver)
        return ship

    # Player chooses the ship position
    def ask_position(self):
        print("\n%s%s:" % (set["space"], self.name))
        row = input_num("%sChoose %s row"
                        % (set["space"], self.name),
                        1, set["board"][1], "int")
        col = input_num("%sChoose %s column"
                        % (set["space"], self.name),
                        1, set["board"][0], "int")
        position = [row, col]
        if self.validate(position):
            return [[True, position]]
        else:
            return False

    # Check if position doesn't conflict with other ships
    def validate(self, position):
        row = position[0]
        col = position[1]
        for ship in self.ships:
            for ship_position in ship.positions:
                if ship_position[1] == [row, col]:
                    if not (set["randomize"] or self.player.ai):
                        print("\n%sPosition already occupied"
                              % (set["space"] * 2))
                    return False
                elif ship_position[1] in [[row - 1, col],
                                          [row + 1, col],
                                          [row, col - 1],
                                          [row, col + 1]]:
                    if not (set["randomize"] or self.player.ai):
                        print("\n%sToo close to another ship"
                              % (set["space"] * 2))
                    return False
        else:
            return True
