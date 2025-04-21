# ch2_12_global_local_variables.py

from microbit import *

# Declare a global variable
counter = 0

def update_counter(increment):
    global counter  # Declare usage of the global variable
    # Local variable
    temp_counter = counter
    temp_counter += increment
    counter = temp_counter
    return counter

def display_counter():
    # Global variable can be accessed inside the function
    display.scroll("Counter: {}".format(counter))

# Main loop
while True:
    if button_a.is_pressed():
        # Increase the counter by 1 when button A is pressed
        update_counter(1)
        display_counter()
        sleep(1000)  # Wait briefly before the button can be pressed again

    elif button_b.is_pressed():
        # Decrease the counter by 1 when button B is pressed
        update_counter(-1)
        display_counter()
        sleep(1000)

    sleep(100)  # Default delay between loops
