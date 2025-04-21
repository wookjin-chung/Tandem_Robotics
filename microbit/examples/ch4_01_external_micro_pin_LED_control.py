# ch4_01_external_micro_pin_LED_control.py

from microbit import *

# Turn on the LED connected to pin P0
pin0.write_digital(1)
sleep(1000)

# Turn off the LED
pin0.write_digital(0)
