#ch4_15_micro_abot_rcTime.py

from microbit_abot import *
abot = bot(8)

while True:
    abot.write_digital(1)
    qt_left = abot.rc_time(1)
    
    #display.scroll(str(qt_left))
    print("Left_sensor:", qt_left)
    sleep(50)
