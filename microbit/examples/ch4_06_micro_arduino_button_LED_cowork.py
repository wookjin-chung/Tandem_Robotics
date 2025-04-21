# ch4_06_micro_arduino_button_LED_cowork.py

from microbit import *
from microbit_abot import *  # Include the custom library

abot = bot(9)

while True:
    # If button A is pressed, show "0" and turn the LED off
    if button_a.is_pressed():
        display.show("0")
        abot.write_digital(0)
    else:
        # Otherwise, show "1" and turn the LED on
        display.show("1")
        abot.write_digital(1)
    sleep(1000)
