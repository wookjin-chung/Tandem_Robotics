# ch4_09_compass_calibration_and_direction.py

from microbit import *

# Calibration function
def calibrate_compass():
    display.scroll("CAL")
    compass.calibrate()
    display.clear()

# Perform calibration at the start
calibrate_compass()

while True:
    # Recalibrate if button A is pressed
    if button_a.is_pressed():
        calibrate_compass()

    # Measure magnetic field values on X, Y, Z axes
    mag_x = compass.get_x()
    mag_y = compass.get_y()
    mag_z = compass.get_z()

    # Get the current heading and initialize a string for direction
    direction = compass.heading()
    direction_str = ""

    # Display direction on the micro:bit LED display
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

    # Wait for 0.2 seconds
    sleep(200)
