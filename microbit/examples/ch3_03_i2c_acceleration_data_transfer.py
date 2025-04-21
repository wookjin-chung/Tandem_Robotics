# ch3_03_i2c_acceleration_data_transfer.py

from microbit import *

while True:
    acceleration = accelerometer.get_x()  # Collect average X-axis acceleration data
    data = bytes(str(acceleration), 'ascii')  # Convert data to ASCII byte format
    i2c.write(0x08, data)  # Send data to Arduino via I2C

    try:
        response = i2c.read(0x08, 2)  # Receive 2 bytes of data from Arduino
        print("Received data:", response)  # Print the received data
    except Exception as e:
        print("Error:", e)
    
    print("X-axis acceleration:", acceleration)
    sleep(1000)  # Wait for 1 second
