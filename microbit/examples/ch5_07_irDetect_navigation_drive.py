# ch5_07_irDetect_navigation_drive.py

from microbit_abot import *

abot = bot(13, 12)
left_sensor = bot(9, 10)
right_sensor = bot(2, 3)

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
    irL = left_sensor.ir_detect(38000)
    irR = right_sensor.ir_detect(38000)
    print("left_sensor:", irL)
    print("right_sensor:", irR)

    if irL == 0 and irR == 0:
        backward()
    elif irL == 1 and irR == 0:
        turnleft()
    elif irL == 0 and irR == 1:
        turnright()
    else:
        forward()
