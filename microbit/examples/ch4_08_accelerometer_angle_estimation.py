# ch4_08_accelerometer_angle_estimation.py

from microbit import *

def estimate_angle(accel_value):
    # The accel_value ranges from -1024 to 1024
    # The angle is estimated between -90 and 90 degrees
    # Assume the angle is ±90° at maximum or minimum acceleration values
    return (accel_value / 1024) * 90

while True:
    # Read X and Y acceleration data from the sensor
    x = accelerometer.get_x()
    y = accelerometer.get_y()

    # Estimate angles for each axis
    angle_x = estimate_angle(x)
    angle_y = estimate_angle(y)

    # Print the angle values to the serial port
    print("X angle:", angle_x, "degrees")
    print("Y angle:", angle_y, "degrees")

    # Simple indication of tilt along the X or Y axis
    if abs(x) > abs(y):
        if x > 200:
            display.show("R")  # Tilted to the right
        elif x < -200:
            display.show("L")  # Tilted to the left
    else:
        if y > 200:
            display.show("U")  # Tilted upward
        elif y < -200:
            display.show("D")  # Tilted downward

    # Wait for 500 ms
    sleep(500)
