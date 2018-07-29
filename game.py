from copy import deepcopy

from settings import settings as set
from player import Player


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
    global players
    rounds = 0
    players = {}
    print("\n======= New Game =======\n")

    names = deepcopy(captains)

    # Initialize each Player(class)
    # Human players
    for player in range(set["players"] - set["ai"]):
        key = "Player %s" % (player + 1)
        players[key] = Player(players, key, False, names)
    # AI players
    for player in range(set["ai"]):
        key = ("Player %s"
               % (player + 1 + (set["players"] - set["ai"])))
        players[key] = Player(players, key, True, names)

    # Loop trought turns
    while True:
        rounds += 1
        print("\n******** Round %d ********\n" % (rounds))

        for player in players:

            if players[player].is_alive is True:
                print("%s Turn\n" % player)
                players[player].get_target()

    return
