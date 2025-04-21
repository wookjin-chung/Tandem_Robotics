# ch4_16_micro_abot_dual_rcTime.py

from microbit_abot import *
left_senser = bot(8)
right_sensor = bot(6)

while True:
    left_senser.write_digital(1)
    qt_left = left_senser.rc_time(1)
    right_sensor.write_digital(1)
    qt_right = right_sensor.rc_time(1)
    
    #display.scroll(str(qt_left))
    print("Left_sensor: ",qt_left)
    #display.scroll(str(qt_right))
    print("Right_sensor: ",qt_right)
    
    sleep(100)
