# ch6_11_micro_uart_radio_relay.py
# Remote_controller

from microbit import *
import radio

# Initialize the radio
radio.on()
radio.config(channel=7)
uart.init(baudrate=115200)

def clean_command(command):
    # Filter out only letters and numbers from the byte string
    return ''.join(chr(b) for b in command if 48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122)

while True:
    if uart.any():
        command = uart.read()
        command = clean_command(command)
        if command in ['forward', 'backward', 'left', 'right', 'stop']:
            radio.send(command)
    sleep(100)
