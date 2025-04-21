# ch6_16_micro_uart_to_radio_relay.py

from microbit import *
import radio

# Turn on the radio
radio.on()
# Configure the radio channel and maximum power
radio.config(channel=7, power=7)

while True:
    # Check if there's any data available via UART
    if uart.any():
        command = uart.readline()
        
        # If a command is available, strip and decode it
        if command:
            command = command.strip().decode()
            # Send the command via radio
            radio.send(command)
            # Provide some feedback on the micro:bit display
            display.show(Image.HAPPY)
            sleep(100)
