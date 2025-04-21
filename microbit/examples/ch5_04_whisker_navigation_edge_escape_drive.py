# ch5_04_whisker_navigation_edge_escape_drive.py

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

def escape_corner():
    # Specific pattern to escape from a corner
    abot.servo_speed(-100, 100)
    display.show(Image.SQUARE)
    sleep(1000)
    abot.servo_speed(100, 100)
    sleep(1200)

# Count of intersection actions and previous state
turn_count = 0
last_sensor = None  

while True:
    whisker_left = left_sensor.read_digital()
    whisker_right = right_sensor.read_digital()

    if whisker_left == 0 and whisker_right == 0:
        escape_corner()
        turn_count = 0
        last_sensor = None  

    elif whisker_left == 1 and whisker_right == 1:
        forward()

    else:
        if whisker_left == 1 and whisker_right == 0:
            turnleft()
            if last_sensor == "right": 
                turn_count += 1
                last_sensor = "left"  
            else:
                turn_count = 0  
                last_sensor = "left"

        elif whisker_left == 0 and whisker_right == 1:
            turnright()
            if last_sensor == "left": 
                turn_count += 1
                last_sensor = "right" 
            else:
                turn_count = 0  
                last_sensor = "right"

        # Call escape_corner if intersection actions occur a certain number of times
        if turn_count >= 4:  # If the number of intersections is limited to 4
            escape_corner()
            turn_count = 0  
            last_sensor = None
