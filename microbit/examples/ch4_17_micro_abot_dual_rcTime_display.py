# ch4_17_micro_abot_dual_rcTime_display.py

from microbit_abot import *

left_sensor = bot(8)
right_sensor = bot(6)

while True:
    # Write a digital high (1) before measuring rc_time
    left_sensor.write_digital(1)
    qt_left = left_sensor.rc_time(1)
    right_sensor.write_digital(1)
    qt_right = right_sensor.rc_time(1)
    
    # Print the raw sensor readings
    print("Left_sensor:", qt_left)
    print("Right_sensor:", qt_right)
    
    # Handle None values returned by rc_time()
    if qt_left is None:
        print("Error: rc_time() for left sensor returned None")
        qt_left = 0  # Set a default value or handle appropriately
    else:
        print("qt_left:", qt_left)  # Verify correct return value
    
    if qt_right is None:
        print("Error: rc_time() for right sensor returned None")
        qt_right = 0  # Set a default value or handle appropriately
    else:
        print("qt_right:", qt_right)  # Verify correct return value
    
    # Set the maximum value to 25,000
    max_value = 25000
    if qt_left > max_value:
        qt_left = max_value
    if qt_right > max_value:
        qt_right = max_value
    
    # Convert the sensor reading to a value from 0 to 25
    # The closer the reading is to 0, the more LEDs will turn on
    left_display_value = 25 - int(qt_left / (max_value / 25))
    right_display_value = 25 - int(qt_right / (max_value / 25))
    
    display.clear()
    
    # For the left sensor: fill columns x=3 and x=4
    for x in [3, 4]:
        for y in range(5):
            if left_display_value > (y * 5 + (x - 3) * 5):
                display.set_pixel(x, y, 9)
    
    # For the right sensor: fill columns x=0 and x=1
    for x in [0, 1]:
        for y in range(5):
            if right_display_value > (y * 5 + x * 5):
                display.set_pixel(x, y, 9)
    
    sleep(50)
