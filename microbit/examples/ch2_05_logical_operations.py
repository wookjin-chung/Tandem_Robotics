# ch2_05_logical_operations.py

from microbit import *

# Logical operations
is_raining = True
is_windy = False

is_bad_weather = is_raining and is_windy  # Both are True
is_either_bad = is_raining or is_windy    # At least one is True
is_not_raining = not is_raining           # Negation

# Display results
display.scroll("Bad Weather: " + str(is_bad_weather))
display.scroll("Either Bad: " + str(is_either_bad))
display.scroll("Not Raining: " + str(is_not_raining))
