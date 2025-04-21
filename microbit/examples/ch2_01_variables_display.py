# ch2_01_variables_display.py

from microbit import *

# Declare and initialize variables
temperature = 25
message = "Hello, Micro:bit!"

# Use variables
display.scroll(message)
display.scroll("Temperature: " + str(temperature) + "C")
