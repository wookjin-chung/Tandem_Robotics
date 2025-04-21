# ch5_17_external_offset_control.py

from microbit_abot import *
from abot_straight_calibrate import *

def main():
    abot = calibratedbot(13, 12)
    abot.servo_attachpins()
    abot.servo_speed(0, 0)
    sleep(500)    
    
    #abot.set_right_speed_offset(7)  # use the positive value
    abot.set_left_speed_offset(-7)  # use the negative value
    
    display.scroll("Ready")
    
    while True:
        abot.drive_straight(80, -80, 5000)
        sleep(1000)
    
main()
