

from settings import settings as sets
import menu


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
        for position in range(sets["shots"]):
            while True:
                if not self.player.ai:
                    print("\n%sGuess shot %i" % (sets["space"], position + 1))
                answer = self.player.get_guess()
                if answer:
                    if answer not in self.positions:
                        self.positions.append(answer)
                        break
                    elif not self.player.ai:
                        print("\n%sYou can't guess the same spot"
                              % sets["space"])
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
            print("\n%sShot %i" % (sets["space"], index))
            index += 1
            if sets["cheat"]:
                print("%s%s Shot: %s" % (sets["space"], self.player.name,
                                         guess))
            result = menu.game.check(self.player, guess)
            # Register score
            self.player.score.add(result)
            menu.game.print_result(self.player, result)
            if result == "hits":
                self.hits.append(guess)
            if result == "sinks":
                self.hits.append(guess)
                self.sink = True
            if result == "win":
                return "win"
        else:
            if self.sink:
                return "sinks"
            elif len(self.hits) > 0:
                return "hits"
            else:
                return "misses"
