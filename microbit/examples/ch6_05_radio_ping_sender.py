# ch6_05_radio_ping_sender.py

from microbit import *
import radio

radio.on()
radio.config(power=7)  # Set the maximum transmission power

while True:
    radio.send('ping')
    sleep(1000)  # Send the message every second
