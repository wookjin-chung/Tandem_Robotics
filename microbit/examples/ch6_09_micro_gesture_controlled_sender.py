# ch6_09_micro_gesture_controlled_sender.py
# Remote_controller

from microbit import *
import radio

# Initialize the radio
radio.on()
radio.config(channel=7)

while True:
    x, y, z = accelerometer.get_values()

    if y < -200:
        radio.send('backward')
    elif y > 200:
        radio.send('forward')
    elif x < -200:
        radio.send('right')
    elif x > 200:
        radio.send('left')
    else:
        radio.send('stop')

    sleep(100)
