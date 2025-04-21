# ch6_03_group_radio_communication_sender.py

from microbit import *
import radio

radio.on()  # Turn on the radio

def send_message(group, message):
    radio.config(group=group)
    # Send the message multiple times to increase the probability of reception
    for _ in range(5):
        radio.send(message)
        sleep(100)

while True:
    if button_a.was_pressed():
        # Send an individual message
        send_message(1, 'Hello, Micro:bit 1!')
        display.scroll('To 1!')

    elif button_b.was_pressed():
        # Send a message to everyone
        send_message(99, 'Hello, everyone!')
        display.scroll('To all!')
