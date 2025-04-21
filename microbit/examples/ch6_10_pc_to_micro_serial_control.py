# ch6_10_pc_to_micro_serial_control.py
# notebook_keyboard_serial

import serial
import time
import msvcrt

# The serial port to which the micro:bit is connected
SERIAL_PORT = 'COM14'  # Change to the appropriate port
BAUD_RATE = 115200

# Configure the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

def send_command(command):
    ser.write((command + '\n').encode())
    time.sleep(0.1)

try:
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'w':
                send_command('forward')
            elif key == 's':
                send_command('backward')
            elif key == 'a':
                send_command('left')
            elif key == 'd':
                send_command('right')
            elif key == 'x':
                send_command('stop')
finally:
    ser.close()
