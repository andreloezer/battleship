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


# Each game
def game():
    rounds = 0
    players = {}
    print("\n======= New Game =======")

    names = deepcopy(captains)

    # Initialize each Player(class)
    # Human players
    for player in range(set["players"] - set["ai"]):
        key = "Player %s" % (player + 1)
        players[key] = Human(players, key, names)
    # AI players
    for player in range(set["ai"]):
        key = ("Player %s"
               % (player + 1 + (set["players"] - set["ai"])))
        players[key] = Machine(players, key, names)

    # Loop trought turns
    while True:
        rounds += 1
        print("\n******** Round %d ********\n" % (rounds))

        for player in players:

            if players[player].is_alive is True:
                print("%s(%s) Turn\n" % (players[player].name, player))
                players[player].get_target()

    return
