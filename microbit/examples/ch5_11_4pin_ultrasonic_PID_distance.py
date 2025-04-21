# ch5_11_4pin_ultrasonic_PID_distance.py

from microbit_abot import *
from ultrasonic import *

abot = bot(13, 12)
ultrasonic_sensor = Ultrasonic(9, 10)

setPoint = 20
kp = -10
abot.servo_attachpins()

while True:
    # Convert to float because the Ultrasonic function can return a string
    distance = ultrasonic_sensor.distance('cm')
    
    if distance is not None:
        # Convert distance to float
        distance = float(distance)
        print("distance is {:.1f} cm".format(distance))
    
        error = setPoint - distance
        tdrobot_speed = kp * error
        
        # Limit the range of speed values
        if tdrobot_speed > 200:
            tdrobot_speed = 200
        if tdrobot_speed < -200:
            tdrobot_speed = -200
        abot.servo_speed(int(tdrobot_speed), int(-tdrobot_speed))
    else:
        print("Invalid distance value: {}".format(distance))

    sleep(30)
