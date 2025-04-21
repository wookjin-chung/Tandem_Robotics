# ch6_15_micro_serial_control_with_joystick_levers.py

import pygame
import serial
import time

# Initialize Pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Configure serial communication
ser = serial.Serial('COM14', 115200)
time.sleep(2)  # Wait for the serial connection to stabilize

# Set threshold
threshold = 0.08  # Range considered as neutral

while True:
    pygame.event.pump()
    
    # Read the y-axis values for the left and right joystick levers
    left_y_axis = joystick.get_axis(1)   # Value between -1 and 1
    right_y_axis = joystick.get_axis(3)  # Value between -1 and 1
    
    # Check if the lever values are outside the threshold
    left_speed = int(-left_y_axis * 100) if abs(left_y_axis) > threshold else 0
    right_speed = int(right_y_axis * 100) if abs(right_y_axis) > threshold else 0
    
    # Format values to two decimals and create a command string
    command = f"{left_speed:.2f},{right_speed:.2f}\n"
    
    # Send data to the micro:bit
    ser.write(command.encode())

    # Simple output
    print(f"Sent: {command}")
    
    time.sleep(0.1)
