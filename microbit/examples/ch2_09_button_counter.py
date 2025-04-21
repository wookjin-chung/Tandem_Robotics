# ch2_09_button_counter.py

from microbit import *

count = 0

while True:
    if button_a.is_pressed():
        count += 1
        display.scroll(str(count))
        sleep(200)  # Add delay to prevent rapid button press detection
    elif button_b.is_pressed():
        count = 0
        display.scroll("Reset")
        sleep(200)
    sleep(100)
