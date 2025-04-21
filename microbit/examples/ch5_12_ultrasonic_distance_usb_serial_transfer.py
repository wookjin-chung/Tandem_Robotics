# ch5_12_ultrasonic_distance_usb_serial_transfer.py

from microbit import *
from microbit_abot import *
from ultrasonic import *

ultrasonic_sensor = Ultrasonic(9)
abot = bot(10)  # Create an instance of the bot class

while True:
    for angle in range(0, 181):
        abot.servo_angle(angle)
        sleep(15)
        distance = ultrasonic_sensor.distance('cm') or 0

        # Data format: "angle,distance."
        data = "%d,%d." % (angle, int(distance))
        print(data, end='')  

    for angle in range(180, -1, -1):
        abot.servo_angle(angle)
        sleep(15)
        distance = ultrasonic_sensor.distance('cm') or 0

        # Data format: "angle,distance."
        data = "%d,%d." % (angle, int(distance))
        print(data, end='') 
