# ch5_03_whisker_navigation_drive.py

from microbit_abot import *

abot = bot(13, 12)
left_sensor = bot(5)
right_sensor = bot(7)

abot.servo_attachpins()

def forward():
    abot.servo_speed(100, -100)
    display.show("F")
    sleep(20)

def backward():
    abot.servo_speed(-100, 100)
    display.show("B")
    sleep(1000)
    abot.servo_speed(100, 100)
    sleep(1200)

def turnright():
    abot.servo_speed(-100, 100)
    display.show("R")
    sleep(1000)
    abot.servo_speed(100, 0)
    sleep(800)

def turnleft():
    abot.servo_speed(-100, 100)
    display.show("L")
    sleep(1000)
    abot.servo_speed(0, -100)
    sleep(800)

while True:
    whisker_left = left_sensor.read_digital()
    whisker_right = right_sensor.read_digital()
    
    if whisker_left == 0 and whisker_right == 0:
        backward()
    elif whisker_left == 1 and whisker_right == 0:
        turnleft()
    elif whisker_left == 0 and whisker_right == 1:
        turnright()
    else:
        forward()
