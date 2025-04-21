# ch6_06_radio_signal_strength.py

from microbit import *
import radio

radio.on()

while True:
    incoming = radio.receive_full()
    if incoming:
        message, signal_strength, timestamp = incoming
        display.clear()
        # Display the signal strength (multiply the received signal strength by -1 to convert it to a positive number)
        display.scroll(str(-signal_strength))
