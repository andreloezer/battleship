"""

   A battleship game from Codecademy's Python lesson 19/19

"""


from random import randint
from time import sleep
# https://pypi.org/project/colorama/
from colorama import init, Fore, Back, Style
import os

# Enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607
os.system('')

init(autoreset=True)

# Default settings
default = {
    "board_size": [12, 12],
    "debug": True,
    "number_of_ships": 4,
    "number_of_players": 8,
    "randomize_ships": True,
    "ai_players": 7,
    "timeout": 1,
    "ship_size": 3
  }

# User settings
board_size = default["board_size"]
debug = default["debug"]
number_of_ships = default["number_of_ships"]
number_of_players = default["number_of_players"]
ai_players = default["ai_players"]
randomize_ships = default["randomize_ships"]
timeout = default["timeout"]
ship_size = default["ship_size"]
players = {}
space = "  "

# Settings values interval
board_interval = [3, 15]
ships_interval = [1, lambda size: ((size[0] + size[1]) / 2) * 0.6]
players_interval = [2, 8]
ai_interval = [0, lambda ai: ai - 1]
time_interval = [0, 5000]
size_interval = [1, 5]


# Print user readable board
def print_board(board):
    header = "%s     " % (space)
    for col in range(board_size[0]):
        if col >= 9:
            header = header + str(col + 1) + "  "
        else:
            header = header + str(col + 1) + "   "
        i = 1
    print(header)
    sub_header = "%s     |%s" % (space, "   |" * (board_size[0] - 1))
    print(sub_header)
    print()
    for row in board:
        if i >= 10:
            print_row = "%s%d-  " % (space, i)
        else:
            print_row = "%s %d-  " % (space, i)
        for item in row:
            if item == "X":
                print_row += Fore.RED + item + Style.RESET_ALL
            elif item == "S":
                print_row += Fore.GREEN + item + Style.RESET_ALL
            else:
                print_row += Fore.BLUE + item + Style.RESET_ALL
            print_row += "   "
        print_row += "-%d" % (i)
        print(print_row)
        print()
        i += 1
    print(sub_header)
    print(header)
    print()


# User input and validation
def input_integer(message, min_value, max_value):
    while True:
        try:
            user_input = int(input("%s (%d to %d): " % (message,
                                                        min_value,
                                                        max_value)))
        except ValueError:
            print("%sEnter a whole number (integer)." % (space))
            continue
        if user_input < min_value or user_input > max_value:
            print("%sThe number must be between %d and %d." % (space,
                                                               min_value,
                                                               max_value))
            continue
        else:
            return user_input
            break


# Initializes Guesses boards if don't exist
def initialize_guesses_boards(player, target):
    try:
        player.guesses_boards[target]
    except KeyError:
        player.guesses_boards[target] = []
        for row in range(board_size[1]):
            player.guesses_boards[target].append(["O"] * board_size[0])


# Check if current player is the only one alive
def is_endgame(players):
    count = 0
    for player in players:
        if not players[player].is_alive:
            count += 1
    if count == len(players) - 1:
        return True
    else:
        return False


# AI players pause
def pause(ai):
    if ai:
        sleep(timeout / 1000)


# Ship Class
class Ship(object):
    def __init__(self, player, ships, name, size=1, direction="random"):
        self.floating = True
        self.size = size
        self.direction = direction
        self.player = player
        self.ships = ships
        self.name = name
        self.hits = 0
        self.positions = []
        self.create_ship()

    def gen_direction(self):
        if self.size == 1:
            return None
        else:
            if self.direction == "random":
                return ["horizontal", "vertical"][randint(0, 1)]
            else:
                return self.direction

    def __str__(self):
        string = ""
        for position in self.positions:
            if position[0]:
                string += Fore.GREEN + str(position[1])
            else:
                string += Fore.RED + str(position[1])
        return string

    def gen_ship(self, hor, ver):
        positions = []
        if self.direction is None:
            position = [hor, ver]
        for point in range(self.size):
            if self.direction == "horizontal":
                position = [hor, ver + point + 1]
            elif self.direction == "vertical":
                position = [hor + point + 1, ver]
            if self.validate(position):
                positions.append([True, position])
            else:
                return False
        else:
            return positions

    # Create ship with size bigger than 1
    def create_ship(self):
        while True:
            if randomize_ships or self.player.ai:
                if self.direction in (None, "random"):
                    self.direction = self.gen_direction()
                if self.direction == "horizontal":
                    hor = randint(1, board_size[1])
                    ver = randint(1, board_size[0] - self.size - 1)
                elif self.direction == "vertical":
                    hor = randint(1, board_size[1] - self.size - 1)
                    ver = randint(1, board_size[0])
                else:
                    hor = randint(1, board_size[1])
                    ver = randint(1, board_size[0])
                ship = self.gen_ship(hor, ver)
            else:
                if self.size == 1:
                    ship = self.ask_position()
                else:
                    ship = self.ask_position_length()
            if ship:
                self.positions = ship
                break

    # Check if ship is still floating
    def is_floating(self):
        if self.hits == self.size:
            self.floating = False
            return False

    # Create position
    def random_position(self):
        row = randint(1, board_size[1])
        col = randint(1, board_size[0])
        return [row, col]

    def ask_direction(self):
        while True:
            direction = input("%sChoose the direction" % (space)
                              + "(horizontal, vertical, random): "
                              ).lower()
            if direction in ("h", "horizontal"):
                return "horizontal"
            elif direction in ("v", "vertical"):
                return "vertical"
            elif direction in ("r", "random"):
                self.direction = "random"
                return self.gen_direction()
            else:
                print("%sEnter a valid direction" % (space))

    def ask_position_length(self):
        print("\n%s%s (lenght: %d)" % (space, self.name, self.size))
        self.direction = self.ask_direction()
        print("%s%s direction: %s"
              % (space * 2, self.name, self.direction))
        if self.direction == "horizontal":
            hor = input_integer("%sChoose row" % (space),
                                1, board_size[1])
            ver = input_integer("%sChoose starting column" % (space),
                                1, board_size[0] - self.size) - 1
        elif self.direction == "vertical":
            ver = input_integer("%sChoose col" % (space),
                                1, board_size[0])
            hor = input_integer("%sChoose starting row" % (space),
                                1, board_size[1] - self.size) - 1
        ship = self.create_ship(hor, ver)
        return ship

    # Player chooses the ship position
    def ask_position(self):
        print("\n%s%s:" % (space, self.name))
        row = input_integer("%sChoose %s row"
                            % (space, self.name),
                            1, board_size[1])
        col = input_integer("%sChoose %s column"
                            % (space, self.name),
                            1, board_size[0])
        position = [row, col]
        if self.validate(position):
            return [[True, position]]
        else:
            return False

    # Check if position doesn't conflict with other ships
    def validate(self, position):
        row = position[0]
        col = position[1]
        for ship in self.ships:
            for ship_position in ship.positions:
                if ship_position[1] == [row, col]:
                    if not (randomize_ships or self.player.ai):
                        print("\n%sPosition already occupied"
                              % (space * 2))
                    return False
                elif ship_position[1] in [[row - 1, col],
                                          [row + 1, col],
                                          [row, col - 1],
                                          [row, col + 1]]:
                    if not (randomize_ships or self.player.ai):
                        print("\n%sToo close to another ship"
                              % (space * 2))
                    return False
        else:
            return True


# Player class
class Player(object):
    def __init__(self, name, ai):
        self.is_alive = True
        self.name = name
        self.ai = ai
        self.ships = []
        self.ships_sunked = 0
        self.ships_board = []
        self.guesses_boards = {}
        self.guess = []
        self.init_ships()

    # Initializes ships class
    def init_ships(self):
        if not (self.ai or randomize_ships):
            print("\n%s%s position your ships:" % (space, self.name))
        for ship in range(number_of_ships):
            self.ships.append(Ship(self, self.ships, "Ship "
                                   + str(ship + 1), ship_size))

    # Print own ships
    def print_ships(self):
        ships = players[self.target].ships
        for ship in ships:
            if ship.floating:
                name = Fore.GREEN + ship.name + Style.RESET_ALL
            else:
                name = Fore.RED + ship.name + Style.RESET_ALL
            print("%s%s: %s" % (space * 2, name, ship))
        print()

    # Ask player to give a target
    def ask_target(self, targets):
        print("%sTargets available:\n" % (space))
        for player in targets:
            print("%s%s" % (space * 2, player))
        print()
        while True:
            response_target = input("%sChoose a target: "
                                    % (space)).lower().capitalize()
            if response_target in (targets):
                self.target = response_target
                break
            elif "Player %s" % (response_target) in (targets):
                self.target = "Player %s" % (response_target)
                break
            else:
                print(space + "Choose a valid target")

    # Choose/determine the target
    def get_target(self):
        targets = []
        for player in players.keys():
            if players[player].is_alive is True:
                targets.append(player)
        targets.remove(self.name)
        if len(targets) == 1:
            self.target = targets[0]
        else:
            if self.ai:
                self.target = targets[randint(0, len(targets) - 1)]
            else:
                self.ask_target(targets)
        print("%sTarget: %s\n" % (space, self.target))

        initialize_guesses_boards(self, self.target)
        self.player_guess()
        return

    # Player guess
    def player_guess(self):
        if not self.ai:
            if debug:
                print("%sEnemy Ships:" % (space))
                self.print_ships()
            print_board(self.guesses_boards[self.target])
        if self.ai:
            self.guess = [randint(1, board_size[1]),
                          randint(1, board_size[0])]
            if debug:
                print("%sAI Guess: %s\n" % (space, self.guess))
        else:
            self.guess = [input_integer("%sGuess Row   " % (space),
                                        1, board_size[1]),
                          input_integer("%sGuess Column" % (space),
                                        1, board_size[0])]
            print()
        self.check()

    # Eliminate current target player, checks for endgame
    def eliminate_player(self, target):
        print_board(self.guesses_boards[self.target])
        target.is_alive = False
        print("%s%s%s%s sunked the last ship of %s%s%s!" %
              (space, Fore.GREEN, self.name, Style.RESET_ALL,
               Fore.RED, self.target, Style.RESET_ALL))
        print("%s%s%s%s was %seliminated%s from the game.\n" %
              (space, Fore.RED, self.target, Style.RESET_ALL,
               Style.BRIGHT, Style.RESET_ALL))
        # All players but self is alive (Winner)
        if is_endgame(players):
            print("%s%s%s%s is the winner!!!%s\n"
                  % (Style.BRIGHT, Fore.GREEN, self.name,
                     Fore.WHITE, Style.RESET_ALL))
            start()
        self.get_target()

# Hit a ship
    def hit(self, target, ship, position):
        if position[0]:
            position[0] = False
            # Register the hit in all players guesse board of the target
            for player in players:
                initialize_guesses_boards(players[player],
                                          self.target)
                board = players[player].guesses_boards
                board[self.target][self.guess[0] - 1][self.guess[1] - 1] = "S"
            ship.hits += 1
            # Ship sunked
            if ship.hits == ship.size:
                print_board(self.guesses_boards[self.target])
                ship.floating = False
                target.ships_sunked += 1
                if target.ships_sunked == number_of_ships:
                    self.eliminate_player(target)
                else:
                    print("%s%s%s%s sunked %s from %s%s%s"
                          % (space, Fore.GREEN, self.name, Style.RESET_ALL,
                             ship.name, Fore.RED, target.name,
                             Style.RESET_ALL))
                    print("%s%s%s%s have %d ships left.\n"
                          % (space, Fore.RED, self.target,
                             Style.RESET_ALL, number_of_ships
                             - target.ships_sunked))
                    pause(self.ai)
                    self.get_target()
            else:
                print("%s%s%s%s hitted %s from %s%s%s\n"
                      % (space, Fore.GREEN, self.name, Style.RESET_ALL,
                         ship.name, Fore.RED, target.name, Style.RESET_ALL))
                pause(self.ai)
                self.player_guess()
        else:
            print("%sPosition was already hitted\n"
                  % (space))

    # Register the wrong guess in the guesses board
    def missed(self, target):
        if (target[self.guess[0] - 1][self.guess[1] - 1] == "X"):
            if self.ai:
                self.player_guess()
            else:
                print("%s%s already guessed that position\n"
                      % (space, self.name))
        else:
            target[self.guess[0] - 1][self.guess[1] - 1] = "X"
            print("%s%s %smissed%s the shot.\n"
                  % (space, self.name, Fore.RED, Style.RESET_ALL))

    # Check guess
    def check(self):
        target = players[self.target]
        for ship in target.ships:
            for position in ship.positions:
                if position[1] == [self.guess[0], self.guess[1]]:
                    # Position is floating
                    self.hit(target, ship, position)
                    return
        else:
            self.missed(self.guesses_boards[self.target])
        pause(self.ai)
        if self.ai is False:
            print_board(self.guesses_boards[self.target])


# Each game
def game():
    global players
    rounds = 0
    players = {}
    print("\n======= New Game =======\n")

    # Initialize each Player(class)
    # Human players
    for player in range(number_of_players - ai_players):
        name = "Player %s" % (player + 1)
        players[name] = Player(name, False)
    # AI players
    for player in range(ai_players):
        name = "Player %s" % (player + 1 + (number_of_players - ai_players))
        players[name] = Player(name, True)

    # Loop trought turns
    while True:
        rounds += 1
        print("\n******** Round %d ********\n" % (rounds))

        for player in players:

            if players[player].is_alive is True:
                print("%s Turn\n" % player)
                players[player].get_target()

    return


# Starting screen with some options
def start():
    global board_size
    global debug
    global number_of_ships
    global number_of_players
    global randomize_ships
    global ai_players
    global timeout
    global ship_size
    print("\n========================")
    print("====== %sBattleship%s ======" % (Back.BLUE, Style.RESET_ALL))
    print("========================\n")
    print("New Game (g)")
    print("Board Size (b)          Current: (%d, %d)"
          % (board_size[0], board_size[1]))
    print("Number of players (p)   Current: %d" % (number_of_players))
    print("Number of ships (ns)     Current: %d" % (number_of_ships))
    print("Ship Size (ss)          Current: %d" % (ship_size))
    print("Cheats/Debug (c)        Current: %s" % (debug))
    print("Randomize ships (r)     Current: %s" % (randomize_ships))
    print("AI players (a)          Current: %d" % (ai_players))
    print("AI pause time (t)       Current: %ss" % (timeout / 1000))
    print("Restore default (d)")
    print("Exit/Quit (e/q)\n")

    answer = input("What's your choice? ").lower()
    print()

    # Player choice
    if answer in ("g",
                  "game",
                  "new game",
                  "new_game",
                  "newgame"):
        game()
        return
    elif answer in ("b",
                    "size",
                    "board size",
                    "board_size",
                    "boardsize"):
        board_size[0] = input_integer("Choose the width of the board",
                                      board_interval[0], board_interval[1])
        board_size[1] = input_integer("Choose the height of the board",
                                      board_interval[0], board_interval[1])
        max_ships = ships_interval[1](board_size)
        if number_of_ships > max_ships:
            number_of_ships = int(max_ships)
            print("The number of ships was reduced to the new maximum: %d"
                  % (max_ships))
        start()
        return
    elif answer in ("p",
                    "players",
                    "number of players",
                    "number_of_players",
                    "numberofplayers"):
        number_of_players = input_integer("Choose the number of players",
                                          players_interval[0],
                                          players_interval[1])
        if ai_players > number_of_players - 1:
            ai_players = number_of_players - 1
            print("AI players reduced to %d." % (ai_players))
        start()
        return
    elif answer in ("c",
                    "cheats",
                    "debug"):
        debug = not debug
        print("Debug mode: %s" % (debug))
        print()
        start()
        return
    elif answer in ("e",
                    "exit",
                    "q",
                    "quit"):
        print("Exit game\n")
        return
    elif answer in ("ns",
                    "number of ships",
                    "number_of_ships",
                    "numberofships"):
        if int(ships_interval[1](board_size)) == 1:
            number_of_ships = 1
            print("At the current board size (%d, %d)"
                  + "there can be only one ship.\n"
                  % (board_size[0], board_size[1]))
        else:
            number_of_ships = input_integer("Choose the number of ships",
                                            ships_interval[0],
                                            ships_interval[1](board_size))
        start()
        return
    elif answer in ("ss",
                    "ship size",
                    "ship_size",
                    "shipsize"):
        ship_size = input_integer("Choose the size of the ships",
                                  size_interval[0],
                                  size_interval[1])
        start()
        return
    elif answer in ("d",
                    "restore",
                    "default",
                    "restore default",
                    "restore_default",
                    "restoredefault"):
        board_size = default["board_size"]
        debug = default["debug"]
        number_of_ships = default["number_of_ships"]
        number_of_players = default["number_of_players"]
        randomize_ships = default["randomize_ships"]
        start()
        return
    elif answer in ("r",
                    "randomize",
                    "randomize ships",
                    "randomize_ships",
                    "randomizeships"):
        randomize_ships = not randomize_ships
        print("Randomize Ships: %s" % (randomize_ships))
        print()
        start()
        return
    elif answer in ("a",
                    "ai",
                    "ai players",
                    "ai_players",
                    "aiplayers"):
        ai_players = input_integer("Choose the number of AI players",
                                   ai_interval[0],
                                   ai_interval[1](number_of_players))
        start()
        return
    elif answer in ("t",
                    "pause",
                    "time",
                    "pause time",
                    "pause_time",
                    "pausetime"):
        timeout = input_integer("Choose a pause time in"
                                + "miliseconds for AI action",
                                time_interval[0],
                                time_interval[1])
        start()
        return
    else:
        print("Enter a valid answer!")
        start()
        return


start()
