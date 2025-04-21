# ch2_11_button_input_function.py

from microbit import *

# Define a function to calculate the sum and product of two numbers
def add_and_multiply(a, b):
    total = a + b
    product = a * b
    return total, product

while True:
    if button_a.is_pressed():
        # When button A is pressed, calculate the result using 3 and 5
        result_sum, result_product = add_and_multiply(3, 5)
        display.scroll("Sum: {}".format(result_sum))
        display.scroll("Product: {}".format(result_product))
        sleep(1000)  # Wait briefly for the next input

        print("Sum: {}, Product: {}".format(result_sum, result_product))

    sleep(100)  # Default waiting time between button input detection
