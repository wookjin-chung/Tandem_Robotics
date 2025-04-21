# ch6_07_tandem_radio_controlled_abot.py

import radio
from microbit_abot import *

# Initialize the radio
radio.on()
radio.config(channel=7)

# Attach servos to pins
abot_left = bot(13)
abot_right = bot(12)

bot(13, 12).servo_attachpins()

while True:
    incoming = radio.receive()
    if incoming:
        if incoming == 'forward':
            abot_left.servo_speed(100)
            abot_right.servo_speed(-100)
            display.show(Image.ARROW_S)

        elif incoming == 'backward':
            abot_left.servo_speed(-100)
            abot_right.servo_speed(100)
            display.show(Image.ARROW_N)

        elif incoming == 'left':
            abot_left.servo_speed(0)
            abot_right.servo_speed(-100)
            display.show(Image.ARROW_E)

        elif incoming == 'right':
            abot_left.servo_speed(100)
            abot_right.servo_speed(0)
            display.show(Image.ARROW_W)

        elif incoming == 'stop':
            abot_left.servo_speed(0)
            abot_right.servo_speed(0)
            display.show(Image.SQUARE)

        # Small delay to allow servos to move
        sleep(100)
