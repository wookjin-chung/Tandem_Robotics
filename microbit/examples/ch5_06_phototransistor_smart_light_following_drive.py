# ch5_06_phototransistor_smart_light_following_drive.py

from microbit_abot import *
from microbit import button_a

abot = bot(13, 12)
left_sensor = bot(8)
right_sensor = bot(6)

abot.servo_attachpins()

# Measure ambient light to use as a baseline
def measure_ambient_light():
    left_sensor.write_digital(1)
    qt_left = left_sensor.rc_time(1)
    right_sensor.write_digital(1)
    qt_right = right_sensor.rc_time(1)

    if qt_left is None or qt_right is None:
        qt_left, qt_right = 0, 0
    return (qt_left + qt_right) / 2  # Use the average of left and right sensors as the baseline

# Measure the initial ambient light
ambient_light_threshold = measure_ambient_light()

# Set reaction threshold to respond when there's a 10% difference in light
reaction_threshold = ambient_light_threshold * 0.1

while True:
    # Update ambient_light_threshold if Button A is pressed
    if button_a.is_pressed():
        ambient_light_threshold = measure_ambient_light()
        print("New Ambient light threshold:", ambient_light_threshold)
        reaction_threshold = ambient_light_threshold * 0.1  # Recalculate the new threshold

    # Measure the light levels from left and right sensors
    left_sensor.write_digital(1)
    qt_left = left_sensor.rc_time(1)
    right_sensor.write_digital(1)
    qt_right = right_sensor.rc_time(1)

    if qt_left is None or qt_right is None:
        qt_left, qt_right = 0, 0

    light_diff_norm = int((qt_left * 200 / (qt_left + qt_right + 1))) - 100
    current_light_level = int((qt_left + qt_right) / 2)

    if current_light_level < ambient_light_threshold - reaction_threshold:
        if light_diff_norm > 0:  # Turn right
            left_speed = 100
            right_speed = -100 + light_diff_norm * 2
            display.show("R")
        else:  # Turn left
            left_speed = 100 + light_diff_norm * 2
            right_speed = -100
            display.show("L")
        abot.servo_speed(left_speed, right_speed)
    else:
        abot.servo_speed(0, 0)
        display.show(Image.SQUARE)

    sleep(200)  # Short delay between iterations
