# ch5_09_ultrasonic_PID_Control.py 

from microbit_abot import *
import utime

abot = bot(13, 12)

setPoint = 20
kp = -4
signal_pin = pin0
abot.servo_attachpins()

def get_distance():
    signal_pin.write_digital(0)
    utime.sleep_us(2)
    signal_pin.write_digital(1)
    utime.sleep_us(5)
    signal_pin.write_digital(0)
    
    signal_pin.set_pull(signal_pin.NO_PULL)
    signal_off = 0
    signal_on = 0
    
    # Wait for echo signal reception
    while signal_pin.read_digital() == 0:
        signal_off = utime.ticks_us()
    
    while signal_pin.read_digital() == 1:
        signal_on = utime.ticks_us()
    
    # Convert time difference to distance (speed of sound is 343m/s)
    time_passed = signal_on - signal_off
    
    # Convert time difference to cm
    distance_cm = (time_passed * 34300) / 2 / 1000000  
    return distance_cm

while True:
    distance = get_distance()
    # display.scroll("{:.2f} cm".format(distance))
    print("distance is {:.1f} cm".format(distance))
    
    error = setPoint - distance
    tdrobot_speed = kp * error
    
    if tdrobot_speed > 200:
        tdrobot_speed = 200
    if tdrobot_speed < -200:
        tdrobot_speed = -200
    abot.servo_speed(tdrobot_speed, -tdrobot_speed)
    sleep(20)
