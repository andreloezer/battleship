from random import randint

from settings import settings as set
from player import Player
from smart import Smart_Guessing


class Machine(Player):
    def __init__(self):
        Player.__init__(self)
        self.ai = True
        self.choose_ship = False
        self.name = self.give_name()
        self.init_ships()
        self.smart = set["smart"]
        self.smart_guess = None

    # Choose/determine the target
    def get_target(self):
        if len(self.hits) == 0:
            targets = self.list_targets()
            self.target = targets[randint(0, len(targets) - 1)]["player"]
        self.init_boards(self)

    # Validate guess position
    def is_position_valid(self, position, direction=None):
        board = self.guesses[self.target]
        col = range(1, set["board"][1] + 1)
        row = range(1, set["board"][0] + 1)
        if position[0] in col and position[1] in row:
            # Position in board
            if board[position[0] - 1][position[1] - 1] == "O":
                return True
            elif board[position[0] - 1][position[1] - 1] == "X":
                # Remove direction
                return False
        else:
            # Position not in board
            self.directions[direction] = False

    # Random guess
    def random_guess(self):
        return [randint(1, set["board"][1]),
                randint(1, set["board"][0])]

    def still_floating(self, hit):
        board = self.guesses[self.target]
        if board[hit[0] - 1][hit[1] - 1] == "S":
            return False
        else:
            return True

    # Player guess
    def player_guess(self, hitted=False):
        guess = []
        # Smart Guessing ship still floating
        if self.smart_guess and self.still_floating(self.smart_guess.hits[0]):
            # Smart Guessing guess hitted
            if hitted and self.hits[-1]["target"] == self.smart_guess.target:
                self.smart_guess.hits.append(self.hits.pop()["position"])
            guess = self.smart_guess.shoot()
        # No Smart Guessing
        else:
            while len(self.hits) > 0:
                hit = self.hits.pop()
                if self.still_floating(hit["position"]):
                    self.smart_guess = Smart_Guessing(self, hit)
                    guess = self.smart_guess.shoot()
                    break
            else:
                self.smart_guess = None
                guess = self.get_guess()
        if not guess:
            self.smart_guess = None
            guess = self.player_guess()
        return guess

    # Random guess
    def get_guess(self):
        while True:
            guess = self.random_guess()
            if self.is_position_valid(guess):
                return guess

    # Display guessing info of the AI
    def cheat(self, guess):
        print("%sAI Target: %s" % (set["space"], self.target.name))
        print("%sAI Guess: %s\n" % (set["space"], guess))
