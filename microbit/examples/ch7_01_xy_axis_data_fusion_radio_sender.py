# ch7_01_xy_axis_data_fusion_radio_sender.py

from microbit import *
import radio

# Radio setup
radio.on()
radio.config(channel=7, power=7)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    y_accel = accelerometer.get_y()
    x_accel = accelerometer.get_x()
    
    # Calculate (a_y, b_y) based on y-axis acceleration
    a_y = map_value(y_accel, -1024, 1024, -100, 100)
    b_y = -a_y  # Opposite value of a_y
    
    if -100 < y_accel < 100:
        a_y = 0
        b_y = 0
    
    # Calculate (a_x, b_x) based on x-axis acceleration
    a_x = map_value(x_accel, -1024, 1024, 100, -100)
    b_x = a_x  # Same value as a_x
    
    if -100 < x_accel < 100:
        a_x = 0
        b_x = 0

    # The range of a and b values is between –200 and +200
    a = (a_y + a_x) * 2
    b = (b_y + b_x) * 2
    
    # Limit a and b values between -200 and +200
    a = max(min(a, 200), -200)
    b = max(min(b, 200), -200)

    # Assign (a, b) values to left_speed and right_speed
    left_speed = a
    right_speed = b
    
    # Send (left_speed, right_speed) via radio
    radio.send("{},{}".format(left_speed, right_speed))
    
    # Print values for debugging
    print("left_speed: {}, right_speed: {}".format(left_speed, right_speed))
    
    sleep(100)
