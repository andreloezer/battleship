
from copy import deepcopy
from random import randint


from settings import settings as set
from functions import offset
from human import Human
from machine import Machine
import menu


# Captains names
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


# Game class
class NewGame(object):
    def __init__(self):
        self.rounds = 0
        self.players = []
        self.names = deepcopy(captains)

    # Game start
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
            if self.rounds < 10:
                off_right = 1
            else:
                off_right = 0
            print("\n%s Round %d %s\n" % (offset() * '=',
                                          self.rounds,
                                          (offset() + off_right) * '='))

            for index, player in enumerate(self.players):
                if player.is_alive:
                    print("\n\nPlayer %d (%s) Turn\n\n" %
                          (index + 1, player.name))
                    player.move("guess")

    # Game ends
    def endgame(self):
        print("\n\n%s Players Scores %s\n" % ((offset() - 2) * '=',
                                              (offset() - 2) * '='))
        for index, player in enumerate(self.players):
            print("\nPlayer %d (%s)\n" % (index + 1, player.name))
            player.score.print_score()
        input("%sPress Enter to continue..." % set["space"])
        menu.menu()
