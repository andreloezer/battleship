"""

   A battleship game from Codecademy's Python lesson 19/19

"""


# https://pypi.org/project/colorama/
from colorama import init
import os


from menu import menu


# Enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607
os.system('')


init(autoreset=True)


menu()
