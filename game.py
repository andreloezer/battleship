from copy import deepcopy

from settings import settings as set
from human import Human
from machine import Machine


captains = ["Captain Jack Sparrow",
            "Captain James T. Kirk",
            "Captain Ahab",
            "Admiral Ackbar",
            "Captain Hendrick van der Decken",
            "Admiral Motti",
            "Captain Haddock",
            "Captain Davy Jones",
            "Captain Hook",
            "Captain Han Solo",
            "Admiral General Aladeen"]


class NewGame(object):
    def __init__(self):
        self.rounds = 0
        self.players = {}
        self.names = deepcopy(captains)

    def start(self):
        print("\n======= New Game =======")

        # Initialize each Player(class)
        # Human players
        for player in range(set["players"] - set["ai"]):
            key = "Player %s" % (player + 1)
            self.players[key] = Human()
        # AI players
        for player in range(set["ai"]):
            key = ("Player %s" % (player + 1 + (set["players"] - set["ai"])))
            self.players[key] = Machine()

        # Loop trought turns
        while True:
            self.rounds += 1
            print("\n******** Round %d ********\n" % (self.rounds))

            for key, player in self.players.items():
                if player.is_alive:
                    print("%s(%s) Turn\n" % (player.name, key))
                    player.get_target()
        return
