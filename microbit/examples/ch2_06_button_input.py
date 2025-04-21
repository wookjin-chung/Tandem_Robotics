# ch2_06_button_input.py

from microbit import *

while True:
    if button_a.is_pressed():
        display.scroll("Button A")
    elif button_b.is_pressed():
        display.scroll("Button B")
    else:
        display.show(Image.HEART)
    sleep(100)
    