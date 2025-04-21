# ch4_07_micro_arduino_digital_read_write.py

from microbit import *
from microbit_abot import *  # Include the custom library

abot = bot(9)

while True:
    # If the digital reading from the Arduino pin is 1,
    # display "0" on the micro:bit and write a digital 0 (LED off, for example).
    if abot.read_digital() == 1:
        display.show("0")
        abot.write_digital(0)

    # If the digital reading from the Arduino pin is 0,
    # display "1" on the micro:bit and write a digital 1 (LED on, for example).
    elif abot.read_digital() == 0:
        display.show("1")
        abot.write_digital(1)

    sleep(1000)
