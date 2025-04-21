# ch6_08_micro_controlled_sender.py
# Remote_controller

from microbit import *
import radio

# Initialize the radio
radio.on()
radio.config(channel=7)

while True:
    # If both buttons are pressed
    if button_a.is_pressed() and button_b.is_pressed():
        radio.send('stop')
    # If only button A is pressed
    elif button_a.is_pressed():
        radio.send('right')
    # If only button B is pressed
    elif button_b.is_pressed():
        radio.send('left')
    else:
        # Use the accelerometer to determine forward/backward movement
        x, y, z = accelerometer.get_values()
        if y < -200:
            radio.send('backward')
        elif y > 200:
            radio.send('forward')
        else:
            radio.send('stop')
    sleep(100)
