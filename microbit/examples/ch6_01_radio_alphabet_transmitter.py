# ch6_01_radio_alphabet_transmitter.py

from microbit import *
import radio

# Radio setup
radio.on()
radio.config(channel=7)

# Initialize alphabet
alphabet = ['A', 'B', 'C', 'D', 'E']
index = 0

while True:
    # Select character
    if button_a.was_pressed():
        index = (index + 1) % len(alphabet)
        display.show(alphabet[index])

    # Send selected character
    elif button_b.was_pressed():
        radio.send(alphabet[index])
        display.clear()
        sleep(500)  # Wait briefly after transmission

    # Receive message
    incoming = radio.receive()
    if incoming:
        display.scroll(incoming)
