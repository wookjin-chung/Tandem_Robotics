# ch4_21_micro_ultrasonic_distance.py

from microbit import *
import utime

# Set up the Parallax 3-pin ultrasonic sensor on pin0
signal_pin = pin0

def get_distance():
    # Configure the signal pin as output to send the Trigger signal
    signal_pin.write_digital(0)
    utime.sleep_us(2)
    signal_pin.write_digital(1)
    utime.sleep_us(5)
    signal_pin.write_digital(0)
    
    # Configure the signal pin as input to receive the Echo signal
    signal_pin.set_pull(signal_pin.NO_PULL)
    # Initialize signal_off and signal_on
    signal_off = 0
    signal_on = 0
    
    # Wait for the Echo signal to go HIGH
    while signal_pin.read_digital() == 0:
        signal_off = utime.ticks_us()
    
    # Wait for the Echo signal to go LOW
    while signal_pin.read_digital() == 1:
        signal_on = utime.ticks_us()
    
    # Convert the time difference to distance (speed of sound is 343 m/s)
    time_passed = signal_on - signal_off
    
    # Convert time difference to centimeters
    distance_cm = (time_passed * 34300) / 2 / 1000000
    return distance_cm

while True:
    distance = get_distance()
    # display.scroll("{:.2f} cm".format(distance))
    print("distance is {:.1f} cm".format(distance))
    sleep(50)  # Measure distance every 50 ms
