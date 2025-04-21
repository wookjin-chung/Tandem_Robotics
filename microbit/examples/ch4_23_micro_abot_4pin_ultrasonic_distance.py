# ch4_23_micro_abot_4pin_ultrasonic_distance.py

from microbit_abot import *
from ultrasonic import *

ultrasonic_sensor = Ultrasonic(9, 10)

while True:
    distance = ultrasonic_sensor.distance('cm')
    print("distance is {:.1f} cm".format(distance))
    
    sleep(30)
