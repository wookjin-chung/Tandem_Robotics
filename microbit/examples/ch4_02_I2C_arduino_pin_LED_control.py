# ch4_02_I2C_arduino_pin_LED_control.py

from microbit_abot import *

abot = bot(8)

while True:
    abot.write_digital(1)  # Turn on the LED connected to pin 8
    sleep(1000)            # Wait for 1 second
    abot.write_digital(0)  # Turn off the LED connected to pin 8
    sleep(1000)            # Wait for 1 second
