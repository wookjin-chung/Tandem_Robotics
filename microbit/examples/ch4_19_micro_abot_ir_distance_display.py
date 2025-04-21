# ch4_19_micro_abot_ir_distance_display.py

from microbit_abot import *
from microbit import display, sleep

left_sensor = bot(9, 10)
right_sensor = bot(2, 3)

def display_distance(sensor_value, column):
    """
    Displays the distance reading on a single column of the micro:bit LED display.

    :param sensor_value: The distance value returned by the IR distance sensor.
    :param column: The x-coordinate (column) on the micro:bit display to use.
    """
    # Calculate the number of LEDs to light based on the sensor value
    num_leds_to_light = 5 - (sensor_value // 2)
    
    for y in range(5):  # y goes from 0 to 4
        if y < num_leds_to_light:
            display.set_pixel(column, y, 9)  # Turn on the LED at full brightness
        else:
            display.set_pixel(column, y, 0)  # Turn off the LED

while True:
    # Get the left and right sensor values
    left_distance = left_sensor.ir_distance()
    right_distance = right_sensor.ir_distance()

    # Adjust the brightness of the LEDs in column 0 according to the left sensor
    display_distance(left_distance, 0)
    
    # Adjust the brightness of the LEDs in column 4 according to the right sensor
    display_distance(right_distance, 4)

    # Print the sensor values to the console
    print("Left_IR:", left_distance)
    print("Right_IR:", right_distance)
    
    sleep(50)
