# ch01_hello_microbit.py

from microbit import *

while True:
    display.scroll('Hello, Micro:bit!')
    display.show(Image.HEART)
    sleep(1000)
    display.clear()
    sleep(1000)
    