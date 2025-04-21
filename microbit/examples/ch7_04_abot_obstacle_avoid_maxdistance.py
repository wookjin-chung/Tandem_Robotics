# ch7_04_abot_obstacle_avoid_maxdistance.py

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

def turn(angle):
    # Positive angle: turn right, Negative angle: turn left
    turn_time = abs(angle) * 5  # Adjust turn angle duration
    if angle > 0:
        abot.servo_speed(100, 100)  # Turn right
        display.show("R")
    else:
        abot.servo_speed(-100, -100)  # Turn left
        display.show("L")
    sleep(turn_time)
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
    # print("distance is {} cm".format(distance))

    if 0 < distance < 30:
        # Obstacle detected within 30 cm
        stop_movement()

        # Scan surroundings
        distance_data = {}
        for angle in range(0, 181, 15):  # Scan every 15 degrees
            scan_servo.servo_angle(angle)
            sleep(50)
            distance = ultrasonic_sensor.distance('cm') or 0
            distance_data[angle] = distance
            sleep(50)

        # Find angle with maximum distance manually
        max_angle = None
        max_distance = -1
        for angle, dist in distance_data.items():
            if dist > max_distance:
                max_distance = dist
                max_angle = angle

        # Handle case where no maximum is found
        if max_angle is not None:
            # Calculate angle to turn (relative to current heading at 90 degrees)
            angle_to_turn = max_angle - 90  # Ensure this is a regular minus sign

            # Turn robot towards the angle with no obstacle
            turn(angle_to_turn)

        # Reset scanning servo to center
        scan_servo.servo_angle(90)
        sleep(100)
    else:
        # No obstacle detected, continue moving forward
        pass
