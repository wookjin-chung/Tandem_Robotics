# ch5_18_offset_robot_drive.py

from microbit_abot import *
from abot_straight_calibrate import *

def main():
    abot = calibratedbot(13, 12)
    abot.servo_attachpins()
    abot.servo_speed(0, 0)
    sleep(500)
    
    # abot.set_right_speed_offset(7)
    abot.set_left_speed_offset(-7)

    display.scroll("Ready")
    abot.servo_speed_calibrated(100, -100)
    sleep(2000)
    abot.servo_speed_calibrated(-100, 100)
    sleep(2000)
    abot.servo_speed_calibrated(0, 0)
    
main()
