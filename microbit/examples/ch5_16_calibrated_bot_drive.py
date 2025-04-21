# ch5_16_calibrated_bot_drive.py

from microbit_abot import *
from abot_straight_calibrate import *

def main():
    abot = calibratedbot(13, 12)
    abot.servo_attachpins()
    abot.servo_speed(0, 0)
    sleep(500)
    display.scroll("Ready")
    
    while True:
        abot.drive_straight(80, -80, 5000)
        sleep(1000)
    
main()
