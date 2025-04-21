# ch4_18_micro_abot_ir_detect_display.py

from microbit_abot import *

left_sensor = bot(9, 10)
right_sensor = bot(2, 3)

while True:
    # Detect IR signals at 38 kHz
    irL = left_sensor.ir_detect(38000)
    irR = right_sensor.ir_detect(38000)

    # Toggle micro:bit display LED (x, y) on/off based on IR detection
    if irL:
        display.set_pixel(4, 2, 0)  # If IR is detected on the left sensor, turn off pixel
    else:
        display.set_pixel(4, 2, 9)  # If not detected, turn on pixel

    if irR:
        display.set_pixel(0, 2, 0)  # If IR is detected on the right sensor, turn off pixel
    else:
        display.set_pixel(0, 2, 9)  # If not detected, turn on pixel

    # Print IR detection status
    print("Left_IR:", irL)
    print("Right_IR:", irR)

    sleep(100)
