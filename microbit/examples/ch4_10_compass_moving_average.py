# ch4_10_compass_moving_average.py

from microbit import *

# Moving average filter class
class MovingAverageFilter:
    def __init__(self, size):
        self.size = size
        self.buffer = [0] * size
        self.index = 0

    def add_value(self, value):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        return sum(self.buffer) / self.size

# Compass calibration function
def calibrate_compass():
    display.scroll("CAL")
    compass.calibrate()
    display.clear()

# Perform calibration at the start
calibrate_compass()

# Create a moving average filter (size = 5)
direction_filter = MovingAverageFilter(5)

while True:
    if button_a.is_pressed():
        calibrate_compass()

    # Measure magnetic field values on X, Y, Z axes
    mag_x = compass.get_x()
    mag_y = compass.get_y()
    mag_z = compass.get_z()

    # Display the direction on the micro:bit LED
    raw_direction = compass.heading()
    direction = direction_filter.add_value(raw_direction)
    direction_str = ""

    if 0 <= direction < 45 or 315 <= direction < 360:
        display.show("S")  # South
        direction_str = "S"
    elif 45 <= direction < 135:
        display.show("W")  # West
        direction_str = "W"
    elif 135 <= direction < 225:
        display.show("N")  # North
        direction_str = "N"
    elif 225 <= direction < 315:
        display.show("E")  # East
        direction_str = "E"

    # Print the measured values to the serial console
    print("X: {} Y: {} Z: {} Direction: {}".format(mag_x, mag_y, mag_z, direction_str))

    # Wait 0.2 seconds
    sleep(200)
