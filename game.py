from copy import deepcopy
from random import randint

from settings import settings as set
from functions import offset
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
        self.players = []
        self.names = deepcopy(captains)

    def start(self):
        print("\n%s New Game %s" % (offset() * '=',
                                    offset() * '='))

        # Initialize each Player(class)
        # Human players
        for player in range(set["players"] - set["ai"]):
            self.players.append(Human())
        # AI players
        for player in range(set["ai"]):
            self.players.append(Machine())

        # Randomize players list
        random_list = []
        while len(self.players) > 0:
            random_list.append(self.players.pop(randint(0, len(self.players)
                                                        - 1)))
        self.players = random_list

        # Loop trought turns
        while True:
            self.rounds += 1
            print("\n%s Round %d %s" % (offset() * '=',
                                        self.rounds,
                                        (offset() + 1) * '='))

            for index, player in enumerate(self.players):
                if player.is_alive:
                    print("%s(Player %s) Turn\n" % (player.name, index + 1))
                    player.get_target()
        return
