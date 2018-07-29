from settings import settings as set


def check_int(user_input):
    try:
        user_input = int(user_input)
    except ValueError:
        return "ValueError"
    else:
        return user_input


def check_float(user_input):
    try:
        user_input = float(user_input)
    except ValueError:
        return "ValueError"
    else:
        return user_input


# User input and validation
def input_num(message, min_value, max_value, type):
    while True:
        user_input = input("%s (%d to %d): "
                           % (message, min_value, max_value))
        if type == "int":
            user_input = check_int(user_input)
        elif type == "float":
            user_input = check_float(user_input)
        if user_input == "ValueError":
            print("%sEnter a whole number (integer)." % (set["space"] * 2))
            continue
        else:
            if user_input < min_value or user_input > max_value:
                print("%sThe number must be between %d and %d."
                      % (set["space"] * 2, min_value, max_value))
                continue
            else:
                return user_input
