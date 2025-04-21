# ch2_08_temperature_sensor.py

from microbit import *

while True:
    temp = temperature()
    if temp > 30:
        display.scroll("Hot!")
    elif temp < 10:
        display.scroll("Cold!")
    else:
        display.scroll("Okay")
    sleep(1000)
    