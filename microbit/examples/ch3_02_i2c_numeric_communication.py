# ch3_02_i2c_numeric_communication.py

from microbit import *

while True:
    try:
        number = 42   # Transfer numeric data
        i2c.write(0x08, bytes([number]))
        print('Sent:', number)
        
        # Receiving numeric data from Arduino
        received_data = i2c.read(0x08, 1)  # read 1 byte
        received_number = received_data[0]
        print('Received:', received_number)
        
        sleep(2000)  # delay 2 seconds
    except Exception as e:
        print('Error: ' + str(e))
        