# ch6_02_radio_with_random_delay.py

from microbit import *
import radio
import random

radio.on()
radio.config(channel=7)

alphabet = ['A', 'B', 'C', 'D', 'E']
index = 0

def attempt_to_send(message):
    # Set a random delay time
    delay = random.randint(100, 500)
    sleep(delay)
    radio.send(message)

while True:
    if button_a.was_pressed():
        index = (index + 1) % len(alphabet)
        display.show(alphabet[index])

    elif button_b.was_pressed():
        attempt_to_send(alphabet[index])
        display.clear()
        sleep(500)

    incoming = radio.receive()
    if incoming:
        display.scroll(incoming)
