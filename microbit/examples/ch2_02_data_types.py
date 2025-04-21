# ch2_02_data_types.py

from microbit import *

# Use various data types
count = 10           # Integer
temperature = 23.5   # Float
greeting = "Hi!"     # String
is_raining = False   # Boolean

# Display variable values
display.scroll(greeting)
display.scroll("Count: " + str(count))
display.scroll("Temp: " + str(temperature))

if is_raining:
    display.scroll("It is raining")
else:
    display.scroll("It is not raining")
