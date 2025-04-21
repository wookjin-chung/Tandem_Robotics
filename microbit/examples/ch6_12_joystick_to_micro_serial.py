#ch6_12_joystick_to_micro_serial.py

import pygame
import serial
import time

# Initialize Pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Configure serial communication with the micro:bit connected to the laptop
ser = serial.Serial('COM3', 115200)  # The COM port may vary depending on the system
time.sleep(2)  # Wait for the serial connection to stabilize

while True:
    pygame.event.pump()

    # Read joystick axis values
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Determine command based on joystick input
    if y_axis < -0.5:
        command = 'forward'
    elif y_axis > 0.5:
        command = 'backward'
    elif x_axis < -0.5:
        command = 'left'
    elif x_axis > 0.5:
        command = 'right'
    else:
        command = 'stop'

    # Send data to micro:bit
    ser.write((command + '\n').encode())

    # Simple output
    print(f'Sent: {command}')

    # Wait briefly so as not to send data too quickly
    time.sleep(0.1)
