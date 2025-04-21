# ch2_10_function.py

from microbit import *

# Function definitions
def display_message(message):
    """Scroll the given message on the display."""
    display.scroll(message)
    sleep(500)

def display_heart():
    """Display a heart image on the screen."""
    display.show(Image.HEART)
    sleep(500)

def clear_display():
    """Clear the display."""
    display.clear()

# Main loop
while True:
    if button_a.is_pressed():
        display_message("Hello!")
    elif button_b.is_pressed():
        display_heart()
    else:
        clear_display()
    sleep(100)  # Add delay to avoid processing button inputs too quickly
