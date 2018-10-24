from random import randint
from time import sleep

from settings import settings as set
from player import Player


class Machine(Player):
    def __init__(self):
        Player.__init__(self)
        self.ai = True
        self.choose_ship = False
        self.hitted = []
        self.try_guess = []
        self.name = self.give_name()
        self.init_ships()
        self.direction = None
        self.target = None
        self.directions = {
            "up": True,
            "down": True,
            "right": True,
            "left": True
        }
        self.smart = set["smart"]

    # Choose/determine the target
    def get_target(self):
        if len(self.hitted) > 0:
            self.player_guess()
            return
        else:
            targets = self.list_targets()
            self.target = targets[randint(0, len(targets) - 1)]["player"]
        self.init_boards(self)
        self.player_guess()
        return

    # Validate guess position
    def is_position_valid(self, position, direction):
        board = self.guesses[self.target]
        col = range(1, set["board"][1] + 1)
        row = range(1, set["board"][0] + 1)
        if position[0] in col and position[1] in row:
            # Position in board
            if board[position[0] - 1][position[1] - 1] == "O":
                self.try_guess.append([position, direction])
            elif board[position[0] - 1][position[1] - 1] == "X":
                # Remove direction
                self.directions[direction] = False
        else:
            # Position not in board
            self.directions[direction] = False

    # Generate guess position
    def next_guesses(self):
        self.try_guess = []
        i = 0
        while len(self.try_guess) == 0:
            i += 1
            if self.directions["up"]:
                position = [self.guess[0] - i,
                            self.guess[1]]
                self.is_position_valid(position, "up")

            if self.directions["down"]:
                position = [self.guess[0] + i,
                            self.guess[1]]
                self.is_position_valid(position, "down")

            if self.directions["left"]:
                position = [self.guess[0],
                            self.guess[1] - i]
                self.is_position_valid(position, "left")

            if self.directions["right"]:
                position = [self.guess[0],
                            self.guess[1] + i]
                self.is_position_valid(position, "right")

    # Player guess
    def player_guess(self):
        sleep(set["timeout"])
        if self.smart and self.guess in self.hitted:
            # Determine the direction of the ship
            if len(self.hitted) > 1:
                # horizontal
                if self.hitted[0][1] - self.hitted[1][1] != 0:
                    self.directions["up"] = False
                    self.directions["down"] = False
                # vertical
                elif self.hitted[0][0] - self.hitted[1][0] != 0:
                    self.directions["right"] = False
                    self.directions["left"] = False
            self.next_guesses()
        if self.smart and len(self.hitted) > 0:
            if len(self.try_guess) == 0:
                self.next_guesses()
            guess = self.try_guess.pop(randint(0,
                                               len(self.try_guess) - 1))
            self.direction = guess[1]
            self.guess = guess[0]
        else:
            # Random guess
            self.guess = [randint(1, set["board"][1]),
                          randint(1, set["board"][0])]
        if set["cheat"]:
            print("%sAI Target: %s" % (set["space"], self.target.name))
            print("%sAI Guess: %s\n" % (set["space"], self.guess))
        sleep(set["timeout"])
        self.check()
