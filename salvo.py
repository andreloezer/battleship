
from settings import settings as set


class Salvo(object):
    def __init__(self, player):
        self.player = player
        self.positions = []
        self.hits = []
        self.sink = False
        if self.player.ai or not self.player.target.is_alive:
            self.player.get_target()

    # Get/ask the guesses for the salvo
    def get_shots(self):
        for position in range(set["shots"]):
            while True:
                if not self.player.ai:
                    print("\n%sGuess shot %i" % (set["space"], position + 1))
                answer = self.player.get_guess()
                if answer:
                    if answer not in self.positions:
                        self.positions.append(answer)
                        break
                    elif not self.player.ai:
                        print("\n%sYou can't guess the same spot"
                              % set["space"])
                else:
                    self.positions = []
                    self.player.get_target()
                    self.player.print_board()
                    self.get_shots()
                    return

    # Check each guess
    def check_shots(self):
        index = 1
        while len(self.positions) > 0:
            guess = self.positions.pop(0)
            print("\n%sShot %i" % (set["space"], index))
            index += 1
            if set["cheat"]:
                print("%s%s Shot: %s" % (set["space"], self.player.name,
                                         guess))
            result = self.player.check(guess)
            self.player.print_result(result)
            if result == "hit":
                self.hits.append(guess)
            if result == "sink":
                self.hits.append(guess)
                self.sink = True
            if result == "win":
                return "win"
        else:
            if self.sink:
                return "sink"
            elif len(self.hits) > 0:
                return "hit"
            else:
                return "miss"
