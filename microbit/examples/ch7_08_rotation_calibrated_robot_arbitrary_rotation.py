# ch7_08_rotation_calibrated_robot_arbitrary_rotation.py

from microbit_abot import *
from abot_rotation_calibrate import *

def main():
    abot = rotationCalibratedBot(13, 12)
    abot.servo_attachpins()
    abot.servo_speed(0, 0)
    sleep(500)

    abot.set_calibrated_speed(73, -71, 2200)
    display.scroll("Ready")
    sleep(500)

    while True:
        # Rotate clockwise by 90 degrees
        print("Rotating clockwise by 90 degrees")
        abot.rotate_degrees(90)
        sleep(1000)  # Wait for 1 second

        # Rotate counter-clockwise by 90 degrees
        print("Rotating counter-clockwise by 90 degrees")
        abot.rotate_degrees(-90)
        sleep(1000)  # Wait for 1 second

if __name__ == "__main__":
    main()
