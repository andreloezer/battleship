

import os
from settings import settings as sets


# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Define offset for printing menu messages
def offset():
    return sets["board"][1] * 2


# Ensure input is a integer
def check_int(user_input):
    try:
        user_input = int(user_input)
    except ValueError:
        return "ValueError"
    else:
        return user_input


# Ensure input is a float
def check_float(user_input):
    try:
        user_input = float(user_input)
    except ValueError:
        return "ValueError"
    else:
        return user_input


# User input and validation
def input_num(message, min_value, max_value, format_type, escape=False):
    while True:
        user_input = input("%s (%d to %d): "
                           % (message, min_value, max_value))
        if escape and user_input.lower() == escape:
            return False
        if format_type == "int":
            user_input = check_int(user_input)
        elif format_type == "float":
            user_input = check_float(user_input)
        if user_input == "ValueError":
            print("%sEnter a whole number (integer)." % (sets["space"] * 2))
            continue
        else:
            if user_input < min_value or user_input > max_value:
                print("%sThe number must be between %d and %d."
                      % (sets["space"] * 2, min_value, max_value))
                continue
            else:
                return user_input
