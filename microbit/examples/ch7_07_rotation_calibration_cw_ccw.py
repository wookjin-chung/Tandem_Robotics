# ch7_07_rotation_calibration_cw_ccw.py
from microbit_abot import *
from abot_rotation_calibrate import *

def main():
    abot = rotationCalibratedBot(13, 12)
    abot.servo_attachpins()
    abot.servo_speed(0, 0)
    sleep(500)

    display.scroll("Ready")
    sleep(500)

    while True:
        # Clockwise calibration using the start_calibration function.
        # Here, we set the calibration speed (e.g., 70) and the base rotation time (2200 ms).
        abot.start_rotation(speed=70, direction=True, base_rotation_time=2200)
        sleep(1000)
        
        # Counter-Clockwise calibration.
        #abot.start_rotation(speed=-70, direction=False, base_rotation_time=2200)
        sleep(1000)
    
main()
