# ch4_13_micro_touch_detection.py

from microbit import *

while True:
    # Detect logo touch
    if pin_logo.is_touched():
        display.show(Image.HAPPY)
        print("Logo touched")
        sleep(1000)  # Wait for 1 second before clearing
        display.clear()

    # Detect touch on pin 0
    elif pin0.is_touched():
        display.show("0")
        print("Pin 0 touched")
        sleep(1000)  # Wait for 1 second before clearing
        display.clear()

    # Detect touch on pin 1
    elif pin1.is_touched():
        display.show("1")
        print("Pin 1 touched")
        sleep(1000)  # Wait for 1 second before clearing
        display.clear()

    # Detect touch on pin 2
    elif pin2.is_touched():
        display.show("2")
        print("Pin 2 touched")
        sleep(1000)  # Wait for 1 second before clearing
        display.clear()

    else:
        display.clear()
