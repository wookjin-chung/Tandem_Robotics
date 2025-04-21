# ch4_20_micro_abot_whisker_sensor_display.py

from microbit_abot import *
left_sensor = bot(5)
right_sensor = bot(7)

while True:
    whisker_left = left_sensor.read_digital()
    whisker_right = right_sensor.read_digital()
    
    if whisker_left == 0:
        display.set_pixel(4, 2, 9) #LED on if left whisker is pressed
    else:
        display.set_pixel(4, 2, 0)
    if whisker_right == 0:
        display.set_pixel(0, 2, 9) #LED on if right whisker is pressed
    else:
        display.set_pixel(0, 2, 0)

    print("whisker_left: ",whisker_left)
    print("whisker_right: ",whisker_right)
