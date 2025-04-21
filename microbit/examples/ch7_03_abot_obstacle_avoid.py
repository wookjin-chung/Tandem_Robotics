# ch7_03_abot_obstacle_avoid.py

from microbit import *
from microbit_abot import *
from ultrasonic import *

# Initialize the wheel servos on pins 13 (left) and 12 (right)
abot = bot(13, 12)
abot.servo_attachpins()

# Initialize the ultrasonic sensor on pin 9
ultrasonic_sensor = Ultrasonic(9)

# Initialize the servo for scanning on pin 10
scan_servo = bot(10)

# Movement functions
def move_forward():
    abot.servo_speed(80, -80)  # Move forward
    display.show("F")

def stop_movement():
    abot.servo_speed(0, 0)  # Stop movement
    display.show("-")

def turn_right():
    abot.servo_speed(100, 100)  # Turn right
    display.show("R")
    sleep(300)
    abot.servo_speed(0, 0)

def turn_left():
    abot.servo_speed(-100, -100)  # Turn left
    display.show("L")
    sleep(300)
    abot.servo_speed(0, 0)

# Main loop
while True:
    # Move forward continuously
    move_forward()

    # Set the scanning servo to the center position (90 degrees)
    scan_servo.servo_angle(90)
    sleep(100)

    # Measure distance to the object ahead
    distance = ultrasonic_sensor.distance('cm') or 0
    #print("distance is {} cm".format(distance))

    if 0 < distance < 20:
        # Obstacle detected within 20 cm
        stop_movement()

        # Scan to the left
        scan_servo.servo_angle(45)
        sleep(100)
        distance_left = ultrasonic_sensor.distance('cm') or 0

        # Scan to the right
        scan_servo.servo_angle(135)
        sleep(100)
        distance_right = ultrasonic_sensor.distance('cm') or 0

        # Decide the direction based on the distance readings
        if distance_left > distance_right:
            turn_left()
        else:
            turn_right()
    else:
        # No obstacle detected; continue moving forward
        pass

    # Return the scanning servo to the center position
    scan_servo.servo_angle(90)
    sleep(100)
