"""

   A battleship game from Codecademy's Python lesson 19/19
   
"""


from random import randint
from copy import copy

# Default settings
default = {
  "board_size": [6, 6],
  "debug": False,
  "number_of_ships": 3,
  "number_of_players": 2,
  "randomize_ships": True,
  "ai_players": 1
  }

# User settings
board_size = default["board_size"]
debug = default["debug"]
number_of_ships = default["number_of_ships"]
number_of_players = default["number_of_players"]
ai_players = default["ai_players"]
randomize_ships = default["randomize_ships"]
space = "  "

# Settings values interval
size_interval = [3, 15]
ships_interval = [1, lambda size : ((size[0] + size[1]) / 2) * 0.6]
players_interval = [2, 8]
ai_interval = [0, lambda ai : ai - 1]

# Print user readable board
def print_board(board):
  header = space + "     "
  for col in range(board_size[0]):
    if col >= 9:
      header = header + str(col + 1) + "  "
    else:
      header = header + str(col + 1) + "   "
    i = 1
  print (header)
  sub_header = space + "     |" + "   |" * (board_size[0] - 1)
  print (sub_header)
  print ()
  for row in board:
    if i >= 10:
      print (space + str(i) + "-  " + "   ".join(row) + "  -" + str(i))
    else:
      print (space + " " + str(i) + "-  " + "   ".join(row) + "  -" + str(i))
    print ()
    i += 1
  print (sub_header)
  print (header)
  print ()

# Randomize position for a ship
def random_position(position_range):
  position = [randint(1, position_range[1]), randint(1, position_range[0])]
  return position

# Print ships dictionary
def print_ships(dict):
  for player in dict:
    print ((space * 2) +"%s: %s" % (player, dict[player]))
  print ()

# User input and validation
def input_integer(message, min_value, max_value):
  while True:
    try:
      user_input = int(input(message + " (%d to %d): " % (min_value, max_value)))
    except ValueError:
      print(space + "Enter a whole number (integer).")
      continue
    if user_input < min_value or user_input > max_value:
      print(space + "The number must be between %d and %d." % (min_value, max_value))
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

# Create ships, ensuring no ships on same position
def create_ship(ships_dict, ship_number, is_ai):
  while True:
    if randomize_ships or is_ai:
      position = random_position (board_size)
      row = position[0]
      col = position[1]
    else:
      print ("\n" + space + "Ship %d:" % (ship_number))
      row = input_integer(space + "Choose Ship %d row" % (ship_number), 1, board_size[1])
      col = input_integer(space + "Choose Ship %d col" % (ship_number), 1, board_size[0])
      position = [row, col]
    if len(ships_dict) == 0:
      return position
    # Return position only when don't conflict with other ships
    for ship in ships_dict:
      if ships_dict[ship][1] == position:
        if not randomize_ships:
          print (space + "That position is already occupied by %s" % (ship))
        break
      elif ships_dict[ship][1] in [[row - 1, col],\
                                   [row + 1, col],\
                                   [row, col - 1],\
                                   [row, col + 1]]:
        if not randomize_ships:
          print (space + "That position is too close to the %s" % (ship))
        break
    else:
      return position

# Check if current player is the only one alive
def is_endgame(players):
  count = 0
  for player in players:
    if players[player].is_alive == False:
      count += 1
  if count == len(players) - 1:
    return True
  else:
    return False

def game():
  print ("\n======= New Game =======\n")
  rounds = 0
  players = {}

  # Generic player class
  class Player(object):
    def __init__(self, name, ai):
      self.is_alive = True
      self.name = name
      self.ai = ai
      self.ships = {}
      self.ships_sunked = 0
      self.ships_board = []
      self.guesses_boards = {}
      self.guess = []

      # Creates dictionary of the ships
      if not self.ai and not randomize_ships:
        print ("\n" + space + "%s position your ships:" % (self.name))
      for ship in range(number_of_ships):
        ship_position = create_ship(self.ships, ship + 1, self.ai)
        self.ships["Ship " + str(ship + 1)] = [True, ship_position]

    # Choose/determine the target
    def get_target(self):
      targets = []
      for player in players.keys():
        if players[player].is_alive == True:
          targets.append(player)
      targets.remove(self.name)
      if len(targets) == 1:
        self.target = targets[0]
      else:
        if self.ai:
          self.target = targets[randint(0, len(targets) - 1)]
        else:
          print (space + "Targets available:\n")
          for player in targets:
            print ("  %s" % (player))
          print ()
          while True:
            response_target = input(space + "Choose a target: ").lower().capitalize()
            if response_target in (targets):
              self.target = response_target
              break
            elif "Player " + str(response_target) in (targets):
              self.target = "Player " + str(response_target)
              break
            else:
              print (space + "Choose a valid target")
      print (space + "Target: %s\n" % self.target)

      initialize_guesses_boards(self, self.target)
      self.player_guess()
      return

    # Player guess
    def player_guess(self):
      if not self.ai:
        if debug:
          print (space + "Enemy Ships:")
          print_ships(players[self.target].ships)
        print_board (self.guesses_boards[self.target])
      if self.ai:
        self.guess = [randint(1, board_size[1]),\
                      randint(1, board_size[0])]
        if debug:
          print (space + "AI Guess: %s\n" % (self.guess))
      else:
        self.guess = [input_integer(space + "Guess Row", 1, board_size[1]),\
                      input_integer(space + "Guess Col", 1, board_size[0])]
        print ()
      self.check()

    # Check guess
    def check(self):
      for key in players[self.target].ships:
        # Hit a ship
        if players[self.target].ships[key][1] == [self.guess[0], self.guess[1]]:
          # Ship hasn't been sunked yet
          if players[self.target].ships[key][0] == True:
            players[self.target].ships[key][0] = False
            players[self.target].ships_sunked += 1
            # All ships have been sunked
            if players[self.target].ships_sunked == number_of_ships:
              players[self.target].is_alive = False
              print (space + "%s sunked the last ship of %s!" % (self.name, self.target))
              print (space + "%s was eliminated from the game.\n" % self.target)
              # All players but self is alive (Winner)
              if is_endgame(players):
                print ("%s is the winner!!!\n" % (self.name))
                start()
              self.get_target()
            # There are more ships to be sinked
            else:
              for player in players:
                initialize_guesses_boards(players[player], self.target)
                players[player].guesses_boards[self.target][self.guess[0] - 1][self.guess[1] - 1] = "S"
              print (space + "%s sinked a %s ship!" % (self.name, self.target))
              print (space + "%s have %d ships left.\n" % (self.target, number_of_ships - players[self.target].ships_sunked))
              self.get_target()
            break
          # Ship already sunked
          else:
            if self.ai:
              self.player_guess()
            else:
              print (space + "That ship has already been sunked.\n")
              break
      # Missed
      else:
        if (self.guesses_boards[self.target][self.guess[0] - 1][self.guess[1] - 1] == "X"):
          if self.ai:
            self.player_guess()
          else:
            print(space + "%s already guessed that position\n" % (self.name))
        else:
          self.guesses_boards[self.target][self.guess[0] - 1][self.guess[1] - 1] = "X"
          print (space + "%s missed the shot.\n" % (self.name))

  # Initialize each Player(class)
  # Human players
  for player in range(number_of_players - ai_players):
    name = "Player " + str(player + 1)
    players[name] = Player(name, False)
  # AI players
  for player in range(ai_players):
    name = "Player " + str(player + 1 + (number_of_players - ai_players))
    players[name] = Player(name, True)
  
  # Loop trought turns
  while True:
    rounds += 1
    print ("\n******** Round %d ********\n" % (rounds))
    
    for player in players:
      
      if players[player].is_alive == True:
        print ("%s Turn\n" % player)
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
  print ("\n========================")
  print ("====== Battleship ======")
  print ("========================\n")
  print ("New Game (g)")
  print ("Board Size (b)          Current: (%d, %d)" % (board_size[0], board_size[1]))
  print ("Number of players (p)   Current: %d" % (number_of_players))
  print ("Number of ships (s)     Current: %d" % (number_of_ships))
  print ("Cheats/Debug (c)        Current: %s" % (debug))
  print ("Randomize ships (r)     Current: %s" % (randomize_ships))
  print ("AI players (a)          Current: %d" % (ai_players))
  print ("Restore default (d)")
  print ("Exit/Quit (e/q)\n")
  
  answer = input("What's your choice? ").lower()
  print ()

  # Player choice
  if answer in ("g",\
                "game",\
                "new game",\
                "new_game",\
                "newgame"):
    game()
    return
  elif answer in ("b",\
                  "size",\
                  "board size",\
                  "board_size",\
                  "boardsize"):
    board_size[0] = input_integer("Choose the width of the board", size_interval[0], size_interval[1])
    board_size[1] = input_integer("Choose the height of the board", size_interval[0], size_interval[1])
    max_ships = ships_interval[1](board_size)
    if number_of_ships > max_ships:
      number_of_ships = max_ships
      print ("The number of ships have been reduced to the new maximum: %d" % (max_ships))
    start()
    return
  elif answer in ("p",\
                  "players",\
                  "number of players",\
                  "number_of_players",\
                  "numberofplayers"):
    number_of_players = input_integer("Choose the number of players", players_interval[0], players_interval[1])
    start()
    return
  elif answer in ("c",\
                  "cheats",\
                  "debug"):
    debug = not debug
    print ("Debug mode: %s" % (debug))
    print ()
    start()
    return
  elif answer in ("e",\
                  "exit",\
                  "q",\
                  "quit"):
    print ("Exit game\n")
    return
  elif answer in ("s",\
                  "ships",\
                  "number of ships",\
                  "number_of_ships",\
                  "numberofships"):
    if int(ships_interval[1](board_size)) == 1:
      number_of_ships = 1
      print ("At the current board size (%d, %d) there can be only one ship.\n" % (board_size[0], board_size[1]))
    else:
      number_of_ships = input_integer("Choose the number of ships", ships_interval[0], ships_interval[1](board_size))
    start()
    return
  elif answer in ("d",\
                  "restore",\
                  "default",\
                  "restore default",\
                  "restore_default",\
                  "restoredefault"):
    board_size = default["board_size"]
    debug = default["debug"]
    number_of_ships = default["number_of_ships"]
    number_of_players = default["number_of_players"]
    randomize_ships = default["randomize_ships"]
    start()
    return
  elif answer in ("r",\
                  "randomize",\
                  "randomize ships",\
                  "randomize_ships",\
                  "randomizeships"):
    randomize_ships = not randomize_ships
    print ("Randomize Ships: %s" % (randomize_ships))
    print ()
    start()
    return
  elif answer in ("a",\
                  "ai",\
                  "ai players",\
                  "ai_players",\
                  "aiplayers"):
    ai_players = input_integer("Choose the number of AI players", ai_interval[0], ai_interval[1](number_of_players))
    start()
    return
  else:
    print ("Enter a valid answer!")
    start()
    return

start()
