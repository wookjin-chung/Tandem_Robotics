# ch5_05_phototransistor_navigation_drive.py

from microbit_abot import *

abot = bot(13, 12)
left_sensor = bot(8)
right_sensor = bot(6)

abot.servo_attachpins()

# Define movement functions
def forward():
    abot.servo_speed(100, -100)  # Move forward
    display.show("F")
    sleep(20)

def stop():
    abot.servo_speed(0, 0)  # Stop
    display.show(Image.SQUARE)
    sleep(100)

def turnright():
    abot.servo_speed(100, 0)  # Turn right
    display.show("R")
    sleep(100)

def turnleft():
    abot.servo_speed(0, -100)  # Turn left
    display.show("L")
    sleep(100)

# Main loop
while True:
    left_sensor.write_digital(1)
    qt_left = left_sensor.rc_time(1)  # Read left sensor
    right_sensor.write_digital(1)
    qt_right = right_sensor.rc_time(1)  # Read right sensor
    if qt_left is None:
        qt_left = 0
    if qt_right is None:
        qt_right = 0

    # Set a threshold to determine if light is "low"
    light_threshold = 1000  # Adjust this value based on sensor characteristics
    difference_threshold = 200  # Adjust this value to determine how much difference causes turning

    # If both sensor signals are above the light threshold, stop
    if qt_left > light_threshold and qt_right > light_threshold:
        stop()
    else:
        # Calculate the difference between left and right sensor values
        light_difference = qt_left - qt_right

        # If the light difference is small, move forward
        if abs(light_difference) < difference_threshold:
            forward()
        # If left sensor sees more light, turn left
        elif light_difference < difference_threshold:
            turnleft()
        # If right sensor sees more light, turn right
        else:
            turnright()

    print("Left_sensor:", qt_left)
    print("Right_sensor:", qt_right)

    sleep(50)  # Small delay between iterations
