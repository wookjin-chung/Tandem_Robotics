# ch6_13_micro_uart_to_radio_relay.py

from microbit import *
import radio

# Turn on the radio
radio.on()
# Configure the radio channel
radio.config(channel=7)

while True:
    # Check if there is any data available from the UART
    if uart.any():
        # Read a line from the UART
        command = uart.readline()
        if command:
            # Strip whitespace and decode
            command = command.strip().decode()
            # Send the command via radio
            radio.send(command)
            # Provide feedback on the micro:bit display
            display.show(Image.HAPPY)
            # Small delay
            sleep(100)
