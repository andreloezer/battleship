

from random import randint
from settings import settings as sets


# Guessing around a hit
class SmartGuessing(object):
    def __init__(self, player, target, start):
        self.player = player
        self.target = target
        self.hits = [start["position"]]
        self.try_shot = []
        self.directions = {
            "up": True,
            "down": True,
            "right": True,
            "left": True
        }
        self.try_shot = self.next_shots()

    # Get guess
    def shoot(self):
        # Determine the direction of the ship
        if len(self.hits) > 1:
            if self.hits[0][1] - self.hits[1][1] != 0:
                # horizontal
                self.directions["up"] = False
                self.directions["down"] = False
            elif self.hits[0][0] - self.hits[1][0] != 0:
                # vertical
                self.directions["right"] = False
                self.directions["left"] = False
        self.try_shot = self.next_shots()
        if self.try_shot:
            return self.random_shot()
        else:
            return False

    # Randomize shot from list of guesses
    def random_shot(self):
        guess = self.try_shot.pop(randint(0,
                                          len(self.try_shot) - 1))
        return guess[0]

    # Validate possible guess
    def is_guess_valid(self, guess, direction):
        board = self.player.guesses[self.target]
        col = range(1, sets["board"][1] + 1)
        row = range(1, sets["board"][0] + 1)
        if guess[0] in col and guess[1] in row:
            # Guess in board
            if board[guess[0] - 1][guess[1] - 1] == "O":
                return True
            elif board[guess[0] - 1][guess[1] - 1] == "X":
                # Remove direction
                self.directions[direction] = False
                return False
            elif board[guess[0] - 1][guess[1] - 1] == "H":
                if guess not in self.hits:
                    self.hits.append(guess)
                return False
            else:
                return False
        else:
            # Position not in board
            self.directions[direction] = False

    # Create possible guesses for each direction
    def next_shots(self):
        shots = []
        for hit in self.hits:
            if self.directions["up"]:
                guess = [hit[0] - 1,
                         hit[1]]
                if self.is_guess_valid(guess, "up"):
                    shots.append([guess, "up"])

            if self.directions["down"]:
                guess = [hit[0] + 1,
                         hit[1]]
                if self.is_guess_valid(guess, "down"):
                    shots.append([guess, "down"])

            if self.directions["left"]:
                guess = [hit[0],
                         hit[1] - 1]
                if self.is_guess_valid(guess, "left"):
                    shots.append([guess, "left"])

            if self.directions["right"]:
                guess = [hit[0],
                         hit[1] + 1]
                if self.is_guess_valid(guess, "right"):
                    shots.append([guess, "right"])
        # It's a decoy
        if not (self.directions["up"] or
                self.directions["down"] or
                self.directions["left"] or
                self.directions["right"]):
            return False
        else:
            return shots
