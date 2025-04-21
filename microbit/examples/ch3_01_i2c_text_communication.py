# ch3_01_i2c_text_communication.py

from microbit import *

while True:
    try:
        # Send text data
        message = 'A'
        i2c.write(0x08, message.encode())
        print('Sent:', message)
        display.show(message)
        sleep(1000)
        
        # Receive text data from Arduino
        received_data = i2c.read(0x08, 1)  # Read 1 byte
        received_message = received_data.decode()
        print('Received:', received_message)
        display.show(received_message)
        sleep(1000)
        display.clear()
        
        sleep(2000)  # Wait for 2 seconds
    except Exception as e:
        print('Error: ' + str(e))
