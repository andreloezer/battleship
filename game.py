

from copy import deepcopy
from random import randint
from time import sleep


from colorama import Fore, Style


from settings import settings as set, captains
from functions import offset
from human import Human
from machine import Machine
from salvo import Salvo
import menu


# Game class
class NewGame(object):
    def __init__(self):
        self.rounds = 0
        self.players = []
        self.names = deepcopy(captains)
        self.totals = {
            "hits": 0,
            "sinks": 0,
            "eliminations": 0,
            "misses": 0
        }

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
        index = 0
        while len(self.players) > 0:
            player = self.players.pop(randint(0, len(self.players) - 1))
            player.index = index
            random_list.append(player)
            index += 1
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

            for player in self.players:
                if player.is_alive:
                    print("\n\nPlayer %d (%s) Turn\n\n" %
                          (player.index + 1, player.name))
                    self.move(player)

    # Control the flow of the player
    def move(self, player, status="guess"):
        if not player.ai and status == "guess":
            player.print_board(player)
        if status == "guess" or not player.target.is_alive:
            player.get_target()
        # Guess
        if status in ("guess", "hits") or set["shots"] <= 1:
            if not player.ai:
                player.print_board()
            if status == "guess":
                guess = player.player_guess()
            elif status == "hits" or set["shots"] <= 1:
                guess = player.player_guess(True)
            if player.ai and set["cheat"]:
                player.cheat(guess)
            # Check guess
            result = self.check(player, guess)
            # Register score
            player.score.add(result)
            # Print result
            self.print_result(player, result)
        # Salvo
        elif status in ("sinks", "eliminates") and set["shots"] > 1:
            if not player.ai:
                player.print_board()
            player.salvo = Salvo(player)
            player.salvo.get_shots()
            # Check salvo
            result = player.salvo.check_shots()
            player.salvo = None
        # Guess did not miss
        if result in ("hits", "eliminates", "sinks"):
            self.move(player, result)
        elif result == "win":
            self.endgame()

    # Checking system

    # Check guess
    def check(self, player, guess):
        for ship in player.target.ships:
            for position in ship.positions:
                if position["coord"] == guess:
                    return self.hit(player, ship, position, guess)
        else:
            return self.missed(player, guess)

    # Register the wrong guess in the guesses board
    def missed(self, player, guess):
        board = player.guesses[player.target]
        board_player = player.target.guesses[player.target]
        if (board[guess[0] - 1][guess[1] - 1] == "X"):
            if not player.ai:
                return "already guessed"
        else:
            board[guess[0] - 1][guess[1] - 1] = "X"
            board_player[guess[0] - 1][guess[1] - 1] = "X"
            return "misses"

    # Hit a ship
    def hit(self, player, ship, position, guess):
        board = player.guesses[player.target]
        board_player = player.target.guesses[player.target]
        if board[guess[0] - 1][guess[1] - 1] == "O":
            board[guess[0] - 1][guess[1] - 1] = "H"
            board_player[guess[0] - 1][guess[1] - 1] = "H"
            if position["floating"]:
                position["floating"] = False
                ship.hits += 1
                if ship.hits == ship.size and \
                   not (set["decoy"] and ship.name == "Decoy"):
                    result = self.sink_ship(player, ship)
                    return result
            if player.ai:
                player.hits.append({"position": guess,
                                   "target": player.target})
            return "hits"
        else:
            return "already hitted"

    # Ship sunked
    def sink_ship(self, player, ship):
        ship.floating = False
        self.register_ship(player, ship)
        if player.ai and player.smart_guess:
            player.smart_guess = None
        player.target.ships_sunked += 1
        if player.target.ships_sunked == set["ships"]:
            return self.eliminate_player(player)
        else:
            player.ship = ship.name
            return "sinks"

    # Register the targets sunked ship in all players guesses board
    def register_ship(self, player, ship):
        for enemy in menu.game.players:
            player.init_boards(enemy)
            board = enemy.guesses[player.target]
            for position in ship.positions:
                board[position["coord"][0] - 1][position["coord"][1] - 1] = "S"

    # Eliminate current target player, checks for endgame
    def eliminate_player(self, player):
        player.target.is_alive = False
        # All players but self is alive (Winner)
        if self.is_endgame(player):
            return "win"
        else:
            return "eliminates"

    # Check if current player is the only one alive
    def is_endgame(self, player):
        for enemy in menu.game.players:
            if enemy != player:
                if enemy.is_alive:
                    return False
        else:
            return True

    # Print the result of the guess
    def print_result(self, player, result):
        if result in ("eliminates", "win"):
            print("%s%s%s%s sunked the last ship of %s%s%s!" %
                  (set["space"], Style.BRIGHT, player.name, Style.RESET_ALL,
                   Style.BRIGHT, player.target.name, Style.RESET_ALL))
            print("%s%s%s%s was %seliminated%s from the game.\n" %
                  (set["space"], Style.BRIGHT, player.target.name,
                   Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
            if result == "win":
                print("%s%s%s%s is the %swinner%s!!!\n"
                      % (set["space"], Style.BRIGHT, player.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
            elif set["shots"] > 1:
                print("%s%s%s%s was awarded with a Salvo of %i shots\n"
                      % (set["space"], Style.BRIGHT, player.name,
                         Style.RESET_ALL, set["shots"]))
        else:
            if result == "hits":
                print("%s%s%s%s %shitted%s something in %s%s%s board.\n"
                      % (set["space"], Style.BRIGHT, player.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                         Style.BRIGHT, player.target.name, Style.RESET_ALL))
            elif result == "already hitted":
                print("%sPosition was already hitted\n"
                      % (set["space"]))
            elif result == "already guessed":
                print("%s%s already guessed that position\n"
                      % (set["space"], player.name))
            elif result == "misses":
                print("%s%s%s%s %smissed%s the shot.\n"
                      % (set["space"], Style.BRIGHT, player.name,
                         Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
            elif result == "sinks":
                print("%s%s%s%s %ssunked%s a %s from %s%s%s."
                      % (set["space"], Style.BRIGHT, player.name,
                         Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL,
                         player.ship, Style.BRIGHT, player.target.name,
                         Style.RESET_ALL))
                print("%s%s%s%s have %d ships left.\n"
                      % (set["space"], Style.BRIGHT, player.target.name,
                         Style.RESET_ALL, set["ships"]
                         - player.target.ships_sunked))
                if set["shots"] > 1:
                    print("%s%s%s%s was awarded with a Salvo of %i shots\n"
                          % (set["space"], Style.BRIGHT, player.name,
                             Style.RESET_ALL, set["shots"]))
                player.ship = None
        sleep(set["timeout"])

    def print_score(self, best_player):
        offset1 = 15
        offset2 = 25
        print("%sBests Scores\n" % set["space"])
        for key, value in best_player.items():
            if key == "accuracy":
                percent = "%"
            else:
                percent = ""
            print("%s%s:%sPlayer %s (%s)%s(%d%s)" %
                  (set["space"] * 2, key.capitalize(),
                   (" " * (offset1 - len(key))), value["player"].index + 1,
                   value["player"].name,
                   (" " * (offset2 - len(value["player"].name))),
                   value["score"], percent))
        print()

    # Game ends
    def endgame(self):
        print("\n\n%s Players Scores %s\n" % ((offset() - 2) * '=',
                                              (offset() - 2) * '='))
        best_player = {
            "hits": {"score": 0, "player": None},
            "accuracy": {"score": 0, "player": None},
            "sinks": {"score": 0, "player": None},
            "eliminations": {"score": 0, "player": None}
        }
        for player in self.players:
            player.score.evaluate_percentages()
            for key, value in best_player.items():
                if player.score.score[key] > best_player[key]["score"]:
                    best_player[key]["score"] = player.score.score[key]
                    best_player[key]["player"] = player
        self.print_score(best_player)
        input("%sPress Enter to continue..." % set["space"])
        if set["scores"]:
            for player in self.players:
                print("\n%sPlayer %d (%s)\n" %
                      (set["space"], player.index + 1, player.name))
                player.score.print_score()
            input("%sPress Enter to continue..." % set["space"])
        menu.menu()
