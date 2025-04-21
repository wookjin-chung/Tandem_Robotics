# ch5_08_irDistance_navigation_drive.py

from microbit_abot import *
from microbit import display, sleep

abot = bot(13, 12)
left_sensor = bot(9, 10)
right_sensor = bot(2, 3)

# Connect servo motor pins
abot.servo_attachpins()

# Set maximum speed and distance
max_speed = 100
base_speed = 80  # Base forward speed
min_distance = 2  # Safe minimum distance (based on sensor value)
adjust_factor = 20  # Coefficient for adjusting rotation sensitivity
max_distance = 9  # Maximum distance value of sensors

while True:
    # Measure distance from left and right infrared sensors
    left_distance = left_sensor.ir_distance()
    right_distance = right_sensor.ir_distance()

    # Handle None values
    if left_distance is None:
        print("Left sensor error")
        left_distance = max_distance  # Or set to 0
    if right_distance is None:
        print("Right sensor error")
        right_distance = max_distance  # Or set to 0

    # Check if an obstacle is too close ahead
    if left_distance < min_distance and right_distance < min_distance:
        # Reverse
        abot.servo_speed(-max_speed, max_speed)
        display.show("B")
        sleep(1000)
        display.clear()
        continue  # Move to the next loop

    # Calculate distance difference to determine rotation direction
    distance_diff = right_distance - left_distance

    # Calculate speed adjustment based on distance difference
    speed_adjust = int(adjust_factor * distance_diff)

    # Calculate speed for left and right wheels
    left_speed = base_speed + speed_adjust
    right_speed = base_speed - speed_adjust

    # Limit speed to maximum value
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))

    # Adjust speed for servo motors
    left_wheel_speed = left_speed
    right_wheel_speed = -right_speed  # Reverse the sign for the right wheel

    # Set servo motor speed
    abot.servo_speed(left_wheel_speed, right_wheel_speed)

    # Print values for debugging
    print("Left distance:", left_distance, "Right distance:", right_distance)
    print("Left speed:", left_speed, "Right speed:", right_speed)

    # Use short delay
    sleep(50)
