# ch6_17_tandem_radio_controlled_abot.py

from microbit import *
import radio
from microbit_abot import *

# Turn on the radio
radio.on()
# Configure the radio channel and max power
radio.config(channel=7, power=7)

# Attach servos to pins
abot_left = bot(13)
abot_right = bot(12)
bot(13, 12).servo_attachpins()

while True:
    incoming = radio.receive()
    if incoming:
        try:
            # Split the received data by comma
            parts = incoming.strip().split(',')
            if len(parts) == 2:
                # Convert the split data to floats
                left_speed, right_speed = map(float, parts)
                abot_left.servo_speed(int(left_speed * 100))
                abot_right.servo_speed(int(right_speed * 100))
                display.show(Image.HEART)
            else:
                raise ValueError("Incorrect number of elements")
        except ValueError as e:
            print("Error:", e)
            display.show(Image.SAD)

        sleep(100)
    else:
        # Actions to perform when there is no incoming data
        abot_left.servo_speed(0)
        abot_right.servo_speed(0)
        display.show(Image.SAD)

        sleep(100)
