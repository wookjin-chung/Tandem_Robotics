# ch2_04_comparison_operators.py

from microbit import *

# Comparison operations
a = 10
b = 5

is_equal = (a == b)            # Equal to
is_not_equal = (a != b)        # Not equal to
is_greater = (a > b)           # Greater than
is_lesser = (a < b)            # Less than
is_greater_or_equal = (a >= b) # Greater than or equal to
is_lesser_or_equal = (a <= b)  # Less than or equal to

# Display results
display.scroll("Equal: " + str(is_equal))
display.scroll("Not Equal: " + str(is_not_equal))
display.scroll("Greater: " + str(is_greater))
display.scroll("Lesser: " + str(is_lesser))
display.scroll("Greater or Equal: " + str(is_greater_or_equal))
display.scroll("Lesser or Equal: " + str(is_lesser_or_equal))
