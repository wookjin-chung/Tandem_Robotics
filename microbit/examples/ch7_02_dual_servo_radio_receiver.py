# ch7_02_dual_servo_radio_receiver.py 

from microbit import *
import radio
from microbit_abot import *

radio.on()
radio.config(channel=7, power=7)

abot_left = bot(13)
abot_right = bot(12)
bot(13, 12).servo_attachpins()

while True:
    incoming = radio.receive()
    if incoming:
        try:
            # Split the received data by commas
            parts = incoming.strip().split(',')
            if len(parts) == 2:
                # Convert the split data to floating point
                left_speed, right_speed = map(float, parts)
                abot_left.servo_speed(int(left_speed))
                abot_right.servo_speed(int(right_speed))
                display.show(Image.HEART)

            else:
                raise ValueError("Incorrect number of elements")

        except ValueError as e:
            print("Error:", e)
            display.show(Image.SAD)

        sleep(100)

    else:
        # Action to perform when there is no data
        abot_left.servo_speed(0)
        abot_right.servo_speed(0)
        display.show(Image.SAD)

        sleep(100)
