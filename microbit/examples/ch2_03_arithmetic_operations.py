# ch2_03_arithmetic_operations.py

from microbit import *

# Arithmetic operations
a = 10
b = 3

sum = a + b           # Addition
difference = a - b    # Subtraction
product = a * b       # Multiplication
quotient = a / b      # Division
quotient_int = a // b # Integer division
remainder = a % b     # Modulus
power = a ** b        # Exponentiation

# Display results
display.scroll("Sum: " + str(sum))
display.scroll("Diff: " + str(difference))
display.scroll("Prod: " + str(product))
display.scroll("Quot: " + str(quotient))
display.scroll("Int Quot: " + str(quotient_int))
display.scroll("Rem: " + str(remainder))
display.scroll("Pow: " + str(power))
